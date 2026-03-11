import pandas as pd
import numpy as np

def generate_sacco_data(n=1000):
    np.random.seed(42)
    data = {
        'member_id': range(1, n + 1),
        'monthly_savings_avg': np.random.randint(2000, 50000, n),
        'savings_volatility': np.random.uniform(0, 1, n), 
        'existing_loans_count': np.random.randint(0, 5, n),
        'mpesa_in_out_ratio': np.random.uniform(0.5, 2.5, n),
        'guarantor_score': np.random.randint(300, 850, n),
        'age': np.random.randint(18, 70, n),
        'defaulted': np.random.choice([0, 1], n, p=[0.85, 0.15])
    }
    
    df = pd.DataFrame(data)
    # Genius Logic: High volatility + low savings = higher chance of default
    df.loc[(df['savings_volatility'] > 0.7) & (df['monthly_savings_avg'] < 5000), 'defaulted'] = 1
    df.to_csv('sacco_members.csv', index=False)
    print("✅ Success: 'sacco_members.csv' generated with 1,000 records.")

if __name__ == "__main__":
    generate_sacco_data() # Fixed the function call here