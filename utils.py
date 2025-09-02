import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
#import spacy
from wordcloud import WordCloud
import matplotlib.pyplot as plt

#nlp = spacy.load("es_core_news_sm")

def load_data(file_path):
    df = pd.read_csv(file_path, encoding='utf-8', sep=',')

    return df


def calcular_NPS_Servicio(df):
    promoters = df[df["NPS_Servicio"] >= 9].shape[0]
    detractors = df[df["NPS_Servicio"] <= 6].shape[0]
    total_responses = df["NPS_Servicio"].shape[0]
    if total_responses == 0:
        return 0
    return (promoters - detractors) / total_responses * 100

def calcular_NPS_Alexia(df):
    promoters = df[df["NPS_Alexia"] >= 9].shape[0]
    detractors = df[df["NPS_Alexia"] <= 6].shape[0]
    total = df["NPS_Alexia"].shape[0]
    nps = ((promoters - detractors) / total) * 100
    #print(nps)
    if total == 0:
        return 0
    return nps

def calcular_CSAT_Capacitacion(df):
    csat = (df["Capacitacion"].isin([4, 5]).sum() / df["Capacitacion"].count()) * 100
    return csat

def calcular_CSAT(df):
    csat = (df["Satisfaccion_Alexia"].isin([4, 5]).sum() / df["Satisfaccion_Alexia"].count()) * 100
    return csat
    

def transformacion_df(df):
   df = df.rename(columns={df.columns[3]: 'Centro',df.columns[8]: 'Antiguedad', df.columns[21]: 'Modulo_Usado',df.columns[33]: 'NPS_Servicio', df.columns[56]:'Satisfaccion_Alexia', df.columns[63]:'NPS_Alexia'})

   return df

def transformar_cargos(df):
    df["Cargo"] = df["Cargo"].str.lower().str.replace("[-_ . , ]", " ", regex=True)

    df.loc[df["Cargo"].str.contains("secretario", case=False), "Cargo"] = "Secretaria/o"
    df.loc[df["Cargo"].str.contains("secretaria", case=False), "Cargo"] = "Secretaria/o"
    df.loc[df["Cargo"].str.contains("secretraria", case=False), "Cargo"] = "Secretaria/o"
    df.loc[df["Cargo"].str.contains("administrador", case=False), "Cargo"] = "Administrador/a"
    df.loc[df["Cargo"].str.contains("administradora", case=False), "Cargo"] = "Administrador/a"
    df.loc[df["Cargo"].str.contains("adminstradora", case=False), "Cargo"] = "Administrador/a"
    df.loc[df["Cargo"].str.contains("administrativa", case=False), "Cargo"] = "Administrador/a"
    df.loc[df["Cargo"].str.contains("administrativo", case=False), "Cargo"] = "Administrador/a"
    df.loc[df["Cargo"].str.contains("adminstrativo", case=False), "Cargo"] = "Administrador/a"
    df.loc[df["Cargo"].str.contains("admisntrativo", case=False), "Cargo"] = "Administrador/a" 
    df.loc[df["Cargo"].str.contains("adminitradora", case=False), "Cargo"] = "Administrador/a" 
    df.loc[df["Cargo"].str.contains("director", case=False), "Cargo"] = "Director/a"


    return df

def transformacion_df_comentarios(df):
    df_comentarios = df[df["Mejoras"].notna() & (df["Mejoras"] != "")]
    df_comentarios = df_comentarios["Mejoras"]
    df_comentarios = df_comentarios.str.lower().str.replace("[-_ . , ]", " ", regex=True)
    return df_comentarios

def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud


