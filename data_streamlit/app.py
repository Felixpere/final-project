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
    st.error(f"signals_all_tp_results.csv not found.")
    df = pd.DataFrame()

# === Overview Section ===
def show_overview():
    st.markdown("""
    ## Project Overview
    This app analyzes the effectiveness of Telegram crypto trading signals.

    **Goals:**
    - Measure hit rates per TP level
    - Compare symbols, directions, and trends
    - Simulate monthly returns based on signals
    """)
    if not df.empty:
        st.markdown("### Dataset Summary")
        st.markdown(f"**Date range:** {df['timestamp'].min().date()} to {df['timestamp'].max().date()}")
        st.markdown(f"**Total signals:** {len(df)}")

# === Charts Section ===
def show_charts():
    st.markdown("## Interactive Charts")
    plot_dir = Path(__file__).parent / ".." / "telegram_signal_extractor" / "outputs" / "plots"
    chart_files = [
        ("tp_hits_raw_count.html", "Raw count of TP hits by level and direction."),
        ("tp_hits_by_direction.html", "Comparison of TP hits between Long and Short signals."),
        ("tp_hit_rate_global.html", "Overall TP hit percentage across all signals."),
        ("tp_hierarchical_hit_rate.html", "Hierarchical success of hitting TP levels sequentially."),
        ("signal_distribution_by_hour.html", "Hourly distribution of signal timestamps (UTC)."),
        ("top10_errors_barchart.html", "Symbols with the highest percentage of signals with no TP reached."),
        ("top10_symbol_errors_table.html", "Table of error stats for top 10 symbols (check file name if broken)."),
        ("tp_signal_count_by_symbol.html", "Number of signals per symbol."),
        ("hierarchical_tp_hit_rate_top10_heatmap.html", "Sequential TP hit rates by top 10 most frequent symbols."),
        ("best_symbols_per_tp.html", "Best performing symbol by each TP level."),
    ]
    for file_name, description in chart_files:
        file_path = plot_dir / file_name
        if file_path.exists():
            st.components.v1.html(file_path.read_text(encoding="utf-8"), height=600)
            st.caption(description)
        else:
            st.warning(f"Chart file not found: {file_name}")

# === KPIs Section ===
def show_kpis():
    st.markdown("## KPIs")
    st.write("Coming soon: Key metrics on signal accuracy, symbol performance and more.")

# === Simulation Section ===
def show_simulation():
    st.markdown("## Monthly Simulation")
    
    st.markdown("""
    This section simulates a trading strategy where **$100 is invested in every trading signal**.

    The returns are estimated based on which TP (Take Profit) level was reached. This analysis provides insights into:
    - The volume and success rate of signals over time
    - Monthly return trends and cumulative growth
    - Return variability and comparison between Long and Short directions

     **Warning**: This simulation does **not account for Stop Loss (SL)**. Therefore, it assumes that unprofitable trades result in a 40% loss. This makes the strategy highly risky in practice.
    """)

    df_path = Path(__file__).parent / ".." / "telegram_signal_extractor" / "data" / "clean" / "signals_tp_clean_with_returns.csv"
    try:
        df = pd.read_csv(df_path, parse_dates=["timestamp"])
        df["month"] = df["timestamp"].dt.to_period("M").astype(str)
    except FileNotFoundError:
        st.error("signals_tp_clean_with_returns.csv not found.")
        return

    plot_dir = Path(__file__).parent / ".." / "telegram_signal_extractor" / "outputs" / "plots"

    # Chart 1: Volume and success rate
    chart1 = plot_dir / "monthly_signal_volume_success_rate.html"
    if chart1.exists():
        st.subheader("Monthly Signal Volume and Success Rate")
        st.components.v1.html(chart1.read_text(encoding="utf-8"), height=600)
        st.markdown("This chart shows the number of signals sent per month (bars) and their corresponding success rate (line). Despite fluctuations in signal volume, the success rate remains relatively stable with a few noticeable drops in early 2025.")
    else:
        st.warning("Chart not found: monthly_signal_volume_success_rate.html")

    # Chart 2: Cumulative return over time
    chart2 = plot_dir / "monthly_return_line_chart.html"
    if chart2.exists():
        st.subheader("Simulated Cumulative Return Over Time")
        st.components.v1.html(chart2.read_text(encoding="utf-8"), height=600)
        st.markdown("This area chart displays the cumulative return assuming $100 per signal. The consistent upward trend indicates that the strategy is generating compounded returns over time.")
    else:
        st.warning("Chart not found: monthly_return_line_chart.html")

    # Chart 3: Boxplot of returns
    chart3 = plot_dir / "returns_histogram_by_month.html"
    if chart3.exists():
        st.subheader("Distribution of Returns per Month (Boxplot)")
        st.components.v1.html(chart3.read_text(encoding="utf-8"), height=600)
        st.markdown("This boxplot shows the spread and median of estimated returns by month. It helps visualize volatility and detect outliers, offering insights into the consistency of the strategy.")
    else:
        st.warning("Chart not found: returns_histogram_by_month.html")

    # Chart 4: Long vs Short comparison
    chart4 = plot_dir / "monthly_total_return_long_short.html"
    if chart4.exists():
        st.subheader("Monthly Total Return: Long vs Short")
        st.components.v1.html(chart4.read_text(encoding="utf-8"), height=600)
        st.markdown("This bar chart compares total returns for Long vs Short signals month by month. Long signals usually perform better, but in some months, Short signals provide higher returns.")
    else:
        st.warning("Chart not found: monthly_total_return_long_short.html")

    # Final Conclusion
    st.markdown("""
    ---
    ### Final Notes

    This simulation suggests that, **without SL**, the trading signals can yield positive cumulative returns if managed consistently over time. However:

    - Return variability is high in some months.
    - Performance between Long and Short signals fluctuates.
    - Using this strategy without SL can lead to **significant drawdowns** in bad periods.

    More robust evaluation would require incorporating **market prices**, **real SL triggers**, and possibly **position sizing or filtering mechanisms**.
    """)


# === Hypothesis Testing Section ===
def show_hypothesis():
    st.markdown("## Hypothesis Testing")
    st.markdown("""
    Results of statistical tests on signal performance:
    - Direction effectiveness (Long vs Short)
    - Entry price correlation
    - Time slot performance
    - Year-over-year trends
    """)

# === Insights Section ===
def show_insights():
    st.markdown("## Key Insights")
    st.write("Final conclusions, takeaways, and potential applications.")

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