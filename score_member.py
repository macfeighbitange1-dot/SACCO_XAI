import pandas as pd
import pickle
import shap
import matplotlib.pyplot as plt
import sys

def explain_decision(member_id):
    # 1. Load the archived brain
    with open('sacco_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('shap_explainer.pkl', 'rb') as f:
        explainer = pickle.load(f)
        
    # 2. Load the data to find the member
    df = pd.read_csv('sacco_members.csv')
    member_data = df[df['member_id'] == member_id]
    
    if member_data.empty:
        print(f"❌ Error: Member ID {member_id} not found in database.")
        return

    # Prepare features for prediction
    features = member_data.drop(['member_id', 'defaulted'], axis=1)
    
    # 3. Get Prediction
    prob = model.predict_proba(features)[0][1]
    decision = "REJECTED" if prob > 0.5 else "APPROVED"
    color = "red" if decision == "REJECTED" else "green"
    
    print(f"\n--- SACCO CREDIT REPORT: MEMBER {member_id} ---")
    print(f"RISK PROBABILITY: {prob:.2%}")
    print(f"DECISION: {decision}")
    print("------------------------------------------")
    print("Generating Explainability Plot... Close the window to exit.")

    # 4. Generate SHAP Waterfall Plot
    shap_values = explainer(features)
    
    # Plotting
    plt.figure(figsize=(10, 6))
    shap.plots.waterfall(shap_values[0], show=False)
    plt.title(f"Credit Decision Factors for Member {member_id} ({decision})")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        explain_decision(int(sys.argv[1]))
    else:
        print("Usage: python score_member.py <member_id>")
        print("Try: python score_member.py 10")