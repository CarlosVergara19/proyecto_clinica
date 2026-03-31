import streamlit as st
from services.data_loader import load_data, save_data
from services.validations import validar_columnas
from services.crud import create_equipo

st.set_page_config(page_title="Sistema Inventario Clínica", layout="wide")



col1, col2 = st.columns([4, 1])

with col1:
    st.markdown("""
        <div  style="background-color: white; padding: 20px; border-radius: 15px; margin-bottom: 20px;
                box-shadow: 0px 4px 10px rgba(0,0,0,0.05);">
        <h1 style='margin-bottom:0; color: black;'>🏥 Sistema de Inventario</h1>
        <h4 style='margin-top:0; color: black;'>Clínica Regional San Jorge</h4>
        </div>
       
    """, unsafe_allow_html=True)

with col2:
    st.image("assets/clinica.jpg", use_container_width=True)
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



menu = st.sidebar.radio(
    "Navegación",
    ["Inventario", "Agregar equipo", "Actualizar / Baja", "Dashboard"]
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
# VISTA DASHBOARD
# =============================

elif menu == "Dashboard":

    st.subheader("📊 Dashboard de Inventario")

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

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total equipos", total)
        col2.metric("Activos", activos)
        col3.metric("Mantenimiento", mantenimiento)
        col4.metric("Baja", baja)

        st.markdown("---")

        # =============================
        # GRÁFICO 1: ESTADO
        # =============================
        estado_counts = df["ESTADO"].value_counts().reset_index()
        estado_counts.columns = ["Estado", "Cantidad"]

        fig_estado = px.pie(
            estado_counts,
            names="Estado",
            values="Cantidad",
            title="Distribución por Estado"
        )

        # =============================
        # GRÁFICO 2: UBICACIÓN
        # =============================
        ubicacion_counts = df["UBICACION"].value_counts().reset_index()
        ubicacion_counts.columns = ["Ubicación", "Cantidad"]

        fig_ubicacion = px.bar(
            ubicacion_counts,
            x="Ubicación",
            y="Cantidad",
            title="Equipos por Ubicación"
        )

        # =============================
        # GRÁFICO 3: MARCAS (TOP 10)
        # =============================
        marca_counts = df["MARCA"].value_counts().reset_index().head(10)
        marca_counts.columns = ["Marca", "Cantidad"]

        fig_marca = px.bar(
            marca_counts,
            x="Marca",
            y="Cantidad",
            title="Top 10 Marcas"
        )

        # =============================
        # MOSTRAR GRÁFICOS
        # =============================
        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(fig_estado, use_container_width=True)

        with col2:
            st.plotly_chart(fig_ubicacion, use_container_width=True)

        st.plotly_chart(fig_marca, use_container_width=True)