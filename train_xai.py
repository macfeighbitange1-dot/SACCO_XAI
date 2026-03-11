import pandas as pd
import xgboost as xgb
import shap
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

def train_sacco_model():
    print("🧠 Loading member data...")
    df = pd.read_csv('sacco_members.csv')
    
    # Separate features (X) and Target (y)
    X = df.drop(['member_id', 'defaulted'], axis=1)
    y = df['defaulted']
    
    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("🚀 Training XGBoost Engine...")
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Check performance
    preds = model.predict(X_test)
    print(f"✅ Training Complete. Accuracy: {accuracy_score(y_test, preds):.2%}")
    
    # Save the model and the explainer to files
    print("💾 Saving model for deployment...")
    with open('sacco_model.pkl', 'wb') as f:
        pickle.dump(model, f)
        
    # Create the SHAP Explainer
    explainer = shap.TreeExplainer(model)
    with open('shap_explainer.pkl', 'wb') as f:
        pickle.dump(explainer, f)
        
    print("🎉 System Ready: Model and Explainer have been archived.")

if __name__ == "__main__":
    train_sacco_model()