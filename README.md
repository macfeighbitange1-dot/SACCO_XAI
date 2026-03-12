# SACCO_XAI: Financial Intelligence & Predictive Analytics
**Explainable AI (XAI) for Member Retention and Risk Management**

## 📌 Executive Overview
SACCO_XAI is a high-performance predictive engine designed to optimize member retention for SACCOs. By leveraging **XGBoost** for predictive modeling and **SHAP (SHapley Additive exPlanations)** for transparency, the system doesn't just predict *who* might leave—it explains *why*.

This project bridges the gap between complex machine learning and actionable financial decisions.

---

## 🚀 Core Features
* **Churn Prediction:** High-accuracy identification of at-risk members using Gradient Boosting.
* **Explainable AI:** Individualized breakdown of risk factors (e.g., loan frequency, savings volatility).
* **Predictive Dashboard:** Real-time Streamlit interface for management decision-making.
* **Vantage-Equity Integration:** RAG-enabled analysis of financial annual reports for contextual insights.

---

## 🛠 Technical Architecture
The system is built for **resilient, offline deployment** in air-gapped environments typical of financial institutions.

* **Language:** Python 3.12
* **Core ML:** XGBoost 2.0.3, Scikit-Learn
* **Explainability:** SHAP 0.45.0
* **Frontend:** Streamlit
* **Deployment:** Docker (Linux-containerized for portability)

---

## 📦 Deployment Guide (IT Teams)

### 1. Standard Installation (Online)
If internet access is available, clone and install:
```bash
git clone [https://github.com/macfeighbitange1-dot/SACCO_XAI.git](https://github.com/macfeighbitange1-dot/SACCO_XAI.git)
cd SACCO_XAI
pip install -r requirements.txt
streamlit run app.py
