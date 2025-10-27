from typing import Dict, Any, List
from app.database.models.inference_input import StartTable as InferenceInputModel
from app.schemas.inference_input import InferenceInput
from random import randint
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def sqlalchemy_to_pydantic(inference_model: InferenceInputModel) -> InferenceInput:
    inference_dict = {
        'id': inference_model.id,
        'timestamp': inference_model.timestamp, 
        'user_id': inference_model.user_id,
        'vehicle_model': inference_model.vehicle_model,
        'battery_capacity_kwh': inference_model.battery_capacity_kwh,
        'vehicle_age_years': inference_model.vehicle_age_years,
        'charging_station_id': inference_model.charging_station_id,
        'charging_station_location': inference_model.charging_station_location,
        'charging_start_time': inference_model.charging_start_time,
        'charging_end_time': inference_model.charging_end_time,
        'energy_consumed_kwh': inference_model.energy_consumed_kwh,
        'charging_duration_h': inference_model.charging_duration_h,
        'charging_rate_kw': inference_model.charging_rate_kw,
        'charging_cost_usd': inference_model.charging_cost_usd,
        'time_of_day': inference_model.time_of_day,
        'day_of_week': inference_model.day_of_week,
        'state_of_charge_start': inference_model.state_of_charge_start,
        'state_of_charge_end': inference_model.state_of_charge_end,
        'distance_driven_since_last_charge_km': inference_model.distance_driven_since_last_charge_km,
        'temperature_c': inference_model.temperature_c,
        'user_type': inference_model.user_type
    }
    
    return InferenceInput(**inference_dict)

def pydantic_to_sqlalchemy(inference_input: InferenceInput) -> InferenceInputModel:
    return InferenceInputModel(
        timestamp=inference_input.timestamp,
        user_id=inference_input.user_id,
        vehicle_model=inference_input.vehicle_model,
        battery_capacity_kwh=inference_input.battery_capacity_kwh,
        vehicle_age_years=inference_input.vehicle_age_years,
        charging_station_id=inference_input.charging_station_id,
        charging_station_location=inference_input.charging_station_location,
        charging_start_time=inference_input.charging_start_time,
        charging_end_time=inference_input.charging_end_time,
        energy_consumed_kwh=inference_input.energy_consumed_kwh,
        charging_duration_h=inference_input.charging_duration_h,
        charging_rate_kw=inference_input.charging_rate_kw,
        charging_cost_usd=inference_input.charging_cost_usd,
        time_of_day=inference_input.time_of_day,
        day_of_week=inference_input.day_of_week,
        state_of_charge_start=inference_input.state_of_charge_start,
        state_of_charge_end=inference_input.state_of_charge_end,
        distance_driven_since_last_charge_km=inference_input.distance_driven_since_last_charge_km,
        temperature_c=inference_input.temperature_c,
        user_type=inference_input.user_type
    )

def pydantic_to_sqlalchemy_dict(inference_input: InferenceInput) -> Dict[str, Any]:
    return inference_input.model_dump()

def generate_random_datetime():
    random_day = randint(0, 364)
    random_hour = randint(0, 23)
    random_minute = randint(0, 59)
    random_second = randint(0, 59)
            
    return datetime(2025, 1, 1, random_hour, random_minute, random_second) + timedelta(days=random_day)

def inference_input_to_dataframe(input_data: InferenceInput):
    data_dict = {
        'id': input_data.id,
        'timestamp': input_data.timestamp,
        'user_id': input_data.user_id,
        'vehicle_model': input_data.vehicle_model,
        'battery_capacity_kwh': input_data.battery_capacity_kwh,
        'vehicle_age_years': input_data.vehicle_age_years,
        'charging_station_id': input_data.charging_station_id,
        'charging_station_location': input_data.charging_station_location,
        'charging_start_time': input_data.charging_start_time,
        'charging_end_time': input_data.charging_end_time,
        'energy_consumed_kwh': input_data.energy_consumed_kwh,
        'charging_duration_h': input_data.charging_duration_h,
        'charging_rate_kw': input_data.charging_rate_kw,
        'charging_cost_usd': input_data.charging_cost_usd,
        'time_of_day': input_data.time_of_day,
        'day_of_week': input_data.day_of_week,
        'state_of_charge_start': input_data.state_of_charge_start,
        'state_of_charge_end': input_data.state_of_charge_end,
        'distance_driven_since_last_charge_km': input_data.distance_driven_since_last_charge_km,
        'temperature_c': input_data.temperature_c,
        'user_type': input_data.user_type
    }

    return pd.DataFrame([data_dict])

def validate_input_data(input_data: InferenceInput) -> List[str]:
    required_fields = [
        'user_id',
        'vehicle_model',
        'battery_capacity_kwh',
        'vehicle_age_years',
        'charging_station_id',
        'charging_station_location',
        'charging_start_time',
        'charging_end_time',
        'energy_consumed_kwh',
        'charging_duration_h',
        'charging_rate_kw',
        'charging_cost_usd',
        'time_of_day',
        'day_of_week',
        'state_of_charge_start',
        'state_of_charge_end',
        'distance_driven_since_last_charge_km',
        'temperature_c',
        'user_type'
    ]

    missing_fields = []
    
    for field in required_fields:
        field_value = getattr(input_data, field)
        if field_value is None or (isinstance(field_value, str) and field_value.strip() == ""):
            missing_fields.append(field)
    
    return missing_fields

def validate_categorical_fields(input_data: InferenceInput) -> Dict[str, List[str]]:
    VALID_CATEGORIES = {
        'vehicle_model': [
            'Tesla Model 3',
            'Hyundai Kona',
            'Nissan Leaf',
            'BMW i3',
            'Chevy Bolt'
        ],
        'charging_station_location': [
            'Los Angeles',
            'San Francisco',
            'Houston',
            'New York',
            'Chicago'
        ],
        'time_of_day': [
            'Morning',
            'Afternoon',
            'Evening',
            'Night'
        ],
        'day_of_week': [
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday'
        ],
        'charger_type': [
            'Level 1',
            'Level 2',
            'DC Fast Charger'
        ],
        'user_type': [
            'Commuter',
            'Long-Distance Traveler',
            'Casual Driver'
        ]
    }
    
    invalid_fields = []
    errors = []
    
    for field_name, valid_values in VALID_CATEGORIES.items():
        field_value = getattr(input_data, field_name, None)
        
        if field_value is None or field_value == "":
            continue
        
        if field_value not in valid_values:
            invalid_fields.append(field_name)
            errors.append(
                f"'{field_name}' has an invalid value '{field_value}'. "
                f"Valid values: {', '.join(valid_values)}"
            )
    
    return {
        'invalid_fields': invalid_fields,
        'errors': errors
    }

def fix_battery_capacity_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    min_capacity_map = {
        'BMW i3': 22.0,
        'Hyundai Kona': 48.4,
        'Chevy Bolt': 60.0,
        'Nissan Leaf': 24.0,
        'Tesla Model 3': 54.0
    }

    max_capacity_map = {
        'BMW i3': 42.2,
        'Hyundai Kona': 64.0,
        'Chevy Bolt': 66.0,
        'Nissan Leaf': 62.0,
        'Tesla Model 3': 82.0
    }

    vehicle_model = df['vehicle_model'].iloc[0]

    if vehicle_model in min_capacity_map:
        min_capacity = min_capacity_map[vehicle_model]
        max_capacity = max_capacity_map[vehicle_model]
        
        df['battery_capacity_kwh'].iloc[0]
        df['battery_capacity_kwh'] = df['battery_capacity_kwh'].clip(
            lower=min_capacity,
            upper=max_capacity
        )
    
    return df

def fix_charging_duration_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    start_time = pd.to_datetime(df['charging_start_time'].iloc[0])
    end_time = pd.to_datetime(df['charging_end_time'].iloc[0])
    
    duration_hours = (end_time - start_time).total_seconds() / 3600
    
    df['charging_duration_h'] = duration_hours
    
    return df

def fix_charging_rate_anomalies(df: pd.DataFrame, trained_df: pd.DataFrame = None) -> pd.DataFrame:
    if trained_df is not None:
        median_value = trained_df['charging_rate_kw'].median()
    else:
        median_value = 25.603799331857445
    
    df['charging_rate_kw'] = df['charging_rate_kw'].fillna(median_value)
    
    return df

def fix_energy_consumed_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    charging_rate = df['charging_rate_kw'].iloc[0]
    charging_duration = df['charging_duration_h'].iloc[0]
    
    energy_consumed = charging_rate * charging_duration
    
    df['energy_consumed_kwh'] = energy_consumed
    
    return df

def fix_time_features_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    start_datetime = pd.to_datetime(df['charging_start_time'].iloc[0])
    
    def get_time_of_day(hour):
        if 6 <= hour < 12:
            return 'Morning'
        elif 12 <= hour < 18:
            return 'Afternoon'
        elif 18 <= hour < 22:
            return 'Evening'
        else:
            return 'Night'
    
    df['time_of_day'] = get_time_of_day(start_datetime.hour)
    
    df['day_of_week'] = start_datetime.day_name()
    
    return df


def fix_distance_driven_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    df['distance_driven_since_last_charge_km'] = df['distance_driven_since_last_charge_km'].fillna(0)
    
    return df

def fix_temperature_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    df['temperature_c'] = df['temperature_c'].clip(upper=50)
    
    return df

def fix_state_of_charge_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    df['state_of_charge_start'] = df['state_of_charge_start'].clip(0, 100)
    df['state_of_charge_end'] = df['state_of_charge_end'].clip(0, 100)
    
    return df

def recalculate_state_of_charge_end(df: pd.DataFrame) -> pd.DataFrame:
    start_charge_kwh = (df['state_of_charge_start'].iloc[0] / 100) * df['battery_capacity_kwh'].iloc[0]
    
    calculated_end_charge_kwh = start_charge_kwh + df['energy_consumed_kwh'].iloc[0]
    
    end_charge_percentage = np.minimum(
        1,
        calculated_end_charge_kwh / df['battery_capacity_kwh'].iloc[0]
    ) * 100
    
    df['state_of_charge_end'] = end_charge_percentage
    
    return df

def encode_day_of_week(df: pd.DataFrame) -> pd.DataFrame:
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    encoded_day_weeks = pd.Categorical(
        df['day_of_week'], 
        categories=days_order, 
        ordered=True
    ).codes
    
    df['day_of_week'] = encoded_day_weeks
    
    return df

def encode_time_of_day(df: pd.DataFrame) -> pd.DataFrame:
    time_order = ['Morning', 'Afternoon', 'Evening', 'Night']
    
    encoded_time_of_day = pd.Categorical(
        df['time_of_day'], 
        categories=time_order, 
        ordered=True
    ).codes
    
    df['time_of_day'] = encoded_time_of_day
    
    return df

def encode_vehicle_model(df: pd.DataFrame, trained_df: pd.DataFrame = None) -> pd.DataFrame:
    if trained_df is not None:
        vehicle_freq_map = trained_df['vehicle_model'].value_counts(normalize=True).to_dict()
    else:
        vehicle_freq_map = {
            'Tesla Model 3': 0.2121,
            'Hyundai Kona': 0.2015,
            'Nissan Leaf': 0.1970,
            'BMW i3': 0.1955,
            'Chevy Bolt': 0.1939
        }
    
    df['vehicle_model'] = df['vehicle_model'].map(vehicle_freq_map)
    
    return df

def encode_charging_station_location(df: pd.DataFrame, trained_df: pd.DataFrame = None) -> pd.DataFrame:
    if trained_df is not None:
        location_freq_map = trained_df['charging_station_location'].value_counts(normalize=True).to_dict()
    else:
        location_freq_map = {
            'Los Angeles': 0.225,
            'San Francisco': 0.200,
            'Houston': 0.198,
            'New York': 0.193,
            'Chicago': 0.183
        }
    
    df['charging_station_location'] = df['charging_station_location'].map(location_freq_map)
    
    return df

def one_hot_encode_user_type(df: pd.DataFrame) -> pd.DataFrame:    
    df['user_type_Commuter'] = (df['user_type'] == 'Commuter').astype(int)
    df['user_type_Long_Distance_Traveler'] = (df['user_type'] == 'Long-Distance Traveler').astype(int)
    
    df = df.drop(columns=['user_type'])
    
    return df

def encode_charging_station_id(df: pd.DataFrame, trained_df: pd.DataFrame = None) -> pd.DataFrame:
    if trained_df is not None:
        station_mean_cost = trained_df.groupby('charging_station_id')['charging_cost_usd'].mean()
        overall_mean = trained_df['charging_cost_usd'].mean()
        df['charging_station_id'] = df['charging_station_id'].map(station_mean_cost).fillna(overall_mean)
    else:
        overall_mean_cost = 11.5
        df['charging_station_id'] = overall_mean_cost
    
    return df

def scale_charging_station_location(df: pd.DataFrame, trained_df: pd.DataFrame = None) -> pd.DataFrame:
    if trained_df is not None:
        location_freq_map = trained_df['charging_station_location'].value_counts(normalize=True).to_dict()
        encoded_values = trained_df['charging_station_location'].map(location_freq_map)
        min_value = encoded_values.min()
        max_value = encoded_values.max()
    else:
        min_value = 0.183
        max_value = 0.225
    
    df['charging_station_location'] = (df['charging_station_location'] - min_value) / (max_value - min_value)
    
    return df

def scale_energy_consumed(df: pd.DataFrame, trained_df: pd.DataFrame = None) -> pd.DataFrame:
    if trained_df is not None:
        mean_value = trained_df['energy_consumed_kwh'].mean()
        std_value = trained_df['energy_consumed_kwh'].std()
    else:
        mean_value = 45.5
        std_value = 15.2
    
    df['energy_consumed_kwh'] = (df['energy_consumed_kwh'] - mean_value) / std_value
    
    return df

def select_model_features(df: pd.DataFrame) -> pd.DataFrame:
    model_columns = [
        'vehicle_model',
        'battery_capacity_kwh',
        'charging_station_id',
        'charging_station_location',
        'charging_start_time',
        'charging_end_time',
        'charging_duration_h',
        'charging_rate_kw',
        'energy_consumed_kwh',
        'time_of_day',
        'day_of_week',
        'charging_cost_usd',
        'vehicle_age_years',
        'distance_driven_since_last_charge_km',
        'temperature_c',
        'state_of_charge_start',
        'state_of_charge_end',
        'user_type_Commuter',
        'user_type_Long_Distance_Traveler'
    ]
    
    return df[model_columns]

def prepare_input_for_prediction(input_data: InferenceInput, trained_df: pd.DataFrame) -> pd.DataFrame:
    # Conver InferenceInput to DataFrame
    df = inference_input_to_dataframe(input_data)
    
    # Fix anomalies end empty data
    df = fix_battery_capacity_anomalies(df)
    df = fix_charging_duration_anomalies(df)
    df = fix_charging_rate_anomalies(df, trained_df)
    df = fix_energy_consumed_anomalies(df)
    df = fix_time_features_anomalies(df)
    df = fix_distance_driven_anomalies(df)
    df = fix_temperature_anomalies(df)
    df = fix_state_of_charge_anomalies(df)
    df = recalculate_state_of_charge_end(df)

    # Encoding Categories
    df = encode_day_of_week(df)
    df = encode_time_of_day(df)
    df = encode_vehicle_model(df, trained_df)
    df = encode_charging_station_location(df, trained_df)
    df = one_hot_encode_user_type(df)
    df = encode_charging_station_id(df, trained_df)

    # Scaling
    df = scale_charging_station_location(df, trained_df)
    df = scale_energy_consumed(df, trained_df)

    # Select mode features
    df = select_model_features(df) 

    return df
