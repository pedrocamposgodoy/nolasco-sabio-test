import streamlit as st
import pandas as pd
import os
# Importamos tus estilos (asegúrate de que el archivo se llame nolasco_styles.py)
try:
    from nolasco_styles import inject_styles
except ImportError:
    def inject_styles(): st.warning("Archivo nolasco_styles.py no encontrado.")

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Nolasco Sabio - TEST", layout="wide", page_icon="🧠")
inject_styles()

# 2. FUNCIÓN PARA CARGAR TU CSV
def cargar_datos():
    ruta_csv = 'datos_simulados.csv'
    if os.path.exists(ruta_csv):
        # Cargamos el CSV que creaste en GitHub
        df = pd.read_csv(ruta_csv)
        return df
    else:
        # Datos de emergencia por si el CSV falla
        st.error(f"No se encuentra el archivo {ruta_csv}")
        return pd.DataFrame()

# 3. INTERFAZ PRINCIPAL
def main():
    st.markdown('<div class="nc-brand-header">Entorno de Pruebas: El Sabio</div>', unsafe_allow_html=True)
    
    # Cargamos los datos del CSV
    df = cargar_datos()

    if not df.empty:
        # --- EL SABIO PROACTIVO ---
        # Cogemos el primer hito del CSV para demostrar que la IA lo lee
        primer_inmueble = df.iloc[0]['Inmueble']
        proximo_hito = df.iloc[0]['Proximo_Hito']
        
        st.markdown(f'''
            <div class="nc-ai-bubble">
                <span style="font-weight:bold; color:#BC84EE;">💡 El Sabio dice:</span><br>
                Pedro, he revisado tu CSV. Veo que para el <b>{primer_inmueble}</b> 
                tienes pendiente: <i>{proximo_hito}</i>. ¿Quieres que preparemos la liquidez?
            </div>
        ''', unsafe_allow_html=True)

        # --- VISUALIZACIÓN DE DATOS ---
        st.markdown('<div class="nc-section-title">Datos detectados en el CSV</div>', unsafe_allow_html=True)
        
        # Mostramos los KPIs basados en el CSV
        col1, col2, col3 = st.columns(3)
        with col1:
            total_renta = df['Renta_Mensual'].sum()
            st.markdown(f'<div class="nc-kpi"><div class="nc-kpi__label">Renta Total</div><div class="nc-kpi__value">{total_renta} €</div></div>', unsafe_allow_html=True)
        with col2:
            num_activos = len(df)
            st.markdown(f'<div class="nc-kpi"><div class="nc-kpi__label">Inmuebles</div><div class="nc-kpi__value">{num_activos}</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="nc-kpi is-highlight"><div class="nc-kpi__label" style="color:white;">Fuente</div><div class="nc-kpi__value" style="color:white;">CSV OK</div></div>', unsafe_allow_html=True)

        st.write("")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Sube el archivo datos_simulados.csv a tu repositorio para ver los datos.")

if __name__ == "__main__":
    main()
