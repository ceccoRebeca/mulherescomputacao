import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency


def testa_dependencia(conting_tab):
    stat, p, dof, expected = chi2_contingency(conting_tab)
    
    alpha = 0.05
    print("p valor é " + str(p))
    if p <= alpha:
        print('Dependência (rejeita H0)')
    else:
        print('Independência')

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
  tab = pd.crosstab(df[col],df['SEXO'])
  #tab["TOTAL"] = tab["F"] + tab["M"]
  
  #total por coluna
  tabper = pd.crosstab(df[col],df['SEXO']).apply(lambda r: r/r.sum(), axis=0) * 100
  
  return tab,tabper

def crosstabper_linha(df,col):
    
  tab = pd.crosstab(df[col],df['SEXO'])
  

  tabper = pd.crosstab(df[col],df['SEXO']).apply(lambda r: r/r.sum(), axis=1) * 100
  
  return tab,tabper

###### CUSTOM PLOTS ######

def hist_plot(data, column, xlabel, title):
    plt.figure(figsize=(6,5))
    ax = sns.histplot(data=data, x=column,kde=True, hue="SEXO",multiple="stack",bins=33)
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

def comparative_bar_plots(df_ccomp, df_engcomp,column_name, 
                          title, paleta, xlabel="Percentual de Alunos"):
    cc_tab, ccomp_tabper = crosstabper(df_ccomp,column_name)
    ec_tab, eng_tabper = crosstabper(df_engcomp,column_name)

    ccomp_stacked = ccomp_tabper.stack().reset_index().rename(columns={0:'value'})
    ccomp_sorted = ccomp_stacked.sort_values(by=["SEXO", "value", column_name], ascending=[True, False, False])

    eng_stacked = eng_tabper.stack().reset_index().rename(columns={0:'value'})
    eng_sorted = eng_stacked.sort_values(by=["SEXO","value", column_name], ascending=[True,False, True])

    ccomp_order = list(ccomp_sorted[column_name].unique())
    if column_name =='FORMA_EVASAO':
        ccomp_order.append("Falecimento")

    fig, axs = plt.subplots(2,1, figsize=(10,18))
    sns.barplot(x=ccomp_sorted.value, y=ccomp_sorted[column_name], hue=ccomp_sorted.SEXO,ax=axs[0],palette=paleta)
    sns.barplot(x=eng_sorted.value, y=eng_sorted[column_name], hue=eng_sorted.SEXO,ax=axs[1],palette=paleta,order=ccomp_order)
    axs[0].set_title("Ciência da Computação",fontsize=16)
    axs[0].set_ylabel(title,fontsize=14)
    axs[0].set_xlabel(xlabel,fontsize=14)
    for i in axs[0].containers:
        axs[0].bar_label(i,fmt='%.2f')
    axs[1].set_title("Engenharia da Computação",fontsize=16)
    axs[1].set_ylabel(title,fontsize=14)
    axs[1].set_xlabel(xlabel,fontsize=14)
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