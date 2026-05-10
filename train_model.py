print("Program Started")

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

print("Libraries Imported Successfully")

# Load dataset
print("Loading CSV File...")

df = pd.read_csv("creditcard.csv")

print("Dataset Loaded Successfully")
print("Dataset Shape:", df.shape)

# Show first 5 rows
print(df.head())

# Features and labels
print("Preparing Features and Labels...")

X = df.drop("Class", axis=1)
y = df["Class"]

print("Splitting Dataset...")

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training Model...")

# Train model
model = RandomForestClassifier(n_estimators=100)

model.fit(X_train, y_train)

print("Model Training Completed")

# Predict
print("Making Predictions...")

y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)

# Save model
joblib.dump(model, "fraud_model.pkl")

print("Model Saved Successfully")
print("Project Finished")