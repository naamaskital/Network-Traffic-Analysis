import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import socket
import struct
import hashlib

# Function to convert IP to a number
def ip_to_int(ip):
    return struct.unpack("!I", socket.inet_aton(ip))[0]

# 1. Try to load the dataset
try:
    df = pd.read_csv('combined_dataset.csv')
except FileNotFoundError:
    print("Error: The file 'combined_dataset.csv' was not found.")
    # Optionally, print the current working directory for reference
    print(f"Current working directory: {os.getcwd()}")
    exit()  # Exit or handle as needed

# 2. Check if dataset is valid
if df.empty or 'Size' not in df.columns or 'Timestamp' not in df.columns:
    print("Dataset is empty or missing essential columns.")
    exit()

# 3. Convert Source IP and Dest IP to numeric values
df['Source IP Numeric'] = df['Source IP'].apply(ip_to_int)
df['Dest IP Numeric'] = df['Dest IP'].apply(ip_to_int)

# 4. Create Flow ID from Source IP, Dest IP, Source Port, Dest Port
df['Flow ID'] = df['Source IP Numeric'].astype(str) + "_" + df['Dest IP Numeric'].astype(str) + "_" + df['Source Port'].astype(str) + "_" + df['Dest Port'].astype(str)

# 5. Convert the 'Flow ID' to a numeric value (using sha256 for stability)
df['Flow ID Hash'] = df['Flow ID'].apply(lambda x: int(hashlib.sha256(x.encode()).hexdigest(), 16) % 10**8)

# 6. Compute "Inter-Arrival Time" since attacker can infer it
df['Inter-Arrival Time'] = df.groupby('Flow ID Hash')['Timestamp'].diff().fillna(0)

# 7. Select features for each case
#  תרחיש 1 – עם Flow Hash
features_case1 = df[['Size', 'Timestamp', 'Flow ID Hash', 'Inter-Arrival Time']]

#  תרחיש 2 – בלי Flow Hash (אבל עם Inter-Arrival Time)
features_case2 = df[['Size', 'Timestamp', 'Inter-Arrival Time']]

# Target variable (app classification)
labels = df['Classification']

# 8. Split the data into training and testing sets
X_train1, X_test1, y_train1, y_test1 = train_test_split(features_case1, labels, test_size=0.3, random_state=42, shuffle=True)
X_train2, X_test2, y_train2, y_test2 = train_test_split(features_case2, labels, test_size=0.3, random_state=42, shuffle=True)

# 9. Scale the features (Standardization)
scaler = StandardScaler()
X_train1 = scaler.fit_transform(X_train1)
X_test1 = scaler.transform(X_test1)

X_train2 = scaler.fit_transform(X_train2)
X_test2 = scaler.transform(X_test2)

# 10. Initialize Random Forest model with more trees for better accuracy
clf1 = RandomForestClassifier(n_estimators=5, random_state=42)
clf2 = RandomForestClassifier(n_estimators=5, random_state=42)

# 11. Train the models
clf1.fit(X_train1, y_train1)
clf2.fit(X_train2, y_train2)

# 12. Make predictions
y_pred1 = clf1.predict(X_test1)
y_pred2 = clf2.predict(X_test2)

# 13. Evaluate performance
accuracy_case1 = accuracy_score(y_test1, y_pred1)
accuracy_case2 = accuracy_score(y_test2, y_pred2)

# 14. Output results
print(f"Accuracy for Case 1 (Flow ID included): {accuracy_case1:.4f}")
print(f"Accuracy for Case 2 (Without Flow ID): {accuracy_case2:.4f}")
