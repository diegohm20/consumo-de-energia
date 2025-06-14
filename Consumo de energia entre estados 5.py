import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configurações da página Streamlit ---
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    /* Estilos para o tema Dark */
    body {
        background-color: #000; /* Fundo mais escuro */
        color: #eee; /* Texto claro para contraste */
    }
    .stApp {
        background-color: #000; /* Garante que o fundo principal do app seja preto */
    }
    .reportview-container {
        background: #000;
        color: #eee;
    }
    .sidebar .sidebar-content {
        background: #111; /* Barra lateral um pouco menos escura que o fundo principal */
        color: #eee;
    }
    
    /* Cores de texto para todos os elementos (ajustado para ser mais abrangente) */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stText, .stInfo, .stSuccess, .stError, .stWarning {
        color: #eee !important; /* Adicionado !important para forçar a cor */
    }

    /* Fundo para mensagens st.info, st.success, st.error, st.warning */
    .stAlert { /* Este seletor pega todos os tipos de alerta (info, success, error, warning) */
        background-color: #222 !important; /* Fundo escuro para alertas */
        border-color: #444 !important; /* Borda também escura */
        color: #eee !important; /* Garante que o texto dentro seja claro */
    }

    .stDataFrame, .stTable {
        color: #eee;
        background-color: #222; /* Fundo dos DataFrames mais escuro */
        border: 1px solid #444;
    }
    .stButton>button {
        color: #eee;
        background-color: #333; /* Fundo dos botões mais escuro */
        border: 1px solid #555;
    }
    .stTextInput>div>div>input, .stPassword>div>div>input {
        color: #eee;
        background-color: #222; /* Fundo dos campos de input e senha mais escuro */
        border: 1px solid #444;
    }
    .stFileUploader>div>div>div>button {
        color: #eee;
        background-color: #333;
        border: 1px solid #555;
    }
    .streamlit-expander {
        background-color: #111; /* Fundo dos expanders mais escuro */
        color: #eee;
        border: 1px solid #333;
    }
    .streamlit-expander-header {
        color: #eee;
    }
    /* Estilo para links de download (mantido, mas não usado diretamente) */
    .stDownloadButton > button {
        background-color: #007bff;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        text-decoration: none;
        display: inline-block;
        font-weight: bold;
    }
    .stDownloadButton > button:hover {
        background-color: #0056b3;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def color_survived(val):
    """Aplica cor a valores numéricos: salmão para negativos, verde claro para positivos."""
    color = 'salmon' if val < 0 else 'lightgreen'
    return f'color: {color}'

def format_kwh(val):
    """Formata um valor como kWh com duas casas decimais."""
    return f"{val:.2f} kWh"

st.title("📊 Análise de Consumo de Energia")
st.markdown("Uma aplicação Streamlit interativa para
