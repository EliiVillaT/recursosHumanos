Prompt 1: "Genera la estructura básica de una app Streamlit que tenga un título, una barra lateral y un área principal. Incluye la carga del dataframe desde una URL".
Respuesta IA: [Código proporcionado por la IA]
Ajuste Manual: la ia me genero uncodigo con st.histogram() la cual no existía en la librería por lo que se consulto a la IA y se realizo el ajuste con st.bar_chart()
Prompt 2: "genera la limpieza de los datos, deberia borrar empleados menor a 18 años y mayor a 65 "
Respuesta IA: [Código]
ajustes: se realiza no solo el rango de edad si no la ia elimino los salarios negativos, el conteo doble de empleados y los años negativos 
en conclusion los datos ya están limpios en cuanto a edad, pero es muy buena práctica tener el filtro por si en el futuro cargas datos con valores atípicos.

Prompt 3:¿Qué 3 KPIs serían relevantes para un dashboard de RRHH basado en columnas típicas de empleados? Genera el código Streamlit para mostrarlos usando st.metric
respuesta IA: [Código]
ajustes: la ia me mostro esquemas del desempeño Promedio, performanceScore que mide la productividad general de la fuerza laboral, la antigüedad Promedio que indica retención y lealtad de empleados y el salario Promedio que ayuda en planificación presupuestaria y competitividad, hubo inconvenientes con la libreria plopt


Prompt 4: Crea un gráfico de dispersión con Plotly Express donde el eje X sea la antigüedad y el eje Y el salario, coloreando por departamento. Intégralo en Streamlit
Respuesta IA:[Codigo]
ajustes: se ajusta el codigo debido a que los ejes que mostraba no era el que se pidio, se realizó la instalacion de la libreria con Conda


prompt 5: usar la barra lateral (st.sidebar) para agregar filtros que me permita filtrar la informacion por Departamento y por Rango de Salario.

respuesta IA: [Codigo]
ajustes: la respuesta del código no actualizaba los graficos por lo que se solicito a la ia la actualización de los mismos, estos realizan el ajuste en la parte inicial quedando la estructura del código de esta forma:
1. Configuración
2. Carga de datos
3. Limpieza de datos
4. filtros unificados
5. KPIs
6. Graficos
7. Tabla
8. Exporta
9. Resumen
10. Pie de pagina
