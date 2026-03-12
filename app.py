import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
import shap
import matplotlib.pyplot as plt

# Page Config
st.set_page_config(page_title="SACCO_XAI | Predictive Intelligence", layout="wide")

st.title("📊 SACCO Member Retention & XAI Dashboard")
st.markdown("---")

# 1. Load Data
@st.cache_data
def load_data():
    try:
        # UPDATED: Matches your 'sacco_members.csv' filename
        return pd.read_csv('sacco_members.csv')
    except Exception as e:
        # Fallback if file isn't found
        return pd.DataFrame({'Error': [f'Data file not found: {str(e)}']})

df = load_data()

# Check if data loaded correctly before proceeding
if 'Error' in df.columns:
    st.error(df['Error'][0])
    st.stop()

# 2. Sidebar for Navigation
st.sidebar.header("Control Panel")
analysis_type = st.sidebar.selectbox("Select View", ["Member Overview", "Individual Risk Analysis"])

if analysis_type == "Member Overview":
    st.subheader("Member Demographics & Churn Risk")
    
    # Calculate Metrics
    total_members = len(df)
    at_risk = len(df[df['Churn_Risk'] == 1]) if 'Churn_Risk' in df.columns else 0
    avg_savings = df['Savings_Balance_KES'].mean() if 'Savings_Balance_KES' in df.columns else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Members", total_members)
    col2.metric("At-Risk Members", at_risk)
    col3.metric("Avg Savings (KES)", f"{avg_savings:,.2f}")
    
    st.write("### Recent Member Log")
    st.dataframe(df.head(20), use_container_width=True)

elif analysis_type == "Individual Risk Analysis":
    st.subheader("Explainable AI: Why is this member at risk?")
    
    if 'Member_ID' in df.columns:
        member_id = st.selectbox("Select Member ID", df['Member_ID'].unique())
        
        # Filter data for the specific member
        member_row = df[df['Member_ID'] == member_id]
        # Drop non-feature columns for display
        display_data = member_row.drop(['Member_ID'], axis=1, errors='ignore')
        
        st.write(f"Analyzing Member: **{member_id}**")
        
        # Visual Indicators
        risk_status = "High Risk" if member_row['Churn_Risk'].values[0] == 1 else "Low Risk"
        color = "red" if risk_status == "High Risk" else "green"
        st.markdown(f"Status: **:{color}[{risk_status}]**")
        
        # Data Table
        st.table(display_data)
        
        st.info("💡 SHAP Explanations: In the live model, a Force Plot would appear here to show exactly which features (e.g., Low Savings or High Defaults) pushed this member toward Churn.")
    else:
        st.warning("Member_ID column not found in data.")

st.sidebar.markdown("---")
st.sidebar.write("Developed by Macfeigh Bitange")