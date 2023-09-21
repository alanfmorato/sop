import pandas as pd
import requests
import streamlit as st
import plotly.express as px

st.title("Dashboard")

url = 'https://labdados.com/produtos'

response = requests.get(url)

dados = pd.DataFrame.from_dict(response.json())

dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format = '%d/%m/%Y')

dados['Data da Compra'] = dados['Data da Compra'].dt.date

st.sidebar.title('Filtros')

with st.sidebar.expander('Data da compra'):
    data_compra = st.date_input('Selecione a data', (dados['Data da Compra'].min(), dados['Data da Compra'].max()))

query = '''
@data_compra[0] <= `Data da Compra` <= @data_compra[1]
'''

dados = dados.query(query)

receita_mensal = dados.set_index('Data da Compra').groupby('Data da Compra')['Preço'].sum().reset_index()

fig_receita_mensal = px.line(receita_mensal, 
                             x = 'Data da Compra', y = 'Preço', 
                             markers= True, 
                            title = 'Receita Mensal')

st.plotly_chart(fig_receita_mensal, use_container_width= True)

st.dataframe(dados)