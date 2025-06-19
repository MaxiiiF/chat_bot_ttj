import streamlit as st
import groq 

# Tener nuestro modelo
MODELOS = ["llama3-8b-8192", "llama3-70b-8192","mixtral-8x7b-32768"]





# Configurar la pagina
def configurar_pagina():
    st.set_page_config(page_title="MI PRIMER TRABAJO EN PYTHON", page_icon="🔥")
    st.title("BIENVENIDOS A CHATBOT")
 
# Mostrar el sidebar con los modelos
def mostrar_sidebar():
    st.sidebar.title("elige tu modelo de ia favorito")
    modelos= st.sidebar.selectbox("¿Cual prefieres?", MODELOS, index=0 )
    st.write(f"**Elegiste este Modelo** : {modelos}")
    return modelos

# Un cliente groq
def crear_cliente_groq ():
    Groq_api_key = st.secrets["Clave_API"] 
    return groq.Groq (api_key=Groq_api_key)

# Inicialiar el estado de los mensajes 
def inicializacion_estado_chat ():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append ({"role":rol, "content":contenido, "avatar":avatar })

def obtener_mensaje_usuario ():
    return st.chat_input ("Enviando...")

def area_chat ():
    contenedorDelChat = st.container(height=400, border=True)
    # Abrimos el contenedor del chat y mosstramos el historial.
    with contenedorDelChat:
        mostrar_historial_chat



def agregar_mensaje_al_historial(role, content):
    st.session_state.mensajes.append({"role":role, "content":content})

def mostrar_mensaje(role, content):
    with st.chat_message(role):
        st.markdown (content)

def mostrar_historial_chat ():
    for mensaje in st.session_state.mensajes:
        with st.chat_message (mensaje["role"]):
            st.markdown(mensaje["content"])            

def obtener_respuesta_modelo(cliente, modelo, mensajes):
    respuesta = cliente.chat.completions.create(
        model= modelo,
        messages= mensajes,
        stream = False
    )
    return respuesta.choices[0].message.content



#flujo de la app
def ejecutarChat():
    configurar_pagina()
    modelo = mostrar_sidebar()
    cliente= crear_cliente_groq()
    print(modelo)
    if cliente is None:
        st.error ("NO SE PUDO CONECTAR, REVISAR API KEY")
        return
    inicializacion_estado_chat()
    mostrar_historial_chat()

    mensajes_usuario =obtener_mensaje_usuario()
    print (mensajes_usuario)
    if mensajes_usuario:
        agregar_mensaje_al_historial("user",mensajes_usuario)
        mostrar_mensaje("user",mensajes_usuario)

        mensaje_modelo= obtener_respuesta_modelo(cliente, modelo, st.session_state.mensajes)

        agregar_mensaje_al_historial("assistant", mensaje_modelo)
        mostrar_mensaje ("assistant", mensaje_modelo)


if __name__ == "__main__": 
    ejecutarChat()

