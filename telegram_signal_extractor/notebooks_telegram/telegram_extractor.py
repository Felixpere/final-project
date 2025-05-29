import os
import json
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
import re
from telethon.sync import TelegramClient

# Load environment variables
load_dotenv(".env")
print("API_ID:", os.getenv("API_ID"))
print("API_HASH:", os.getenv("API_HASH"))


#API_ID = "25302624"
#API_HASH = "24e68493404fba657f5588d73a30f571"
GROUP_ID = 1001717037581

# Define paths
raw_path = Path("../data/raw/raw_messages.json")
backup_path = Path(f"../data/backups/signals_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
log_path = Path("../logs/extractor_log.txt")

# Load existing signals to detect last timestamp
signals_csv = Path("../data/telegram_signals_clean.csv")
if signals_csv.exists():
    existing_signals = pd.read_csv(signals_csv)
    last_timestamp = pd.to_datetime(existing_signals['timestamp']).max()
else:
    existing_signals = pd.DataFrame()
    last_timestamp = datetime(2023, 1, 1)

# ========== MESSAGE COLLECTION ==========
async def collect_messages():
    messages = []
    async with TelegramClient("session_felix", API_ID, API_HASH) as client:
        async for msg in client.iter_messages(GROUP_ID, offset_date=last_timestamp, reverse=True):
            if msg.text:
                messages.append({
                    "text": msg.text,
                    "timestamp": msg.date.isoformat()
                })

    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

    with open(log_path, "a") as log:
        log.write(f"[{datetime.now()}] Downloaded {len(messages)} new messages.\n")

# ========== MESSAGE PARSING ==========
def parse_signal(text):
    result = {}
    symbol_match = re.search(r"#([A-Z0-9]+)[^\s/]*/USDT", text)
    if symbol_match:
        result["symbol"] = symbol_match.group(1) + "/USDT"

    direction_match = re.search(r"\b(Long|Short)\b", text, re.IGNORECASE)
    if direction_match:
        result["direction"] = direction_match.group(1).capitalize()

    entry_match = re.search(r"Entry[^0-9]{0,10}(\d+\.\d+)", text)
    if entry_match:
        result["entry"] = float(entry_match.group(1))

    tp_matches = re.findall(r"(\d+\.\d+)\s*\((\d+)% of profit\)", text)
    for price, percent in tp_matches:
        result[f"tp_{percent}"] = float(price)

    price_hit = re.search(r"Price[^0-9]{0,10}(\d+\.\d+)", text)
    if price_hit:
        result["hit_price"] = float(price_hit.group(1))

    return result

# ========== DUPLICATE CHECK ==========
def is_duplicate_signal(new_signal, existing_df, time_tolerance_minutes=60):
    if existing_df.empty:
        return False
    new_time = pd.to_datetime(new_signal["timestamp"])
    filtered = existing_df[
        (existing_df["symbol"] == new_signal.get("symbol")) &
        (existing_df["direction"] == new_signal.get("direction")) &
        (abs(existing_df["entry"] - new_signal.get("entry", 0)) < 0.0001) &
        (abs(pd.to_datetime(existing_df["timestamp"]) - new_time) <= pd.Timedelta(minutes=time_tolerance_minutes))
    ]
    for tp in ["tp_40", "tp_60", "tp_80", "tp_100"]:
        if tp in new_signal:
            filtered = filtered[abs(filtered[tp] - new_signal.get(tp, 0)) < 0.0001]
    return not filtered.empty

# ========== EXECUTE SCRIPT ==========
async def main():
    await collect_messages()

    with open(raw_path, "r", encoding="utf-8") as f:
        raw_messages = json.load(f)

    parsed_messages = []
    for msg in raw_messages:
        parsed = parse_signal(msg["text"])
        parsed["timestamp"] = msg["timestamp"]
        parsed_messages.append(parsed)

    signal_data, update_data, others = [], [], []
    for parsed in parsed_messages:
        if "entry" in parsed and any(k.startswith("tp_") for k in parsed):
            if not is_duplicate_signal(parsed, existing_signals):
                signal_data.append(parsed)
        elif "symbol" in parsed and "entry" not in parsed and "hit_price" in parsed:
            update_data.append(parsed)
        else:
            others.append(parsed)

    df_signals = pd.DataFrame(signal_data)
    df_signals.dropna(subset=["symbol", "entry", "tp_40", "tp_60", "tp_80", "tp_100"], inplace=True)

    df_signals['symbol'] = df_signals['symbol'].str.replace("/", "").str.upper()
    df_signals["timestamp"] = pd.to_datetime(df_signals["timestamp"])

    # Merge with existing and save with backup
    if signals_csv.exists():
        existing_signals.to_csv(backup_path, index=False)
        df_signals = pd.concat([existing_signals, df_signals], ignore_index=True).drop_duplicates()

    df_signals.to_csv(signals_csv, index=False)

    with open(log_path, "a") as log:
        log.write(f"[{datetime.now()}] Signals merged: {df_signals.shape[0]} total rows.\n")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
