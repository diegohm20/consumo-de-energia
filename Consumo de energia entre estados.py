import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Análise de Consumo de Energia por Estado")

# Barra lateral para carregar o arquivo CSV
with st.sidebar:
    st.header("Carregar Arquivo CSV")
    uploaded_file = st.file_uploader("Selecione o arquivo CSV", type=["csv"])

# Verifica se um arquivo foi carregado
if uploaded_file is not None:
    try:
        # Lê o arquivo CSV com pandas
        df = pd.read_csv(uploaded_file)

        # Verifica se as colunas esperadas estão presentes
        if not all(col in df.columns for col in ["sigla_uf", "consumo"]):
            st.error(
                "O arquivo CSV precisa conter as colunas 'sigla_uf' e 'consumo'.")
        else:
            # Agrupa os dados por estado e calcula o consumo total
            consumo_por_estado = df.groupby(
                "sigla_uf")["consumo"].sum().reset_index()
            consumo_por_estado = consumo_por_estado.rename(
                columns={"consumo": "consumo_total"})

            # Ordena os estados por consumo total (opcional)
            consumo_por_estado_ordenado = consumo_por_estado.sort_values(
                by="consumo_total", ascending=False)

            # Cria o gráfico de barras com Plotly Express
            fig = px.bar(consumo_por_estado_ordenado,
                         x="sigla_uf",
                         y="consumo_total",
                         labels={"sigla_uf": "Estado",
                                 "consumo_total": "Consumo Total de Energia"},
                         title="Comparação do Consumo Total de Energia por Estado")

            # Exibe o gráfico no Streamlit
            st.plotly_chart(fig)

            # Opcional: Exibe a tabela com os resultados
            st.subheader("Consumo Total por Estado:")
            st.dataframe(consumo_por_estado_ordenado)

    except pd.errors.EmptyDataError:
        st.error("O arquivo CSV está vazio.")
    except pd.errors.ParserError:
        st.error("Erro ao ler o arquivo CSV. Verifique se o formato está correto.")

else:
    st.info("Por favor, carregue um arquivo CSV com os dados de consumo de energia.")
