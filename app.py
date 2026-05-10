import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# 1. ESTILOS Y CONFIGURACIÓN
try:
    from nolasco_styles import inject_styles
except ImportError:
    def inject_styles(): st.write("Cargando estilos base...")

st.set_page_config(page_title="Nolasco Sabio - CHAT TEST", layout="wide")
inject_styles()

# 2. CARGA DE DATOS (Tu "Información Veraz")
def cargar_datos():
    if os.path.exists('datos_simulados.csv'):
        return pd.read_csv('datos_simulados.csv')
    return pd.DataFrame()

df = cargar_datos()

# 3. INTERFAZ VISUAL (La lista que ya tenías)
st.markdown('<div class="nc-brand-header">El Sabio Patrimonial</div>', unsafe_allow_html=True)
st.dataframe(df, use_container_width=True)

# ================================================================
# 4. EL CHATBOT (La ventanita interactiva)
# ================================================================
st.markdown("---")
st.subheader("💬 Consulta al Sabio sobre tus datos")

# Inicializar el historial del chat para que no se borre al escribir
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# CAJA DE ENTRADA (La ventanita de abajo)
if prompt := st.chat_input("Escribe tu pregunta aquí..."):
    # 1. Mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generar respuesta de la IA (El Cerebro)
    with st.chat_message("assistant"):
        # Le pasamos los datos del CSV como "contexto"
        contexto_datos = df.to_string()
        
        # OJO: Aquí es donde mañana el programador conectará la API real
        # Por ahora, simulamos la respuesta si no hay clave API
        try:
            # Si tienes la clave en Secrets de Streamlit, esto funcionará:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"Eres el Sabio de Nolasco Capital. Responde usando estos datos: {contexto_datos}"},
                    {"role": "user", "content": prompt}
                ]
            )
            full_response = response.choices[0].message.content
        except:
            # Respuesta "Mock" por si aún no has configurado la clave API
            full_response = f"Simulación: Veo que preguntas por '{prompt}'. Según el CSV, el Piso en Recogidas alquilado por 850€ es tu activo principal."

        st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
