import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Dashboard RRHH", layout="wide", page_icon="👥")

# Título principal
st.title("👥 Dashboard de Análisis de Empleados - RRHH")

# =============================================================================
# 🎨 PALETA DE COLORES POR DEPARTAMENTO
# =============================================================================
DEPARTMENT_COLORS = {
    "Sales": "#FF6B6B",           # Rojo coral
    "Marketing": "#4ECDC4",        # Turquesa
    "HR": "#95E1D3",               # Verde menta
    "Engineering": "#3498DB",      # Azul
    "Finance": "#F39C12"           # Naranja dorado
}

# =============================================================================
# CARGA DE DATOS
# =============================================================================
@st.cache_data
def load_data():
    return pd.read_csv("employees.csv")

df = load_data()
df_original = df.copy()

# =============================================================================
# LIMPIEZA DE DATOS
# =============================================================================
st.sidebar.header("🧹 Limpieza de Datos")

# 1. Filtro por edad (18-65 años)
edad_min = st.sidebar.number_input("Edad mínima", min_value=0, max_value=100, value=18)
edad_max = st.sidebar.number_input("Edad máxima", min_value=0, max_value=100, value=65)
df = df[(df["Age"] >= edad_min) & (df["Age"] <= edad_max)]

# 2. Salarios positivos
df = df[df["Salary"] > 0]

# 3. Años en empresa no negativos
df = df[df["YearsAtCompany"] >= 0]

# 4. PerformanceScore en rango 0-100
df = df[(df["PerformanceScore"] >= 0) & (df["PerformanceScore"] <= 100)]

# 5. Eliminar duplicados
df = df.drop_duplicates(subset=["EmployeeID"])

# 6. Estandarizar Género
df["Gender"] = df["Gender"].str.upper().str.strip()

# Resumen de limpieza
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Resumen de Limpieza")
st.sidebar.write(f"**Total original:** {len(df_original)}")
st.sidebar.write(f"**Después de limpieza:** {len(df)}")
if len(df_original) - len(df) > 0:
    st.sidebar.warning(f"⚠️ {len(df_original) - len(df)} registros eliminados")
else:
    st.sidebar.success("✅ Todos los datos son válidos")

# =============================================================================
# FILTROS DE ANÁLISIS
# =============================================================================
st.sidebar.header("🔍 Filtros de Análisis")

departamentos = st.sidebar.multiselect(
    "Departamento",
    options=df["Department"].unique(),
    default=df["Department"].unique()
)

generos = st.sidebar.multiselect(
    "Género",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

min_salario, max_salario = int(df["Salary"].min()), int(df["Salary"].max())
rango_salario = st.sidebar.slider("Rango de Salario ($)", min_salario, max_salario, (min_salario, max_salario))

min_anios, max_anios = int(df["YearsAtCompany"].min()), int(df["YearsAtCompany"].max())
rango_anios = st.sidebar.slider("Años en la Empresa", min_anios, max_anios, (min_anios, max_anios))

# Aplicar filtros
df_filtrado = df[
    (df["Department"].isin(departamentos)) &
    (df["Gender"].isin(generos)) &
    (df["Salary"] >= rango_salario[0]) &
    (df["Salary"] <= rango_salario[1]) &
    (df["YearsAtCompany"] >= rango_anios[0]) &
    (df["YearsAtCompany"] <= rango_anios[1])
]

# =============================================================================
# 🎯 KPIs PRINCIPALES
# =============================================================================
st.subheader("🎯 Indicadores Clave de Desempeño (KPIs)")

col1, col2, col3 = st.columns(3)

# KPI 1: Desempeño Promedio
kpi_desempeno = df_filtrado["PerformanceScore"].mean()
delta_desempeno = kpi_desempeno - 80

with col1:
    st.metric(
        label="⭐ Desempeño Promedio",
        value=f"{kpi_desempeno:.1f} / 100",
        delta=f"{delta_desempeno:+.1f} vs meta 80",
        delta_color="normal" if delta_desempeno >= 0 else "inverse"
    )

# KPI 2: Antigüedad Promedio
kpi_antiguedad = df_filtrado["YearsAtCompany"].mean()
delta_antiguedad = kpi_antiguedad - 5

with col2:
    st.metric(
        label="📅 Antigüedad Promedio",
        value=f"{kpi_antiguedad:.1f} años",
        delta=f"{delta_antiguedad:+.1f} vs meta 5 años",
        delta_color="normal" if delta_antiguedad >= 0 else "inverse"
    )

# KPI 3: Salario Promedio
kpi_salario = df_filtrado["Salary"].mean()
delta_salario = kpi_salario - 70000

with col3:
    st.metric(
        label="💰 Salario Promedio",
        value=f"${kpi_salario:,.0f}",
        delta=f"${delta_salario:,.0f} vs mercado",
        delta_color="normal" if delta_salario >= 0 else "inverse"
    )

# =============================================================================
# 📊 KPIs ADICIONALES
# =============================================================================
st.subheader("📈 KPIs Adicionales de RRHH")

col4, col5, col6, col7 = st.columns(4)

# KPI 4: Total Empleados
with col4:
    st.metric(label="👥 Total Empleados", value=len(df_filtrado), delta_color="off")

# KPI 5: Top Performers
top_performers = len(df_filtrado[df_filtrado["PerformanceScore"] >= 90])
porcentaje_top = (top_performers / len(df_filtrado) * 100) if len(df_filtrado) > 0 else 0

with col5:
    st.metric(
        label="🏆 Top Performers",
        value=f"{top_performers} ({porcentaje_top:.0f}%)",
        delta="Desempeño ≥ 90",
        delta_color="off"
    )

# KPI 6: Brecha Salarial por Género
if "M" in df_filtrado["Gender"].values and "F" in df_filtrado["Gender"].values:
    salario_m = df_filtrado[df_filtrado["Gender"] == "M"]["Salary"].mean()
    salario_f = df_filtrado[df_filtrado["Gender"] == "F"]["Salary"].mean()
    brecha_salarial = ((salario_m - salario_f) / salario_m * 100) if salario_m > 0 else 0
else:
    brecha_salarial = 0

with col6:
    st.metric(
        label="⚖️ Brecha Salarial",
        value=f"{brecha_salarial:.1f}%",
        delta="M vs F",
        delta_color="inverse" if brecha_salarial > 10 else "off"
    )

# KPI 7: Empleados Nuevos
empleados_nuevos = len(df_filtrado[df_filtrado["YearsAtCompany"] < 2])
porcentaje_nuevos = (empleados_nuevos / len(df_filtrado) * 100) if len(df_filtrado) > 0 else 0

with col7:
    st.metric(
        label="🔄 Empleados Nuevos",
        value=f"{empleados_nuevos} ({porcentaje_nuevos:.0f}%)",
        delta="< 2 años",
        delta_color="off"
    )

# =============================================================================
# 📊 GRÁFICO PRINCIPAL: SALARIO VS ANTIGÜEDAD (PLOTLY)
# =============================================================================
st.subheader("🔍 Análisis: Salario vs Antigüedad por Departamento")

# Opciones de personalización
col_opt1, col_opt2 = st.columns(2)

with col_opt1:
    color_by = st.selectbox(
        "Colorear por:",
        options=["Department", "Gender", "Position"],
        index=0
    )

with col_opt2:
    show_trendline = st.checkbox("Mostrar línea de tendencia", value=True)

# Crear mapa de colores personalizado para Departamento
if color_by == "Department":
    color_discrete_map = DEPARTMENT_COLORS
else:
    color_discrete_map = None

# Crear gráfico de dispersión
fig_scatter = px.scatter(
    df_filtrado,
    x="YearsAtCompany",
    y="Salary",
    color=color_by,
    color_discrete_map=color_discrete_map,  # ✅ Paleta personalizada
    size="PerformanceScore",
    hover_data=["Name", "Position", "Age", "Gender"],
    title=f"💰 Salario vs Antigüedad (coloreado por {color_by})",
    labels={
        "YearsAtCompany": "📅 Años en la Empresa",
        "Salary": "💵 Salario ($)",
        "PerformanceScore": "⭐ Desempeño",
        color_by: "Categoría"
    },
    template="plotly_white",
    height=550
)

# Agregar línea de tendencia si está activado
if show_trendline and len(df_filtrado) > 2:
    fig_scatter.add_trace(
        px.scatter(df_filtrado, x="YearsAtCompany", y="Salary", trendline="ols").data[1]
    )

# Mejorar diseño del gráfico
fig_scatter.update_traces(
    marker=dict(line=dict(width=1, color='DarkSlateGray'), opacity=0.8),
    selector=dict(mode='markers')
)

# Actualizar layout
fig_scatter.update_layout(
    legend_title_text="📋 " + color_by,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    hovermode="closest"
)

# Mostrar en Streamlit
st.plotly_chart(fig_scatter, use_container_width=True)

# === INSIGHTS DEL GRÁFICO ===
with st.expander("💡 Interpretación del Gráfico"):
    st.markdown("""
    ### 🔍 Qué observar en este gráfico:
    
    | Elemento | Significado |
    |----------|-------------|
    | **Eje X** | Años que el empleado lleva en la empresa |
    | **Eje Y** | Salario anual en dólares |
    | **Colores** | Representan diferentes departamentos |
    | **Tamaño del punto** | Indica el nivel de desempeño (PerformanceScore) |
    | **Línea de tendencia** | Muestra la correlación general entre antigüedad y salario |
    
    ### 📊 Patrones clave:
    1. **Correlación positiva**: Generalmente, más antigüedad = mayor salario
    2. **Engineering**: Tiende a tener los salarios más altos (azul)
    3. **HR**: Incluye el salario más alto (Director - $105k)
    4. **Outliers**: Kevin Hill (Intern) - 1 año, $40k, desempeño 65
    """)

# =============================================================================
# 📊 GRÁFICOS ADICIONALES
# =============================================================================
st.subheader("📈 Visualizaciones Complementarias")

col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("💰 Salario Promedio por Departamento")
    salario_dept = df_filtrado.groupby("Department")["Salary"].mean().sort_values()
    
    # Crear gráfico de barras con colores personalizados
    fig_barras = px.bar(
        salario_dept.reset_index(),
        x="Department",
        y="Salary",
        color="Department",
        color_discrete_map=DEPARTMENT_COLORS,
        labels={"Department": "Departamento", "Salary": "Salario Promedio ($)"},
        template="plotly_white",
        height=400
    )
    fig_barras.update_layout(showlegend=False)
    st.plotly_chart(fig_barras, use_container_width=True)

with col_g2:
    st.subheader("⭐ Desempeño vs Años en Empresa")
    st.scatter_chart(
        df_filtrado[["YearsAtCompany", "PerformanceScore"]],
        x="YearsAtCompany",
        y="PerformanceScore"
    )

col_g3, col_g4 = st.columns(2)

with col_g3:
    st.subheader("👥 Empleados por Género")
    genero_count = df_filtrado["Gender"].value_counts()
    st.bar_chart(genero_count)

with col_g4:
    st.subheader("🎂 Distribución de Edades")
    age_bins = pd.cut(df_filtrado["Age"], bins=10)
    age_counts = age_bins.value_counts().sort_index()
    age_counts.index = age_counts.index.astype(str)
    st.bar_chart(age_counts)

# =============================================================================
# 📋 TABLA DE DATOS
# =============================================================================
with st.expander("📋 Ver Datos Completos", expanded=False):
    st.dataframe(df_filtrado, use_container_width=True)

# =============================================================================
# 💾 EXPORTAR DATOS
# =============================================================================
st.sidebar.markdown("---")
st.sidebar.subheader("💾 Exportar Datos")

if st.sidebar.button("Generar Archivo CSV"):
    csv = df_filtrado.to_csv(index=False, encoding='utf-8-sig')
    st.sidebar.download_button(
        label="⬇️ Descargar Datos Filtrados",
        data=csv,
        file_name="empleados_rrhh_filtrados.csv",
        mime="text/csv"
    )

# Exportar gráfico
if st.sidebar.button("Exportar Gráfico como PNG"):
    st.sidebar.info("📌 Para exportar el gráfico, usa el menú del gráfico (⋮ → Download plot as PNG)")

# =============================================================================
# 📊 RESUMEN POR DEPARTAMENTO

# =============================================================================
st.subheader("🏢 Resumen por Departamento")

resumen_dept = df_filtrado.groupby("Department").agg({
    "EmployeeID": "count",
    "Salary": ["mean", "min", "max"],
    "PerformanceScore": "mean",
    "YearsAtCompany": "mean"
}).round(2)

resumen_dept.columns = ["Empleados", "Salario Promedio", "Salario Mín", "Salario Máx", "Desempeño Prom.", "Años Prom."]
resumen_dept["Salario Promedio"] = resumen_dept["Salario Promedio"].apply(lambda x: f"${x:,.0f}")
resumen_dept["Salario Mín"] = resumen_dept["Salario Mín"].apply(lambda x: f"${x:,.0f}")
resumen_dept["Salario Máx"] = resumen_dept["Salario Máx"].apply(lambda x: f"${x:,.0f}")

st.dataframe(resumen_dept, use_container_width=True)

# =============================================================================
# PIE DE PÁGINA
# =============================================================================
st.markdown("---")
st.caption("📌 Dashboard RRHH | Creado con Streamlit + Plotly | Datos de empleados")