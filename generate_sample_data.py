import pandas as pd
import random

# Generate sample transaction data
# Create some accounts that will have multiple fraudulent transactions
account_ids = ['ACC1001', 'ACC1002', 'ACC1003', 'ACC1004', 'ACC1005', 
               'ACC1006', 'ACC1007', 'ACC1008', 'ACC1009', 'ACC1010']

# Some accounts will have multiple suspicious transactions
transaction_accounts = [
    'ACC1001', 'ACC1002', 'ACC1003', 'ACC1002',  # ACC1002 has 2 transactions
    'ACC1004', 'ACC1005', 'ACC1002', 'ACC1006',  # ACC1002 has 3 total
    'ACC1007', 'ACC1008', 'ACC1009', 'ACC1010',
    'ACC1001', 'ACC1003', 'ACC1004', 'ACC1005',  # ACC1001 has 2 total
    'ACC1006', 'ACC1007', 'ACC1008', 'ACC1001'   # ACC1001 has 3 total
]

data = {
    'AccountID': transaction_accounts,
    'TransactionAmount': [1500, 7500, 2300, 9800, 500, 3200, 12000, 450, 5600, 15000,
                          800, 6200, 1800, 4500, 700, 8900, 3400, 600, 11000, 2100],
    'TransactionDuration': [45, 5, 30, 8, 60, 25, 3, 90, 15, 2,
                           55, 12, 40, 20, 70, 7, 28, 65, 4, 35],
    'LoginAttempts': [1, 5, 2, 4, 1, 2, 6, 1, 3, 7,
                     1, 4, 2, 2, 1, 5, 2, 1, 8, 2],
    'AccountBalance': [15000, 8000, 25000, 10000, 12000, 18000, 5000, 30000, 20000, 8000,
                      22000, 12000, 16000, 24000, 14000, 9000, 19000, 28000, 6000, 17000],
    'CustomerAge': [35, 22, 45, 28, 52, 38, 19, 60, 31, 75,
                   42, 26, 50, 36, 48, 23, 41, 58, 21, 44]
}

# Create DataFrame
df = pd.DataFrame(data)

# Add TransactionID and other columns
df['TransactionID'] = [f'TXN{str(i).zfill(4)}' for i in range(1, 21)]
df['TransactionDate'] = pd.date_range(start='2025-01-01', periods=20, freq='D')
df['MerchantCategory'] = random.choices(['Retail', 'Online', 'Dining', 'Travel', 'Entertainment'], k=20)

# Reorder columns - AccountID first, then TransactionID
df = df[['AccountID', 'TransactionID', 'TransactionDate', 'TransactionAmount', 'TransactionDuration', 
         'LoginAttempts', 'AccountBalance', 'CustomerAge', 'MerchantCategory']]

# Save to both Excel and CSV
df.to_excel('sample_transactions.xlsx', index=False)
print("✓ Sample Excel file created: sample_transactions.xlsx")

df.to_csv('sample_transactions.csv', index=False)
print("✓ Sample CSV file created: sample_transactions.csv")

print(f"\n✓ Generated {len(df)} sample transactions")
print("\nPreview:")
print(df.head())
