from datetime import date, datetime, timedelta

import joblib
import pandas as pd

from api import google_maps

# User only inputs point A, B, max_speed, vehicle_type, driver_age
new_data = pd.DataFrame({
    'point_a': ['100 Universal City Plaza, Universal City, CA'],
    'point_b': ['1600 Amphitheatre Parkway, Mountain View, CA'],
    'distance': [""],
    'max_speed': [75],
    'road_condition': [""],
    'traffic_condition': [""],
    'date': [date.today().strftime('%Y-%m-%d')],
    'departure_time': [(datetime.now() + timedelta(hours=1)).strftime('%H:%M')],
    'vehicle_type': ['Motorcycle'],
    'driver_age': [59]
})

departure_time = datetime.now() + timedelta(hours=1)
distance, road_condition, traffic_condition, _ = google_maps.get_conditions(
    new_data.at[0, 'point_a'], new_data.at[0, 'point_b'], departure_time
)
new_data.at[0, 'distance'] = distance
new_data.at[0, 'road_condition'] = road_condition
new_data.at[0, 'traffic_condition'] = traffic_condition

model = joblib.load('../model.h5')

print(f'Distance: {distance}')
print(f'Road Condition: {road_condition}')
print(f'Traffic Condition: {traffic_condition}')


predicted_time = model.predict(new_data)
print(f"Predicted travel time: {predicted_time[0]} hours")
