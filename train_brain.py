import pandas as pd
import xgboost as xgb
import shap
import pickle
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# 1. Load the data
print("--- Loading SACCO Member Data ---")
df = pd.read_csv('sacco_members.csv')
X = df.drop(['member_id', 'defaulted'], axis=1)
y = df['defaulted']

# 2. Split for validation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Train the XGBoost Model
print("--- Training XGBoost Intelligence Engine ---")
model = xgb.XGBClassifier(
    n_estimators=100,
    learning_rate=0.05,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8
)
model.fit(X_train, y_train)

# 4. Initialize SHAP Explainer
print("--- Initializing XAI (Explainability) Layer ---")
explainer = shap.TreeExplainer(model)

# 5. Save the "Brain" and "Explainer" so we don't have to retrain
with open('sacco_model.pkl', 'wb') as f:
    pickle.dump((model, explainer, X_test), f)

print("--- Success: Model and Explainer saved to 'sacco_model.pkl' ---")