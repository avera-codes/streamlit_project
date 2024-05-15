import yfinance as yf
import pandas as pd
import streamlit as st
from datetime import datetime
import pytz


# Функция для получения данных о бумаге
def get_stock_data(tickerSymbol, start_date, end_date):
    tickerData = yf.Ticker(tickerSymbol)
    tickerDf = tickerData.history(period="1d", start=start_date, end=end_date)
    return tickerDf


# Функция для конвертации датафрейма в CSV формат
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")


# Определение дат
start_date = datetime(2010, 5, 31, tzinfo=pytz.UTC)
end_date = datetime(2020, 5, 31, tzinfo=pytz.UTC)

# Виджеты в боковой панели
with st.sidebar:
    tickerSymbol = st.text_input("Ticker Symbol")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

# Если выбран CSV файл, читаем его и обрабатываем данные
if uploaded_file is not None:
    uploaded_df = pd.read_csv(uploaded_file)
    st.write("Data from uploaded CSV file:")
    st.write(uploaded_df)
    # Отображаем графики
    st.write(
        """
        ## Data Visualization
        """
    )
    for column in uploaded_df.columns:
        if column != "Date":  # Исключаем столбец "Date" из графиков
            st.line_chart(uploaded_df[column])

else:
    # Загружаем данные о бумаге
    tickerDf = get_stock_data(tickerSymbol, start_date, end_date)
    st.write(
        """
        # Simple Stock Price App
        
        Shown are the stock closing price and volume of {}!
        """.format(
            tickerSymbol
        )
    )
    st.line_chart(tickerDf["Close"])
    st.line_chart(tickerDf["Volume"])

    # Конвертируем данные в CSV и добавляем кнопку для их скачивания
    csv_data = convert_df_to_csv(tickerDf)
    st.download_button(
        label="Download data as CSV",
        data=csv_data,
        file_name="stock_data.csv",
        mime="text/csv",
    )
