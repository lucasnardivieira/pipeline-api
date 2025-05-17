import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import pandas as pd
import altair as alt

# Carregar variáveis de ambiente
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Criar engine de conexão
engine = create_engine(DATABASE_URL)

# Título
st.title("📈 Dashboard de Preço do Bitcoin")

# Função para carregar dados do banco
@st.cache_data(ttl=60)  # Cache com atualização a cada 60 segundos
def load_data():
    query = "SELECT * FROM bitcoin_data ORDER BY timestamp DESC LIMIT 100"
    df = pd.read_sql(query, engine)
    return df.sort_values("timestamp")

# Botão de atualização manual
if st.button("🔄 Atualizar dados"):
    st.cache_data.clear()

# Carregar dados
df = load_data()

if df.empty:
    st.warning("Sem dados disponíveis no momento.")
else:
    # Mostrar tabela
    st.subheader("📋 Últimos Registros")
    st.dataframe(df, use_container_width=True)

    # Gráfico de linha com Altair
    st.subheader("📊 Evolução do Preço do Bitcoin")
    chart = alt.Chart(df).mark_line(point=True).encode(
        x="timestamp:T",
        y="value:Q",
        tooltip=["timestamp:T", "value:Q"]
    ).properties(width="container")
    
    st.altair_chart(chart, use_container_width=True)

    # Estatísticas básicas
    st.subheader("📌 Estatísticas")
    st.metric("Valor Atual", f"${df['value'].iloc[-1]:,.2f}")
    st.metric("Valor Máximo", f"${df['value'].max():,.2f}")
    st.metric("Valor Mínimo", f"${df['value'].min():,.2f}")
