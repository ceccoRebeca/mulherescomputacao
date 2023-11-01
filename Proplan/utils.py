import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency




def classes(row):
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
    
def crosstabper(df, col):
      
  #total por linha
  tab_linha = pd.crosstab(df[col],df['SEXO'])
  #tab["TOTAL"] = tab["F"] + tab["M"]
  
  #total por coluna
  tab_coluna = pd.crosstab(df[col],df['SEXO']).apply(lambda r: r/r.sum(), axis=0) * 100
  
  return tab_linha,tab_coluna

def crosstabper_linha(df,col):
    
  tab_linha_abs = pd.crosstab(df[col],df['SEXO'])
  

  tab_linha_per = pd.crosstab(df[col],df['SEXO']).apply(lambda r: r/r.sum(), axis=1) * 100
  
  return tab_linha_abs,tab_linha_per

###### CUSTOM PLOTS ######

def hist_plot(data, column, xlabel, title, paleta):
    plt.figure(figsize=(6,5))
    ax = sns.histplot(data=data, x=column,kde=True, hue="SEXO",multiple="stack",bins=33, palette=paleta)
    for i in ax.containers:
        ax.bar_label(i,fontsize=10)
    #ax.set_xticks(df.ANO_INGRESSO.values)
    plt.xticks(fontsize=10,rotation=90)
    plt.ylabel('Quantidade de Alunos')
    plt.xlabel(xlabel)
    plt.title(title)

def comparative_hist_plots(df,figsize=(20,15),nrows=1,ncols=2):
    masc = df[df['SEXO'] == 'M'] 
    femi = df[df['SEXO'] == 'F']

    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)

    sns.histplot(data=masc,x="IDADE",ax=ax[0])
    sns.histplot(data=femi,x="IDADE",ax=ax[1])

    ax[0].set_title("Homens")
    ax[1].set_title("Mulheres")

def plot_boxplot(data, x, y, hue, xlabel, ylabel, title, notch):
    sns.boxplot(x=x, y=y, hue=hue, data=data, notch=notch)

    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)


def mutiple_hist_plots(df1, df2, col1_name, col2_name,
                         title1, title2, maintitle, xlabel1, xlabel2,
                         ylabel1, ylabel2, hue, paleta,
                        figsize = (20,15), nrows=1, ncols=2):
    
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
    sns.histplot(data=df1,x=col1_name,ax=ax[0], hue=hue,multiple="stack",bins=33,kde=True, palette=paleta)
    sns.histplot(data=df2,x=col2_name,ax=ax[1], hue=hue,multiple="stack",bins=33, kde=True, palette=paleta )
    
    fig.suptitle(maintitle)

    for a in ax:
        for p in a.patches:
            a.annotate(format(p.get_height(), '.0f'), (p.get_x() + p.get_width() / 2., p.get_height()),
                       ha = 'center', va = 'center', xytext = (0, 5), textcoords = 'offset points', fontsize=10)

    ax[0].set_title(title1)
    ax[0].set_ylabel(ylabel1)
    ax[0].set_xlabel(xlabel1)
    ax[1].set_title(title2)
    ax[1].set_ylabel(ylabel2)
    ax[1].set_xlabel(xlabel2)

def single_bar_plot(df, column_name, title, paleta, ylabel,
                     xlabel="Percentual de Alunos" ):
    
    tab_evasao, tabper_evasao = crosstabper(df,column_name)
    stacked = tabper_evasao.stack().reset_index().rename(columns={0:'value'})
    sorted = stacked.sort_values(['value',column_name],ascending=False)

    ax = sns.barplot(x=sorted.value, y=sorted[column_name],
                      hue=sorted.SEXO, palette=paleta)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    for i in ax.containers:
        ax.bar_label(i,fmt='%.2f',fontsize=10)
    
    plt.legend(loc="lower right")
    plt.show()

def comparative_bar_plots(df_ccomp, df_engcomp,column_name, maintitle,
                         paleta,ylabel=None, showylabel=False, xlabel="Percentual de Alunos",figsize=(10,28)):
    cc_tab, ccomp_tabper = crosstabper(df_ccomp,column_name)
    ec_tab, eng_tabper = crosstabper(df_engcomp,column_name)

    ccomp_stacked = ccomp_tabper.stack().reset_index().rename(columns={0:'value'})
    ccomp_sorted = ccomp_stacked.sort_values(by=["SEXO", "value", column_name], ascending=[True, False, False])

    eng_stacked = eng_tabper.stack().reset_index().rename(columns={0:'value'})
    eng_sorted = eng_stacked.sort_values(by=["SEXO","value", column_name], ascending=[True,False, True])

    ccomp_order = list(ccomp_sorted[column_name].unique())
    if column_name =='FORMA_EVASAO':
        ccomp_order.append("Falecimento")

    fig, axs = plt.subplots(2,1, figsize=figsize)
    fig.suptitle(maintitle,fontsize=16)
    #talvez seja isso pra tirar espaço mas ctrl c ctrl v
    #fig.subplots_adjust(top=0.85);
    sns.barplot(x=ccomp_sorted.value, y=ccomp_sorted[column_name], hue=ccomp_sorted.SEXO,ax=axs[0],palette=paleta)
    sns.barplot(x=eng_sorted.value, y=eng_sorted[column_name], hue=eng_sorted.SEXO,ax=axs[1],palette=paleta,order=ccomp_order)
    axs[0].set_title("Ciência da Computação",fontsize=14)
    
    if(showylabel):
        axs[0].set_ylabel(ylabel,fontsize=14)
        axs[1].set_ylabel(ylabel,fontsize=14)

    else:
        axs[0].set_ylabel("")
        axs[1].set_ylabel("")
    axs[0].set_xlabel(xlabel,fontsize=14)
    axs[1].set_xlabel(xlabel,fontsize=14)
    
    for i in axs[0].containers:
        axs[0].bar_label(i,fmt='%.2f')
    axs[1].set_title("Engenharia da Computação",fontsize=14)

    
    for i in axs[1].containers:
        axs[1].bar_label(i,fmt='%.2f')

    plt.legend(loc="lower right")
    plt.show()

def pie_plot(data, column_name, title):
    plt.pie(data[column_name].value_counts(), 
            labels = data[column_name].unique(),autopct='%.0f%%')
    plt.legend()
    plt.title(title)
    plt.show()

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
        
        axs[i].legend()
        axs[i].set_title(title)
    
    plt.tight_layout()  # Ajusta o layout dos subplots
    plt.show()

def testa_dependencia(conting_tab):
    stat, p, dof, expected = chi2_contingency(conting_tab)
    
    alpha = 0.05
    print("p valor é " + str(p))
    if p <= alpha:
        print('Dependência (rejeita H0)')
    else:
        print('Independência')

def batch_testa_dependencia(df,column_name):
    soma_linha, soma_coluna = crosstabper(df, column_name)
    testa_dependencia(soma_linha)