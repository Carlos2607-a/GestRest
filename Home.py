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
    page_title='GestRest',
    layout='wide',
    page_icon='📊'
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.image("_ba1584f3-7062-4fef-8d34-ed1437d99ad3-removebg-preview.png", width=300)  # Ajusta el ancho según tus necesidades.
# Título
st.title('Welcome to GestRest')

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
    st.title('Funciones')
    with st.expander("Contenido Permitido", expanded=True):
        st.page_link("pages/Pedidos.py", disabled=False)
        st.page_link("pages/Soporte Tecnico.py", disabled=False)
        st.page_link("pages/Administración.py", disabled=True) 

elif st.session_state["authentication_status"] is False:
    st.error('Usuario/contraseña incorrectos')
elif st.session_state["authentication_status"] is None:
    st.warning('Por favor, ingresa tu usuario y contraseña')

# Guardar las credenciales actualizadas en el archivo YAML
with open('credenciales.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)

