import pandas as pd
from datetime import datetime
import streamlit as st
from funciones import añadir_producto, to_excel, descargar_excel, seleccionar_productos, vista_previa, mostrar_carrito, seleccionar_productos_cocina
from productos import restaurantes, restaurantes_cocina

st.set_page_config(
    page_title='Solicitud de Productos',
    layout='wide',
    page_icon= '📄')

st.title('Solicitud de Productos')

# Crea una lista de subcategorías para 'Pedidos'
subcategorias = ['Productos Cocina', 'Productos Barra', 'Productos Limpieza']
# Crea un widget selectbox en la barra lateral para seleccionar la subcategoría
subcategoria_seleccionada = st.selectbox('Selecciona una subcategoría', subcategorias)

# Asegurémonos de que 'pedidos' esté siempre presente en la sesión, para evitar sobreescritura
if 'pedidos' not in st.session_state:
    st.session_state['pedidos'] = pd.DataFrame(columns=['Producto'])

# Muestra el contenido correspondiente a la subcategoría seleccionada
if subcategoria_seleccionada == 'Productos Cocina':
    st.write('Productos Cocina')
    
    # Selección de restaurante
    restaurante_seleccionado = st.selectbox('Selecciona el Restaurante', [''] + list(restaurantes_cocina.keys()))

    if restaurante_seleccionado:
        productos = restaurantes_cocina[restaurante_seleccionado]

        # Selección de categoría
        categoria = st.selectbox('Selecciona una categoría', list(productos.keys()))

        # Selección de productos
        seleccionar_productos_cocina(categoria, productos)

        # Vista previa del DataFrame
        vista_previa(st.session_state['pedidos'])

        # Mostrar el carrito
        mostrar_carrito(st.session_state['pedidos'])

    nombre_archivo = f"Pedido_{restaurante_seleccionado}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    descargar_excel(st.session_state['pedidos'], nombre_archivo)

elif subcategoria_seleccionada == 'Productos Barra':
    st.write('Productos de Barra')

    # Selección de restaurante
    restaurante_seleccionado = st.selectbox('Selecciona el Restaurante', [''] + list(restaurantes.keys()))

    if restaurante_seleccionado:
        productos = restaurantes[restaurante_seleccionado]

        # Selección de categoría
        categoria = st.selectbox('Selecciona una categoría', list(productos.keys()))

        # Selección de productos
        seleccionar_productos(categoria, productos)

    # Vista previa del DataFrame
    vista_previa(st.session_state['pedidos'])

    # Mostrar el carrito
    mostrar_carrito(st.session_state['pedidos'])

    nombre_archivo = f"Pedido_{restaurante_seleccionado}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    descargar_excel(st.session_state['pedidos'], nombre_archivo)

elif subcategoria_seleccionada == 'Productos Limpieza':
    st.write('Productos Limpieza')

    # Selección de restaurante
    restaurante_seleccionado = st.selectbox('Selecciona el Restaurante', [''] + list(restaurantes.keys()))

    if restaurante_seleccionado:
        productos = restaurantes[restaurante_seleccionado]

        # Selección de categoría
        categoria = st.selectbox('Selecciona una categoría', list(productos.keys()))

        # Selección de productos
        seleccionar_productos(categoria, productos)

    # Vista previa del DataFrame
    vista_previa(st.session_state['pedidos'])

    # Mostrar el carrito
    mostrar_carrito(st.session_state['pedidos'])

    nombre_archivo = f"Pedido_{restaurante_seleccionado}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    descargar_excel(st.session_state['pedidos'], nombre_archivo)

# Si el botón "Volver al Menú Principal" es presionado, recargar la página principal
if st.button("Volver al Menú Principal"):
    st.experimental_rerun()  # Esto recarga la aplicación
