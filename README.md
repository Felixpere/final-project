# 📊 Telegram Signal TP Analysis Dashboard

This project analyzes the **effectiveness of crypto trading signals** shared in a Telegram group, with the goal of evaluating how often these signals hit Take-Profit (TP) targets and whether a user following them could obtain consistent returns.

## 📁 Project Structure

```
final_project/
├── bybit_connector/
│   └── 03_track_prices_and_compare.ipynb
├── data_streamlit/
│   └── app.py
├── telegram_signal_extractor/
│   ├── data/
│   │   ├── clean/
│   │   ├── raw/
│   │   └── trading_signals.db
│   ├── notebooks_telegram/
│   └── outputs/
│       └── plots/
```

## 🎯 Objectives

- Measure hit rates for each TP level (TP40 to TP100)
- Compare performance by symbol and direction (Long vs Short)
- Simulate investment outcomes over time
- Explore statistical KPIs and visual patterns
- Validate or reject key trading hypotheses

## 📦 Dataset

- **Source:** Telegram signal group (parsed via script and cleaning)
- **Period Covered:** 2023 to May 2025
- **Volume:** 3,000+ unique signals, 10,000+ updates
- **Content:**
  - Entry prices, TP levels (40–100), directions (Long/Short)
  - Hit indicators per TP
  - Timestamps and validation against Bybit price data
  - Simulated returns for each signal

## 📈 Streamlit App Features

The interactive dashboard lets you explore the data and results:

### 🛍️ Overview
- General context, methodology and assumptions

### 📊 Charts
- TP hit rate by level
- TP progression patterns (e.g., TP40 → TP60)
- Time of day distribution
- Top symbols and error rates

### 📌 KPIs
- Hit rate heatmap by symbol
- Best and worst-performing months
- Sharpe ratio vs volatility

### 📈 Simulation
- $100 invested per signal
- Monthly return distributions
- Long vs Short strategy comparison
- Cumulative return evolution

### 🧪 Hypothesis Testing

| Hypothesis                           | Result                |
|--------------------------------------|------------------------|
| Long vs Short returns are different  | ❌ Not significant     |
| 2024 signals outperform 2023         | ✅ Confirmed           |
| Morning signals perform better       | ✅ Statistically true  |
| Recent signals perform better        | ✅ Confirmed           |

## 📌 Key Insights

- **TP40** is hit ~60% of the time, making it the most reliable.
- **Morning signals (7–11am UTC)** deliver better results.
- **Assets like PYTH, TIA, MYRO** show consistent performance.
- **No Stop Loss strategy** used — high volatility and risk.
- Blindly following signals can lead to strong returns, but also large drawdowns.

## 🧠 Assumptions

- Simulations use a fixed investment per signal with no SL
- Each TP is sequential: TP100 assumes TP40, TP60, TP80 were also hit
- Simulated profit/loss:
  - TP40 → +$10, TP60 → +$20, TP80 → +$30, TP100 → +$40
  - No TP hit → –$40

## ▶️ How to Run

```bash
cd data_streamlit
streamlit run app.py
```

> Python 3.8+ is recommended  
> Required packages: `streamlit`, `pandas`, `plotly`, `pathlib`

## 🚀 Future Improvements

- Integrate real-time prices from Bybit or Binance
- Add Stop Loss logic and risk controls
- Deploy the app publicly (Streamlit Cloud / AWS)
- Build alert system for strong signals

## 📚 Acknowledgments

This project was developed during the final module of the Ironhack Data Analytics Bootcamp.