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



st.set_page_config(
    page_title='Gestión de Restaurantes',
    layout='wide',
    page_icon= '📊')
st.title('Bienvenido GestRest')

with open('credenciales.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

authenticator.login()


if st.session_state["authentication_status"]:
    authenticator.logout()
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

# Función para manejar el evento del botón de reinicio de contraseña
def handle_reset_password():
    try:
        if authenticator.reset_password(st.session_state["username"]):
            st.success('Contraseña modificada exitosamente')
    except Exception as e:
        st.error(e)

# Crear un botón desplegable para reiniciar la contraseña
if st.button("Restablecer Contraseña"):
    handle_reset_password()


with open('credenciales.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)
