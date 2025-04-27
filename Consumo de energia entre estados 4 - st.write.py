import streamlit as st
import pandas as pd
import plotly.express as px

def color_survived(val):
    """
    Colors the text based on the value.
    """
    color = 'red' if val < 0 else 'green'
    return f'color: {color}'

st.title("Análise de Consumo de Energia")

with st.sidebar:
    with st.form(key="login_form"):
        st.header("Login")
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        login_button = st.form_submit_button("Login")

        if login_button:
            if username == "usuario" and password == "senha":
                st.success("Login realizado com sucesso!")
                st.session_state.logged_in = True
            else:
                st.error("Usuário ou senha incorretos.")

if not hasattr(st.session_state, "logged_in") or not st.session_state.logged_in:
    st.info("Por favor, faça login na barra lateral para acessar a análise.")
else:
    with st.sidebar:
        st.header("Carregar Arquivo CSV")
        uploaded_file = st.file_uploader("Selecione o arquivo CSV", type=["csv"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            df["Selecionar"] = False

            st.subheader("Dados Carregados:")
            edited_df = st.data_editor(
                df,
                column_config={
                    "Selecionar": st.column_config.CheckboxColumn(
                        "Selecionar",
                        default=False,
                    ),
                },
                num_rows=10,
            )

            selected_rows = edited_df[edited_df["Selecionar"]]
            if not selected_rows.empty:
                st.subheader("Linhas Selecionadas:")
                st.dataframe(selected_rows.style.applymap(color_survived, subset=['consumo', 'numero_consumidores'])) # Aplica estilo
            else:
                st.info("Nenhuma linha selecionada.")


            if not all(col in df.columns for col in ["sigla_uf", "consumo", "numero_consumidores", "tipo_consumo"]):
                st.error("O arquivo CSV precisa conter as colunas 'sigla_uf', 'consumo', 'numero_consumidores' e 'tipo_consumo'.")
            else:
                st.subheader("Comparação do Consumo Total por Estado:")
                consumo_por_estado = df.groupby("sigla_uf")["consumo"].sum().reset_index()
                consumo_por_estado = consumo_por_estado.rename(columns={"consumo": "consumo_total"})
                consumo_por_estado_ordenado = consumo_por_estado.sort_values(by="consumo_total", ascending=False)
                fig_bar_estado = px.bar(consumo_por_estado_ordenado, x="sigla_uf", y="consumo_total", labels={"sigla_uf": "Estado", "consumo_total": "Consumo Total de Energia"}, title="Comparação do Consumo Total de Energia por Estado (Barras)")
                st.plotly_chart(fig_bar_estado)
                st.dataframe(consumo_por_estado_ordenado.style.applymap(color_survived, subset=['consumo_total'])) # Aplica estilo

                st.subheader("Visualização Adicional (Estado):")
                col1_estado, col2_estado = st.columns(2)
                with col1_estado:
                    fig_line_estado = px.line(consumo_por_estado_ordenado, x="sigla_uf", y="consumo_total", labels={"sigla_uf": "Estado", "consumo_total": "Consumo Total de Energia"}, title="Consumo Total de Energia por Estado (Linhas)")
                    st.plotly_chart(fig_line_estado)
                with col2_estado:
                    fig_pie_estado = px.pie(consumo_por_estado, names="sigla_uf", values="consumo_total", title="Participação Percentual do Consumo por Estado")
                    st.plotly_chart(fig_pie_estado)

                st.subheader("Consumo Médio por Consumidor:")
                df["consumo_medio"] = df["consumo"] / df["numero_consumidores"]
                consumo_medio_por_estado = df.groupby("sigla_uf")["consumo_medio"].mean().reset_index()
                consumo_medio_por_estado_ordenado = consumo_medio_por_estado.sort_values(by="consumo_medio", ascending=False)
                fig_bar_medio_estado = px.bar(consumo_medio_por_estado_ordenado, x="sigla_uf", y="consumo_medio", labels={"sigla_uf": "Estado", "consumo_medio": "Consumo Médio por Consumidor"}, title="Consumo Médio de Energia por Consumidor por Estado (Barras)")
                st.plotly_chart(fig_bar_medio_estado)
                st.dataframe(consumo_medio_por_estado_ordenado.style.applymap(color_survived, subset=['consumo_medio'])) # Aplica estilo

                consumo_medio_por_tipo = df.groupby("tipo_consumo")["consumo_medio"].mean().reset_index()
                consumo_medio_por_tipo_ordenado = consumo_medio_por_tipo.sort_values(by="consumo_medio", ascending=False)
                fig_bar_medio_tipo = px.bar(consumo_medio_por_tipo_ordenado, x="tipo_consumo", y="consumo_medio", labels={"tipo_consumo": "Tipo de Consumo", "consumo_medio": "Consumo Médio por Consumidor"}, title="Consumo Médio de Energia por Consumidor por Tipo de Consumo (Barras)")
                st.plotly_chart(fig_bar_medio_tipo)
                st.dataframe(consumo_medio_por_tipo_ordenado.style.applymap(color_survived, subset=['consumo_medio'])) # Aplica estilo

                st.subheader("Consumo Médio por Estado e Tipo de Consumo:")
                consumo_medio_estado_tipo = df.groupby(["sigla_uf", "tipo_consumo"])["consumo_medio"].mean().reset_index()
                st.dataframe(consumo_medio_estado_tipo.style.applymap(color_survived, subset=['consumo_medio'])) # Aplica estilo

        except pd.errors.EmptyDataError:
            st.error("O arquivo CSV está vazio.")
        except pd.errors.ParserError:
            st.error("Erro ao ler o arquivo CSV. Verifique se o formato está correto.")
        except KeyError as e:
            st.error(f"A coluna '{e}' não foi encontrada no arquivo CSV. Certifique-se de que as colunas 'sigla_uf', 'consumo', 'numero_consumidores' e 'tipo_consumo' estão presentes.")

    else:
        st.info("Por favor, faça login e carregue um arquivo CSV com os dados de consumo de energia.")
