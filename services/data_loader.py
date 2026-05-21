import pandas as pd
from services.validations import validar_columnas

FILE_PATH = "data/COMPUTADORES NEW.xlsx"

def load_data():
    try:

        # ✅ LEER EXCEL FORZANDO ANYDESK COMO TEXTO
        df = pd.read_excel(
            FILE_PATH,
            dtype={"ANYDESK": str}
        )

        # ✅ Limpiar nombres columnas
        df.columns = df.columns.str.strip()

        # ✅ Limpiar ANYDESK
        if "ANYDESK" in df.columns:

            df["ANYDESK"] = (
                df["ANYDESK"]
                .fillna("")
                .astype(str)
                .str.replace(".0", "", regex=False)
                .str.strip()
            )

        validar_columnas(df)

        return df

    except FileNotFoundError:
        return pd.DataFrame()

def save_data(df):

    # ✅ EVITAR QUE ANYDESK SE GUARDE COMO FLOAT
    if "ANYDESK" in df.columns:

        df["ANYDESK"] = (
            df["ANYDESK"]
            .fillna("")
            .astype(str)
            .str.replace(".0", "", regex=False)
            .str.strip()
        )

    df.to_excel(FILE_PATH, index=False)
