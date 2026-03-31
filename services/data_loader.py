import pandas as pd
from services.validations import validar_columnas

FILE_PATH = "data/COMPUTADORES NEW.xlsx"

def load_data():
    try:
        df = pd.read_excel(FILE_PATH)

        # Limpiar nombres
        df.columns = df.columns.str.strip()

        validar_columnas(df)

        return df

    except FileNotFoundError:
        return pd.DataFrame()

def save_data(df):
    df.to_excel(FILE_PATH, index=False)