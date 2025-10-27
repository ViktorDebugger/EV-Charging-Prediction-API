from typing import Dict, Any, Tuple, List
from app.database.models.processed_feature import ProcessedFeature as ProcessedFeatureModel
from app.schemas.processed_feature import ProcessedFeature
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def sqlalchemy_to_pydantic(feature_model: ProcessedFeatureModel) -> ProcessedFeature:
    feature_dict = {
        'id': feature_model.id,
        'timestamp': feature_model.timestamp,
        'vehicle_model': feature_model.vehicle_model,
        'battery_capacity_kwh': feature_model.battery_capacity_kwh,
        'vehicle_age_years': feature_model.vehicle_age_years,
        'charging_station_id': feature_model.charging_station_id,
        'charging_station_location': feature_model.charging_station_location,
        'charging_start_time': feature_model.charging_start_time,
        'charging_end_time': feature_model.charging_end_time,
        'charging_duration_h': feature_model.charging_duration_h,
        'charging_rate_kw': feature_model.charging_rate_kw,
        'energy_consumed_kwh': feature_model.energy_consumed_kwh,
        'time_of_day': feature_model.time_of_day,
        'charging_cost_usd': feature_model.charging_cost_usd,
        'day_of_week': feature_model.day_of_week,
        'distance_driven_since_last_charge_km': feature_model.distance_driven_since_last_charge_km,
        'temperature_c': feature_model.temperature_c,
        'state_of_charge_start': feature_model.state_of_charge_start,
        'state_of_charge_end': feature_model.state_of_charge_end,
        'charger_type_Level_1': feature_model.charger_type_Level_1,
        'charger_type_Level_2': feature_model.charger_type_Level_2,
        'user_type_Commuter': feature_model.user_type_Commuter,
        'user_type_Long_Distance_Traveler': feature_model.user_type_Long_Distance_Traveler
    }
    
    return ProcessedFeature(**feature_dict)

def pydantic_to_sqlalchemy(feature: ProcessedFeature) -> ProcessedFeatureModel:
    return ProcessedFeatureModel(
        id=feature.id,
        timestamp=feature.timestamp,
        vehicle_model=feature.vehicle_model,
        battery_capacity_kwh=feature.battery_capacity_kwh,
        vehicle_age_years=feature.vehicle_age_years,
        charging_station_id=feature.charging_station_id,
        charging_station_location=feature.charging_station_location,
        charging_start_time=feature.charging_start_time,
        charging_end_time=feature.charging_end_time,
        charging_duration_h=feature.charging_duration_h,
        charging_rate_kw=feature.charging_rate_kw,
        energy_consumed_kwh=feature.energy_consumed_kwh,
        time_of_day=feature.time_of_day,
        charging_cost_usd=feature.charging_cost_usd,
        day_of_week=feature.day_of_week,
        distance_driven_since_last_charge_km=feature.distance_driven_since_last_charge_km,
        temperature_c=feature.temperature_c,
        state_of_charge_start=feature.state_of_charge_start,
        state_of_charge_end=feature.state_of_charge_end,
        charger_type_Level_1=feature.charger_type_Level_1,
        charger_type_Level_2=feature.charger_type_Level_2,
        user_type_Commuter=feature.user_type_Commuter,
        user_type_Long_Distance_Traveler=feature.user_type_Long_Distance_Traveler
    )

def pydantic_to_sqlalchemy_dict(feature: ProcessedFeature) -> Dict[str, Any]:
    return feature.model_dump()

def get_model_fields() -> list:
    return [
        'id', 'timestamp', 'vehicle_model', 'battery_capacity_kwh', 'vehicle_age_years',
        'charging_station_id', 'charging_station_location', 'charging_start_time',
        'charging_end_time', 'charging_duration_h', 'charging_rate_kw', 'energy_consumed_kwh',
        'time_of_day', 'day_of_week', 'charging_cost_usd', 'distance_driven_since_last_charge_km',
        'temperature_c', 'state_of_charge_start', 'state_of_charge_end',
        'charger_type_Level_1', 'charger_type_Level_2', 'user_type_Commuter',
        'user_type_Long_Distance_Traveler'
    ]

def prepare_dataframe(features: List[ProcessedFeature]) -> pd.DataFrame:
    data = []
    for feature in features:
        data.append({
            'id': feature.id,
            'timestamp': feature.timestamp,
            'vehicle_model': feature.vehicle_model,
            'battery_capacity_kwh': feature.battery_capacity_kwh,
            'vehicle_age_years': feature.vehicle_age_years,
            'charging_station_id': feature.charging_station_id,
            'charging_station_location': feature.charging_station_location,
            'charging_start_time': feature.charging_start_time,
            'charging_end_time': feature.charging_end_time,
            'charging_duration_h': feature.charging_duration_h,
            'charging_rate_kw': feature.charging_rate_kw,
            'energy_consumed_kwh': feature.energy_consumed_kwh,
            'time_of_day': feature.time_of_day,
            'charging_cost_usd': feature.charging_cost_usd,
            'day_of_week': feature.day_of_week,
            'distance_driven_since_last_charge_km': feature.distance_driven_since_last_charge_km,
            'temperature_c': feature.temperature_c,
            'state_of_charge_start': feature.state_of_charge_start,
            'state_of_charge_end': feature.state_of_charge_end,
            'charger_type_Level_1': feature.charger_type_Level_1,
            'charger_type_Level_2': feature.charger_type_Level_2,
            'user_type_Commuter': feature.user_type_Commuter,
            'user_type_Long_Distance_Traveler': feature.user_type_Long_Distance_Traveler
        })
    
    return pd.DataFrame(data)



def prepare_data(df):
    conditions = [
        df['charger_type_Level_1'] == True,
        df['charger_type_Level_2'] == True
    ]
    choices = ['Level_1', 'Level_2']
    df['ChargerType_Target'] = np.select(conditions, choices, default='DC Fast Charger')
    
    y_column = 'ChargerType_Target'

    columns_to_drop = [
        'id',
        'timestamp', 
        'charging_station_id',
        'charging_start_time',
        'charging_end_time',
        'vehicle_model',
        'charging_station_location',
        'time_of_day',
        'day_of_week',
        'charger_type_Level_1',
        'charger_type_Level_2',
        'ChargerType_Target'
    ]

    existing_columns_to_drop = [col for col in columns_to_drop if col in df.columns]
    x_columns = df.columns.drop(existing_columns_to_drop)
    
    X = df[x_columns]
    y = df[y_column]

    return X, y

def split_data(X: pd.DataFrame, y: pd.Series, train_ratio: float = 0.9, random_state: int = 42) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        train_size=train_ratio, 
        random_state=random_state,
        shuffle=True,
        stratify=y
    )

    return X_train, y_train, X_test, y_test