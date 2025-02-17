from datetime import datetime
from typing import Optional

from geopy.distance import geodesic

def calculate_speed(lat1: float, lon1: float, 
                   lat2: float, lon2: float,
                   time1: datetime, time2: datetime) -> float:
    """
    Calculate speed between two points in km/h
    """
    if not all([lat1, lon1, lat2, lon2, time1, time2]):
        return 0.0
        
    # Calculate distance in kilometers
    distance = geodesic(
        (lat1, lon1),
        (lat2, lon2)
    ).kilometers
    
    # Calculate time difference in hours
    time_diff = (time2 - time1).total_seconds() / 3600
    
    # Avoid division by zero
    if time_diff == 0:
        return 0.0
        
    return distance / time_diff

def format_speed(speed: float) -> str:
    """
    Format speed value with units
    """
    return f"{speed:.1f} km/h"
