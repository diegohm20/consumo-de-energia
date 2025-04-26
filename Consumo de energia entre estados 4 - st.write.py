import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Análise de Consumo de Energia")

with st.sidebar:
    st.header("Carregar Arquivo CSV")
    uploaded_file = st.file_uploader("Selecione o arquivo CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if not all(col in df.columns for col in ["sigla_uf", "consumo", "numero_consumidores", "tipo_consumo"]):
            st.error(
                "O arquivo CSV precisa conter as colunas 'sigla_uf', 'consumo', 'numero_consumidores' e 'tipo_consumo'.")
        else:
            st.subheader("Comparação do Consumo Total por Estado:")
            consumo_por_estado = df.groupby(
                "sigla_uf")["consumo"].sum().reset_index()
            consumo_por_estado = consumo_por_estado.rename(
                columns={"consumo": "consumo_total"})
            consumo_por_estado_ordenado = consumo_por_estado.sort_values(
                by="consumo_total", ascending=False)
            fig_bar_estado = px.bar(consumo_por_estado_ordenado, x="sigla_uf", y="consumo_total", labels={
                                    "sigla_uf": "Estado", "consumo_total": "Consumo Total de Energia"}, title="Comparação do Consumo Total de Energia por Estado (Barras)")
            st.plotly_chart(fig_bar_estado)
            st.write(consumo_por_estado_ordenado)

            st.subheader("Visualização Adicional (Estado):")
            col1_estado, col2_estado = st.columns(2)
            with col1_estado:
                fig_line_estado = px.line(consumo_por_estado_ordenado, x="sigla_uf", y="consumo_total", labels={
                                          "sigla_uf": "Estado", "consumo_total": "Consumo Total de Energia"}, title="Consumo Total de Energia por Estado (Linhas)")
                st.plotly_chart(fig_line_estado)
            with col2_estado:
                fig_pie_estado = px.pie(consumo_por_estado, names="sigla_uf", values="consumo_total",
                                        title="Participação Percentual do Consumo por Estado")
                st.plotly_chart(fig_pie_estado)

            st.subheader("Consumo Médio por Consumidor:")
            df["consumo_medio"] = df["consumo"] / df["numero_consumidores"]

            st.subheader("Consumo Médio por Estado:")
            consumo_medio_por_estado = df.groupby(
                "sigla_uf")["consumo_medio"].mean().reset_index()
            consumo_medio_por_estado_ordenado = consumo_medio_por_estado.sort_values(
                by="consumo_medio", ascending=False)
            fig_bar_medio_estado = px.bar(consumo_medio_por_estado_ordenado, x="sigla_uf", y="consumo_medio", labels={
                                          "sigla_uf": "Estado", "consumo_medio": "Consumo Médio por Consumidor"}, title="Consumo Médio de Energia por Consumidor por Estado (Barras)")
            st.plotly_chart(fig_bar_medio_estado)
            st.write(consumo_medio_por_estado_ordenado)

            st.subheader("Consumo Médio por Tipo de Consumo:")
            consumo_medio_por_tipo = df.groupby(
                "tipo_consumo")["consumo_medio"].mean().reset_index()
            consumo_medio_por_tipo_ordenado = consumo_medio_por_tipo.sort_values(
                by="consumo_medio", ascending=False)
            fig_bar_medio_tipo = px.bar(consumo_medio_por_tipo_ordenado, x="tipo_consumo", y="consumo_medio", labels={
                                        "tipo_consumo": "Tipo de Consumo", "consumo_medio": "Consumo Médio por Consumidor"}, title="Consumo Médio de Energia por Consumidor por Tipo de Consumo (Barras)")
            st.plotly_chart(fig_bar_medio_tipo)
            st.write(consumo_medio_por_tipo_ordenado)

            st.subheader("Consumo Médio por Estado e Tipo de Consumo:")
            consumo_medio_estado_tipo = df.groupby(["sigla_uf", "tipo_consumo"])[
                "consumo_medio"].mean().reset_index()
            st.write(consumo_medio_estado_tipo)

    except pd.errors.EmptyDataError:
        st.error("O arquivo CSV está vazio.")
    except pd.errors.ParserError:
        st.error("Erro ao ler o arquivo CSV. Verifique se o formato está correto.")
    except KeyError as e:
        st.error(f"A coluna '{e}' não foi encontrada no arquivo CSV. Certifique-se de que as colunas 'sigla_uf', 'consumo', 'numero_consumidores' e 'tipo_consumo' estão presentes.")

else:
    st.info("Por favor, carregue um arquivo CSV com os dados de consumo de energia.")

else:
    st.info("Por favor, carregue um arquivo CSV com os dados de consumo de energia.")
