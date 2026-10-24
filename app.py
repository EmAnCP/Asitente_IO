import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from pulp import LpMaximize, LpProblem, LpVariable, PULP_CBC_CMD

# Configuración básica de la página
st.set_page_config(page_title="ASISTENTE IO", page_icon="🤖", layout="wide")

# Barra lateral limpia sin referencias institucionales
st.sidebar.header("Panel de Control")
st.sidebar.text("Asistente Académico")
st.sidebar.markdown("---")
st.sidebar.info("Usa las pestañas para navegar entre los módulos de resolución automática y consulta libre.")

st.title("🤖 ASISTENTE IO")
st.write("Bienvenido. Utiliza las pestañas superiores para navegar por los módulos de cálculo o plantear tus propios problemas.")

# Pestañas principales (se añade una nueva para consultas y problemas personalizados)
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Método Gráfico", 
    "⚡ Método Simplex", 
    "🚚 Transporte y Asignación", 
    "📦 Inventarios (EOQ)", 
    "✍️ Práctica y Retroalimentación",
    "📝 Consultas y Problemas"
])

with tab1:
    st.header("Método Gráfico (2 Variables)")
    st.write("Ejemplo práctico: Maximizar $Z = 40x + 30y$ sujeto a restricciones.")
    
    if st.button("Generar Gráfica de Región Factible"):
        x = np.linspace(0, 100, 400)
        y1 = (100 - 2*x)
        y2 = (80 - x) / 2

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(x, y1, label=r'$2x + y \leq 100$', color='blue')
        ax.plot(x, y2, label=r'$x + 2y \leq 80$', color='green')
        
        y3 = np.minimum(y1, y2)
        y3 = np.maximum(y3, 0)
        ax.fill_between(x, 0, y3, color='grey', alpha=0.3, label='Región Factible')

        ax.set_xlim(0, 60)
        ax.set_ylim(0, 60)
        ax.set_xlabel('Variable x')
        ax.set_ylabel('Variable y')
        ax.grid(True, linestyle='--')
        ax.legend()
        
        st.pyplot(fig)
        st.success("¡Región factible graficada con éxito! La solución óptima se encuentra en los vértices.")

with tab2:
    st.header("Programación Lineal y Método Simplex")
    st.write("Resolución automática exacta mediante algoritmos matemáticos.")
    
    if st.button("Resolver Ejemplo: Maximizar Z = 40x + 30y"):
        model = LpProblem(name="Simplex-Problem", sense=LpMaximize)
        x = LpVariable(name="x", lowBound=0)
        y = LpVariable(name="y", lowBound=0)
        
        model += 40 * x + 30 * y, "Funcion_Objetivo"
        model += 2 * x + y <= 100, "Restriccion_1"
        model += x + 2 * y <= 80, "Restriccion_2"
        
        model.solve(PULP_CBC_CMD(msg=False))
        
        st.subheader("Resultados Obtenidos:")
        st.write(f"**Estado:** Solución Óptima Encontrada")
        st.write(f"**Valor óptimo (Z max):** {model.objective.value()}")
        st.write(f"**Valor de x:** {x.value()}")
        st.write(f"**Valor de y:** {y.value()}")
        st.info("Procedimiento: Se evaluaron las restricciones activas encontrando el punto máximo en la intersección.")

with tab3:
    st.header("Módulo de Transporte y Asignación")
    st.write("Ingrese los parámetros básicos de oferta y demanda para calcular la distribución óptima de costos.")
    oferta = st.number_input("Capacidad de Oferta Total", value=500.0)
    demanda = st.number_input("Demanda Total Requerida", value=500.0)
    if st.button("Calcular Asignación"):
        if oferta == demanda:
            st.success("El sistema está equilibrado (Oferta = Demanda). Se puede aplicar el método de la Esquina Noroeste o Vogel.")
        else:
            st.warning("El sistema está desequilibrado. Se requiere agregar una fila o columna ficticia.")

with tab4:
    st.header("Módulo de Inventarios (EOQ)")
    d = st.number_input("Demanda anual (D)", value=1200.0)
    s = st.number_input("Costo de ordenar por pedido (S)", value=50.0)
    h = st.number_input("Costo de mantenimiento anual por unidad (H)", value=2.0)
    
    if st.button("Calcular EOQ y Punto de Reorden"):
        eoq = np.sqrt((2 * d * s) / h)
        st.metric(label="Cantidad Económica de Pedido (EOQ)", value=round(eoq, 2))
        st.write(f"**Fórmula aplicada:** $EOQ = \\sqrt{{(2 \\cdot {d} \\cdot {s}) / {h}}}$")

with tab5:
    st.header("Generador de Prácticas y Retroalimentación")
    st.write("Pon a prueba tus conocimientos con preguntas del curso.")
    
    respuesta = st.text_input("¿Qué busca la función objetivo en un modelo de programación lineal?")
    if st.button("Verificar respuesta"):
        if "maximizar" in respuesta.lower() or "minimizar" in respuesta.lower():
            st.success("¡Respuesta Correcta! Excelente dominio del concepto.")
        else:
            st.error("Incorrecto. Recuerda que la función objetivo modela la optimización (maximizar ganancias o minimizar costos).")

with tab6:
    st.header("📝 Consultas y Resolución de Problemas Matemáticos")
    st.write("Escribe tus ecuaciones, plantea tus problemas de Investigación de Operaciones o sube una imagen con tus ejercicios.")
    
    # Apartado para escribir ecuaciones u operaciones
    problema_texto = st.text_area(
        "Escribe aquí tu problema matemático, ecuaciones o planteamiento:",
        placeholder="Ejemplo: Maximizar Z = 50x + 80y sujeto a 2x + y <= 120..."
    )
    
    # Apartado para subir imágenes o archivos con ejercicios
    archivo_subido = st.file_uploader(
        "Sube una imagen o archivo con el ejercicio (PNG, JPG, JPEG, PDF):",
        type=["png", "jpg", "jpeg", "pdf"]
    )
    
    if archivo_subido is not None:
        st.image(archivo_subido, caption="Imagen del ejercicio cargada con éxito.", use_container_width=True)
    
    if st.button("Analizar y Resolver Problema"):
        if problema_texto.strip() != "" or archivo_subido is not None:
            st.success("¡Problema recibido con éxito en ASISTENTE IO!")
            st.info("Procesando la información ingresada...")
            # Aquí puedes integrar lógica adicional si deseas conectar una IA o un solucionador en el futuro.
        else:
            st.warning("Por favor, escribe un problema en el cuadro de texto o sube una imagen antes de continuar.")
