import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la página
st.set_page_config(page_title="Análisis de Empleados", layout="wide", page_icon="👥")

# Título principal
st.title("👥 Dashboard de Análisis de Empleados")

# =============================================================================
# CARGA DE DATOS
# =============================================================================
@st.cache_data
def load_data():
    return pd.read_csv("employees.csv")

df = load_data()
df_original = df.copy()  # Guardar copia original

# =============================================================================
# LIMPIEZA DE DATOS
# =============================================================================
st.sidebar.header("🧹 Limpieza de Datos")

# 1. Filtro por edad (18-65 años)
st.sidebar.subheader("Edad")
edad_min = st.sidebar.number_input("Edad mínima", min_value=0, max_value=100, value=18)
edad_max = st.sidebar.number_input("Edad máxima", min_value=0, max_value=100, value=65)
df = df[(df["Age"] >= edad_min) & (df["Age"] <= edad_max)]

# 2. Salarios positivos
df = df[df["Salary"] > 0]

# 3. Años en empresa no negativos
df = df[df["YearsAtCompany"] >= 0]

# 4. PerformanceScore en rango 0-100
df = df[(df["PerformanceScore"] >= 0) & (df["PerformanceScore"] <= 100)]

# 5. Eliminar duplicados por EmployeeID
df = df.drop_duplicates(subset=["EmployeeID"])

# 6. Estandarizar Género
df["Gender"] = df["Gender"].str.upper().str.strip()
df = df[df["Gender"].isin(["M", "F"])]

# 7. Manejar valores nulos
valores_nulos = df.isnull().sum().sum()
if valores_nulos > 0:
    st.sidebar.warning(f"⚠️ Se encontraron {valores_nulos} valores nulos")
    opcion_nulos = st.sidebar.selectbox(
        "¿Qué hacer con valores nulos?",
        ["Eliminar filas", "Rellenar con promedio", "Rellenar con 0"]
    )
    if opcion_nulos == "Eliminar filas":
        df = df.dropna()
    elif opcion_nulos == "Rellenar con promedio":
        df = df.fillna(df.mean(numeric_only=True))
    else:
        df = df.fillna(0)

# 8. Detectar valores atípicos en Salary (opcional)
st.sidebar.subheader("🔍 Valores Atípicos")
detectar_outliers = st.sidebar.checkbox("Detectar salarios atípicos", value=False)
if detectar_outliers:
    Q1 = df["Salary"].quantile(0.25)
    Q3 = df["Salary"].quantile(0.75)
    IQR = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    outliers = df[(df["Salary"] < limite_inferior) | (df["Salary"] > limite_superior)]
    if len(outliers) > 0:
        st.sidebar.warning(f"⚠️ {len(outliers)} salarios atípicos detectados")
        if st.sidebar.button("Eliminar outliers"):
            df = df[(df["Salary"] >= limite_inferior) & (df["Salary"] <= limite_superior)]
            st.sidebar.success("✅ Outliers eliminados")

# Resumen de limpieza
registros_eliminados = len(df_original) - len(df)
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Resumen de Limpieza")
st.sidebar.write(f"**Total original:** {len(df_original)}")
st.sidebar.write(f"**Después de limpieza:** {len(df)}")
if registros_eliminados > 0:
    st.sidebar.warning(f"⚠️ {registros_eliminados} registros eliminados")
else:
    st.sidebar.success("✅ Todos los datos son válidos")

# =============================================================================
# FILTROS DE ANÁLISIS
# =============================================================================
st.sidebar.header("🔍 Filtros de Análisis")

# Filtro por Departamento
departamentos = st.sidebar.multiselect(
    "Selecciona Departamento(s)",
    options=df["Department"].unique(),
    default=df["Department"].unique()
)

# Filtro por Rango de Salario
min_salario, max_salario = int(df["Salary"].min()), int(df["Salary"].max())
rango_salario = st.sidebar.slider(
    "Rango de Salario ($)",
    min_salario, max_salario,
    (min_salario, max_salario)
)

# Filtro por Género
generos = st.sidebar.multiselect(
    "Selecciona Género",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

# Filtro por Rango de Años en Empresa
min_anios, max_anios = int(df["YearsAtCompany"].min()), int(df["YearsAtCompany"].max())
rango_anios = st.sidebar.slider(
    "Años en la Empresa",
    min_anios, max_anios,
    (min_anios, max_anios)
)

# Aplicar filtros de análisis
df_filtrado = df[
    (df["Department"].isin(departamentos)) &
    (df["Salary"] >= rango_salario[0]) &
    (df["Salary"] <= rango_salario[1]) &
    (df["Gender"].isin(generos)) &
    (df["YearsAtCompany"] >= rango_anios[0]) &
    (df["YearsAtCompany"] <= rango_anios[1])
]

# =============================================================================
# PANEL DE MÉTRICAS
# =============================================================================
st.subheader("📈 Métricas Principales")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Empleados", len(df_filtrado))
col2.metric("Salario Promedio", f"${df_filtrado['Salary'].mean():,.0f}")
col3.metric("Desempeño Promedio", f"{df_filtrado['PerformanceScore'].mean():.1f}")
col4.metric("Años Promedio en Empresa", f"{df_filtrado['YearsAtCompany'].mean():.1f}")

# =============================================================================
# TABLA DE DATOS
# =============================================================================
with st.expander("📋 Ver Datos Completos", expanded=False):
    st.dataframe(df_filtrado, use_container_width=True)

# =============================================================================
# GRÁFICOS - FILA 1
# =============================================================================
st.subheader("📊 Visualizaciones")
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("💰 Salario Promedio por Departamento")
    salario_dept = df_filtrado.groupby("Department")["Salary"].mean().sort_values()
    st.bar_chart(salario_dept)

with col_g2:
    st.subheader("⭐ Desempeño vs Años en la Empresa")
    st.scatter_chart(
        df_filtrado[["YearsAtCompany", "PerformanceScore"]],
        x="YearsAtCompany",
        y="PerformanceScore"
    )

# =============================================================================
# GRÁFICOS - FILA 2
# =============================================================================
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
# GRÁFICOS - FILA 3 (Análisis Adicional)
# =============================================================================
col_g5, col_g6 = st.columns(2)

with col_g5:
    st.subheader("🏢 Empleados por Departamento")
    dept_count = df_filtrado["Department"].value_counts()
    st.bar_chart(dept_count)

with col_g6:
    st.subheader("💵 Salario vs Desempeño")
    st.scatter_chart(
        df_filtrado[["Salary", "PerformanceScore"]],
        x="Salary",
        y="PerformanceScore"
    )

# =============================================================================
# EXPORTAR DATOS
# =============================================================================
st.sidebar.markdown("---")
st.sidebar.subheader("💾 Exportar Datos")
if st.sidebar.button("Generar Archivo CSV"):
    csv = df_filtrado.to_csv(index=False, encoding='utf-8-sig')
    st.sidebar.download_button(
        label="⬇️ Descargar Datos Filtrados",
        data=csv,
        file_name="empleados_limpios_filtrados.csv",
        mime="text/csv"
    )

# =============================================================================
# PIE DE PÁGINA
# =============================================================================
st.markdown("---")
st.caption("📌 Dashboard creado con Streamlit | Datos de empleados RRHH")