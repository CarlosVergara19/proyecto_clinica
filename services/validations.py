# =============================
# VALIDACIONES BASE OFICIAL
# =============================

COLUMNAS_REQUERIDAS = [
    "ID",
    "UBICACION",
    "TIPO",
    "UNIDA FUNCIONAL",
    "USUARIO O CARGO",
    "PROCESADOR",
    "ESPACIO",
    "MEMORIA RAM",
    "MONITOR",
    "NOMBRE DE EQUIPO",
    "ESTADO",
    "OBSERVACION",
    "ANYDESK"
]

def validar_columnas(df):
    columnas_requeridas = [
        "ID", "UBICACION", "UNIDA FUNCIONAL", "USUARIO O CARGO",
        "PROCESADOR", "ESPACIO", "MEMORIA RAM", "MONITOR",
        "NOMBRE DE EQUIPO", "ESTADO", "ANYDESK", "OBSERVACION"
    ]
    faltantes = [c for c in columnas_requeridas if c not in df.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas en el Excel: {faltantes}")

def validar_campos_obligatorios(datos):
    obligatorios = ["USUARIO O CARGO", "NOMBRE DE EQUIPO"]
    for campo in obligatorios:
        if not datos.get(campo, "").strip():
            raise ValueError(f"El campo '{campo}' es obligatorio")