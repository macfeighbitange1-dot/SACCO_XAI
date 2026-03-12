import streamlit as st
import pandas as pd
import os

# Page Config
st.set_page_config(page_title="SACCO_XAI | Core Engine", layout="wide")

# --- DATA PERSISTENCE LOGIC ---
DATA_FILE = 'sacco_members.csv'

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

@st.cache_data
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=['Member_ID', 'Name', 'Savings_Balance_KES', 'Loan_Balance_KES', 'Churn_Risk'])

# --- APP UI ---
st.title("🛡️ SACCO_XAI: Management & Credit Scoring")

# Load existing data
df = load_data()

# Sidebar Navigation
menu = st.sidebar.radio("Navigation", ["Dashboard", "Search & Credit Score", "Add/Upload Clients"])

# --- 1. ADD/UPLOAD CLIENTS ---
if menu == "Add/Upload Clients":
    st.subheader("📥 Data Ingestion")
    
    tab1, tab2 = st.tabs(["Add Single Client", "Bulk Upload (CSV)"])
    
    with tab1:
        with st.form("add_member_form"):
            m_id = st.text_input("Member ID (e.g., M-1001)")
            name = st.text_input("Full Name")
            savings = st.number_input("Savings Balance (KES)", min_value=0)
            loans = st.number_input("Loan Balance (KES)", min_value=0)
            submit = st.form_submit_button("Register Client")
            
            if submit:
                new_row = pd.DataFrame([[m_id, name, savings, loans, 0]], 
                                       columns=['Member_ID', 'Name', 'Savings_Balance_KES', 'Loan_Balance_KES', 'Churn_Risk'])
                df = pd.concat([df, new_row], ignore_index=True)
                save_data(df)
                st.success(f"Client {name} added successfully!")

    with tab2:
        uploaded_file = st.file_uploader("Upload Client CSV", type=["csv"])
        if uploaded_file:
            new_data = pd.read_csv(uploaded_file)
            df = pd.concat([df, new_data], ignore_index=True).drop_duplicates(subset=['Member_ID'])
            save_data(df)
            st.success("Bulk data integrated successfully.")

# --- 2. SEARCH & CREDIT SCORE ---
elif menu == "Search & Credit Score":
    st.subheader("🔍 Individual Client Search")
    
    search_query = st.text_input("Enter Member ID or Name to Search")
    
    if search_query:
        # Search filter
        results = df[df['Member_ID'].str.contains(search_query, case=False, na=False) | 
                    df['Name'].str.contains(search_query, case=False, na=False)]
        
        if not results.empty:
            for index, row in results.iterrows():
                with st.expander(f"Results for: {row['Name']} ({row['Member_ID']})"):
                    col1, col2 = st.columns(2)
                    col1.write(f"**Savings:** KES {row['Savings_Balance_KES']:,.2f}")
                    col1.write(f"**Loans:** KES {row['Loan_Balance_KES']:,.2f}")
                    
                    # Credit Score Calculation Logic
                    risk_prob = row.get('Churn_Risk', 0.5)
                    credit_score = int(850 - (risk_prob * 550))
                    
                    col2.metric("Credit Score", credit_score)
                    if credit_score > 650:
                        st.success("Status: Low Risk / High Creditworthiness")
                    else:
                        st.error("Status: High Risk / Action Required")
        else:
            st.warning("No client found with those details.")

# --- 3. DASHBOARD ---
else:
    st.subheader("📈 SACCO Portfolio Overview")
    st.dataframe(df, use_container_width=True)