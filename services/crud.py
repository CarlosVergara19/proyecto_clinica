import pandas as pd
from datetime import datetime
from services.validations import (validar_campos_obligatorios)


def generar_nuevo_id(df):
    """
    Genera un ID incremental automático.
    """
    if df.empty:
        return 1

    return int(df["id"].max()) + 1


def create_equipo(df, datos):
    """
    Agrega un nuevo equipo al inventario con validaciones completas.
    """

    # ===============================
    # VALIDACIONES
    # ===============================

    validar_campos_obligatorios(datos)

    # ===============================
    # GENERAR ID
    # ===============================

    nuevo_id = generar_nuevo_id(df)

    # ===============================
    # CREAR REGISTRO
    # ===============================

    nuevo_equipo = {
        "id": nuevo_id,
        "nombre": datos["nombre"].strip(),
        "marca": datos["marca"].strip(),
        "modelo": datos["modelo"].strip(),
        "procesador": datos.get("procesador", "").strip(),
        "ram": datos.get("ram", "").upper().strip(),
        "disco": datos.get("disco", "").strip(),
        "ubicacion": datos["ubicacion"].strip(),
        "estado": datos["estado"],
        "fecha_ingreso": datetime.now().date(),
        "fecha_baja": None,
        "responsable": datos.get("responsable", "").strip(),
        "serial": datos.get("serial", "").strip()
    }

    # ===============================
    # AGREGAR AL DATAFRAME
    # ===============================

    df = pd.concat([df, pd.DataFrame([nuevo_equipo])], ignore_index=True)

    return df

def update_equipo(df, id_equipo, datos_actualizados):

    if id_equipo not in df["ID"].values:
        raise ValueError("El equipo no existe.")

    for campo, valor in datos_actualizados.items():
        df.loc[df["ID"] == id_equipo, campo] = valor

    return df

def delete_equipo(df, id_equipo):
    if id_equipo not in df["ID"].values:
        raise ValueError("El equipo no existe.")

    df = df[df["ID"] != id_equipo]

    return df