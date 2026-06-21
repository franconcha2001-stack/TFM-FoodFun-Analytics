# =====================================================
# FOOD&FUN ANALYTICS
# Trabajo Fin de Máster
# =====================================================

# Importación de librerías

import streamlit as st
import pandas as pd

# =====================================================
# CONFIGURACIÓN DE LA PÁGINA
# =====================================================

st.set_page_config(
    page_title="Food&Fun Analytics",
    layout="wide"
)

# =====================================================
# ESTILO PERSONALIZADO
# =====================================================

st.markdown("""
<style>

.stApp {
    background-color: #5A5D48;
}

h1, h2, h3, h4, h5, h6 {
    color: white !important;
}

p, label {
    color: white !important;
}

[data-testid="stMetricValue"] {
    color: white !important;
}

[data-testid="stMetricLabel"] {
    color: white !important;
}

[data-testid="stSidebar"] {
    background-color: #4d503d;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* Selectbox: texto negro */

[data-baseweb="select"] {
    color: black !important;
}

[data-baseweb="select"] * {
    color: black !important;
}

/* Menú desplegable */

div[role="listbox"] {
    color: black !important;
}

div[role="option"] {
    color: black !important;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# MENÚ LATERAL
# =====================================================

st.sidebar.image(
    "LogoF&F.png",
    width=180
)

st.sidebar.title("Food&Fun")

opcion = st.sidebar.radio(
    "Seleccionar módulo",
    [
        "Dashboard Ejecutivo",
        "Control de Ventas",
        "Gestión Operativa de Eventos",
        "Predicción de Demanda",
        "Predicción de Ocupación",
        "Calendario Optimizado",
        "Conclusiones"
    ]
)

# =====================================================
# CARGA DE DATOS
# =====================================================

try:

    df = pd.read_excel(
        "Compras_2526_F&F.xlsx"
    )

except:

    st.error(
        "No se encuentra Compras_2526_F&F.xlsx"
    )

    st.stop()

try:

    df_operativo = pd.read_excel(
        "FoodFun_Analytics_Operativo.xlsx"
    )

except:

    df_operativo = None
# =====================================================
# DASHBOARD EJECUTIVO
# =====================================================

if opcion == "Dashboard Ejecutivo":

    # Banner principal

    st.image(
        "Banner.png",
        width="stretch"
    )

    # Título

    st.title("Food&Fun Analytics")

    st.markdown("""
    ### Trabajo Fin de Máster

    **Business Analytics aplicado a FOOD&FUN**

    Análisis predictivo de la demanda mediante técnicas de Machine Learning y optimización matemática.
    """)

    st.header("📊 Dashboard Ejecutivo")

    # KPI's principales

    facturacion = df["Importe Total"].sum()

    pedidos = df["Número de Pedido"].nunique()

    plazas = df["Cantidad de Plazas"].sum()

    ticket = facturacion / pedidos

    talleres = df["Taller"].nunique()

    # Visualización KPI's

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Facturación",
        f"{facturacion:,.0f} €"
    )

    col2.metric(
        "Pedidos",
        pedidos
    )

    col3.metric(
        "Plazas",
        plazas
    )

    col4.metric(
        "Ticket Medio",
        f"{ticket:.2f} €"
    )

    col5.metric(
        "Talleres",
        talleres
    )

    # Facturación por taller

        # Facturación por taller

    st.subheader(
        "Top 10 talleres por facturación"
    )

    facturacion_taller = (
        df.groupby("Taller")["Importe Total"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(
        facturacion_taller
    )

    # Antelación de reserva

    if df_operativo is not None and "Antelacion Dias" in df_operativo.columns:

        st.subheader(
            "Distribución de la antelación de reserva"
        )

        antelacion = (
            df_operativo["Antelacion Dias"]
            .dropna()
            .astype(int)
            .value_counts()
            .sort_index()
        )

        st.bar_chart(
            antelacion
        )

    # Evolución temporal

    st.subheader(
        "Evolución mensual de la facturación"
    )

    df["Fecha de Compra"] = pd.to_datetime(
        df["Fecha de Compra"]
    )

    ventas_mes = (
        df.groupby(
            df["Fecha de Compra"].dt.to_period("M")
        )["Importe Total"]
        .sum()
    )

    ventas_mes.index = ventas_mes.index.astype(str)

    st.line_chart(
        ventas_mes
    )

# =====================================================
# CONTROL DE VENTAS
# =====================================================

elif opcion == "Control de Ventas":

    st.header(
        "💰 Control de Ventas"
    )

    # -----------------------------------------
    # Preparación de datos
    # -----------------------------------------

    df["Fecha Taller"] = pd.to_datetime(
        df["Fecha Taller"],
        errors="coerce"
    )

    df["Importe Neto"] = (
        df["Importe Total"]
        - df["IMPORTE DEVOLUCIÓN"].fillna(0)
    )

    control_ventas = (
        df.dropna(subset=["Fecha Taller"])
        .groupby(
            ["Taller", "Fecha Taller"],
            as_index=False
        )
        .agg({
            "Cantidad de Plazas": "sum",
            "Importe Neto": "sum"
        })
    )

    # -----------------------------------------
    # Día de la semana
    # -----------------------------------------

    dias = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }

    control_ventas["Curso"] = (
        control_ventas["Fecha Taller"]
        .dt.day_name()
        .map(dias)
    )

    # -----------------------------------------
    # Plazas
    # -----------------------------------------

    control_ventas["Plazas Máximas"] = 18

    control_ventas["Plazas Vendidas"] = (
        control_ventas["Cantidad de Plazas"]
    )

    control_ventas["Plazas Disponibles"] = (
        control_ventas["Plazas Máximas"]
        - control_ventas["Plazas Vendidas"]
    )

    # -----------------------------------------
    # Año y mes
    # -----------------------------------------

    control_ventas["Año"] = (
        control_ventas["Fecha Taller"]
        .dt.year
    )

    control_ventas["Mes"] = (
        control_ventas["Fecha Taller"]
        .dt.month
    )

    # -----------------------------------------
    # Filtros
    # -----------------------------------------

    col1, col2 = st.columns(2)

    lista_anios = ["Todos"] + sorted(
        control_ventas["Año"]
        .dropna()
        .unique()
        .tolist()
    )

    anio = col1.selectbox(
        "Seleccionar año",
        lista_anios
    )

    meses = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre"
    }

    lista_meses = ["Todos"] + list(
        meses.values()
    )

    mes = col2.selectbox(
        "Seleccionar mes",
        lista_meses
    )

    control_filtrado = control_ventas.copy()

    if anio != "Todos":

        control_filtrado = control_filtrado[
            control_filtrado["Año"] == anio
        ]

    if mes != "Todos":

        mes_num = {
            v: k for k, v in meses.items()
        }[mes]

        control_filtrado = control_filtrado[
            control_filtrado["Mes"] == mes_num
        ]

    # -----------------------------------------
    # KPIs
    # -----------------------------------------

    facturacion = (
        control_filtrado["Importe Neto"]
        .sum()
    )

    plazas = (
        control_filtrado["Plazas Vendidas"]
        .sum()
    )

    talleres = len(
        control_filtrado
    )

    ticket = (
        facturacion / plazas
        if plazas > 0
        else 0
    )

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "Facturación",
        f"{facturacion:,.0f} €"
    )

    k2.metric(
        "Plazas Vendidas",
        int(plazas)
    )

    k3.metric(
        "Ticket Medio",
        f"{ticket:.2f} €"
    )

    k4.metric(
        "Talleres",
        talleres
    )

    # -----------------------------------------
    # Tabla
    # -----------------------------------------

    tabla = control_filtrado.copy()

    tabla["Fecha Taller"] = (
        tabla["Fecha Taller"]
        .dt.strftime("%d/%m/%Y")
    )

    tabla = tabla[
        [
            "Taller",
            "Curso",
            "Fecha Taller",
            "Plazas Máximas",
            "Plazas Vendidas",
            "Plazas Disponibles",
            "Importe Neto"
        ]
    ]

    st.dataframe(
        tabla,
        use_container_width=True,
        hide_index=True
    )
# =====================================================
# PREDICCIÓN DE DEMANDA
# =====================================================

elif opcion == "Predicción de Demanda":

    st.header(
        "🤖 Predicción de Demanda"
    )

    try:

        demanda = pd.read_excel(
            "resultados_demanda.xlsx"
        )

        st.dataframe(
            demanda,
            width="stretch"
        )

    except:

        st.warning(
            "No se encuentra resultados_demanda.xlsx"
        )

# =====================================================
# PREDICCIÓN DE OCUPACIÓN
# =====================================================

elif opcion == "Predicción de Ocupación":

    st.header(
        "👥 Predicción de Ocupación"
    )

    try:

        ocupacion = pd.read_excel(
            "resultados_ocupacion.xlsx"
        )

        st.dataframe(
            ocupacion,
            width="stretch"
        )

    except:

        st.warning(
            "No se encuentra resultados_ocupacion.xlsx"
        )

# =====================================================
# CALENDARIO OPTIMIZADO
# =====================================================

elif opcion == "Calendario Optimizado":

    st.header(
        "📅 Calendario Optimizado mediante Gurobi"
    )

    try:

        calendario = pd.read_excel(
            "Calendario_Optimizado_FoodFun_2026.xlsx"
        )

        st.dataframe(
            calendario,
            width="stretch"
        )

    except:

        st.warning(
            "No se encuentra Calendario_Optimizado_FoodFun_2026.xlsx"
        )

# =====================================================
# GESTIÓN OPERATIVA DE EVENTOS
# =====================================================

elif opcion == "Gestión Operativa de Eventos":

    st.header(
        "🎯 Gestión Operativa de Eventos"
    )

    if df_operativo is None:

        st.warning(
            "No se encuentra FoodFun_Analytics_Operativo.xlsx"
        )

    else:

        talleres = sorted(
            df_operativo["Taller"]
            .dropna()
            .unique()
        )

        taller_seleccionado = st.selectbox(
            "Seleccionar taller",
            talleres
        )

        datos_taller = df_operativo[
            df_operativo["Taller"]
            == taller_seleccionado
        ]

        fechas = sorted(
    datos_taller["Fecha Taller"]
    .dropna()
    .unique(),
    key=lambda x: pd.to_datetime(
        x,
        format="%d/%m/%Y"
    )
)

        fecha_seleccionada = st.selectbox(
            "Seleccionar fecha",
            fechas
        )

        datos = datos_taller[
            datos_taller["Fecha Taller"]
            == fecha_seleccionada
        ]

        st.subheader(
            f"{taller_seleccionado} | {pd.to_datetime(fecha_seleccionada).strftime('%d/%m/%Y')}"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Plazas vendidas",
            int(datos["Cantidad de Plazas"].sum())
        )

        col2.metric(
            "Ingresos",
            f"{datos['Importe Total'].sum():,.0f} €"
        )

        col3.metric(
            "Pedidos",
            datos["Número de Pedido"].nunique()
        )

        st.subheader(
            "Detalle de reservas"
        )

        columnas = [
            "Fecha de Compra",
            "Fecha Taller",
            "Número de Pedido",
            "Cantidad de Plazas",
            "Importe Total",
            "Método de Pago",
            "Antelacion Dias"
        ]

        columnas = [
            c for c in columnas
            if c in datos.columns
        ]
        
        st.dataframe(
            datos[columnas]
            .sort_values("Fecha de Compra"),
            use_container_width=True
        )
# =====================================================
# CONCLUSIONES
# =====================================================

elif opcion == "Conclusiones":

    st.header(
        "📝 Conclusiones"
    )

    st.markdown("""
### Principales resultados

✅ El modelo de predicción de demanda alcanzó un **R² = 0.850**.

✅ El modelo de predicción de ocupación alcanzó un **R² = 0.275**.

✅ Se desarrolló un calendario anual optimizado mediante **Gurobi**.

✅ La integración de Business Analytics, Machine Learning y Optimización Matemática proporciona una herramienta de apoyo a la toma de decisiones para Food&Fun.
""")