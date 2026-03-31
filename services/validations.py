# =============================
# VALIDACIONES BASE OFICIAL
# =============================

COLUMNAS_REQUERIDAS = [
    "ID",
    "CATEGORIA",
    "UBICACION",
    "TIPO",
    "UNIDA FUNCIONAL",
    "USUARIO O CARGO",
    "MARCA",
    "BOARD",
    "MODELO",
    "PROCESADOR",
    "DISCO DURO",
    "ESPACIO",
    "MEMORIA RAM",
    "MONITOR",
    "TECLADO",
    "MOUSE",
    "NOMBRE DE EQUIPO",
    "ESTADO",
    "FECHA DE FAC",
    "Nº FACTURA",
    "OBSERVACION"
]


def validar_columnas(df):
    """
    Verifica que el Excel tenga todas las columnas oficiales requeridas.
    """
    columnas_faltantes = [col for col in COLUMNAS_REQUERIDAS if col not in df.columns]

    if columnas_faltantes:
        raise ValueError(f"Faltan columnas en el Excel: {columnas_faltantes}")


def validar_campos_obligatorios(datos):
    """
    Verifica que los campos críticos no estén vacíos.
    """
    campos_obligatorios = [
        "ID",
        "CATEGORIA",
        "UBICACION",
        "MARCA",
        "MODELO",
        "ESTADO"
    ]

    for campo in campos_obligatorios:
        if not datos.get(campo):
            raise ValueError(f"El campo '{campo}' es obligatorio.")