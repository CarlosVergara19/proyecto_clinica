import streamlit as st
from services.data_loader import load_data, save_data
from services.validations import validar_columnas
from services.crud import create_equipo
from services.qr import generar_qr

st.set_page_config(
    page_title="Sistema Inventario Clínica",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>

/* Caja blanca */
.header-box {
    
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
}

/* Logo */
.header-logo {
    width: 120px;
}
            
/* 🔵 PC (GRANDE COMO QUIERES) */
.title-main {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 0;
    color: black;
}

.subtitle {
    font-size: 22px;
    margin-top: 0;
    color: #black;
}

/* 📱 MÓVIL AUTOMÁTICO */
@media (max-width: 768px) {

    .title-main {
        font-size: 50px !important;
    }

    .subtitle {
        font-size: 30px !important;
    }

    .header-box {
        padding: 12px;
    }
            
    .header-logo {
        width: 80px;
    }
}

/* 📱 MÓVIL PEQUEÑO */
@media (max-width: 480px) {

    .title-main {
        font-size: 33px !important;
    }

    .subtitle {
        font-size: 25px !important;
    }

    .header-logo {
        width: 60px;
    }
}

</style>
""", unsafe_allow_html=True)


# 🔹 CONTENEDOR
with st.container():

  col1, col2 = st.columns([4, 1])

with col1:
    st.markdown("""
        <div class="header-box">
            <h1 class="title-main"> Sistema de Inventario</h1>
            <h4 class="subtitle">🏥 Clínica Regional San Jorge</h4>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.image("assets/clinica.jpg", width=400)

# =============================
# OPCIONES PREDEFINIDAS
# =============================

OPCIONES_RAM = [
    "DDR3 4 GB",
    "DDR3 8 GB",
    "DDR4 4 GB",
    "DDR4 8 GB",
    "DDR4 16 GB",
    "DDR5 16 GB"
]

OPCIONES_ESTADO = ["ACTIVO", "MANTENIMIENTO", "BAJA"]

OPCIONES_MARCA = [
    "ASUS", "COMPUMAX", "GENERICO", "HP", "POWER", "JANUS", "DELL"
]

OPCIONES_PROCESADOR = [
    "INTEL CORE I3", "INTEL CORE I5", "INTEL CORE I7", "INTEL CORE I9", 
    "INTEL CELERON","INTEL PENTIUM", "AMD RYZEN 5", "INTEL INSIDE",
    "AMD ATHLON","AMD RYZEN 7", "AMD RYZEN 9"
]

OPCIONES_ESPACIO = [
    "120 GB",
    "240 GB",
    "250 GB",
    "256 GB",
    "500 GB",
    "512 GB",
    "1 TB"
]

OPCIONES_TIPO = ["ESCRITORIO", "PORTATIL"]

OPCIONES_CATEGORIA = ["EQUIPO DE OFICINA"]

OPCIONES_UBICACION = [
    "ADMINISTRACION", "ADMISIONES", "ARCHIVO", "AUDITORIA",
    "CALIDAD", "CALL CENTER", "CARTERA", "CONSULTA EXTERNA",
    "CONSULTORIO 0", "CONSULTORIO 1", "CONSULTORIO 2", "CONSULTORIO 3",
    "CONSULTORIO 4", "CONSULTORIO 5", "CONSULTORIO 6", "CONSULTORIO 7",
    "CONSULTORIO DE TRIAJE", "CONSULTORIO OBSTETRICO", "CONTABILIDAD",
    "CUARTO DE SANGRE", "DIRECCION CIENTIFICA", "FACTURACION", "FACTURACION 2DO PISO",
    "FARMACIA", "GERENCIA", "HOSPITALIZACION 2DO PISO", "HUMALIB",
    "LINEA DE FRENTE", "MANTENIMIENTO", "OBSERVACION 1", "OBSERVACION 2",
    "OFICINA DE PANESSO", "PABELLON MATERNO", "REPARACION", "RX",
    "SALA DE ESPERA", "SALA DE PROCEDIMIENTO", "SALA DE QUIROFANO 1", "SALA DE QUIROFANO 2",
    "SIAU", "STAR DE ENFERMERIA", "TALENTO HUMANO", "TRANSITORIA"
]

OPCIONES_UNIDAD = [
    "FACTURACION", "AUDITORIA", "CONSULTA EXTERNA",
    "TALENTO HUMANO", "CALIDAD", "SISTEMAS", "SST",
    "CARTERA", "CONTABILIDAD", "SIAU", "ARCHIVO"
]

try:
    df = load_data()
    validar_columnas(df)
except Exception as e:
    st.error(str(e))
    st.stop()

# =============================
# MODO QR (VISTA DIRECTA)
# =============================

query_params = st.query_params

if "id" in query_params:

    id_qr = query_params["id"]

    # ⚠️ IMPORTANTE: a veces viene como lista
    if isinstance(id_qr, list):
        id_qr = id_qr[0]

    equipo_qr = df[df["ID"] == id_qr]

    if equipo_qr.empty:
        st.error("Equipo no encontrado")
        st.stop()

    equipo = equipo_qr.iloc[0]

    st.title(f"💻 Equipo {equipo['ID']}")

    st.markdown("### 📋 Información general")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Categoría:** {equipo['CATEGORIA']}")
        st.write(f"**Tipo:** {equipo['TIPO']}")
        st.write(f"**Unidad Funcional:** {equipo['UNIDA FUNCIONAL']}")
        st.write(f"**Usuario:** {equipo['USUARIO O CARGO']}")

    with col2:
        st.write(f"**Marca:** {equipo['MARCA']}")
        st.write(f"**Modelo:** {equipo['MODELO']}")
        st.write(f"**Procesador:** {equipo['PROCESADOR']}")
        st.write(f"**RAM:** {equipo['MEMORIA RAM']}")
        st.write(f"**Estado:** {equipo['ESTADO']}")

    st.markdown("### 🛠 Historial del equipo")

    try:
        import pandas as pd

        historial = pd.read_excel("data/historial_equipos.xlsx")

        historial["ID_EQUIPO"] = historial["ID_EQUIPO"].astype(str).str.strip()
        id_qr = str(id_qr).strip()

        historial_equipo = historial[historial["ID_EQUIPO"] == id_qr]

        if historial_equipo.empty:
            st.info("No hay historial registrado.")
        else:
            st.dataframe(historial_equipo, use_container_width=True)

    except Exception as e:
        st.error(f"Error cargando historial: {e}")

    # 🚨 ESTO ES LO MÁS IMPORTANTE
    st.stop()

query_params = st.query_params

id_url = query_params.get("id", None)

menu = st.sidebar.radio(
    "Navegación",
    ["Inventario", "Agregar equipo", "Actualizar / Baja", "Historial" , "Dashboard"]
)

# =============================
# VISTA INVENTARIO
# =============================

if menu == "Inventario":

    st.subheader("Inventario de Equipos")

    if df.empty:
        st.info("No hay equipos registrados.")
    else:

        df_filtrado = df.copy()

        with st.form("form_filtros"):

            st.markdown("### 🔍 Filtros")

            col1, col2, col3 = st.columns(3)

            with col1:
                estados = st.multiselect(
                    "Estado",
                    options=sorted(df["ESTADO"].dropna().unique())
                )

            with col2:
                unidades = st.multiselect(
                    "Unidad Funcional",
                    options=sorted(df["UNIDA FUNCIONAL"].dropna().unique())
                )

            with col3:
                marcas = st.multiselect(
                    "Marca",
                    options=sorted(df["MARCA"].dropna().unique())
                )

            col4, col5 = st.columns(2)

            with col4:
                rams = st.multiselect(
                    "Memoria RAM",
                    options=sorted(df["MEMORIA RAM"].dropna().unique())
                )

            with col5:
                busqueda = st.text_input("Buscar (modelo o nombre)").strip().lower()

            aplicar = st.form_submit_button("Aplicar filtros")

        
        # ================= FILTRO =================
        if aplicar:

            if estados:
                df_filtrado = df_filtrado[df_filtrado["ESTADO"].isin(estados)]

            if unidades:
                df_filtrado = df_filtrado[df_filtrado["UNIDA FUNCIONAL"].isin(unidades)]

            if marcas:
                df_filtrado = df_filtrado[df_filtrado["MARCA"].isin(marcas)]

            if rams:
                df_filtrado = df_filtrado[df_filtrado["MEMORIA RAM"].isin(rams)]

            if busqueda:
                df_filtrado = df_filtrado[
                    df_filtrado["MODELO"].str.lower().str.contains(busqueda, na=False)
                    | df_filtrado["NOMBRE DE EQUIPO"].str.lower().str.contains(busqueda, na=False)
                ]

        st.markdown(f"### Resultados: {len(df_filtrado)} equipo(s)")
        st.dataframe(df_filtrado, use_container_width=True)


        st.subheader("Generar QR de equipo")

    id_qr = st.selectbox("Selecciona equipo", df["ID"])

    if st.button("Generar QR"):

        qr_img = generar_qr(id_qr, "https://proyectocrsj.streamlit.app")

        st.image(qr_img, caption=f"QR para {id_qr}")

        st.download_button(
            "Descargar QR",
            data=qr_img,
            file_name=f"{id_qr}.png",
            mime="image/png"
        )
# =============================
# VISTA AGREGAR
# =============================

elif menu == "Agregar equipo":

    st.subheader("Agregar nuevo equipo")

    with st.form("form_nuevo_equipo", clear_on_submit=True):

        col1, col2 = st.columns(2)

        with col1:
            id_equipo = st.text_input("ID (ej: CRSJ003)")
            categoria = st.selectbox("Categoría", OPCIONES_CATEGORIA)
            ubicacion = st.selectbox("Ubicación", OPCIONES_UBICACION)
            tipo = st.selectbox("Tipo", OPCIONES_TIPO)
            unidad_funcional = st.selectbox("Unidad Funcional", OPCIONES_UNIDAD)
            usuario = st.text_input("Usuario o Cargo")
            marca = st.text_input("Marca")
            board = st.text_input("Board")
            modelo = st.text_input("Modelo")
            procesador = st.selectbox("Procesador", OPCIONES_PROCESADOR)

        with col2:
            disco = st.text_input("Disco Duro")
            espacio = st.selectbox("Espacio", OPCIONES_ESPACIO)
            memoria = st.selectbox("Memoria RAM", OPCIONES_RAM)
            monitor = st.text_input("Monitor")
            teclado = st.text_input("Teclado")
            mouse = st.text_input("Mouse")
            nombre_equipo = st.text_input("Nombre de Equipo")
            estado = st.selectbox("Estado", OPCIONES_ESTADO)
            fecha_fac = st.text_input("Fecha de Factura")
            factura = st.text_input("Nº Factura")

        observacion = st.text_area("Observación")

        submitted = st.form_submit_button("Guardar equipo")

        if submitted:

            nuevo_equipo = {
                "ID": id_equipo.strip(),
                "CATEGORIA": categoria.strip(),
                "UBICACION": ubicacion.strip(),
                "TIPO": tipo.strip(),
                "UNIDA FUNCIONAL": unidad_funcional.strip(),
                "USUARIO O CARGO": usuario.strip(),
                "MARCA": marca.strip(),
                "BOARD": board.strip(),
                "MODELO": modelo.strip(),
                "PROCESADOR": procesador.strip(),
                "DISCO DURO": disco.strip(),
                "ESPACIO": espacio.strip(),
                "MEMORIA RAM": memoria.strip(),
                "MONITOR": monitor.strip(),
                "TECLADO": teclado.strip(),
                "MOUSE": mouse.strip(),
                "NOMBRE DE EQUIPO": nombre_equipo.strip(),
                "ESTADO": estado,
                "FECHA DE FAC": fecha_fac.strip(),
                "Nº FACTURA": factura.strip(),
                "OBSERVACION": observacion.strip()
            }

            try:
                import pandas as pd

                df = pd.concat([df, pd.DataFrame([nuevo_equipo])], ignore_index=True)
                save_data(df)

                st.success("Equipo agregado correctamente")
                st.rerun()

            except Exception as e:
                st.error(str(e))
# =============================
# VISTA ACTUALIZAR / BAJA
# =============================

elif menu == "Actualizar / Baja":
    st.subheader("Editar equipo")

    if df.empty:
        st.warning("No hay registros disponibles.")
    else:

        id_seleccionado = st.selectbox(
            "Selecciona ID del equipo",
            df["ID"]
        )

        equipo = df[df["ID"] == id_seleccionado].iloc[0]

        with st.form("form_editar_equipo"):

            col1, col2 = st.columns(2)

            with col1:
                categoria = st.selectbox(
                    "Categoría",
                    OPCIONES_CATEGORIA,
                    index=OPCIONES_CATEGORIA.index(equipo["CATEGORIA"])
                    if equipo["CATEGORIA"] in OPCIONES_CATEGORIA else 0
                )

                ubicacion = st.selectbox(
                    "Ubicación",
                    OPCIONES_UBICACION,
                    index=OPCIONES_UBICACION.index(equipo["UBICACION"])
                    if equipo["UBICACION"] in OPCIONES_UBICACION else 0
                )

                tipo = st.selectbox(
                    "Tipo",
                    OPCIONES_TIPO,
                    index=OPCIONES_TIPO.index(equipo["TIPO"])
                    if equipo["TIPO"] in OPCIONES_TIPO else 0
                )

                unidad_funcional = st.selectbox(
                    "Unidad Funcional",
                    OPCIONES_UNIDAD,
                    index=OPCIONES_UNIDAD.index(equipo["UNIDA FUNCIONAL"])
                    if equipo["UNIDA FUNCIONAL"] in OPCIONES_UNIDAD else 0
                )

                usuario = st.text_input("Usuario o Cargo", value=equipo["USUARIO O CARGO"])

                marca = st.selectbox(
                    "Marca",
                    OPCIONES_MARCA,
                    index=OPCIONES_MARCA.index(equipo["MARCA"])
                    if equipo["MARCA"] in OPCIONES_MARCA else 0
                )

                board = st.text_input("Board", value=equipo["BOARD"])
                modelo = st.text_input("Modelo", value=equipo["MODELO"])

                procesador = st.selectbox(
                    "Procesador",
                    OPCIONES_PROCESADOR,
                    index=OPCIONES_PROCESADOR.index(equipo["PROCESADOR"])
                    if equipo["PROCESADOR"] in OPCIONES_PROCESADOR else 0
                )

            with col2:
                disco = st.text_input("Disco Duro", value=equipo["DISCO DURO"])

                espacio = st.selectbox(
                    "Espacio",
                    OPCIONES_ESPACIO,
                    index=OPCIONES_ESPACIO.index(equipo["ESPACIO"])
                    if equipo["ESPACIO"] in OPCIONES_ESPACIO else 0
                )

                memoria = st.selectbox(
                    "Memoria RAM",
                    OPCIONES_RAM,
                    index=OPCIONES_RAM.index(equipo["MEMORIA RAM"])
                    if equipo["MEMORIA RAM"] in OPCIONES_RAM else 0
                )

                monitor = st.text_input("Monitor", value=equipo["MONITOR"])
                teclado = st.text_input("Teclado", value=equipo["TECLADO"])
                mouse = st.text_input("Mouse", value=equipo["MOUSE"])
                nombre_equipo = st.text_input("Nombre de Equipo", value=equipo["NOMBRE DE EQUIPO"])

                estado = st.selectbox(
                    "Estado",
                    ["ACTIVO", "MANTENIMIENTO", "BAJA"],
                    index=["ACTIVO", "MANTENIMIENTO", "BAJA"].index(equipo["ESTADO"])
                    if equipo["ESTADO"] in ["ACTIVO", "MANTENIMIENTO", "BAJA"] else 0
                )

                fecha_fac = st.text_input("Fecha de Factura", value=equipo["FECHA DE FAC"])
                factura = st.text_input("Nº Factura", value=equipo["Nº FACTURA"])

            observacion = st.text_area("Observación", value=equipo["OBSERVACION"])

            submitted = st.form_submit_button("Guardar cambios")

            if submitted:

                datos_actualizados = {
                    "CATEGORIA": categoria.strip(),
                    "UBICACION": ubicacion.strip(),
                    "TIPO": tipo.strip(),
                    "UNIDA FUNCIONAL": unidad_funcional.strip(),
                    "USUARIO O CARGO": usuario.strip(),
                    "MARCA": marca.strip(),
                    "BOARD": board.strip(),
                    "MODELO": modelo.strip(),
                    "PROCESADOR": procesador.strip(),
                    "DISCO DURO": disco.strip(),
                    "ESPACIO": espacio.strip(),
                    "MEMORIA RAM": memoria.strip(),
                    "MONITOR": monitor.strip(),
                    "TECLADO": teclado.strip(),
                    "MOUSE": mouse.strip(),
                    "NOMBRE DE EQUIPO": nombre_equipo.strip(),
                    "ESTADO": estado.strip(),
                    "FECHA DE FAC": fecha_fac.strip(),
                    "Nº FACTURA": factura.strip(),
                    "OBSERVACION": observacion.strip()
                }

                try:
                    from services.crud import update_equipo
                    df = update_equipo(df, id_seleccionado, datos_actualizados)
                    save_data(df)
                    st.success("Equipo actualizado correctamente")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))

        # =============================
        # ACCIONES CRÍTICAS
        # =============================

        st.markdown("---")
        st.subheader("⚠️ Acciones críticas")

        col1, col2 = st.columns(2)

        # 🔴 ELIMINAR DEFINITIVO
        with col1:
            confirmar = st.checkbox("Confirmar eliminación permanente")

            if st.button("🗑️ Eliminar equipo", use_container_width=True):

                if not confirmar:
                    st.warning("Debes confirmar la eliminación")
                else:
                    try:
                        from services.crud import delete_equipo
                        df = delete_equipo(df, id_seleccionado)
                        save_data(df)
                        st.success("Equipo eliminado correctamente")
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))

        # 🟡 MARCAR COMO BAJA
        with col2:
            if st.button("📉 Marcar como BAJA", use_container_width=True):
                try:
                    df.loc[df["ID"] == id_seleccionado, "ESTADO"] = "BAJA"
                    save_data(df)
                    st.success("Equipo marcado como BAJA")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))                    
                    
# =============================
# VISTA HISTORIAL
# =============================

elif menu == "Historial":

    st.subheader("Historial de Equipos")

    from services.historial import (
        load_historial, save_historial,
        agregar_historial, update_historial, delete_historial
    )

    historial_df = load_historial()

    if df.empty:
        st.warning("No hay equipos registrados.")
    else:

        if id_url and id_url in df["ID"].values:
            id_equipo = id_url
            st.success(f"Equipo cargado automáticamente: {id_equipo}")
        else:
            id_equipo = st.selectbox("Selecciona equipo", df["ID"])

        historial_equipo = historial_df[
            historial_df["ID_EQUIPO"] == id_equipo
        ]

        st.markdown("### Historial")

        if historial_equipo.empty:
            st.info("Este equipo no tiene historial.")
        else:
            st.dataframe(historial_equipo, use_container_width=True)

        # =============================
        # EDITAR / ELIMINAR
        # =============================

        if not historial_equipo.empty:

            st.markdown("### ✏️ Editar / Eliminar registro")

            id_registro = st.selectbox(
                "Selecciona registro",
                historial_equipo["ID_REGISTRO"]
            )

            registro = historial_df[
                historial_df["ID_REGISTRO"] == id_registro
            ].iloc[0]

            with st.form("form_editar_historial"):

                fecha = st.date_input("Fecha", value=registro["FECHA"])

                tipo = st.selectbox(
                    "Tipo",
                    ["MANTENIMIENTO", "REPARACIÓN", "CAMBIO DE PIEZA", "FORMATEO"],
                    index=["MANTENIMIENTO", "REPARACIÓN", "CAMBIO DE PIEZA", "FORMATEO"].index(registro["TIPO"])
                )

                descripcion = st.text_area("Descripción", value=registro["DESCRIPCION"])
                tecnico = st.text_input("Técnico", value=registro["TECNICO"])

                col1, col2 = st.columns(2)

                with col1:
                    actualizar = st.form_submit_button("Actualizar")

                with col2:
                    eliminar = st.form_submit_button("Eliminar")

                if actualizar:
                    datos = {
                        "FECHA": fecha,
                        "TIPO": tipo,
                        "DESCRIPCION": descripcion,
                        "TECNICO": tecnico
                    }

                    historial_df = update_historial(historial_df, id_registro, datos)
                    save_historial(historial_df)

                    st.success("Registro actualizado")
                    st.rerun()

                if eliminar:
                    historial_df = delete_historial(historial_df, id_registro)
                    save_historial(historial_df)

                    st.warning("Registro eliminado")
                    st.rerun()

        # =============================
        # AGREGAR
        # =============================

        st.markdown("---")
        st.markdown("### ➕ Agregar registro")

        with st.form("form_historial"):

            fecha = st.date_input("Fecha")

            tipo = st.selectbox(
                "Tipo",
                ["MANTENIMIENTO", "REPARACIÓN", "CAMBIO DE PIEZA", "FORMATEO"]
            )

            descripcion = st.text_area("Descripción")
            tecnico = st.selectbox(
                "Tecnico", 
                ["ANDRES MONTIEL", "CARLOS VERGARA", "JESUS OLIVERO"]
                )

            guardar = st.form_submit_button("Guardar")

            if guardar:
                datos = {
                    "ID_EQUIPO": id_equipo,
                    "FECHA": fecha,
                    "TIPO": tipo,
                    "DESCRIPCION": descripcion,
                    "TECNICO": tecnico
                }

                historial_df = agregar_historial(historial_df, datos)
                save_historial(historial_df)

                st.success("Registro agregado")
                st.rerun()
   # =============================
# VISTA DASHBOARD
# =============================

elif menu == "Dashboard":

    # 🎨 ESTILO POWER BI (SOLO DASHBOARD)
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #0f172a;
    }

    h1, h2, h3, h4, h5, h6, p, label {
        color: white !important;
    }

    .kpi-card {
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        background: linear-gradient(135deg, #1e293b, #334155);
        box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
    }

    .kpi-title {
        font-size: 14px;
        color: #cbd5f5;
    }

    .kpi-value {
        font-size: 28px;
        font-weight: bold;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("## 📊 Dashboard de Inventario")

    if df.empty:
        st.warning("No hay datos para mostrar.")
    else:
        import plotly.express as px

        # =============================
        # KPIs
        # =============================
        total = len(df)
        activos = len(df[df["ESTADO"] == "ACTIVO"])
        mantenimiento = len(df[df["ESTADO"] == "MANTENIMIENTO"])
        baja = len(df[df["ESTADO"] == "BAJA"])

        def kpi(valor, titulo):
            return f"""
            <div class="kpi-card">
                <div class="kpi-title">{titulo}</div>
                <div class="kpi-value">{valor}</div>
            </div>
            """

        col1, col2, col3, col4 = st.columns(4)

        col1.markdown(kpi(total, "Total equipos"), unsafe_allow_html=True)
        col2.markdown(kpi(activos, "Activos"), unsafe_allow_html=True)
        col3.markdown(kpi(mantenimiento, "Mantenimiento"), unsafe_allow_html=True)
        col4.markdown(kpi(baja, "Baja"), unsafe_allow_html=True)

        st.markdown("---")

        # =============================
        # PREPARACIÓN DATOS
        # =============================
        estado_counts = df["ESTADO"].value_counts().reset_index()
        estado_counts.columns = ["Estado", "Cantidad"]

        unidad_counts = df["UNIDA FUNCIONAL"].value_counts().reset_index()
        unidad_counts.columns = ["Unidad", "Cantidad"]

        marca_counts = df["MARCA"].value_counts().reset_index().head(10)
        marca_counts.columns = ["Marca", "Cantidad"]

        tipo_counts = df["TIPO"].value_counts().reset_index()
        tipo_counts.columns = ["Tipo", "Cantidad"]

        # =============================
        # GRÁFICOS POWER BI
        # =============================
        fig_estado = px.pie(
            estado_counts,
            names="Estado",
            values="Cantidad",
            hole=0.5
        )
        fig_estado.update_layout(
            template="plotly_dark",
            title="Estado de Equipos"
        )

        fig_unidad = px.bar(
            unidad_counts,
            x="Unidad",
            y="Cantidad"
        )
        fig_unidad.update_layout(
            template="plotly_dark",
            title="Equipos por Unidad"
        )

        fig_marca = px.bar(
            marca_counts,
            x="Marca",
            y="Cantidad"
        )
        fig_marca.update_layout(
            template="plotly_dark",
            title="Top Marcas"
        )

        fig_tipo = px.pie(
            tipo_counts,
            names="Tipo",
            values="Cantidad"
        )
        fig_tipo.update_layout(
            template="plotly_dark",
            title="Tipos de Equipos"
        )

        # =============================
        # LAYOUT GRÁFICOS
        # =============================
        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(fig_estado, use_container_width=True)
            st.plotly_chart(fig_tipo, use_container_width=True)

        with col2:
            st.plotly_chart(fig_unidad, use_container_width=True)
            st.plotly_chart(fig_marca, use_container_width=True)

        # =============================
        # EXPORTAR PDF (BÁSICO POR AHORA)
        # =============================
        st.markdown("### 📄 Exportar Dashboard")

        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        import tempfile

        def generar_pdf():
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            doc = SimpleDocTemplate(tmp_file.name)

            styles = getSampleStyleSheet()
            contenido = []

            contenido.append(Paragraph("Reporte de Inventario - Clínica", styles["Title"]))
            contenido.append(Spacer(1, 12))

            contenido.append(Paragraph(f"Total equipos: {total}", styles["Normal"]))
            contenido.append(Paragraph(f"Activos: {activos}", styles["Normal"]))
            contenido.append(Paragraph(f"Mantenimiento: {mantenimiento}", styles["Normal"]))
            contenido.append(Paragraph(f"Baja: {baja}", styles["Normal"]))

            doc.build(contenido)

            return tmp_file.name

        if st.button("📥 Descargar PDF"):
            pdf_path = generar_pdf()

            with open(pdf_path, "rb") as f:
                st.download_button(
                    "Descargar reporte",
                    f,
                    file_name="dashboard.pdf",
                    mime="application/pdf"
                )