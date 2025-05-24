import pandas as pd
import numpy as np


def rename_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(' ', '_')
        .str.replace(r'[^\w_]', '', regex=True)
    )
    return df


def convert_to_numeric(df):
    df['price_per_unit'] = pd.to_numeric(df['price_per_unit'], errors='coerce')
    df['total_price'] = pd.to_numeric(df['total_price'], errors='coerce')
    df['phone'] = df['phone'].astype(str).str.replace(r'\D', '', regex=True)

    return df


def convert_to_category(df):
    df['category'] = df['category'].astype('category')

    return df



def convert_to_datetime(df):
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    return df



def parse_price(text):
    if pd.isna(text) or str(text).strip().lower() == 'price not available':
        return np.nan
    
    try:
        price_str = str(text).replace('USD', '').strip()
        return float(price_str)
    except ValueError:
        return np.nan
    

def extract_numerical_values(df):
    df['price_per_unit'] = df['price_per_unit'].apply(parse_price)
    return df

def calculating_total_price(df):
    df['total_price'] = df['price_per_unit'] * df['quantity']
    return df

def deduplicate_data(df):
    df.drop_duplicates(inplace=True, keep='first', ignore_index=False)
    return df


def prepared_data(df):
    return df.pipe(rename_columns).pipe(extract_numerical_values).pipe(convert_to_numeric).pipe(calculating_total_price).pipe(convert_to_category).pipe(convert_to_datetime).pipe(deduplicate_data)
