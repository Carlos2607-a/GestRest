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
import pickle
import pathlib as Path
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from funciones import añadir_producto, to_excel, descargar_excel, seleccionar_productos, vista_previa, mostrar_carrito
from productos import restaurantes

# Configurar la página
st.set_page_config(
    page_title='GestRest',
    layout='wide',
    page_icon='📊'
)

# Ocultar elementos de Streamlit
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.image("_ba1584f3-7062-4fef-8d34-ed1437d99ad3-removebg-preview.png", width=300)
st.title('Welcome to GestRest')

# Cargar credenciales desde el archivo YAML
with open('credenciales.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Aquí ya no se necesita la autenticación con contraseña
# Suponiendo que no es necesario verificar el login, podemos saltarnos el paso de autenticación
# Pero si deseas un login automático con un usuario predefinido, solo debes asignar el valor deseado
# al nombre del usuario directamente, por ejemplo:

# Asignamos un nombre de usuario fijo para el login automático
st.session_state["authentication_status"] = True
st.session_state["name"] = "Usuario Automático"

# Mostrar mensaje de bienvenida
if st.session_state["authentication_status"]:
    st.write(f'Bienvenido *{st.session_state["name"]}*')
    st.title('Funciones')
    with st.expander("Contenido Permitido", expanded=True):
        st.page_link("pages/Pedidos.py", disabled=False)
        st.page_link("pages/Soporte Tecnico.py", disabled=False)
        st.page_link("pages/Administración.py", disabled=True)
else:
    st.warning('Autenticación fallida')

# Guardar credenciales actualizadas solo si cambian
if 'credentials' in config:
    with open('credenciales.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
