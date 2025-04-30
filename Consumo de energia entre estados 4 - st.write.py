import streamlit as st
import pandas as pd
import plotly.express as px

def color_survived(val):
    color = 'red' if val < 0 else 'green'
    return f'color: {color}'

def format_kwh(val):
    return f"{val} kWh"

st.title("Análise de Consumo de Energia")

with st.sidebar:
    with st.form(key="login_form"):
        st.header("Login")
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        login_button = st.form_submit_button("Login")
        if login_button:
            if username == "usuario" and password == "senha":
                st.success("Login realizado!")
                st.session_state.logged_in = True
            else:
                st.error("Erro de login.")

if not hasattr(st.session_state, "logged_in") or not st.session_state.logged_in:
    st.info("Faça login para acessar a análise.")
else:
    with st.sidebar:
        st.header("Carregar CSV")
        uploaded_file = st.file_uploader("Selecione o CSV", type=["csv"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            df["Selecionar"] = False
            st.subheader("Dados Carregados:")
            edited_df = st.data_editor(df, column_config={"Selecionar": st.column_config.CheckboxColumn("Selecionar", default=False)}, num_rows=10)
            selected_rows = edited_df[edited_df["Selecionar"]]
            if not selected_rows.empty:
                st.subheader("Selecionados:")
                st.dataframe(selected_rows.style.applymap(color_survived, subset=['consumo', 'numero_consumidores']).format({'consumo': '{:.2f} kWh', 'numero_consumidores': '{:.0f}'}))
            else:
                st.info("Nenhuma linha selecionada.")
            if not all(col in df.columns for col in ["sigla_uf", "consumo", "numero_consumidores", "tipo_consumo"]):
                st.error("Colunas ausentes no CSV.")
            else:
                st.subheader("Consumo Total por Estado:")
                consumo_por_estado = df.groupby("sigla_uf")["consumo"].sum().reset_index()
                consumo_por_estado = consumo_por_estado.rename(columns={"consumo": "consumo_total"})
                consumo_por_estado_ordenado = consumo_por_estado.sort_values(by="consumo_total", ascending=False)
                fig_bar_estado = px.bar(consumo_por_estado_ordenado, x="sigla_uf", y="consumo_total", labels={"sigla_uf": "Estado", "consumo_total": "Consumo Total de Energia (kWh)"}, title="Consumo Total por Estado (Barras)")
                st.plotly_chart(fig_bar_estado)
                st.dataframe(consumo_por_estado_ordenado.style.applymap(color_survived, subset=['consumo_total']).format({'consumo_total': '{:.2f} kWh'}))
                st.subheader("Visualização Adicional (Estado):")
                col1_estado, col2_estado = st.columns(2)
                with col1_estado:
                    fig_line_estado = px.line(consumo_por_estado_ordenado, x="sigla_uf", y="consumo_total", labels={"sigla_uf": "Estado", "consumo_total": "Consumo Total de Energia (kWh)"}, title="Consumo Total por Estado (Linhas)")
                    st.plotly_chart(fig_line_estado)
                with col2_estado:
                    fig_pie_estado = px.pie(consumo_por_estado, names="sigla_uf", values="consumo_total", title="Participação Percentual por Estado")
                    st.plotly_chart(fig_pie_estado)
                st.subheader("Consumo Médio por Consumidor:")
                df["consumo_medio"] = df["consumo"] / df["numero_consumidores"]
                consumo_medio_por_estado = df.groupby("sigla_uf")["consumo_medio"].mean().reset_index()
                consumo_medio_por_estado_ordenado = consumo_medio_por_estado.sort_values(by="consumo_medio", ascending=False)
                fig_bar_medio_estado = px.bar(consumo_medio_por_estado_ordenado, x="sigla_uf", y="consumo_medio", labels={"sigla_uf": "Estado", "consumo_medio": "Consumo Médio por Consumidor (kWh)"}, title="Consumo Médio por Estado (Barras)")
                st.plotly_chart(fig_bar_medio_estado)
                st.dataframe(consumo_medio_por_estado_ordenado.style.applymap(color_survived, subset=['consumo_medio']).format({'consumo_medio': '{:.2f} kWh'}))
                consumo_medio_por_tipo = df.groupby("tipo_consumo")["consumo_medio"].mean().reset_index()
                consumo_medio_por_tipo_ordenado = consumo_medio_por_tipo.sort_values(by="consumo_medio", ascending=False)
                fig_bar_medio_tipo = px.bar(consumo_medio_por_tipo_ordenado, x="tipo_consumo", y="consumo_medio", labels={"tipo_consumo": "Tipo", "consumo_medio": "Consumo Médio (kWh)"}, title="Consumo Médio por Tipo (Barras)")
                st.plotly_chart(fig_bar_medio_tipo)
                st.dataframe(consumo_medio_por_tipo_ordenado.style.applymap(color_survived, subset=['consumo_medio']).format({'consumo_medio': '{:.2f} kWh'}))
                st.subheader("Consumo Médio por Estado e Tipo:")
                consumo_medio_estado_tipo = df.groupby(["sigla_uf", "tipo_consumo"])["consumo_medio"].mean().reset_index()
                st.dataframe(consumo_medio_estado_tipo.style.applymap(color_survived, subset=['consumo_medio']).format({'consumo_medio': '{:.2f} kWh'}))
        except pd.errors.EmptyDataError:
            st.error("CSV vazio.")
        except pd.errors.ParserError:
            st.error("Erro ao ler CSV.")
        except KeyError:
            st.error("Coluna esperada não encontrada.")
    else:
        st.info("Carregue um CSV.")
