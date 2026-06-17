from supabase import create_client
import streamlit as st

def get_supabase():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

# ── Crear equipo ──────────────────────────────────────
def create_equipo(df, datos):
    # No se usa desde app.py (app.py maneja esto directo)
    pass

# ── Actualizar equipo ─────────────────────────────────
def update_equipo(df, id_equipo, datos_actualizados):
    supabase = get_supabase()

    # Mapear nombres app.py → columnas Supabase
    mapeo = {
        "CATEGORIA":        "categoria",
        "UBICACION":        "ubicacion",
        "TIPO":             "tipo",
        "UNIDA FUNCIONAL":  "unidad_funcional",
        "USUARIO O CARGO":  "usuario_cargo",
        "MARCA":            "marca",
        "PROCESADOR":       "procesador",
        "ESPACIO":          "espacio",
        "MEMORIA RAM":      "memoria_ram",
        "MONITOR":          "monitor",
        "NOMBRE DE EQUIPO": "nombre_equipo",
        "ESTADO":           "estado",
        "ANYDESK":          "anydesk",
        "FECHA DE FAC":     "fecha_factura",
        "Nº FACTURA":       "num_factura",
        "OBSERVACION":      "observacion",
    }

    datos_supabase = {
        mapeo[k]: v
        for k, v in datos_actualizados.items()
        if k in mapeo
    }

    supabase.table("equipos").update(datos_supabase).eq("id", id_equipo).execute()

    # Actualizar también el DataFrame local para que st.rerun() refleje el cambio
    for campo, valor in datos_actualizados.items():
        df.loc[df["ID"] == id_equipo, campo] = valor

    return df

# ── Eliminar equipo ───────────────────────────────────
def delete_equipo(df, id_equipo):
    supabase = get_supabase()
    supabase.table("equipos").delete().eq("id", id_equipo).execute()
    df = df[df["ID"] != id_equipo]
    return df