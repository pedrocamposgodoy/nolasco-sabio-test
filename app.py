import streamlit as st
import pandas as pd
import os

# Importamos tus estilos (asegúrate de que el archivo se llame nolasco_styles.py en GitHub)
try:
    from nolasco_styles import inject_styles
except ImportError:
    def inject_styles(): 
        st.warning("Archivo nolasco_styles.py no encontrado. Asegúrate de que esté en el repositorio.")

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Nolasco Sabio - TEST", layout="wide", page_icon="🧠")

# Aplicamos el CSS de Nolasco
inject_styles()

# 2. FUNCIÓN PARA CARGAR TU CSV
def cargar_datos():
    ruta_csv = 'datos_simulados.csv'
    if os.path.exists(ruta_csv):
        # Cargamos el CSV que creaste en GitHub
        df = pd.read_csv(ruta_csv)
        return df
    else:
        # Error si el archivo no existe en el repositorio
        st.error(f"No se encuentra el archivo {ruta_csv} en el repositorio.")
        return pd.DataFrame()

# 3. INTERFAZ PRINCIPAL
def main():
    st.markdown('<div class="nc-brand-header">Entorno de Pruebas: El Sabio</div>', unsafe_allow_html=True)
    
    # Cargamos los datos del CSV
    df = cargar_datos()

    if not df.empty:
        # --- EL SABIO PROACTIVO (Lectura de datos veraces) ---
        # Cogemos datos de la primera fila para demostrar que la IA "lee" el archivo
        primer_inmueble = df.iloc[0]['Inmueble']
        proximo_hito = df.iloc[0]['Proximo_Hito']
        renta_mensual = df.iloc[0]['Renta_Mensual']
        
        st.markdown(f'''
            <div class="nc-ai-bubble">
                <span style="font-weight:bold; color:#BC84EE;">💡 El Sabio dice:</span><br>
                Pedro, he analizado tu archivo <b>datos_simulados.csv</b>. 
                Para tu activo <b>{primer_inmueble}</b>, que genera <b>{renta_mensual}€</b> al mes, 
                tienes este hito próximo: <i>{proximo_hito}</i>. 
                ¿Quieres que recalculemos el flujo de caja?
            </div>
        ''', unsafe_allow_html=True)

        # --- VISUALIZACIÓN DE TABLAS Y KPIs ---
        st.markdown('<div class="nc-section-title">Análisis de la Cartera (Datos CSV)</div>', unsafe_allow_html=True)
        
        # Mostramos los KPIs basados en el CSV
        col1, col2, col3 = st.columns(3)
        with col1:
            total_renta = df['Renta_Mensual'].sum()
            st.markdown(f'''
                <div class="nc-kpi">
                    <div class="nc-kpi__label">Renta Total Mensual</div>
                    <div class="nc-kpi__value">{total_renta:,.0f} €</div>
                </div>
            ''', unsafe_allow_html=True)
        with col2:
            num_activos = len(df)
            st.markdown(f'''
                <div class="nc-kpi">
                    <div class="nc-kpi__label">Activos en Cartera</div>
                    <div class="nc-kpi__value">{num_activos}</div>
                </div>
            ''', unsafe_allow_html=True)
        with col3:
            st.markdown(f'''
                <div class="nc-kpi is-highlight">
                    <div class="nc-kpi__label" style="color:white;">Estado Veracidad</div>
                    <div class="nc-kpi__value" style="color:white;">CSV OK</div>
                </div>
            ''', unsafe_allow_html=True)

        st.write("")
        # Mostramos la tabla completa para verificar
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Esperando a que subas 'datos_simulados.csv' al repositorio para empezar el análisis.")

if __name__ == "__main__":
    main()
