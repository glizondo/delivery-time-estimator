import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

locations = [
    ("1600 Pennsylvania Ave NW, Washington, DC", "350 5th Ave, New York, NY", 226),
    ("1 Infinite Loop, Cupertino, CA", "600 Montgomery St, San Francisco, CA", 43),
    ("233 S Wacker Dr, Chicago, IL", "1600 Amphitheatre Parkway, Mountain View, CA", 2140),
    ("405 Lexington Ave, New York, NY", "1600 Pennsylvania Ave NW, Washington, DC", 228),
    ("4 Pennsylvania Plaza, New York, NY", "1500 Sugar Bowl Dr, New Orleans, LA", 1193),
    ("1 Dr Carlton B Goodlett Pl, San Francisco, CA", "1600 Pennsylvania Ave NW, Washington, DC", 2835),
    ("1211 Avenue of the Americas, New York, NY", "350 5th Ave, New York, NY", 226),
    ("701 5th Ave, Seattle, WA", "233 S Wacker Dr, Chicago, IL", 2065),
    ("1 Microsoft Way, Redmond, WA", "701 5th Ave, Seattle, WA", 16),
    ("1 Apple Park Way, Cupertino, CA", "600 Montgomery St, San Francisco, CA", 43),
    ("2755 Station Club Dr, Suwanee, GA", "350 5th Ave, New York, NY", 754),
    ("100 Universal City Plaza, Universal City, CA", "1 Infinite Loop, Cupertino, CA", 343),
    ("350 5th Ave, New York, NY", "233 S Wacker Dr, Chicago, IL", 791),
    ("1 Googleplex, Mountain View, CA", "1 Apple Park Way, Cupertino, CA", 43),
    ("1 Hacker Way, Menlo Park, CA", "1 Infinite Loop, Cupertino, CA", 128),
    ("120 Broadway, New York, NY", "1600 Pennsylvania Ave NW, Washington, DC", 227),
    ("1515 Broadway, New York, NY", "1600 Amphitheatre Parkway, Mountain View, CA", 2889),
    ("721 Broadway, New York, NY", "1600 Pennsylvania Ave NW, Washington, DC", 226),
    ("400 Broad St, Seattle, WA", "1600 Amphitheatre Parkway, Mountain View, CA", 842),
    ("1600 Amphitheatre Parkway, Mountain View, CA", "1 Infinite Loop, Cupertino, CA", 43),
    ("11 Wall St, New York, NY", "1600 Pennsylvania Ave NW, Washington, DC", 228),
    ("1 Times Square, New York, NY", "1600 Pennsylvania Ave NW, Washington, DC", 227),
    ("30 Rockefeller Plaza, New York, NY", "1600 Pennsylvania Ave NW, Washington, DC", 228),
    ("1 World Trade Center, New York, NY", "1600 Pennsylvania Ave NW, Washington, DC", 227),
    ("1500 Broadway, New York, NY", "1600 Pennsylvania Ave NW, Washington, DC", 227),
    ("1211 Avenue of the Americas, New York, NY", "1600 Pennsylvania Ave NW, Washington, DC", 227),
    ("45 Rockefeller Plaza, New York, NY", "1600 Pennsylvania Ave NW, Washington, DC", 228),
    ("333 Bush St, San Francisco, CA", "1 Infinite Loop, Cupertino, CA", 128),
    ("1 Hacker Way, Menlo Park, CA", "1600 Amphitheatre Parkway, Mountain View, CA", 128),
    ("500 Terry A Francois Blvd, San Francisco, CA", "1 Infinite Loop, Cupertino, CA", 128),
    ("401 N Michigan Ave, Chicago, IL", "1600 Amphitheatre Parkway, Mountain View, CA", 2142),
    ("1 Market St, San Francisco, CA", "1 Infinite Loop, Cupertino, CA", 128),
    ("1 Franklin Pkwy, San Mateo, CA", "1 Infinite Loop, Cupertino, CA", 128),
    ("1601 Willow Rd, Menlo Park, CA", "1 Infinite Loop, Cupertino, CA", 128),
    ("1515 Broadway, New York, NY", "233 S Wacker Dr, Chicago, IL", 791),
    ("2755 Station Club Dr, Suwanee, GA", "1600 Pennsylvania Ave NW, Washington, DC", 546),
    ("742 Evergreen Terrace, Springfield, IL", "1600 Amphitheatre Parkway, Mountain View, CA", 2171),
    ("100 Universal City Plaza, Universal City, CA", "1600 Amphitheatre Parkway, Mountain View, CA", 343),
    ("350 5th Ave, New York, NY", "1 Infinite Loop, Cupertino, CA", 2907),
    ("1 Googleplex, Mountain View, CA", "233 S Wacker Dr, Chicago, IL", 2141),
    ("1 Hacker Way, Menlo Park, CA", "350 5th Ave, New York, NY", 2885),
    ("120 Broadway, New York, NY", "1 Infinite Loop, Cupertino, CA", 2891),
    ("1515 Broadway, New York, NY", "1600 Pennsylvania Ave NW, Washington, DC", 227),
    ("721 Broadway, New York, NY", "1600 Amphitheatre Parkway, Mountain View, CA", 2887)
]

def random_dates(start, end, n=1):
    start_u = start.value // 10**9
    end_u = end.value // 10**9
    dates = pd.to_datetime(np.random.randint(start_u, end_u, n), unit='s')
    return dates.strftime('%Y-%m-%d')

def generate_vehicle_eta_data(num_rows):
    data = []

    for _ in range(num_rows):
        point = random.choice(locations)
        point_a = point[0]
        point_b = point[1]
        distance = point[2]

        avg_speed = round(np.random.uniform(25, 60), 2)
        min_speed = round(avg_speed - np.random.uniform(10, 15), 2)
        max_speed = round(avg_speed + np.random.uniform(10, 20), 2)

        min_speed = round(min(min_speed, avg_speed - 1), 2)
        max_speed = round(max(max_speed, avg_speed + 1), 2)

        if min_speed > max_speed or min_speed < 40 or max_speed > 80:
            continue

        base_travel_time = round(distance / avg_speed, 2)  # in hours
        stop_time = round(np.random.uniform(0.1, 0.5) * np.random.randint(0, 5), 2)  # random stop time in hours
        traffic_delay = round(np.random.uniform(0.05, 0.3) * np.random.choice([0, 1, 2]), 2)  # random traffic delay in hours
        travel_time = round(base_travel_time + stop_time + traffic_delay, 2)

        row = {
            "point_a": point_a,
            "point_b": point_b,
            "distance": distance,
            "avg_speed": avg_speed,
            "max_speed": max_speed,
            "min_speed": min_speed,
            "road_condition": np.random.choice([0, 1, 2, 3]),
            "date": random_dates(pd.to_datetime('2023-01-01'), pd.to_datetime('2023-12-31'))[0],
            "departure_time": (datetime(2023, 1, 1) + timedelta(minutes=random.randint(0, 1440))).strftime('%H:%M'),
            "number_stops": np.random.randint(0, 5),
            "vehicle_type": np.random.choice([0, 1, 2]),
            "vehicle_weight": round(np.random.uniform(2200, 88000), 2),
            "driver_age": np.random.randint(18, 70),
            "fuel_capacity": round(np.random.uniform(10, 105), 2),
            "traffic_condition": np.random.choice([0, 1, 2]),
            "travel_time": travel_time  # Adding travel time
        }

        data.append(row)

    df = pd.DataFrame(data)

    file_path = 'vehicle_eta_validation_data.csv'
    df.to_csv(file_path, index=False)

    return file_path

num_rows = 20000
generate_vehicle_eta_data(num_rows)
