# --- BLOQUE DE CHAT CON AUTODIAGNÓSTICO ---
if prompt := st.chat_input("Pregunta al Sabio..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # COMPROBACIÓN TÉCNICA
        if "OPENAI_API_KEY" not in st.secrets:
            st.error("❌ ERROR: No encuentro la clave en 'Secrets' de Streamlit.")
            full_response = "Por favor, configura la clave en los ajustes de Streamlit Cloud."
        else:
            try:
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                # Aquí la IA ya leerá TODO el CSV
                contexto_datos = df.to_string()
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": f"Eres el Sabio Patrimonial. Datos reales: {contexto_datos}"},
                        {"role": "user", "content": prompt}
                    ]
                )
                full_response = response.choices[0].message.content
                st.success("✅ Conexión con ChatGPT exitosa")
            except Exception as e:
                st.error(f"❌ ERROR DE API: {str(e)}")
                full_response = "Tengo la clave, pero OpenAI me da error (posiblemente falta de saldo)."

        st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
