import pandas as pd
import seaborn as sns
import streamlit as st
import numpy as np
import time

st.set_page_config(layout="wide")

st.title('Mulheres na Computação UFES')

with st.expander('Sobre a Página'):
  st.write('Apresentação dos principais resultados encontrados no PG')
  #st.image('https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png', width=250)

my_bar = st.progress(0)

for percent_complete in range(100):
     time.sleep(0.05)
     my_bar.progress(percent_complete + 1)

st.balloons()

st.sidebar.header('Menu de Opções')
add_sidebar = st.sidebar.selectbox("Selecione",("Resultados do PG","Outras Funcionalidades"))
st.header('Output')


if add_sidebar == "Resultados do PG":
    
    path = "C:\\Users\\USER\\Documents\\GitHub\\mulherescomputacao\\DadosRebeca.csv"
    df = pd.read_csv(path)

    st.subheader('Selecione um curso')

    option = st.selectbox(
        'Selecione o curso?',
        df['NOME_CURSO'].unique())

    'You selected: ', option

    values = st.slider(
     'Selecione um período para análise',
     1990, 2022, (1990, 2022))
    st.write('Values:', values)



else:
    st.write('WORK IN PROGRESS')
