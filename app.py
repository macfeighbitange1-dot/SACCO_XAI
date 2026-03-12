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
        # Tries to load the sample data we generated
        return pd.read_csv('sacco_sample_data.csv')
    except:
        # Fallback if file isn't found
        return pd.DataFrame({'Error': ['Sample data not found. Please run generator.']})

df = load_data()

# 2. Sidebar for Navigation
st.sidebar.header("Control Panel")
analysis_type = st.sidebar.selectbox("Select View", ["Member Overview", "Individual Risk Analysis"])

if analysis_type == "Member Overview":
    st.subheader("Member Demographics & Churn Risk")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Members", len(df))
    col2.metric("At-Risk Members", len(df[df['Churn_Risk'] == 1]))
    col3.metric("Avg Savings (KES)", f"{df['Savings_Balance_KES'].mean():,.2f}")
    
    st.dataframe(df.head(10), use_container_width=True)

elif analysis_type == "Individual Risk Analysis":
    st.subheader("Explainable AI: Why is this member at risk?")
    member_id = st.selectbox("Select Member ID", df['Member_ID'].tolist())
    
    # Filter data for the specific member
    member_data = df[df['Member_ID'] == member_id].drop(['Member_ID', 'Churn_Risk'], axis=1)
    
    st.write(f"Analyzing Member: **{member_id}**")
    
    # Placeholder for SHAP - In a real app, you'd load your .json model here
    st.info("💡 In the production demo, this section will render the SHAP force plot explaining specific risk factors.")
    st.table(member_data)

st.sidebar.markdown("---")
st.sidebar.write("Developed by Macfeigh Bitange")