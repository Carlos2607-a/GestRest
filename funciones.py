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



def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, startrow=2)  # Deja dos filas en blanco en la parte superior para el título y la fecha

        # Obtén la hoja de trabajo de xlsxwriter
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']

        # Crea un formato para el título
        title_format = workbook.add_format({'font_size': 26, 'bg_color': 'black', 'font_color': 'white'})

        # Escribe el título
        worksheet.write('A1', 'Solicitud de Productos', title_format)

        # Aplica el formato de título a las celdas B1 a D1
        for col in range(1, 5):  # Las columnas en xlsxwriter comienzan en 0, por lo que 1 es la columna B y 4 es la columna E
            worksheet.write(0, col, '', title_format)  # La fila 0 es la fila 1 en Excel

        # Crea un formato con bordes y texto centrado
        bordered_format = workbook.add_format({'border':1, 'align':'center'})

        # Aplica el formato a las celdas con información
        for row_num, row_data in enumerate(df.values):
            for col_num, cell_data in enumerate(row_data):
                # Solo aplicamos el formato si la celda contiene datos
                if cell_data:
                    worksheet.write(row_num+3, col_num, cell_data, bordered_format)

        # Establece el ancho de las columnas
        worksheet.set_column('A:A', 60) 
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 40)

        # Agrega la fecha actual a una celda
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        worksheet.write('D1', 'Fecha:', bordered_format)
        worksheet.write('D2', fecha_actual, bordered_format)

    processed_data = output.getvalue()
    return processed_data


def descargar_excel(df, nombre_archivo):
    st.download_button(
        label="Descargar Excel",
        data=to_excel(df),
        file_name=nombre_archivo,
        mime="application/vnd.ms-excel"
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


