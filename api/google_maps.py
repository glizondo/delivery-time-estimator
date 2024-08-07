import googlemaps
import credentials.user_credentials
import numpy as np

API_KEY = credentials.user_credentials.google_api_creds
gmaps = googlemaps.Client(key=API_KEY)


def map_conditions(value, thresholds, conditions):
    """
    Map a continuous value to a discrete condition based on thresholds.

    Parameters:
    - value: The real value to be mapped.
    - thresholds: List of thresholds to define conditions.
    - conditions: List of integer conditions corresponding to each threshold.

    Returns:
    - Integer condition based on the value and thresholds.
    """
    for threshold, condition in zip(thresholds, conditions):
        if value <= threshold:
            return condition
    return conditions[-1]


def get_conditions(point_a, point_b, departure_time):
    try:
        directions_result = gmaps.directions(point_a, point_b, departure_time=departure_time)
        if directions_result:
            leg = directions_result[0]['legs'][0]
            distance = leg['distance']['value'] / 1000  # Convert meters to kilometers
            duration = leg['duration']['value'] / 60  # Convert seconds to minutes
            traffic_duration = leg.get('duration_in_traffic', {}).get('value',
                                                                      duration) / 60  # Convert seconds to minutes

            # Define thresholds and conditions for road and traffic conditions
            road_condition_thresholds = [10, 50, 100]  # Example thresholds for distance
            road_condition_values = [0, 1, 2, 3]  # Example conditions for road quality

            traffic_condition_thresholds = [10, 20]  # Example thresholds for traffic delay
            traffic_condition_values = [0, 1, 2]  # Example conditions for traffic intensity

            # Map real values to integer conditions
            road_condition = map_conditions(distance, road_condition_thresholds, road_condition_values)
            traffic_condition = map_conditions(traffic_duration, traffic_condition_thresholds, traffic_condition_values)

            return distance, road_condition, traffic_condition, duration
        else:
            return None, None, None, None
    except Exception as e:
        print(f"Error getting conditions from API: {e}")
        return None, None, None, None
