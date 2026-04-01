import pandas as pd
from datetime import datetime

FILE_PATH = "data/historial_equipos.xlsx"


def load_historial():
    try:
        df = pd.read_excel(FILE_PATH)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame(columns=[
            "ID_REGISTRO", "ID_EQUIPO", "FECHA", "TIPO", "DESCRIPCION", "TECNICO"
        ])


def save_historial(df):
    df.to_excel(FILE_PATH, index=False)


def generar_id(df):
    if df.empty:
        return 1
    return int(df["ID_REGISTRO"].max()) + 1


def agregar_historial(df, datos):
    nuevo = {
        "ID_REGISTRO": generar_id(df),
        "ID_EQUIPO": datos["ID_EQUIPO"],
        "FECHA": datos["FECHA"],
        "TIPO": datos["TIPO"],
        "DESCRIPCION": datos["DESCRIPCION"],
        "TECNICO": datos["TECNICO"]
    }

    df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
    return df


def update_historial(df, id_registro, datos):
    for campo, valor in datos.items():
        df.loc[df["ID_REGISTRO"] == id_registro, campo] = valor
    return df


def delete_historial(df, id_registro):
    df = df[df["ID_REGISTRO"] != id_registro]
    return df