import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Función para cargar los datos de dividendos utilizando yfinance
@st.cache
def load_dividend_data(ticker):
    stock = yf.Ticker(ticker)
    dividends = stock.dividends
    dividends = dividends.reset_index()
    dividends.columns = ['Fecha', 'Dividendo']
    dividends['Fecha'] = pd.to_datetime(dividends['Fecha'])
    return dividends

# Función para obtener información del stock
@st.cache
def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return info

# Título de la aplicación
st.title('Análisis de Dividendos Pagados')

# Campo para ingresar el símbolo de la acción
ticker = st.text_input('Ingrese el símbolo de la acción', 'AAPL')

if ticker:
    # Obtener información de la acción
    stock_info = get_stock_info(ticker)
    company_name = stock_info.get('longName', 'Nombre no disponible')
    current_price = stock_info.get('currentPrice', 'Precio no disponible')

    # Mostrar el nombre de la compañía y el precio actual de la acción
    st.subheader(f'{company_name} ({ticker})')
    st.write(f'Precio Actual: ${current_price}')

    # Cargar los datos de dividendos
    dividend_data = load_dividend_data(ticker)

    # Mostrar una vista previa de los datos
    st.subheader('Datos de Dividendos')
    st.write(dividend_data)

    # Calcular estadísticas descriptivas
    st.subheader('Análisis Descriptivo')
    st.write(dividend_data.describe())

    # Calcular la suma total de dividendos pagados
    total_dividends = dividend_data['Dividendo'].sum()
    st.subheader('Total de Dividendos Pagados')
    st.write(f'${total_dividends:.2f}')

    # Graficar los dividendos a lo largo del tiempo
    fig = px.line(dividend_data, x='Fecha', y='Dividendo', title='Dividendos Pagados a lo largo del Tiempo')
    st.plotly_chart(fig, use_container_width=True)

    # Graficar un histograma de los dividendos
    fig_hist = px.histogram(dividend_data, x='Dividendo', nbins=20, title='Histograma de Dividendos')
    st.plotly_chart(fig_hist, use_container_width=True)

    # Resumen por año
    dividend_data['Año'] = pd.to_datetime(dividend_data['Fecha']).dt.year
    yearly_summary = dividend_data.groupby('Año')['Dividendo'].sum()

    # Mostrar resumen por año
    st.subheader('Resumen Anual de Dividendos')
    st.bar_chart(yearly_summary)

    # Campo para ingresar el número de acciones y el valor promedio
    st.sidebar.subheader('Cálculo de Dividendos Personales')
    num_shares = st.sidebar.number_input('Número de acciones que tienes', min_value=1, value=100)
    avg_value = st.sidebar.number_input('Valor promedio de cada acción (en $)', min_value=0.0, value=150.0, step=0.01)

    # Obtener el último dividendo pagado
    last_dividend = dividend_data['Dividendo'].iloc[-1] if not dividend_data.empty else 0

    # Calcular dividendos recibidos con el último dividendo pagado
    total_dividends_received = last_dividend * num_shares

    # Mostrar el cálculo de dividendos recibidos
    st.sidebar.subheader('Dividendos Recibidos')
    st.sidebar.write(f'Total de dividendos recibidos (último dividendo): ${total_dividends_received:.2f}')

    # Calcular el valor total de las acciones
    total_value_of_shares = num_shares * avg_value

    # Mostrar el valor total de las acciones
    st.sidebar.subheader('Valor Total de las Acciones')
    st.sidebar.write(f'Valor total de tus acciones: ${total_value_of_shares:.2f}')
