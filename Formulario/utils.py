import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def intervalo_ano(row):
    if (row.ANO_INGRESSO >= 1900) & (row.ANO_INGRESSO < 1995):
        return "1990-1994"
    elif (row.ANO_INGRESSO >= 1995) & (row.ANO_INGRESSO < 2000):
        return "1995-1999"
    elif (row.ANO_INGRESSO >= 2000 ) & (row.ANO_INGRESSO < 2005):
        return "2000-2004"
    elif (row.ANO_INGRESSO >= 2005 ) & (row.ANO_INGRESSO < 2010):
        return "2005-2009"
    elif (row.ANO_INGRESSO >= 2010 ) & (row.ANO_INGRESSO < 2015):
        return "2010-2014"
    elif (row.ANO_INGRESSO >= 2015 ) & (row.ANO_INGRESSO < 2020):
        return "2015-2019"
    else:
        return "2020-"
    
def intervalo_renda(row):
    if(row.RENDA_FAMILIAR == '1º Até 1,5 salário mínimo'):
        return 'Até 1,5 SM'
    elif(row.RENDA_FAMILIAR == '2º De 1,5 a 3 salários mínimos'):
        return 'Entre 1,5 e 3 SM'
    else :
        return "Acima de 3 SM"
    
def pie_plot(df, column, title):
    ax = plt.pie(x=df[column].value_counts(),
                 labels=df[column].unique(),autopct='%0.0f%%')
    plt.title(title)
    plt.show()

def instituicao_em(row):
    if (row.TIPO_INST_EM == ('Privada - Ensino Médio Comum'
                             or 'Privada - Ensino Médio Integrado com Técnico')): 
        return 'Particular'
    elif (row.TIPO_INST_EM == ('Pública - Ensino Médio Comum'
                               or 'Pública - Ensino Médio Integrado comTécnico')):
        return 'Pública'
    else:
        return 'Misto'
        
def create_subplots(dataframes, column_names, titles, maintitle, figsize=(15, 5)):
    fig, axs = plt.subplots(1, 3, figsize=figsize) 
    
    fig.suptitle(maintitle)
    for i, dataframe in enumerate(dataframes):
        column_name = column_names[i]
        title = titles[i]
        
        value_counts = dataframe[column_name].value_counts()
        labels = dataframe[column_name].unique()
        
        # Cria o gráfico de pizza no subplot correspondente
        wedges, _, autotexts = axs[i].pie(value_counts, labels=labels, autopct='%.0f%%')
        
        # Adiciona os valores absolutos como anotações em cada fatia do gráfico
        absolute_values = value_counts.values
        for j, autotext in enumerate(autotexts):
            autotext.set_text(f'{autotext.get_text()} ({absolute_values[j]})')
        
        #axs[i].legend()
        axs[i].set_title(title)
    
    plt.tight_layout()  # Ajusta o layout dos subplots
    plt.show()

def barplot_multilabel(df, y, x, title, ylabel, xlabel, figsize):
    
    fig, ax = plt.subplots(figsize=figsize)
    sns.barplot(data=df, y=y, x=x, ax=ax)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    for i in ax.containers:
        ax.bar_label(i,fmt='%d',fontsize=10)

