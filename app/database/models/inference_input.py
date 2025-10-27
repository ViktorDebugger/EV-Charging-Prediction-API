from sqlalchemy import Column, Integer, Float, String, DateTime
from app.database.models import Base

class StartTable(Base):
    __tablename__ = 'Inference-Inputs'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=True)
    
    # User
    user_id = Column(String, nullable=True)
    
    # Vehicle
    vehicle_model = Column(String, nullable=True)
    battery_capacity_kwh = Column(Float, nullable=True)
    vehicle_age_years = Column(Float, nullable=True)
    
    # Charging Station
    charging_station_id = Column(String, nullable=True)
    charging_station_location = Column(String, nullable=True)
    
    # Charging Session
    charging_start_time = Column(String, nullable=True)
    charging_end_time = Column(String, nullable=True)
    energy_consumed_kwh = Column(Float, nullable=True)
    charging_duration_h = Column(Float, nullable=True)
    charging_rate_kw = Column(Float, nullable=True)
    charging_cost_usd = Column(Float, nullable=True)
    
    # Date and Time
    time_of_day = Column(String, nullable=True)
    day_of_week = Column(String, nullable=True)
    
    # Charging State
    state_of_charge_start = Column(Float, nullable=True)
    state_of_charge_end = Column(Float, nullable=True)
    
    # Distance and Temperature
    distance_driven_since_last_charge_km = Column(Float, nullable=True)
    temperature_c = Column(Float, nullable=True)
    
    # Categories
    user_type = Column(String, nullable=True)