import pandas as pd
from supabase import create_client
import streamlit as st

def get_supabase():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

def load_historial():
    supabase = get_supabase()
    response = supabase.table("historial").select("*").execute()
    df = pd.DataFrame(response.data)

    if df.empty:
        return pd.DataFrame(columns=[
            "ID_REGISTRO", "ID_EQUIPO", "FECHA", "TIPO", "DESCRIPCION", "TECNICO"
        ])

    df = df.rename(columns={
        "id_registro": "ID_REGISTRO",
        "id_equipo":   "ID_EQUIPO",
        "fecha":       "FECHA",
        "tipo":        "TIPO",
        "descripcion": "DESCRIPCION",
        "tecnico":     "TECNICO",
    })

    return df

def save_historial(df):
    # Ya no se usa — las operaciones van directo a Supabase
    pass

def agregar_historial(df, datos):
    supabase = get_supabase()

    nuevo = {
        "id_equipo":   datos["ID_EQUIPO"],
        "fecha":       str(datos["FECHA"]),
        "tipo":        datos["TIPO"],
        "descripcion": datos["DESCRIPCION"],
        "tecnico":     datos["TECNICO"],
    }

    supabase.table("historial").insert(nuevo).execute()

    # Recargar historial actualizado
    return load_historial()

def update_historial(df, id_registro, datos):
    supabase = get_supabase()

    datos_supabase = {
        "fecha":       str(datos["FECHA"]),
        "tipo":        datos["TIPO"],
        "descripcion": datos["DESCRIPCION"],
        "tecnico":     datos["TECNICO"],
    }

    supabase.table("historial").update(datos_supabase).eq("id_registro", id_registro).execute()

    return load_historial()

def delete_historial(df, id_registro):
    supabase = get_supabase()
    supabase.table("historial").delete().eq("id_registro", id_registro).execute()
    return load_historial()