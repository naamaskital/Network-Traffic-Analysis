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

# Required columns for dataset
required_columns = {"Timestamp", "Size", "Source IP", "Dest IP", "Source Port", "Dest Port", "Classification"}

# 1. Try to load the dataset
try:
    df = pd.read_csv('combined_dataset.csv')
except FileNotFoundError:
    print("Error: The file 'combined_dataset.csv' was not found.")
    exit()

# 2. Simple dataset validation
if not required_columns.issubset(df.columns):
    missing = required_columns - set(df.columns)
    print(f"Error: Missing required columns: {missing}")
    exit()

# Handle missing values
missing_values = df.isnull().sum()
if missing_values.any():
    print("Warning: Dataset contains missing values.")
    print(missing_values[missing_values > 0])  # Show which columns have missing values

    # Fill missing values with the last valid value (forward fill)
    df.ffill(inplace=True)

    # Fill remaining missing values with the next valid value (backward fill)
    df.bfill(inplace=True)

    # If there are still missing values (unlikely), drop the rows
    df.dropna(inplace=True)

if not pd.api.types.is_numeric_dtype(df["Classification"]):
    print("Error: 'Classification' column must be numeric.")
    exit()

if not pd.api.types.is_numeric_dtype(df["Classification"]):
    print("Error: 'Classification' column must be numeric.")
    exit()

print("✅ Dataset validation passed. Proceeding with processing...")

# 3. Convert Source IP and Dest IP to numeric values
df["Source IP Numeric"] = df["Source IP"].apply(ip_to_int)
df["Dest IP Numeric"] = df["Dest IP"].apply(ip_to_int)

# 4. Create Flow ID
df["Flow ID"] = df["Source IP Numeric"].astype(str) + "_" + df["Dest IP Numeric"].astype(str) + "_" + df["Source Port"].astype(str) + "_" + df["Dest Port"].astype(str)

# 5. Convert Flow ID to a numeric hash
df["Flow ID Hash"] = df["Flow ID"].apply(lambda x: int(hashlib.sha256(x.encode()).hexdigest(), 16) % 10**8)

# 6. Compute Inter-Arrival Time
df["Inter-Arrival Time"] = df.groupby("Flow ID Hash")["Timestamp"].diff().fillna(0)

# 7. Select features
features_case1 = df[["Size", "Timestamp", "Flow ID Hash", "Inter-Arrival Time"]]
features_case2 = df[["Size", "Timestamp", "Inter-Arrival Time"]]
labels = df["Classification"]

# 8. Split data
X_train1, X_test1, y_train1, y_test1 = train_test_split(features_case1, labels, test_size=0.3, random_state=42, shuffle=True)
X_train2, X_test2, y_train2, y_test2 = train_test_split(features_case2, labels, test_size=0.3, random_state=42, shuffle=True)

# 9. Scale features
scaler = StandardScaler()
X_train1 = scaler.fit_transform(X_train1)
X_test1 = scaler.transform(X_test1)
X_train2 = scaler.fit_transform(X_train2)
X_test2 = scaler.transform(X_test2)

# 10. Train Random Forest models
clf1 = RandomForestClassifier(n_estimators=5, random_state=42)
clf2 = RandomForestClassifier(n_estimators=5, random_state=42)

clf1.fit(X_train1, y_train1)
clf2.fit(X_train2, y_train2)

# 11. Make predictions
y_pred1 = clf1.predict(X_test1)
y_pred2 = clf2.predict(X_test2)

# 12. Evaluate accuracy
accuracy_case1 = accuracy_score(y_test1, y_pred1)
accuracy_case2 = accuracy_score(y_test2, y_pred2)

# 13. Output results
print(f"Accuracy for Case 1 (Flow ID included): {accuracy_case1:.4f}")
print(f"Accuracy for Case 2 (Without Flow ID): {accuracy_case2:.4f}")
