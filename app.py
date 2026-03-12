import streamlit as st
import pandas as pd
import os

# Page Config
st.set_page_config(page_title="SACCO_XAI | Core Engine", layout="wide")

# --- DATA PERSISTENCE LOGIC ---
DATA_FILE = 'sacco_members.csv'

def save_data(df):
    df.to_csv(DATA_FILE, index=False)
    st.cache_data.clear()

@st.cache_data
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    # Default sample structure
    return pd.DataFrame(columns=['Member_ID', 'Name', 'Savings_Balance_KES', 'Loan_Balance_KES', 'Churn_Risk', 'Monthly_Income_KES'])

# --- APP UI ---
st.title("🛡️ SACCO_XAI: Financial Intelligence")

df = load_data()

# Updated Navigation
menu = st.sidebar.radio("Navigation", ["Dashboard", "Search & Credit Score"])

# --- 1. DASHBOARD (Instructions & Upload) ---
if menu == "Dashboard":
    st.subheader("📈 System Dashboard & Data Management")
    
    # Instructions Section
    with st.expander("📝 Requirements for Data Upload (Read First)", expanded=True):
        st.write("""
        To ensure the AI calculates Credit Scores accurately, your CSV file must contain the following columns:
        1. **Member_ID**: Unique identifier for the member.
        2. **Name**: Full name of the member.
        3. **Savings_Balance_KES**: Total current savings.
        4. **Loan_Balance_KES**: Outstanding loan amount.
        5. **Churn_Risk**: A value between 0 (Stable) and 1 (Likely to leave).
        6. **Monthly_Income_KES**: Monthly earning of the member.
        """)

    # Data Operations
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("### Upload New Data")
        uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
        if uploaded_file:
            new_df = pd.read_csv(uploaded_file)
            if st.button("Confirm & Save Uploaded Data"):
                save_data(new_df)
                st.success("System data updated!")
                st.rerun()

    with col2:
        st.write("### Reset / Remove")
        if st.button("🗑️ Clear All Data (Revert to Sample)"):
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
                st.cache_data.clear()
                st.warning("All uploaded data removed. System reverted to sample.")
                st.rerun()

    st.divider()
    st.write("### Current Database Preview")
    st.dataframe(df, use_container_width=True)

# --- 2. SEARCH & CREDIT SCORE (Lookup & Advice) ---
elif menu == "Search & Credit Score":
    st.subheader("🔍 Member Credit Assessment")
    
    search_id = st.text_input("Enter Member ID to view full credit profile")
    
    if search_id:
        # Exact ID match
        result = df[df['Member_ID'].astype(str) == search_id]
        
        if not result.empty:
            row = result.iloc[0]
            st.success(f"Record Found: {row['Name']}")
            
            # Layout for Details
            c1, c2, c3 = st.columns(3)
            
            # Credit Score Calculation
            risk_prob = row.get('Churn_Risk', 0.5)
            credit_score = int(850 - (risk_prob * 550))
            
            c1.metric("Credit Score", credit_score)
            c2.metric("Savings Balance", f"KES {row['Savings_Balance_KES']:,.0f}")
            c3.metric("Loan/Income Ratio", f"{(row['Loan_Balance_KES']/row.get('Monthly_Income_KES', 1))*100:.1f}%")

            # Valuable Detailed Info
            st.write("### Detailed Financial Profile")
            st.json({
                "Member Name": row['Name'],
                "Current Debt": f"KES {row['Loan_Balance_KES']:,.2f}",
                "Stability Index": "High" if risk_prob < 0.3 else "Moderate" if risk_prob < 0.7 else "Low",
                "Monthly Income": f"KES {row.get('Monthly_Income_KES', 0):,.2f}"
            })

            # Genius Advice Section
            st.divider()
            st.write("### 💡 Financial Improvement Suggestions")
            
            advice = []
            if credit_score < 750:
                advice.append(f"**Increase Savings:** Current savings are {row['Savings_Balance_KES']/row.get('Monthly_Income_KES', 1):.1f}x monthly income. Aim for 3x to boost score.")
            if row['Loan_Balance_KES'] > (row.get('Monthly_Income_KES', 0) * 5):
                advice.append("**Debt Consolidation:** High loan-to-income ratio detected. Advise member to clear small debts first.")
            if risk_prob > 0.5:
                advice.append("**Engagement:** Member has low activity. Suggest enrolling in the 'Golden Member' savings plan to improve stability.")
            
            if advice:
                for tip in advice:
                    st.info(tip)
            else:
                st.balloons()
                st.success("This member is in the top 1% of financial health. Eligible for maximum credit limit.")
                
        else:
            st.error("No member found with that ID. Please check the Dashboard to ensure the data is uploaded.")

st.sidebar.markdown("---")
st.sidebar.write("Developed by Macfeigh Bitange")