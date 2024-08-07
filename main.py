from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

from api import google_maps

# Sample data
data = pd.read_csv("data/vehicle_eta_training_data.csv")

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
    'point_a': ['1600 Pennsylvania Ave NW, Washington, DC'],
    'point_b': ['350 5th Ave, New York, NY'],
    'distance': [226],
    'max_speed': [75],
    'road_condition': [np.random.choice([0, 1, 2, 3])],  # Random road condition
    'traffic_condition': [np.random.choice([0, 1, 2])],  # Random traffic condition
    'date': [date.today().strftime('%Y-%m-%d')],
    'departure_time': [(datetime.now() + timedelta(hours=1)).strftime('%H:%M')],
    'vehicle_type': ['SUV'],
    'driver_age': [35]
})

departure_time = datetime.now() + timedelta(hours=1)
distance, road_condition, traffic_condition, _ = google_maps.get_conditions(
    new_data.at[0, 'point_a'], new_data.at[0, 'point_b'], departure_time
)
new_data.at[0, 'distance'] = distance
new_data.at[0, 'road_condition'] = road_condition
new_data.at[0, 'traffic_condition'] = traffic_condition

predicted_time = model.predict(new_data)
print(f"Predicted travel time: {predicted_time[0]} hours")