import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Análise de Consumo de Energia por Estado")

with st.sidebar:
    st.header("Carregar Arquivo CSV")
    uploaded_file = st.file_uploader("Selecione o arquivo CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if not all(col in df.columns for col in ["sigla_uf", "consumo"]):
            st.error(
                "O arquivo CSV precisa conter as colunas 'sigla_uf' e 'consumo'.")
        else:
            consumo_por_estado = df.groupby(
                "sigla_uf")["consumo"].sum().reset_index()
            consumo_por_estado = consumo_por_estado.rename(
                columns={"consumo": "consumo_total"})
            consumo_por_estado_ordenado = consumo_por_estado.sort_values(
                by="consumo_total", ascending=False)
            fig_bar = px.bar(consumo_por_estado_ordenado, x="sigla_uf", y="consumo_total", labels={
                             "sigla_uf": "Estado", "consumo_total": "Consumo Total de Energia"}, title="Comparação do Consumo Total de Energia por Estado (Barras)")
            st.plotly_chart(fig_bar)
            st.subheader("Consumo Total por Estado:")
            st.dataframe(consumo_por_estado_ordenado)

            st.subheader("Visualização Adicional:")
            col1, col2 = st.columns(2)

            with col1:
                fig_line = px.line(consumo_por_estado_ordenado, x="sigla_uf", y="consumo_total", labels={
                                   "sigla_uf": "Estado", "consumo_total": "Consumo Total de Energia"}, title="Consumo Total de Energia por Estado (Linhas)")
                st.plotly_chart(fig_line)

            with col2:
                fig_pie = px.pie(consumo_por_estado, names="sigla_uf", values="consumo_total",
                                 title="Participação Percentual do Consumo por Estado")
                st.plotly_chart(fig_pie)

    except pd.errors.EmptyDataError:
        st.error("O arquivo CSV está vazio.")
    except pd.errors.ParserError:
        st.error("Erro ao ler o arquivo CSV. Verifique se o formato está correto.")

else:
    st.info("Por favor, carregue um arquivo CSV com os dados de consumo de energia.")
