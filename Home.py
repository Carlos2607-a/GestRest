import pandas as pd
import base64
from io import BytesIO
from datetime import datetime
import streamlit as st
import altair as alt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from funciones import añadir_producto, to_excel, descargar_excel, seleccionar_productos, vista_previa, mostrar_carrito
from productos import restaurantes
import pickle
import pathlib as Path
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Configurar la página
st.set_page_config(
    page_title='Gestión de Restaurantes',
    layout='wide',
    page_icon='📊'
)

# Título
st.title('Bienvenido a GestRest')

# Cargar las credenciales desde el archivo YAML
with open('credenciales.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Inicializar el autenticador
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

# Iniciar sesión
authenticator.login()

# Verificar el estado de autenticación
if st.session_state["authentication_status"]:
    authenticator.logout()
    st.write(f'Bienvenido *{st.session_state["name"]}*')
    st.title('Contenido')
    with st.expander("Contenido Permitido", expanded=True):
        st.page_link("pages/Pedidos.py", disabled=False)
        if st.button("Volver al Menu Principal"):
            st.page_link("Home.py", disabled=False)
        st.page_link("pages/Soporte Tecnico.py", disabled=False)
        if st.button("Volver al Menu Principal"):
            st.page_link("Home.py", disabled=False)
        st.page_link("pages/Administración.py", disabled=True)
    

elif st.session_state["authentication_status"] is False:
    st.error('Usuario/contraseña incorrectos')
elif st.session_state["authentication_status"] is None:
    st.warning('Por favor, ingresa tu usuario y contraseña')

# Función para manejar el evento del botón de restablecimiento de contraseña
def handle_reset_password():
    try:
        if authenticator.reset_password(st.session_state["username"]):
            st.success('Contraseña modificada exitosamente')
    except Exception as e:
        st.error(e)

# Crear un botón para restablecer la contraseña
if st.button("Restablecer Contraseña"):
    handle_reset_password()

# Guardar las credenciales actualizadas en el archivo YAML
with open('credenciales.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)

