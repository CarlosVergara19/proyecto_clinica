import pandas as pd
from supabase import create_client
import streamlit as st

# ── Conexión ──────────────────────────────────────────
@st.cache_resource
def get_supabase():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

# ── Cargar equipos ────────────────────────────────────
def load_data():
    supabase = get_supabase()
    response = supabase.table("equipos").select("*").execute()
    df = pd.DataFrame(response.data)

    if df.empty:
        return df

    # Renombrar columnas Supabase → nombres que usa app.py
    df = df.rename(columns={
        "id":               "ID",
        "ubicacion":        "UBICACION",
        "unidad_funcional": "UNIDA FUNCIONAL",
        "usuario_cargo":    "USUARIO O CARGO",
        "procesador":       "PROCESADOR",
        "espacio":          "ESPACIO",
        "memoria_ram":      "MEMORIA RAM",
        "monitor":          "MONITOR",
        "nombre_equipo":    "NOMBRE DE EQUIPO",
        "estado":           "ESTADO",
        "anydesk":          "ANYDESK",
        "observacion":      "OBSERVACION",
    })

    # Limpiar ANYDESK
    if "ANYDESK" in df.columns:
        df["ANYDESK"] = (
            df["ANYDESK"]
            .fillna("")
            .astype(str)
            .str.replace(".0", "", regex=False)
            .str.strip()
        )

    return df

# ── Guardar / actualizar un equipo ───────────────────
def save_data(df):
    # Esta función ya no se usa directamente.
    # Las operaciones se hacen en crud.py con Supabase.
    pass