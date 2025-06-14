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
    h1, h2, h3, h4, h5, h6, p, .st-emotion-cache-10q7673, .st-emotion-cache-1gh866b, .st-emotion-cache-1c7y2jl, .st-emotion-cache-nahz7x, .st-emotion-cache-1i07m2x { /* Adicionado seletores para st.info, st.success, st.error, st.warning e outros textos */
        color: #eee;
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
st.markdown("Uma aplicação Streamlit interativa para visualizar dados de consumo de energia.")

# --- Lógica de Login ---
with st.sidebar:
    st.header("🔒 Login")
    # Informação das credenciais de login
    st.info("Credenciais de login:\n\n**Usuário:** `usuario`\n**Senha:** `senha`")
    
    with st.form(key="login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        login_button = st.form_submit_button("Entrar")
        if login_button:
            if username == "usuario" and password == "senha": # Credenciais de exemplo
                st.success("✅ Login realizado com sucesso!")
                st.session_state.logged_in = True
            else:
                st.error("❌ Erro de login. Verifique suas credenciais.")

# Verifica o estado de login
if not hasattr(st.session_state, "logged_in") or not st.session_state.logged_in:
    st.info("🔑 Faça login na barra lateral para acessar a análise.")
else:
    df = None # Inicializa df como None

    # --- NOVO: Carrega o DataFrame diretamente da URL do Google Drive ---
    # IMPORTANTE: Esta é uma URL de download direto do Google Drive.
    # A URL original foi convertida para este formato.
    google_drive_url = 'https://drive.google.com/uc?export=download&id=1tDyGszbunFW1iibNoGstsIPbcAHSlXxC'

    try:
        with st.spinner("Carregando dados do Google Drive..."):
            df = pd.read_csv(google_drive_url)
           
        # Garante que a coluna 'Selecionar' exista para o data_editor, se necessário
        if "Selecionar" not in df.columns:
            df["Selecionar"] = False
        st.success(f"✅ Dados carregados com sucesso da URL: '{google_drive_url}'")
    except Exception as e:
        st.error(f"⚠️ Ocorreu um erro ao carregar os dados da URL: {e}. Verifique se a URL está correta e se o arquivo CSV está acessível.")

    # --- Lógica de Análise (só executa se o DataFrame foi carregado com sucesso) ---
    if df is not None:
        st.subheader("🔍 Pré-visualização dos Dados Carregados:")
        edited_df = st.data_editor(
            df.head(10), # Mostra apenas as 10 primeiras linhas para pré-visualização
            column_config={"Selecionar": st.column_config.CheckboxColumn("Selecionar", default=False)},
            num_rows="dynamic",
            key="data_preview_editor" # Adiciona uma chave única para o data_editor
        )
        selected_rows = edited_df[edited_df["Selecionar"]]

        if not selected_rows.empty:
            st.subheader("📌 Linhas Selecionadas:")
            st.dataframe(selected_rows.style.applymap(color_survived, subset=['consumo', 'numero_consumidores']).format({'consumo': '{:.2f}', 'numero_consumidores': '{:.0f}'}))
        else:
            st.info("👆 Selecione linhas na tabela para destacar.")

        # Verifica se as colunas obrigatórias existem antes de prosseguir com as análises
        required_columns = ["sigla_uf", "consumo", "numero_consumidores", "tipo_consumo"]
        if not all(col in df.columns for col in required_columns):
            st.error(f"⚠️ As colunas {', '.join(required_columns)} são obrigatórias no CSV. Verifique seu arquivo.")
        else:
            st.subheader("📊 Análises de Consumo:")

            # Consumo Total por Estado
            st.markdown("### 🌎 Consumo Total de Energia por Unidade Federativa")
            consumo_por_estado = df.groupby("sigla_uf")["consumo"].sum().reset_index()
            consumo_por_estado = consumo_por_estado.rename(columns={"consumo": "consumo_total"}).sort_values(by="consumo_total", ascending=False)
            col1, col2 = st.columns(2)
            with col1:
                fig_bar_estado = px.bar(consumo_por_estado, x="sigla_uf", y="consumo_total", labels={"sigla_uf": "Estado", "consumo_total": "Consumo Total (kWh)"}, title="Gráfico de Barras")
                st.plotly_chart(fig_bar_estado, use_container_width=True)
            with col2:
                fig_pie_estado = px.pie(consumo_por_estado, names="sigla_uf", values="consumo_total", title="Participação Percentual")
                st.plotly_chart(fig_pie_estado, use_container_width=True)
            st.dataframe(consumo_por_estado.style.format({'consumo_total': '{:.2f} kWh'}))

            # Consumo Médio por Consumidor
            st.markdown("### 👤 Consumo Médio de Energia por Consumidor")
            # Evita divisão por zero se 'numero_consumidores' for 0
            df["consumo_medio"] = df.apply(lambda row: row["consumo"] / row["numero_consumidores"] if row["numero_consumidores"] != 0 else 0, axis=1)

            consumo_medio_por_estado = df.groupby("sigla_uf")["consumo_medio"].mean().reset_index().sort_values(by="consumo_medio", ascending=False)
            col3, col4 = st.columns(2)
            with col3:
                fig_bar_medio_estado = px.bar(consumo_medio_por_estado, x="sigla_uf", y="consumo_medio", labels={"sigla_uf": "Estado", "consumo_medio": "Consumo Médio (kWh)"}, title="Por Estado")
                st.plotly_chart(fig_bar_medio_estado, use_container_width=True)
            with col4:
                consumo_medio_por_tipo = df.groupby("tipo_consumo")["consumo_medio"].mean().reset_index().sort_values(by="consumo_medio", ascending=False)
                fig_bar_medio_tipo = px.bar(consumo_medio_por_tipo, x="tipo_consumo", y="consumo_medio", labels={"tipo_consumo": "Tipo de Consumo", "consumo_medio": "Consumo Médio (kWh)"}, title="Por Tipo de Consumo")
                st.plotly_chart(fig_bar_medio_tipo, use_container_width=True)
            st.dataframe(consumo_medio_por_estado.style.format({'consumo_medio': '{:.2f} kWh'}))
            st.dataframe(consumo_medio_por_tipo.style.format({'consumo_medio': '{:.2f} kWh'}))

            # Consumo Médio por Estado e Tipo
            st.markdown("### 🏘️ Consumo Médio Detalhado por Estado e Tipo de Consumo")
            consumo_medio_estado_tipo = df.groupby(["sigla_uf", "tipo_consumo"])["consumo_medio"].mean().reset_index()
            st.dataframe(consumo_medio_estado_tipo.style.format({'consumo_medio': '{:.2f} kWh'}))
