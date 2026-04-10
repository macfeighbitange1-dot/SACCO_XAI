import pandas as pd
import numpy as np

def generate_enterprise_data(filename='sacco_members.csv', n=10):
    np.random.seed(42)
    
    # Generate realistic names
    first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth"]
    last_names = ["Kamau", "Ochieng", "Njoroge", "Musa", "Wanjiku", "Otieno", "Mwangi", "Mutua", "Kibet", "Cherono"]
    
    data = []
    for i in range(n):
        income = np.random.randint(30000, 250000) # Monthly Income in KES
        savings = np.random.uniform(5000, income * 5) # Savings usually tied to income
        loans = np.random.uniform(0, income * 10) # Some have high debt
        
        # Calculate a logical Churn_Risk between 0 and 1
        # Risk increases if loans are high relative to savings/income
        risk_calc = (loans / (savings + income)) * 0.5
        churn_risk = round(min(max(risk_calc, 0.05), 0.95), 2)
        
        data.append({
            'Member_ID': f'M-{1000 + i}',
            'Name': f"{first_names[i]} {last_names[i]}",
            'Savings_Balance_KES': round(savings, 2),
            'Loan_Balance_KES': round(loans, 2),
            'Churn_Risk': churn_risk,
            'Monthly_Income_KES': income
        })
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"✅ Success: '{filename}' created with {n} professional records.")

if __name__ == "__main__":
    generate_enterprise_data()