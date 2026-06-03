"""
Dashboard Streamlit Moderno - Dataset Olist Brazilian E-Commerce
Design SaaS inspirado em Stripe, Linear e Vercel.
"""
import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os

# Configuração da página com tema escuro
st.set_page_config(
    page_title="Olist Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS para tema escuro elegante
st.markdown("""
<style>
    .stApp {
        background-color: #0a0e27;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    h1, h2, h3 {
        color: #ffffff;
        font-weight: 600;
    }
    .stMetric {
        background-color: #1a1f3a;
        border: 1px solid #2d3748;
        border-radius: 8px;
        padding: 1rem;
    }
    .stMetric label {
        color: #a0aec0;
        font-size: 0.875rem;
    }
    .stMetric div {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 600;
    }
    div[data-testid="stSidebar"] {
        background-color: #0d1229;
    }
    .css-1d391kg {
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# URL da API
API_URL = os.getenv("API_URL", "http://localhost:8000")


def carregar_kpis():
    """Carrega todos os KPIs da API."""
    try:
        response = requests.get(f"{API_URL}/api/v1/kpi/")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Erro ao carregar KPIs: {str(e)}")
        return None


def fazer_pergunta_ia(pergunta):
    """Envia uma pergunta para a IA."""
    try:
        response = requests.post(
            f"{API_URL}/api/v1/ia/perguntar",
            json={"pergunta": pergunta}
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Erro ao processar pergunta: {str(e)}")
        return None


# Sidebar com navegação
with st.sidebar:
    st.markdown("## 📊 Olist Analytics")
    st.markdown("---")
    
    pagina = st.radio(
        "Navegação",
        ["Visão Executiva", "Produtos", "Clientes e Geografia", "Assistente IA"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### Dataset")
    st.info("Olist Brazilian E-Commerce")
    st.markdown("---")
    st.markdown("### Versão")
    st.caption("v2.0.0")


# Página 1 - Visão Executiva
if pagina == "Visão Executiva":
    st.title("Visão Executiva")
    st.markdown("---")
    
    # Carregar dados
    with st.spinner("Carregando dados..."):
        kpis = carregar_kpis()
    
    if kpis:
        # KPIs principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Receita Total",
                value=f"R$ {float(kpis['receita_total']):,.2f}",
                delta="Total"
            )
        
        with col2:
            st.metric(
                label="Pedidos",
                value=f"{kpis['numero_pedidos']:,}",
                delta="Total"
            )
        
        with col3:
            st.metric(
                label="Clientes Únicos",
                value=f"{kpis['clientes_unicos']:,}",
                delta="Total"
            )
        
        with col4:
            st.metric(
                label="Ticket Médio",
                value=f"R$ {float(kpis['ticket_medio']):,.2f}",
                delta="Média"
            )
        
        st.markdown("---")
        
        # Gráficos principais
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Receita por Mês")
            if kpis.get('receita_por_mes'):
                df_receita = pd.DataFrame(kpis['receita_por_mes'])
                df_receita['periodo'] = df_receita['ano'].astype(str) + '-' + df_receita['mes'].astype(str).str.zfill(2)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df_receita['periodo'],
                    y=df_receita['receita'],
                    mode='lines+markers',
                    name='Receita',
                    line=dict(color='#6366f1', width=3),
                    marker=dict(size=8)
                ))
                fig.update_layout(
                    title="Evolução da Receita Mensal",
                    xaxis_title="Período",
                    yaxis_title="Receita (R$)",
                    hovermode='x unified',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#ffffff'),
                    xaxis=dict(gridcolor='#2d3748'),
                    yaxis=dict(gridcolor='#2d3748')
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Sem dados de receita mensal")
        
        with col2:
            st.subheader("Receita por Estado")
            if kpis.get('receita_por_estado'):
                df_estado = pd.DataFrame(kpis['receita_por_estado'])
                fig = px.bar(
                    df_estado,
                    x='estado',
                    y='receita',
                    title="Receita por Estado",
                    color='receita',
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#ffffff'),
                    xaxis=dict(gridcolor='#2d3748'),
                    yaxis=dict(gridcolor='#2d3748')
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Sem dados por estado")
        
        st.markdown("---")
        
        # Gráfico de evolução temporal
        st.subheader("Evolução Temporal")
        if kpis.get('receita_por_mes'):
            df_evolucao = pd.DataFrame(kpis['receita_por_mes'])
            df_evolucao['periodo'] = df_evolucao['ano'].astype(str) + '-' + df_evolucao['mes'].astype(str).str.zfill(2)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_evolucao['periodo'],
                y=df_evolucao['receita'],
                mode='lines+markers',
                name='Receita',
                fill='tozeroy',
                line=dict(color='#8b5cf6', width=2),
                marker=dict(size=6)
            ))
            fig.update_layout(
                title="Evolução da Receita ao Longo do Tempo",
                xaxis_title="Período",
                yaxis_title="Receita (R$)",
                hovermode='x unified',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#ffffff'),
                xaxis=dict(gridcolor='#2d3748'),
                yaxis=dict(gridcolor='#2d3748')
            )
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.warning("Não foi possível carregar os KPIs. Verifique se a API está rodando e se há dados no banco.")


# Página 2 - Produtos
elif pagina == "Produtos":
    st.title("Análise de Produtos")
    st.markdown("---")
    
    # Carregar dados
    with st.spinner("Carregando dados..."):
        kpis = carregar_kpis()
    
    if kpis:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top 10 Produtos")
            if kpis.get('top_produtos'):
                df_produtos = pd.DataFrame(kpis['top_produtos'])
                fig = px.bar(
                    df_produtos,
                    x='faturamento',
                    y='product_id',
                    orientation='h',
                    title="Top 10 Produtos por Faturamento",
                    color='faturamento',
                    color_continuous_scale='Plasma'
                )
                fig.update_layout(
                    yaxis={'categoryorder': 'total ascending'},
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#ffffff'),
                    xaxis=dict(gridcolor='#2d3748'),
                    yaxis=dict(gridcolor='#2d3748')
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Sem dados de produtos")
        
        with col2:
            st.subheader("Top 10 Categorias")
            if kpis.get('top_categorias'):
                df_categorias = pd.DataFrame(kpis['top_categorias'])
                fig = px.bar(
                    df_categorias,
                    x='faturamento',
                    y='categoria',
                    orientation='h',
                    title="Top 10 Categorias por Faturamento",
                    color='faturamento',
                    color_continuous_scale='Cividis'
                )
                fig.update_layout(
                    yaxis={'categoryorder': 'total ascending'},
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#ffffff'),
                    xaxis=dict(gridcolor='#2d3748'),
                    yaxis=dict(gridcolor='#2d3748')
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Sem dados de categorias")
        
        st.markdown("---")
        
        # Receita por categoria
        st.subheader("Receita por Categoria")
        if kpis.get('top_categorias'):
            df_categorias = pd.DataFrame(kpis['top_categorias'])
            fig = px.pie(
                df_categorias,
                values='faturamento',
                names='categoria',
                title="Distribuição de Receita por Categoria",
                hole=0.4
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#ffffff')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Quantidade vendida por categoria
        st.subheader("Quantidade Vendida por Categoria")
        if kpis.get('top_categorias'):
            df_categorias = pd.DataFrame(kpis['top_categorias'])
            fig = px.bar(
                df_categorias,
                x='categoria',
                y='quantidade',
                title="Quantidade Vendida por Categoria",
                color='quantidade',
                color_continuous_scale='Turbo'
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#ffffff'),
                xaxis=dict(gridcolor='#2d3748'),
                yaxis=dict(gridcolor='#2d3748')
            )
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.warning("Não foi possível carregar os KPIs.")


# Página 3 - Clientes e Geografia
elif pagina == "Clientes e Geografia":
    st.title("Clientes e Geografia")
    st.markdown("---")
    
    # Carregar dados
    with st.spinner("Carregando dados..."):
        kpis = carregar_kpis()
    
    if kpis:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distribuição por Estado")
            if kpis.get('pedidos_por_estado'):
                df_estado = pd.DataFrame(kpis['pedidos_por_estado'])
                fig = px.bar(
                    df_estado,
                    x='estado',
                    y='quantidade',
                    title="Pedidos por Estado",
                    color='quantidade',
                    color_continuous_scale='Spectral'
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#ffffff'),
                    xaxis=dict(gridcolor='#2d3748'),
                    yaxis=dict(gridcolor='#2d3748')
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Sem dados por estado")
        
        with col2:
            st.subheader("Receita por Estado")
            if kpis.get('receita_por_estado'):
                df_estado = pd.DataFrame(kpis['receita_por_estado'])
                fig = px.bar(
                    df_estado,
                    x='estado',
                    y='receita',
                    title="Receita por Estado",
                    color='receita',
                    color_continuous_scale='Rainbow'
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#ffffff'),
                    xaxis=dict(gridcolor='#2d3748'),
                    yaxis=dict(gridcolor='#2d3748')
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Sem dados por estado")
        
        st.markdown("---")
        
        # KPIs de clientes
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="Clientes Únicos",
                value=f"{kpis['clientes_unicos']:,}"
            )
        
        with col2:
            st.metric(
                label="Pedidos por Cliente",
                value=f"{kpis['numero_pedidos'] / kpis['clientes_unicos']:.2f}" if kpis['clientes_unicos'] > 0 else "0"
            )
        
        st.markdown("---")
        
        # Métodos de pagamento
        st.subheader("Métodos de Pagamento")
        if kpis.get('metodos_pagamento'):
            df_pagamentos = pd.DataFrame(kpis['metodos_pagamento'])
            fig = px.pie(
                df_pagamentos,
                values='valor_total',
                names='tipo',
                title="Distribuição por Método de Pagamento",
                hole=0.4
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#ffffff')
            )
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.warning("Não foi possível carregar os KPIs.")


# Página 4 - Assistente IA
elif pagina == "Assistente IA":
    st.title("Assistente de Dados")
    st.markdown("---")
    
    st.markdown("""
    Faça perguntas sobre os dados do Olist em linguagem natural.
    
    **Exemplos de perguntas:**
    - Qual estado gerou mais receita?
    - Qual categoria vendeu mais?
    - Qual produto teve maior faturamento?
    - Qual método de pagamento é mais utilizado?
    - Quantos pedidos ocorreram em janeiro?
    """)
    
    st.markdown("---")
    
    # Histórico de conversas
    if "mensagens" not in st.session_state:
        st.session_state.mensagens = []
    
    # Exibir histórico
    for mensagem in st.session_state.mensagens:
        with st.chat_message(mensagem["role"]):
            st.markdown(mensagem["content"])
            
            if mensagem.get("sql"):
                with st.expander("Ver SQL gerado"):
                    st.code(mensagem["sql"], language="sql")
            
            if mensagem.get("dados"):
                with st.expander("Ver dados brutos"):
                    st.json(mensagem["dados"])
    
    # Input do usuário
    pergunta = st.chat_input("Faça uma pergunta sobre os dados Olist...")
    
    if pergunta:
        # Adicionar pergunta do usuário ao histórico
        st.session_state.mensagens.append({"role": "user", "content": pergunta})
        
        # Exibir pergunta
        with st.chat_message("user"):
            st.markdown(pergunta)
        
        # Processar pergunta
        with st.chat_message("assistant"):
            with st.spinner("Processando..."):
                resposta = fazer_pergunta_ia(pergunta)
            
            if resposta:
                if resposta['sucesso']:
                    st.markdown(resposta['resposta'])
                    
                    # Adicionar resposta ao histórico
                    st.session_state.mensagens.append({
                        "role": "assistant",
                        "content": resposta['resposta'],
                        "sql": resposta.get('sql'),
                        "dados": resposta.get('dados')
                    })
                else:
                    st.error(resposta['resposta'])
                    
                    st.session_state.mensagens.append({
                        "role": "assistant",
                        "content": resposta['resposta']
                    })
            else:
                st.error("Erro ao processar pergunta. Verifique se a IA está configurada.")
    
    # Botão para limpar histórico
    if st.button("Limpar Histórico"):
        st.session_state.mensagens = []
        st.rerun()
