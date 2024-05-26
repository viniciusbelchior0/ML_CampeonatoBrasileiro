import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px

#para rodar o app, digitar no terminal: streamlit run app_streamlit.py
# Titulo
st.image('Campeonato_Brasileiro_Série_B_logo.png')
st.write("""
_ \n
Dados originalmente coletados de: [FBRef](https://fbref.com/en/) |
Dados individuais para cada time: [dados para Equipes (ex: Goiás)](https://fbref.com/en/squads/78c617cc/2024/matchlogs/c38/schedule/Goias-Scores-and-Fixtures-Serie-B). \n

Os dados utilizados refletem capacidade ofensivas e defensivas dos times; estatísticas auxiliares também são utilizadas.
Clique aqui para conferir o [dicionário de dados](https://github.com/viniciusbelchior0/EstudosdeCaso/blob/main/Esportes/ML_CampeonatoBrasileiro/Dicionario_Dados.pdf) e
a [Pipeline do projeto](https://raw.githubusercontent.com/viniciusbelchior0/EstudosdeCaso/main/Esportes/ML_CampeonatoBrasileiro/Workflow_cb.png).
""")

# fazendo as tabelas
url = f"https://docs.google.com/spreadsheets/d/13fiUifen26hCVwjLG7BiJ1gcr4CGUyR--U-m16R4Su0/gviz/tq?tqx=out:csv&sheet=dados"
dados_brasileirao = pd.read_csv(url, encoding="utf8", decimal=",")
tab_1 = dados_brasileirao.groupby('team',as_index=False).agg({'gf': np.mean, 'shots': np.mean, 'goals_shots': np.mean,
                                                 'shotsontarget_against': np.mean,'p_saves': np.mean, 'ga': np.mean})
tab_1 = tab_1.round(decimals = 2)
st.table(tab_1)

st.subheader("Capacidade ofensiva e defensiva")
#pegando variavies para ajustar as linhas do grafico
v_of = tab_1['shots'].median()
h_of = tab_1['goals_shots'].median()
v_def = tab_1['shotsontarget_against'].median()
h_def = tab_1['p_saves'].median()

# graficos de desempenho
fig1 = px.scatter(tab_1, x="shots", y="goals_shots", size = "gf", hover_name = "team", color="gf",color_continuous_scale="algae",
       labels={"shots": "Chutes por Partida","goals_shots": "Gols por Chute",
               "gf": "Gols por Jogo"}, title= "Capacidade Ofensiva das Equipes") #ofensivo
fig1.add_hline(y = h_of, line_width=1.3, line_dash="dash",line_color="gray")
fig1.add_vline(x = v_of, line_width=1.3, line_dash="dash",line_color="gray")
fig1.add_hrect(y0 =h_of, y1= 0.3,line_width=0, fillcolor="green",opacity =0.1, annotation_text="Ataques sem volume eficientes",annotation_position="top left")
fig1.add_hrect(y0 =0, y1=h_of, line_width=0, fillcolor="red", opacity=0.1, annotation_text="Ataques com volume ineficientes", annotation_position="bottom right")
fig1.add_vrect(x0 =0.25, x1= v_of,line_width=0, fillcolor="palevioletred",opacity =0.1, annotation_text="Ataques sem volume ineficientes",annotation_position="bottom left")
fig1.add_vrect(x0 =v_of, x1= 25,line_width=0, fillcolor="green",opacity =0.08, annotation_text="Ataques com volume eficientes",annotation_position="top right")
fig1.update_layout(title_font_color = "forestgreen", legend_title_font_color="gray", title={'x':0.5, 'xanchor': 'center', 'yanchor': 'top'})
fig1.update_layout(title_font_color = "forestgreen", legend_title_font_color="gray", title={'x':0.5, 'xanchor': 'center', 'yanchor': 'top'})
st.plotly_chart(fig1, use_container_width=True)

st.write("""
Em relação as capacidades ofensivas de uma equipe, três métricas são importantes: 'Chutes por partida',
'Gols por Chute' e 'Gols por Jogo'. \n

O quanto uma equipe chuta ao gol é um indicativo do seu volume ofensivo, no entanto, esse volume deve-se converter em
gols; assim, os gols por chute indicam a efetividade da equipe em transformar esse volume em gols. Gols por jogo
sintetiza a capacidade ofensiva.
""")

fig2 = px.scatter(tab_1, x="shotsontarget_against", y="p_saves", size = "ga", hover_name = "team", color="ga",color_continuous_scale="Oryel",
       labels={"shotsontarget_against": "Chutes sofridos por Jogo","p_saves": "% de Defesas dos Chutes",
               "ga": "Gols sofridos por Jogo"}, title= "Capacidade Defensiva das Equipes")
fig2.add_hline(y = h_def, line_width=1.3, line_dash="dash",line_color="gray")
fig2.add_vline(x = v_def, line_width=1.3, line_dash="dash",line_color="gray")
fig2.add_hrect(y0 =h_def, y1= 1,line_width=0, fillcolor="green",opacity =0.1, annotation_text="Defesa sólida e goleiro eficiente",annotation_position="top left")
fig2.add_hrect(y0 =0.5, y1=h_def, line_width=0, fillcolor="red", opacity=0.1, annotation_text="Defesa frágil e goleiro falho", annotation_position="bottom right")
fig2.add_vrect(x0 =4, x1= v_def,line_width=0, fillcolor="green",opacity =0.1, annotation_text="Defesa sólida e goleiro falho",annotation_position="bottom left")
fig2.add_vrect(x0 =v_def, x1= 8,line_width=0, fillcolor="palevioletred",opacity =0.08, annotation_text="Defesa frágil e goleiro eficiente",annotation_position="top right")
fig2.update_layout(title_font_color = "darkslategray", legend_title_font_color="gray", title={'x':0.5, 'xanchor': 'center', 'yanchor': 'top'})
st.plotly_chart(fig2, use_container_width=True)

st.write("""
Se tratando da defesa, 'Chutes sofridos por partida', '% de Defesas' e 'Gols sofridos por jogo' são indicadores
do potencial da equipe nesse aspecto. \n

A quantidade de chutes sofridos indica o quanto a defesa permite que o adversário chegue próximo ao seu objetivo -
quanto menos chutes levar, mais solida é a defesa - o goleiro, também deve ser avaliado; sua capacidade em defender os
chutes sofridos é medida pela sua % de Defesas. Gols sofridos por jogo é uma síntese da capacidade defensiva da equipe.
""")

# Prevendo uma partida
st.header('Predição do Resultado da partida')
st.write("""
O objetivo foi tentar predizer o resultado das partidas baseado no desempenho recente dos times (5 últimas rodadas). Dessa maneira,
o desempenho das equipes - altamente variável, que pode apresentar oscilações durante períodos de tempo - recebe correções,
gerando uma estimativa mais fiel da sua capacidade. \n

""")

# Dados do campeonato
def get_dados_serieb(df):
    st.sidebar.header("Parâmetros")
    home = st.sidebar.selectbox('Time da Casa',['Amazonas-FC','America-MG','Avai','Botafogo-SP','Brusque-Futebol-Clube','Ceara','Chapecoense','Coritiba','CRB','Goias','Gremio-Novorizontino','Guarani','Ituano','Mirassol-Futebol-Clube','Operario','Paysandu','Ponte-Preta','Santos','Sport-Recife','Vila-Nova'])
    away = st.sidebar.selectbox('Time Visitante',['Amazonas-FC','America-MG','Avai','Botafogo-SP','Brusque-Futebol-Clube','Ceara','Chapecoense','Coritiba','CRB','Goias','Gremio-Novorizontino','Guarani','Ituano','Mirassol-Futebol-Clube','Operario','Paysandu','Ponte-Preta','Santos','Sport-Recife','Vila-Nova'])
    n_rodada = st.sidebar.slider('Rodada Atual (a ser predita)',6,38,6)

    home_t = home
    away_t = away
    rodada = n_rodada - 3
    rodada_max = n_rodada

    df = df[['round','team','tournament','opponent','result','points','gf','ga','possession','gdiff','shots','p_shotsontarget','goals_shots','penalty_goals','p_penaltyconverted','shotsontarget_against','p_saves','cleansheets','penalty_attempted_against','p_penalty_saved','yellow_cards','red_cards','fouls_commited','fouls_draw','offsides','crosses','interceptions','tackles_won','own_goals']]
    df['cardscore'] = df['yellow_cards'] + df['red_cards']*5
    df['foulsdiff'] = df['fouls_draw'] - df['fouls_commited']
    df = df[(df['team'] == home_t) | (df['team'] == away_t)]

    # filtrar os dados
    home = df.loc[(df['team'] == home_t) & (df['round'] >= rodada) & (df['round'] < rodada_max)]
    away = df.loc[(df['team'] == away_t) & (df['round'] >= rodada) & (df['round'] < rodada_max)]

    # Agregar os dados -- alterar a agregação com base nas variáveis utilizadas
    away = away.groupby('team').agg({'points':'sum','gf':'mean','ga':'mean','possession':'mean','gdiff':'sum','shots':'mean','p_shotsontarget':'mean',\
                            'goals_shots':'mean','penalty_goals':'sum','p_penaltyconverted':'mean','shotsontarget_against':'mean',\
                            'p_saves':'mean','cleansheets':'sum','penalty_attempted_against':'sum',\
                            'p_penalty_saved':'mean','cardscore':'mean','foulsdiff':'mean','offsides':'mean','crosses':'mean',\
                            'interceptions':'mean','tackles_won':'mean','own_goals':'sum'})
    away = away[['points','gf','ga','possession','gdiff','shots','p_shotsontarget','goals_shots','penalty_goals','p_penaltyconverted','shotsontarget_against','p_saves','cleansheets','penalty_attempted_against','p_penalty_saved','cardscore','foulsdiff','offsides','crosses','interceptions','tackles_won','own_goals']]
    away = away.assign(key='1')

    home = home.groupby('team').agg({'points':'sum','gf':'mean','ga':'mean','possession':'mean','gdiff':'sum','shots':'mean','p_shotsontarget':'mean',\
                            'goals_shots':'mean','penalty_goals':'sum','p_penaltyconverted':'mean','shotsontarget_against':'mean',\
                            'p_saves':'mean','cleansheets':'sum','penalty_attempted_against':'sum',\
                            'p_penalty_saved':'mean','cardscore':'mean','foulsdiff':'mean','offsides':'mean','crosses':'mean',\
                            'interceptions':'mean','tackles_won':'mean','own_goals':'sum'})
    home['venue'] = 1
    home = home[['venue','points','gf','ga','possession','gdiff','shots','p_shotsontarget','goals_shots','penalty_goals','p_penaltyconverted','shotsontarget_against','p_saves','cleansheets','penalty_attempted_against','p_penalty_saved','cardscore','foulsdiff','offsides','crosses','interceptions','tackles_won','own_goals']]
    home = home.assign(key='1')

    df_serieb = pd.merge(home, away, on='key')
    df_serieb = df_serieb.drop('key', axis=1)
    #renomear
    df_serieb.columns = ['venue','points','gf','ga','possession','gdiff','shots','p_shotsontarget','goals_shots','penalty_goals',\
                     'p_penaltyconverted','shotsontarget_against','p_saves','cleansheets','penalty_attempted_against','p_penalty_saved',\
                     'cardscore','foulsdiff','offsides','crosses','interceptions','tackles_won','own_goals','opp_points','opp_gf','opp_ga',\
                     'opp_possession','opp_gdiff','opp_shots','opp_p_shotsontarget','opp_goals_shots','opp_penalty_goals','opp_p_penaltyconverted',\
                     'opp_shotsontarget_against','opp_p_saves','opp_cleansheets','opp_penalty_attempted_against','opp_p_penalty_saved','opp_cardscore',\
                     'opp_foulsdiff','opp_offsides','opp_crosses','opp_interceptions','opp_tackles_won','opp_own_goals']

    return df_serieb

df_serieb = get_dados_serieb(dados_brasileirao)

# carregando o modelo
classificador_vit = joblib.load('classificador-vit.joblib')
classificador_emp = joblib.load('classificador-emp.joblib')
classificador_der = joblib.load('classificador-der.joblib')

# Predicao
p_vitoria = classificador_vit.predict_proba(df_serieb)
p_empate = classificador_emp.predict_proba(df_serieb)
p_derrota = classificador_der.predict_proba(df_serieb)

print(p_vitoria)
print(p_empate)
print(p_derrota)
resultados = {'Vitória':p_vitoria[0][1],
              'Empate':p_empate[0][1],
              'Derrota':p_derrota[0][1]}

resultado_predito = max(resultados, key=resultados.get)

st.write('Estatísticas das equipes:')
st.dataframe(df_serieb)
st.subheader('Resultado')
st.text(f"O resultado predito da partida é: {resultado_predito} para o time da casa")