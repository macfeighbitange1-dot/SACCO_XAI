import pandas as pd
import xgboost as xgb
import shap
from sklearn.model_selection import train_test_split

# 1. Load Data
df = pd.read_csv('sacco_members.csv')
X = df.drop(['member_id', 'defaulted'], axis=1)
y = df['defaulted']

# 2. Train Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Train XGBoost (The "Speed" Engine)
model = xgb.XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.1)
model.fit(X_train, y_train)

# 4. SHAP (The "Truth" Engine)
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

print("Model Trained. We now have the 'Power of Explanation'.")