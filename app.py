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
    return dividends

# Definir el símbolo de la acción
st.title('Análisis de Dividendos Pagados')
ticker = st.text_input('Ingrese el símbolo de la acción', 'AAPL')

# Cargar los datos de dividendos
if ticker:
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

    # Filtrar por fecha
    start_date = st.date_input('Seleccionar Fecha de Inicio', dividend_data['Fecha'].min())
    end_date = st.date_input('Seleccionar Fecha de Fin', dividend_data['Fecha'].max())

    filtered_data = dividend_data[(dividend_data['Fecha'] >= pd.to_datetime(start_date)) & (dividend_data['Fecha'] <= pd.to_datetime(end_date))]

    # Mostrar datos filtrados
    st.subheader('Datos Filtrados por Fecha')
    st.write(filtered_data)

    # Resumen por año
    dividend_data['Año'] = pd.to_datetime(dividend_data['Fecha']).dt.year
    yearly_summary = dividend_data.groupby('Año')['Dividendo'].sum()

    # Mostrar resumen por año
    st.subheader('Resumen Anual de Dividendos')
    st.bar_chart(yearly_summary)
