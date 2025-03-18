import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Personal Expense Tracker")

if "expenses" not in st.session_state:
    st.session_state["expenses"] = pd.DataFrame(columns=["Date", "Category", "Amount", "Notes", "Payment Method"])

date = st.date_input("Date")
category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Shopping", "Bills", "Other"])
amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")
notes = st.text_area("Notes (optional)")
payment_method = st.selectbox("Payment Method", ["Cash", "Credit Card", "Debit Card", "UPI", "Other"])

if st.button("Add Expense"):
    new_expense = pd.DataFrame([[pd.to_datetime(date), category, amount, notes, payment_method]], 
                               columns=["Date", "Category", "Amount", "Notes", "Payment Method"])
    st.session_state["expenses"] = pd.concat([st.session_state["expenses"], new_expense], ignore_index=True)
    st.success("Expense added successfully!")

df = st.session_state["expenses"]

if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")  # Convert to string format

st.subheader("Expense History")
st.dataframe(df)

st.subheader("Expense Summary")
if not df.empty:
    category_summary = df.groupby("Category")["Amount"].sum()

    fig, ax = plt.subplots()
    category_summary.plot(kind="bar", ax=ax, color="skyblue")
    ax.set_ylabel("Amount Spent (₹)")
    ax.set_title("Expenses by Category")
    st.pyplot(fig)

    total_spent = df["Amount"].sum()
    st.subheader(f"Total Spent: ₹{total_spent:.2f}")

    budget_limit = st.number_input("Set Monthly Budget (₹)", min_value=0.0, format="%.2f")
    if budget_limit and total_spent > budget_limit:
        st.warning(f"You have exceeded your budget of ₹{budget_limit:.2f}!")
    elif budget_limit:
        st.success(f"You are within your budget of ₹{budget_limit:.2f}.")

    df["Month"] = pd.to_datetime(df["Date"]).dt.strftime("%B %Y")
    month_summary = df.groupby("Month")["Amount"].sum()
    st.subheader("Monthly Expense Breakdown")
    st.bar_chart(month_summary)

    selected_category = st.selectbox("Filter by Category", df["Category"].unique())
    filtered_df = df[df["Category"] == selected_category]
    st.dataframe(filtered_df)

    if st.button("Delete Last Expense"):
        if not df.empty:
            st.session_state["expenses"] = df.iloc[:-1].reset_index(drop=True)
            st.warning("Last expense entry deleted!")

    search_term = st.text_input("Search Expenses by Keyword")
    if search_term:
        search_results = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
        st.dataframe(search_results)

    sort_order = st.radio("Sort by Amount", ("Ascending", "Descending"))
    sorted_df = df.sort_values(by="Amount", ascending=(sort_order == "Ascending"))
    st.dataframe(sorted_df)

    daily_expense = df.groupby("Date")["Amount"].sum()
    st.subheader("Daily Expense Tracking")
    st.line_chart(daily_expense)

    st.subheader("Future Expense Prediction (Coming Soon)")
    st.info("This feature will use AI to predict future expenses based on spending patterns.")

    st.subheader("Export Data")
    if st.button("Download CSV"):
        df.to_csv("expenses.csv", index=False)
        st.success("CSV file generated successfully! Download from your file system.")

else:
    st.info("No expenses recorded yet.")
