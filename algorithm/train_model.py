from datetime import date, datetime, timedelta

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, StackingRegressor
from sklearn.linear_model import RidgeCV
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from api import google_maps

# Sample data
data = pd.read_csv("../data/vehicle_eta_training_data.csv")

# Convert the dictionary to a pandas DataFrame
df = pd.DataFrame(data)

# Preprocessing
X = df.drop('travel_time', axis=1)
y = df['travel_time']

# Column transformer to handle preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), [
            'distance', 'max_speed', 'road_condition', 'driver_age', 'traffic_condition'
        ]),
        ('cat', OneHotEncoder(handle_unknown='ignore'), [
            'point_a', 'point_b', 'date', 'departure_time', 'vehicle_type'
        ])
    ],
    remainder='passthrough'
)

# Define the base models
rf = RandomForestRegressor(n_estimators=100, random_state=42)
gb = GradientBoostingRegressor(n_estimators=100, random_state=42)

# Define the stacking ensemble with base models and a meta-model
stacking_model = StackingRegressor(
    estimators=[('rf', rf), ('gb', gb)],
    final_estimator=RidgeCV()
)

# Define the pipeline with preprocessing and model
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', stacking_model)
])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model.fit(
    X_train,
    y_train
)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Save the model to a file
joblib.dump(model, '../model.h5')
