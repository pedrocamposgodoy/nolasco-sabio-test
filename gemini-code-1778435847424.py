import streamlit as st
import pandas as pd
from openai import OpenAI

# ==========================================
# 1. CONFIGURACIÓN Y ESTILOS BÁSICOS
# ==========================================
st.set_page_config(page_title="Boceto - El Sabio", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    .sabio-bubble {
        background-color: #F8FAFC;
        border-left: 5px solid #BC84EE;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 El Sabio Patrimonial (Entorno de Prueba)")
st.write("Prueba de conexión de IA con datos financieros reales.")

# ==========================================
# 2. SIMULACIÓN DE TUS DATOS (Contexto Veraz)
# ==========================================
# Aquí simulamos lo que tu app principal le enviará al Sabio
@st.cache_data
def cargar_datos_demo():
    datos = {
        "Activo": ["Piso Centro", "Local Comercial", "Garaje"],
        "Renta_Mensual": [850, 1200, 100],
        "Prox_Impuesto": ["IBI (Oct) - 400€", "Seguro (Nov) - 300€", "Ninguno"],
        "Liquidez_Actual": [2500, 4000, 500]
    }
    return pd.DataFrame(datos)

df_cartera = cargar_datos_demo()

with st.expander("📊 Ver los datos que está leyendo El Sabio", expanded=False):
    st.dataframe(df_cartera, use_container_width=True)

# ==========================================
# 3. CONEXIÓN A LA IA Y MEMORIA DEL CHAT
# ==========================================
# Tu clave API debe ir aquí (Cámbiala por la tuya en tu ordenador)
# st.secrets es la forma segura de Streamlit, pero para probar puedes pegarla directamente (¡no la subas a internet!)
API_KEY = "PEGA_TU_CLAVE_AQUI_PARA_PROBAR" 

try:
    client = OpenAI(api_key=API_KEY)
except:
    st.warning("⚠️ Falta la clave API para conectar con el cerebro de la IA.")

# Memoria del chat (para que recuerde la conversación)
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Mostrar historial
for msg in st.session_state.mensajes:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    else:
        st.markdown(f'<div class="sabio-bubble"><b>💡 El Sabio:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

# ==========================================
# 4. EL CHATBOT (Interacción)
# ==========================================
# st.chat_input es la caja de texto nativa de Streamlit
prompt_usuario = st.chat_input("Pregúntale al Sabio sobre tus inmuebles...")

if prompt_usuario:
    # Mostramos lo que escribe el usuario
    with st.chat_message("user"):
        st.write(prompt_usuario)
    st.session_state.mensajes.append({"role": "user", "content": prompt_usuario})

    # Construimos el "Cerebro" (System Prompt + Datos Veraces)
    # Convertimos la tabla a texto para que la IA la entienda
    datos_texto = df_cartera.to_string()
    
    instrucciones_sabio = f"""
    Eres 'El Sabio Patrimonial', un consultor proactivo para el propietario Nolasco.
    Responde SIEMPRE basándote en esta tabla de datos reales de su cartera:
    {datos_texto}
    
    Reglas:
    1. Si pregunta por IBI o liquidez, usa los datos exactos de la tabla.
    2. Da respuestas muy cortas (máximo 3 frases).
    3. Tono amable, profesional y directo.
    4. NO inventes datos. Si no está en la tabla, dile que no tienes esa información.
    """

    # Llamamos a la API
    if API_KEY != "PEGA_TU_CLAVE_AQUI_PARA_PROBAR":
        with st.spinner("El Sabio está analizando tus números..."):
            respuesta_ia = client.chat.completions.create(
                model="gpt-4o-mini", # O el modelo que estés usando
                messages=[
                    {"role": "system", "content": instrucciones_sabio},
                    {"role": "user", "content": prompt_usuario}
                ]
            )
            
            texto_respuesta = respuesta_ia.choices[0].message.content
            
            # Mostramos y guardamos la respuesta
            st.markdown(f'<div class="sabio-bubble"><b>💡 El Sabio:</b><br>{texto_respuesta}</div>', unsafe_allow_html=True)
            st.session_state.mensajes.append({"role": "assistant", "content": texto_respuesta})