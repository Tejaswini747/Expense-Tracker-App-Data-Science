import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Expense Tracker Pro", layout="wide")

# -------------------------------
# CUSTOM CSS (UI IMPROVEMENT)
# -------------------------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
h1 {
    color: #2c3e50;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# LOAD DATA
# -------------------------------
df = pd.read_csv("data/cleaned_expenses.csv")
df["Date"] = pd.to_datetime(df["Date"])

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("🔍 Filters")

# Date Filter
min_date = df["Date"].min()
max_date = df["Date"].max()

date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# Category Filter
category = st.sidebar.multiselect(
    "Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

# Type Filter
type_filter = st.sidebar.selectbox("Transaction Type", ["All", "Expense", "Income"])

# -------------------------------
# APPLY FILTERS
# -------------------------------
filtered_df = df[
    (df["Category"].isin(category)) &
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1]))
]

if type_filter != "All":
    filtered_df = filtered_df[filtered_df["Type"] == type_filter]

# -------------------------------
# TITLE
# -------------------------------
st.title("💰 Expense Tracker Pro Dashboard")

# -------------------------------
# KPI SECTION
# -------------------------------
total_expense = filtered_df[filtered_df["Type"] == "Expense"]["Amount"].sum()
total_income = filtered_df[filtered_df["Type"] == "Income"]["Amount"].sum()
savings = total_income - total_expense

col1, col2, col3 = st.columns(3)

col1.metric("💸 Total Expense", f"₹{total_expense}")
col2.metric("💰 Total Income", f"₹{total_income}")
col3.metric("💼 Savings", f"₹{savings}")

st.markdown("---")

# -------------------------------
# DOWNLOAD BUTTON
# -------------------------------
st.download_button(
    label="📥 Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_expenses.csv",
    mime="text/csv"
)

# -------------------------------
# CHARTS ROW 1
# -------------------------------
col1, col2 = st.columns(2)

# Bar Chart
with col1:
    st.subheader("📊 Category-wise Spending")
    expense_df = filtered_df[filtered_df["Type"] == "Expense"]
    category_data = expense_df.groupby("Category")["Amount"].sum()
    st.bar_chart(category_data)

# Line Chart
with col2:
    st.subheader("📈 Monthly Trend")
    monthly = filtered_df.groupby(filtered_df["Date"].dt.month)["Amount"].sum()
    st.line_chart(monthly)

# -------------------------------
# CHARTS ROW 2
# -------------------------------
col1, col2 = st.columns(2)

# Pie Chart
with col1:
    st.subheader("🥧 Expense Distribution")
    fig, ax = plt.subplots()
    category_data.plot.pie(autopct="%1.1f%%", ax=ax)
    ax.set_ylabel("")
    st.pyplot(fig)

# Heatmap
with col2:
    st.subheader("🔥 Spending Heatmap")
    heatmap_data = filtered_df.pivot_table(
        values="Amount",
        index=filtered_df["Date"].dt.month,
        columns="Category",
        aggfunc="sum"
    )

    fig, ax = plt.subplots(figsize=(8,4))
    sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="coolwarm", ax=ax)
    st.pyplot(fig)

# -------------------------------
# INSIGHTS ENGINE
# -------------------------------
st.markdown("---")
st.subheader("📌 Smart Insights")

if total_expense > total_income:
    st.error("⚠️ Overspending Alert! You are spending more than your income.")

if not category_data.empty:
    top_category = category_data.idxmax()
    st.success(f"💡 Highest spending category: {top_category}")

avg_spending = category_data.mean() if not category_data.empty else 0
st.info(f"📊 Average category spending: ₹{avg_spending:.2f}")

# -------------------------------
# RAW DATA
# -------------------------------
st.markdown("---")
if st.checkbox("📂 Show Raw Data"):
    st.dataframe(filtered_df)