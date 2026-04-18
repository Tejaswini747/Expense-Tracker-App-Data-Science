import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# STEP 1: Generate Synthetic Data
# -------------------------------
np.random.seed(42)

dates = pd.date_range(start="2024-01-01", end="2024-03-31")

categories = ["Food", "Travel", "Rent", "Shopping", "Bills", "Entertainment"]
types = ["Expense", "Income"]

data = []

for date in dates:
    for _ in range(np.random.randint(1, 3)):
        category = np.random.choice(categories)
        amount = np.random.randint(100, 5000)
        t_type = "Expense"

        # Random income
        if np.random.rand() > 0.9:
            category = "Salary"
            amount = np.random.randint(20000, 50000)
            t_type = "Income"

        data.append([date, category, amount, t_type])

df = pd.DataFrame(data, columns=["Date", "Category", "Amount", "Type"])

df.to_csv("data/expenses.csv", index=False)

print("✅ Synthetic Data Created")

# -------------------------------
# STEP 2: Cleaning
# -------------------------------
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)

df["Date"] = pd.to_datetime(df["Date"])
df["Amount"] = pd.to_numeric(df["Amount"])

df["Category"] = df["Category"].str.title()
df["Type"] = df["Type"].str.title()

df["Month"] = df["Date"].dt.month_name()
df["Weekday"] = df["Date"].dt.day_name()

df.to_csv("data/cleaned_expenses.csv", index=False)

print("✅ Data Cleaned")

# -------------------------------
# STEP 3: Analysis
# -------------------------------
expense_df = df[df["Type"] == "Expense"]

category_sum = expense_df.groupby("Category")["Amount"].sum()

monthly_trend = expense_df.groupby(df["Date"].dt.month)["Amount"].sum()

# -------------------------------
# STEP 4: Visualization
# -------------------------------
sns.set()

# Bar Chart
plt.figure()
category_sum.plot(kind="bar")
plt.title("Category-wise Spending")
plt.savefig("outputs/category_bar.png")
plt.show()

# Pie Chart
plt.figure()
category_sum.plot(kind="pie", autopct="%1.1f%%")
plt.title("Expense Distribution")
plt.savefig("outputs/pie_chart.png")
plt.show()

# Line Chart
plt.figure()
monthly_trend.plot(marker="o")
plt.title("Monthly Spending Trend")
plt.savefig("outputs/monthly_trend.png")
plt.show()

# -------------------------------
# STEP 5: Insights
# -------------------------------
print("\n📊 INSIGHTS:")

print("Top Spending Category:", category_sum.idxmax())
print("Total Spending:", category_sum.sum())

if category_sum.max() > 20000:
    print("⚠️ Overspending detected!")
