import pickle
import shap
import matplotlib.pyplot as plt
import sys

# Load the brain
with open('sacco_model.pkl', 'rb') as f:
    model, explainer, X_test = pickle.load(f)

def explain_decision(member_index):
    # Get specific member data
    member_data = X_test.iloc[[member_index]]
    
    # Get prediction
    prob = model.predict_proba(member_data)[0][1]
    decision = "REJECT" if prob > 0.5 else "APPROVE"
    
    print(f"\nANALYSIS FOR MEMBER AT INDEX: {member_index}")
    print(f"Risk Probability: {prob:.2%}")
    print(f"Final Decision: {decision}")
    print("-" * 30)
    
    # Generate SHAP values for this person
    shap_values = explainer(member_data)
    
    # Create the visualization
    plt.figure(figsize=(10,6))
    shap.plots.waterfall(shap_values[0], show=False)
    plt.title(f"Decision Logic: Member {member_index} ({decision})")
    
    filename = f"decision_member_{member_index}.png"
    plt.savefig(filename, bbox_inches='tight')
    print(f"Explanation Plot saved as: {filename}")

if __name__ == "__main__":
    # Test with the first member in the test set
    index_to_test = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    explain_decision(index_to_test)