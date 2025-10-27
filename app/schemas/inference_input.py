from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class InferenceInput(BaseModel):
    id: Optional[int] = None
    timestamp: Optional[datetime] = None
    
    # User
    user_id: Optional[str] = None

    # Vehicle
    vehicle_model: Optional[str] = None
    battery_capacity_kwh: Optional[float] = None
    vehicle_age_years: Optional[float] = None

    # Charging Station
    charging_station_id: Optional[str] = None
    charging_station_location: Optional[str] = None
    
    # Charging Session
    charging_start_time: Optional[str] = None
    charging_end_time: Optional[str] = None
    energy_consumed_kwh: Optional[float] = None
    charging_duration_h: Optional[float] = None
    charging_rate_kw: Optional[float] = None
    charging_cost_usd: Optional[float] = None
    
    # Date and Time
    time_of_day: Optional[str] = None
    day_of_week: Optional[str] = None
    
    # Charging State
    state_of_charge_start: Optional[float] = None
    state_of_charge_end: Optional[float] = None
    
    # Distance and Temperature
    distance_driven_since_last_charge_km: Optional[float] = None
    temperature_c: Optional[float] = None
    
    # Categories
    user_type: Optional[str] = None