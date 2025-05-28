import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configurações da página Streamlit (mantido como está) ---
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    .reportview-container {
        background: #111; /* Fundo escuro */
        color: #eee; /* Texto claro */
    }
    .sidebar .sidebar-content {
        background: #222;
        color: #eee;
    }
    h1, h2, h3, h4, h5, h6, p, st.info, st.success, st.error, st.warning {
        color: #eee;
    }
    .stDataFrame, .stTable {
        color: #eee;
        background-color: #333;
        border: 1px solid #555;
    }
    .stButton>button {
        color: #eee;
        background-color: #444;
        border: 1px solid #666;
    }
    .stTextInput>div>div>input {
        color: #eee;
        background-color: #333;
        border: 1px solid #555;
    }
    .stPassword>div>div>input {
        color: #eee;
        background-color: #333;
        border: 1px solid #555;
    }
    .stFileUploader>div>div>div>button {
        color: #eee;
        background-color: #444;
        border: 1px solid #666;
    }
    .streamlit-expander {
        background-color: #222;
        color: #eee;
        border: 1px solid #444;
    }
    .streamlit-expander-header {
        color: #eee;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def color_survived(val):
    color = 'salmon' if val < 0 else 'lightgreen'
    return f'color: {color}'

def format_kwh(val):
    return f"{val:.2f} kWh"

st.title("📊 Análise de Consumo de Energia")
st.markdown("Uma aplicação Streamlit interativa para visualizar dados de consumo de energia.")

# --- Lógica de Login (mantido como está) ---
with st.sidebar:
    st.header("🔒 Login")
    with st.form(key="login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        login_button = st.form_submit_button("Entrar")
        if login_button:
            if username == "usuario" and password == "senha":
                st.success("✅ Login realizado com sucesso!")
                st.session_state.logged_in = True
            else:
                st.error("❌ Erro de login. Verifique suas credenciais.")

if not hasattr(st.session_state, "logged_in") or not st.session_state.logged_in:
    st.info("🔑 Faça login na barra lateral para acessar a análise.")
else:
    # --- NOVO: Carregamento do DataFrame diretamente do repositório ---
    data_file_path = 'data/seu_arquivo_de_dados.csv' # AJUSTE ESTE CAMINHO se o arquivo estiver em outro lugar!

    try:
        df = pd.read_csv(data_file_path)
        df["Selecionar"] = False # Certifique-se de que esta coluna ainda é necessária
        st.success(f"Dados carregados com sucesso de '{data_file_path}'!") # Confirma o carregamento

        # --- Restante do seu código de análise (mantido como está) ---
        st.subheader("🔍 Pré-visualização dos Dados Carregados:")
        edited_df = st.data_editor(
            df.head(10),
            column_config={"Selecionar": st.column_config.CheckboxColumn("Selecionar", default=False)},
            num_rows="dynamic",
        )
        selected_rows = edited_df[edited_df["Selecionar"]]
        if not selected_rows.empty:
            st.subheader("📌 Linhas Selecionadas:")
            st.dataframe(selected_rows.style.applymap(color_survived, subset=['consumo', 'numero_consumidores']).format({'consumo': '{:.2f}', 'numero_consumidores': '{:.0f}'}))
        else:
            st.info("👆 Selecione linhas na tabela para destacar.")

        if not all(col in df.columns for col in ["sigla_uf", "consumo", "numero_consumidores", "tipo_consumo"]):
            st.error("⚠️ Colunas 'sigla_uf', 'consumo', 'numero_consumidores' e 'tipo_consumo' são obrigatórias no CSV.")
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
            df["consumo_medio"] = df["consumo"] / df["numero_consumidores"]
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

    except FileNotFoundError:
        st.error(f"⚠️ Erro: O arquivo '{data_file_path}' não foi encontrado. Certifique-se de que ele está no seu repositório Git no caminho correto.")
    except pd.errors.EmptyDataError:
        st.error("⚠️ O arquivo CSV está vazio.")
    except pd.errors.ParserError:
        st.error("⚠️ Erro ao ler o arquivo CSV. Verifique o formato.")
    except KeyError as e:
        st.error(f"⚠️ A coluna '{e}' não foi encontrada no CSV. Verifique se as colunas obrigatórias estão presentes.")
    except Exception as e:
        st.error(f"⚠️ Ocorreu um erro inesperado ao carregar ou processar os dados: {e}")