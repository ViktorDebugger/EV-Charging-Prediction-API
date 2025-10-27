from sqlalchemy import Column, Integer, Float, String, DateTime
from app.database.models import Base

class ProcessedFeature(Base):
    __tablename__ = 'Processed-Features'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=True)

    # Vehicle
    vehicle_model = Column(Float)
    battery_capacity_kwh = Column(Float)
    vehicle_age_years = Column(Float)
    
    # Charging Station
    charging_station_id = Column(Float)
    charging_station_location = Column(Float)
    
    # Charging Session
    charging_start_time = Column(String)
    charging_end_time = Column(String)
    charging_duration_h = Column(Float)
    charging_rate_kw = Column(Float)
    energy_consumed_kwh = Column(Float)
    charging_cost_usd = Column(Float)

    # Date and Time
    time_of_day = Column(Integer)
    day_of_week = Column(Integer)
    
    # Distance and Temperature
    distance_driven_since_last_charge_km = Column(Float)
    temperature_c = Column(Float)
    
    # Charging State
    state_of_charge_start = Column(Float)
    state_of_charge_end = Column(Float)
    
    # One-Hot Encoded Categories
    charger_type_Level_1 = Column(Integer)
    charger_type_Level_2 = Column(Integer)
    user_type_Commuter = Column(Integer)
    user_type_Long_Distance_Traveler = Column(Integer)