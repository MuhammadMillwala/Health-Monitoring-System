import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load the data
data = pd.read_csv('heart.csv')

# Separate the features and the target
X = data.drop(columns='target')
y = data['target']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest model
random_forest_model = RandomForestClassifier(n_estimators=500, max_depth=16, min_samples_split=10)
random_forest_model.fit(X_train, y_train)

# Evaluate the model
y_pred = random_forest_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Random Forest model accuracy: {accuracy:.2f}")

# Save the trained model
joblib.dump(random_forest_model, 'random_forest_heart_disease_model.pkl')


