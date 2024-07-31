import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


# Sample data
data = {
    'point_a': ['A', 'B', 'A', 'C'],
    'point_b': ['B', 'C', 'C', 'D'],
    'distance': [50, 70, 30, 90],
    'avg_speed': [60, 55, 70, 65],
    'max_speed': [100, 90, 120, 110],
    'min_speed': [40, 30, 50, 45],
    'road_condition': ['Good', 'Fair', 'Poor', 'Good'],
    'date': ['2024-07-30', '2024-07-31', '2024-08-01', '2024-08-02'],
    'departure_time': ['08:00', '09:00', '10:00', '11:00'],
    'num_pitstops': [1, 0, 2, 1],
    'vehicle_type': ['Sedan', 'SUV', 'Truck', 'Sedan'],
    'vehicle_weight': [1500, 2000, 3500, 1600],
    'driver_age': [35, 40, 50, 30],
    'fuel_capacity': [50, 60, 80, 55],
    'traffic_condition': ['Light', 'Heavy', 'Moderate', 'Light'],
    'travel_time': [50, 70, 30, 90]  # time in minutes
}

# Convert the dictionary to a pandas DataFrame
df = pd.DataFrame(data)

# Preprocessing
X = df.drop('travel_time', axis=1)
y = df['travel_time']

# Column transformer to handle preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), [
            'distance', 'avg_speed', 'max_speed', 'min_speed', 'vehicle_weight', 'driver_age', 'fuel_capacity'
        ]),
        ('cat', OneHotEncoder(handle_unknown='ignore'), [
            'point_a', 'point_b', 'road_condition', 'date', 'departure_time', 'vehicle_type', 'traffic_condition'
        ])
    ],
    remainder='passthrough'
)

# Define the pipeline with preprocessing and model
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Predict travel time for new data
new_data = pd.DataFrame({
    'point_a': ['A'],
    'point_b': ['B'],
    'distance': [55],
    'avg_speed': [65],
    'max_speed': [105],
    'min_speed': [45],
    'road_condition': ['Good'],
    'date': ['2024-08-01'],
    'departure_time': ['09:30'],
    'num_pitstops': [1],
    'vehicle_type': ['Sedan'],
    'vehicle_weight': [1600],
    'driver_age': [33],
    'fuel_capacity': [55],
    'traffic_condition': ['Light']
})

predicted_time = model.predict(new_data)
print(f"Predicted travel time: {predicted_time[0]} minutes")
