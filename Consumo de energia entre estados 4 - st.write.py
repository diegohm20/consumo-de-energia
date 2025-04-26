import streamlit as st
import pandas as pd

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
            st.write(consumo_por_estado_ordenado)

            st.subheader("Consumo Médio por Consumidor:")
            df["consumo_medio"] = df["consumo"] / df["numero_consumidores"]

            st.subheader("Consumo Médio por Estado:")
            consumo_medio_por_estado = df.groupby(
                "sigla_uf")["consumo_medio"].mean().reset_index()
            consumo_medio_por_estado_ordenado = consumo_medio_por_estado.sort_values(
                by="consumo_medio", ascending=False)
            st.write(consumo_medio_por_estado_ordenado)

            st.subheader("Consumo Médio por Tipo de Consumo:")
            consumo_medio_por_tipo = df.groupby(
                "tipo_consumo")["consumo_medio"].mean().reset_index()
            consumo_medio_por_tipo_ordenado = consumo_medio_por_tipo.sort_values(
                by="consumo_medio", ascending=False)
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
