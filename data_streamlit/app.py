import streamlit as st
import pandas as pd
from pathlib import Path
import streamlit.components.v1 as components

# === Config ===
st.set_page_config(page_title="TP Analysis Dashboard", layout="wide")
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Overview", "Charts", "KPIs", "Simulation", "Hypothesis Testing", "Insights"])

# === Load CSV ===
data_path = Path(__file__).parent / ".." / "telegram_signal_extractor" / "data" / "clean" / "signals_all_tp_results.csv"
try:
    df = pd.read_csv(data_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
except FileNotFoundError:
    st.error("signals_all_tp_results.csv not found.")
    df = pd.DataFrame()

# === Overview Section ===
def show_overview():
    st.markdown("## Overview")
    st.markdown("This dashboard analyzes crypto trading signals from a Telegram group to evaluate whether they can be used to build a profitable strategy.")
    
    st.markdown("### Warning")
    st.warning("This analysis does not include Stop Loss (SL). The risk of loss is significantly higher without SL protection.")

    if st.button("Start the Analysis"):
        st.markdown("### Project Summary")
        st.markdown("""
        - Goal: Evaluate the effectiveness of trading signals.
        - Scope: Analyze target hit rates, simulate trading returns, and perform statistical analysis.
        - Method: Simulate $100 per signal, measure returns, volatility, and hit success.
        """)

        if not df.empty:
            st.markdown("### Dataset Summary")
            st.markdown(f"- Date range: {df['timestamp'].min().date()} to {df['timestamp'].max().date()}")
            st.markdown(f"- Total signals: {len(df)}")
            st.markdown(f"- Columns: {', '.join(df.columns)}")

# === Charts Section ===
def show_charts():
    st.markdown("## Charts")
    plot_dir = Path(__file__).parent / ".." / "telegram_signal_extractor" / "outputs" / "plots"
    chart_files = [
        ("tp_hits_raw_count.html", "TP Hit Count: Raw count of hits by level and direction."),
        ("tp_hits_by_direction.html", "TP Hit Count by Signal Direction (Long vs Short)."),
        ("tp_hit_rate_global.html", "Overall TP Hit Rate."),
        ("tp_hierarchical_hit_rate.html", "Hierarchical TP Hit Rate (Sequential Success)."),
        ("signal_distribution_by_hour.html", "Hourly Distribution of Signals (UTC)."),
        ("top10_errors_barchart.html", "Top 10 Symbols with Highest Error Rate."),
        ("top10_symbol_errors_table.html", "Table: Error Statistics by Symbol."),
        ("tp_signal_count_by_symbol.html", "Signal Count per Symbol."),
        ("hierarchical_tp_hit_rate_top10_heatmap.html", "Heatmap: Sequential TP Hit Rates for Top 10 Symbols."),
        ("best_symbols_per_tp.html", "Best Performing Symbol for Each TP Level.")
    ]
    for file_name, description in chart_files:
        file_path = plot_dir / file_name
        if file_path.exists():
            st.subheader(description)
            st.components.v1.html(file_path.read_text(encoding="utf-8"), height=600)
            # Optional conclusions per chart
            if "tp_hit_rate_global" in file_name:
                st.markdown("**Conclusion:** TP40 is the most consistent level hit across all signals.")
            elif "signal_distribution_by_hour" in file_name:
                st.markdown("**Conclusion:** Most signals are sent during morning UTC hours, possibly due to market activity.")
            elif "top10_errors_barchart" in file_name:
                st.markdown("**Conclusion:** Some symbols have consistently high error rates, indicating unreliable performance.")
            elif "best_symbols_per_tp" in file_name:
                st.markdown("**Conclusion:** Certain assets repeatedly achieve top performance at specific TP levels.")
        else:
            st.warning(f"Chart file not found: {file_name}")

# === KPIs Section ===
def show_kpis():
    st.markdown("## KPIs")
    st.markdown("""
    - TP Hit Rate by Level (TP40, TP60, TP80, TP100)
    - Hierarchical TP Hit Rate (sequential)
    - Top Performing Symbols
    - Monthly Sharpe Ratio and Volatility
    - Monthly Average and Cumulative Return
    """)

    plot_dir = Path(__file__).parent / ".." / "telegram_signal_extractor" / "outputs" / "plots"

    # 1. Heatmap
    file_path = plot_dir / "hierarchical_tp_hit_rate_top10_heatmap.html"
    if file_path.exists():
        st.subheader("Heatmap: Sequential TP Hit Rates (Top 10 Symbols)")
        st.components.v1.html(file_path.read_text(encoding="utf-8"), height=600)
        st.markdown("**Conclusion:** Some symbols reach multiple TP levels consistently, showing stronger signal quality.")
    else:
        st.warning("Chart not found: hierarchical_tp_hit_rate_top10_heatmap.html")

    # 2. Sharpe vs Volatility
    file_path = plot_dir / "sharpe_vs_volatility.html"
    if file_path.exists():
        st.subheader("Sharpe Ratio vs Volatility")
        st.components.v1.html(file_path.read_text(encoding="utf-8"), height=600)
        st.markdown("**Conclusion:** More stable months (low volatility) tend to have higher Sharpe Ratios.")
    else:
        st.warning("Chart not found: sharpe_vs_volatility.html")

    # 3. Monthly summary
    file_path = plot_dir / "monthly_summary_volume_success.html"
    if file_path.exists():
        st.subheader("Monthly Summary Table (Returns, Std Dev, Success Rate)")
        st.components.v1.html(file_path.read_text(encoding="utf-8"), height=600)
        st.markdown("**Conclusion:** Performance varies widely across months, with some offering higher average returns and others higher risk.")
    else:
        st.warning("Chart not found: monthly_summary_volume_success.html")

# === Simulation Section ===
def show_simulation():
    st.markdown("## Simulation")
    st.markdown("""
    Simulation Logic:
    - $100 per signal
    - No Stop Loss applied
    - TP reached determines return
    """)

    plot_dir = Path(__file__).parent / ".." / "telegram_signal_extractor" / "outputs" / "plots"

    chart_files = [
        ("returns_histogram_by_month.html", "Monthly Return Distribution"),
        ("monthly_total_return_long_short.html", "Long vs Short Return Comparison"),
        ("cumulative_monthly_return.html", "Cumulative Return Over Time"),
    ]
    for file_name, description in chart_files:
        file_path = plot_dir / file_name
        if file_path.exists():
            st.subheader(description)
            st.components.v1.html(file_path.read_text(encoding="utf-8"), height=600)
            if "returns_histogram_by_month" in file_name:
                st.markdown("**Conclusion:** Monthly return distributions show high variability, indicating inconsistent performance.")
            elif "monthly_total_return_long_short" in file_name:
                st.markdown("**Conclusion:** On average, Long and Short signals perform similarly.")
            elif "cumulative_monthly_return" in file_name:
                st.markdown("**Conclusion:** The strategy accumulates gains over time but experiences significant drawdowns.")
        else:
            st.warning(f"Chart not found: {file_name}")

    st.markdown("### Conclusions from Simulation")
    st.markdown("""
    - High-performing months often correlate with lower volatility.
    - Long and Short signals yield similar results on average.
    - No clear correlation between signal volume and success rate.
    """)

# === Hypothesis Testing Section ===
def show_hypothesis():
    st.markdown("## Hypothesis Testing")
    st.markdown("""
    Statistical Tests Conducted:

    | Hypothesis | Test | Conclusion |
    |------------|------|------------|
    | Long vs Short returns differ? | t-test | No significant difference |
    | Are 2024 signals better than 2023? | t-test | Yes, 2024 performs better |
    | Do morning signals perform better? | t-test | Yes, statistically higher returns |
    | Do recent signals outperform older ones? | t-test | Yes, recent signals perform better |

    These results are based on return distributions and statistical confidence levels.
    """)

    plot_dir = Path(__file__).parent / ".." / "telegram_signal_extractor" / "outputs" / "plots"

    # 1. Long vs Short
    file_path = plot_dir / "monthly_total_return_long_short.html"
    if file_path.exists():
        st.subheader("Long vs Short Return Comparison")
        st.components.v1.html(file_path.read_text(encoding="utf-8"), height=600)
        st.markdown("**Conclusion:** Returns are statistically similar for Long and Short signals, despite perceived directional bias.")
    else:
        st.warning("Chart not found: monthly_total_return_long_short.html")


    # 3. Morning vs other hours
    file_path = plot_dir / "avg_return_by_hour.html"
    if file_path.exists():
        st.subheader("Average Return by Hour (UTC)")
        st.components.v1.html(file_path.read_text(encoding="utf-8"), height=600)
        st.markdown("**Conclusion:** Signals sent early in the UTC day have higher average returns, supporting the time-of-day hypothesis.")
    else:
        st.warning("Chart not found: avg_return_by_hour.html")


# === Insights Section ===
def show_insights():
    st.markdown("## Insights")

    st.markdown("### Key Insights")
    st.markdown("""
    - TP40 is the most consistently reached level.
    - Signals sent during morning UTC hours show higher returns.
    - No significant difference between Long and Short signals.
    - Symbols such as PYTH, TIA, and MYRO perform best.
    - Sharpe Ratio varies month to month.
    """)

    st.markdown("### Limitations")
    st.markdown("""
    - No Stop Loss used, leading to potential high drawdowns.
    - Daily high/low used for validation, not real-time execution.
    - Assumes $100 fixed investment per signal.
    - Market prices are not confirmed through exchange APIs.
    """)

    st.markdown("### Final Conclusions")
    st.markdown("""
    Telegram signals show potential for profitability, especially at conservative targets. However, due to volatility and risk, they should not be used without proper risk management and further real-time testing.
    """)

# === Section router ===
if section == "Overview":
    show_overview()
elif section == "Charts":
    show_charts()
elif section == "KPIs":
    show_kpis()
elif section == "Simulation":
    show_simulation()
elif section == "Hypothesis Testing":
    show_hypothesis()
elif section == "Insights":
    show_insights()

