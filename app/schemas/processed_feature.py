from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProcessedFeature(BaseModel):
    id: Optional[int] = None
    timestamp: Optional[datetime] = None

    # Vehicle
    vehicle_model: float
    battery_capacity_kwh: float
    vehicle_age_years: float

    # Charging Station
    charging_station_id: float
    charging_station_location: float

    # Charging Session
    charging_start_time: str
    charging_end_time: str
    charging_duration_h: float
    charging_rate_kw: float
    energy_consumed_kwh: float
    charging_cost_usd: float 

    # Date and Time
    time_of_day: int
    day_of_week: int

    # Distance and Temperature
    distance_driven_since_last_charge_km: float
    temperature_c: float

    # Charging State
    state_of_charge_start: float
    state_of_charge_end: float

    # One-Hot Encoded Categories
    charger_type_Level_1: int
    charger_type_Level_2: int
    user_type_Commuter: int
    user_type_Long_Distance_Traveler: int