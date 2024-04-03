import pandas as pd
import streamlit as st
from io import BytesIO
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os


def añadir_producto(producto, cantidad, tipo, unidad):
    # Comprueba si 'pedidos' existe en st.session_state y si no, lo inicializa con un DataFrame vacío
    if 'pedidos' not in st.session_state:
        st.session_state['pedidos'] = pd.DataFrame(columns=['Producto', 'Cantidad', 'Tipo', 'Unidad'])

    # Comprueba si el producto ya existe en 'pedidos'
    if 'Producto' in st.session_state['pedidos'].columns and producto in st.session_state['pedidos']['Producto'].values:
        indice = st.session_state['pedidos'][st.session_state['pedidos']['Producto'] == producto].index[0]
        st.session_state['pedidos'].at[indice, 'Cantidad'] = cantidad  # Establece la cantidad directamente
    else:
        # Si el producto no existe en 'pedidos', añade una nueva fila
        nuevo_pedido = pd.DataFrame({'Producto': [producto], 'Cantidad': [cantidad], 'Tipo': [tipo], 'Unidad': [unidad]})
        st.session_state['pedidos'] = pd.concat([st.session_state['pedidos'], nuevo_pedido], ignore_index=True)

def seleccionar_productos(categoria, productos):
    st.subheader(categoria)
    productos_procesados = set()
    if categoria in ['Alcohol', 'Vinos']:
        tipo_alcohol = st.selectbox(f'Selecciona un tipo de {categoria}', list(productos[categoria].keys()))
        # Crea dos columnas
        col1, col2 = st.columns(2)
        for i, item in enumerate(productos[categoria][tipo_alcohol]):
            if item not in productos_procesados:
                # Asigna los widgets a las columnas
                if i % 2 == 0:
                    col = col1
                else:
                    col = col2
                # Verifica si el widget de entrada ya está en el estado de la sesión
                key = f"{categoria}_{tipo_alcohol}_{item}"
                if key not in st.session_state:
                    # Si no está, inicializa el widget de entrada en el estado de la sesión
                    st.session_state[key] = 0

                # Crea el widget de entrada usando el valor en el estado de la sesión
                cantidad = col.number_input(f'{item}', min_value=0, step=1, value=st.session_state[key], key=key)

                # Actualiza el valor en el estado de la sesión cada vez que el widget de entrada cambia
                if cantidad != st.session_state[key]:
                    st.session_state[key] = cantidad

                if cantidad > 0:
                    unidad = 'Botellas' if categoria == 'Alcohol' else 'Cajas'
                    añadir_producto(item, cantidad, tipo_alcohol, unidad)
                productos_procesados.add(item)
    else:
        # Similar a lo anterior, pero para la otra categoría
        col1, col2 = st.columns(2)
        for i, item in enumerate(productos[categoria]):
            if item not in productos_procesados:
                if i % 2 == 0:
                    col = col1
                else:
                    col = col2
                # Similar a lo anterior, mantiene el estado del widget de entrada
                key = f"{categoria}_{item}"
                if key not in st.session_state:
                    st.session_state[key] = 0

                cantidad = col.number_input(f'{item}', min_value=0, step=1, value=st.session_state[key], key=key)

                if cantidad != st.session_state[key]:
                    st.session_state[key] = cantidad

                if cantidad > 0:
                    unidad = 'Barriles' if categoria == 'Barriles' else 'Cajas'
                    añadir_producto(item, cantidad, categoria, unidad)
                productos_procesados.add(item)



def to_excel(df, template_path, output_path, nombre_del_restaurante):
    # Escribe el DataFrame a un archivo Excel temporal
    df.to_excel('temp.xlsx', index=False)

    # Lee la plantilla y el archivo Excel temporal
    template_df = pd.read_excel(template_path)
    temp_df = pd.read_excel('temp.xlsx')

    # Comprueba si las columnas son iguales
    st.text("Las columnas son iguales: " + str(temp_df.columns.equals(template_df.columns)))

    # Encuentra las columnas en el DataFrame que no están en la plantilla
    diff_df = set(temp_df.columns) - set(template_df.columns)
    st.text("Columnas en el DataFrame que no están en la plantilla: " + str(diff_df))

    # Encuentra las columnas en la plantilla que no están en el DataFrame
    diff_template = set(template_df.columns) - set(temp_df.columns)
    st.text("Columnas en la plantilla que no están en el DataFrame: " + str(diff_template))

    # Rellena el DataFrame de la plantilla con los datos del archivo Excel temporal
    for col in temp_df.columns:
        if col in template_df.columns:
            template_df[col] = temp_df[col]

    # Escribe el DataFrame de la plantilla a tu archivo de salida
    template_df.to_excel(output_path, index=False)
    # Escribe el DataFrame en un nuevo archivo de Excel
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        template_df.to_excel(writer, index=False)  # Deja una fila en blanco en la parte superior para la fecha y el nombre del restaurante

        # Obtén la hoja de trabajo de xlsxwriter
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']

        # Crea un formato con bordes y texto centrado
        bordered_format = workbook.add_format({'border':1, 'align':'center'})

        # Agrega la fecha actual y el nombre del restaurante a las celdas
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        worksheet.write('D3', fecha_actual, bordered_format)

    # Devuelve los datos del archivo de Excel como bytes
    with open(output_path, 'rb') as f:
        return f.read()

def descargar_excel(df, nombre_archivo, nombre_del_restaurante):
    st.download_button(
        label="Descargar Excel",
        data=to_excel(df, "plantilla/plantilla.xlsx", nombre_archivo, nombre_del_restaurante),
        file_name=nombre_archivo,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


def vista_previa(df):
    if st.button('Vista Previa'):
        st.dataframe(df)

def mostrar_carrito(pedidos):
    # Crea una lista de productos en el carrito
    productos_en_carrito = pedidos['Producto'].tolist()
        
    # Crea un multiselect con los productos en el carrito
    productos_seleccionados = st.multiselect("Elimina Producto Carrito", productos_en_carrito)
        
    for producto in productos_seleccionados:
        if st.button(f"Eliminar {producto}"):
            indice = pedidos[pedidos['Producto'] == producto].index[0]
            pedidos.drop(indice, inplace=True)
            pedidos.reset_index(drop=True, inplace=True)


