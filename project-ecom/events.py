import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from time import sleep
import os


st.set_page_config(page_title='ecom_events', layout='wide', page_icon='bar_chart')

a, e, i = st.columns([2, 3, 2])
with e:
    st.markdown(
        """
        <h1 style="font-family:sans-serif; color:#1f77b4; text-align:center;">
            <span class="animated-title">Bem vindo a Ecom-Web Eventos</span>
        </h1>

        <style>
        .animated-title {
            display: inline-block;
            overflow: hidden;
            border-right: .15em solid #1f77b4;
            white-space: nowrap;
            animation: typing 3s steps(40, end), blink-caret .75s step-end infinite;
            font-size: 20px;
        }

        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }

        @keyframes blink-caret {
            from, to { border-color: transparent }
            50% { border-color: #1f77b4; }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

#with st.sidebar:
    #op = st.selectbox('Catálogo', options=['👥 Clientes', '📈Financeiro', '🗄️Bancos de Dados'], placeholder='Home')

dados = {
    'Mobiliário': {
        'Mesas': 1000,
        'Cadeiras': 100,
        'Kit Utensilios por Mesas': 300,
        'Piscina': 2000,
        'Decorativos': 8000,
        'Jardim': 3000 },
    'alimentação': {
        'Bolo': 1000,
        'Sobremesa': 100,
        'Salgados': 300,
        'Bifé': 2000,
        'Saladas': 8000,
        'Churrasco': 3000
    },
    'entretenimento': {
        'Som': 1000,
        'DJ': 100,
        'Artista ou Banda': 300,
        'Animação em Led': 2000,
        'Fogo de Artifício': 8000,
        'After Party': 3000

    }
}

for key in ['max', 'mean', 'aval', 'carrinho', 'len']:
    if key not in st.session_state:
        st.session_state[key] = [0] if key != 'carrinho' else []
if 'banco_dados' not in st.session_state:
    st.session_state.banco_dados = []


def adicionar_ao_carrinho(nome, preco, pr):
    df_item = {
        'Data': pd.to_datetime(datetime.now()),
        'Categorias': nome,
        'Qtd': pr,
        'Preço': preco,
        'Valor': pr * preco
    }
    st.session_state.carrinho.append(df_item)
    st.toast(f"{pr}x{nome} no carrinho ✅!", icon="🎉")

# Função para exibir itens (mob, alim, entr)
def exibir_itens(dicionario, especiais=[], coluna=None):
    with coluna:
        for nome, preco in dicionario.items():
            caminho_pasta = os.path.join(os.path.dirname(__file__), 'images')
            caminho_imagem = os.path.join(caminho_pasta, f"{nome}.jpg")
            if os.path.exists(caminho_imagem):
                st.image(caminho_imagem)
            else:
                st.warning(f"Imagem não encontrada: {caminho_imagem}")
            if nome in especiais:
                pr = st.slider(f'Para adicionar **{nome}** arraste para 1', 0, 1, 0)
            else:
                pr = st.number_input(f'Número de {nome}', 0, 100, 0)

            a, i = st.columns(2)
            with a:
                button = st.button(f'Adicionar', key=f'{nome}')
                if button:
                    placeholder = st.empty()
                    if pr == 0:
                        placeholder.warning(f"⚠️ O número de **{nome}** deve ser igual ou maior que 1.")
                        sleep(1.5)
                        placeholder.empty()
                    else:
                        adicionar_ao_carrinho(nome, preco, pr)
            with i:
                st.write(f':green[Preço: **{preco}** Mts/unit]')


taba, tabe, tabi, tabo = st.tabs(['👥Cliente', '📈Financeiro', '🗄️Banco de Dados', '⚙️Sobre'])
try:
    with taba:
        col_a, col_e, col_i = st.columns(3)
        exibir_itens(dados['Mobiliário'], especiais=['Jardim', 'Piscina', 'Decorativos'], coluna=col_a)
        exibir_itens(dados['alimentação'], especiais=['Bolo'], coluna=col_e)
        exibir_itens(dados['entretenimento'], especiais=['Som', 'DJ', 'Artista ou Banda', 'Fogo de Artifício', 'After Party'], coluna=col_i)
    
        with st.sidebar:
            st.title('Carrinho')
            new_data = pd.DataFrame(st.session_state.carrinho)
            select = st.selectbox('Selecione o número da linha ou index', options=new_data.index)
            if st.button('Eliminar Item'):
                st.session_state.carrinho.pop(select)
                st.session_state.dados.pop(select)
                st.rerun()
            st.dataframe(new_data)
            st.metric("O Pagamento total", f"{new_data['Valor'].sum():.2f} Mts")
    
            if st.button("✅ Confirmar e Guardar no Banco de Dados"):
                # Acumula no banco de dados
                st.session_state.banco_dados.extend(st.session_state.carrinho)
                st.success("Itens guardados no banco de dados!")
    
                data_base = pd.DataFrame(st.session_state.banco_dados)
    
                st.session_state.aval.append(data_base['Valor'].sum())
                st.session_state.mean.append(data_base['Valor'].mean())
                st.session_state.max.append(data_base['Valor'].max())
                st.session_state.len.append(len(data_base))
    
            else:
                st.info("Carrinho vazio")
except:
    st.empty()


data_base = pd.DataFrame(st.session_state.banco_dados)

try:
    with tabe:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            try:
                preview = st.session_state.aval[::-1][1]
                st.metric(":grey[*Total de vendas anterior*]", f"{preview:,} Mts")
                st.divider()
                total = data_base['Valor'].sum()
                growth = ((total - preview) / preview) * 100
            except (IndexError, ZeroDivisionError):
                preview = 0
                total = data_base['Valor'].sum()
                growth = 0
            st.metric("Total de Vendas", f"{total:,.2f} Mts", f"{growth:.2f}%")
        with col2:
            try:
                preview = st.session_state.mean[::-1][1]
                st.metric(":grey[*Média anterior*]", f"{preview:,.2f} Mts")
                st.divider()
                total = data_base['Valor'].mean()
                growth = ((total - preview) / preview) * 100
            except (IndexError, ZeroDivisionError):
                preview = 0
                total = data_base['Valor'].mean()
                growth = 0
            st.metric("Média de Venda", f"{total:,.2f} Mts", f"{growth:,.2f}%")

        with col3:
            try:
                preview = st.session_state.max[::-1][1]
                st.metric(":grey[*O Máximo de Vendas anterior*]", f"{preview:,} Mts")
                st.divider()
                total = data_base['Valor'].max()
                growth = ((total - preview) / preview) * 100
            except (IndexError, ZeroDivisionError):
                preview = 0
                total = data_base['Valor'].max()
                growth = 0
            st.metric("Máximo das Vendas", f"{total:,.2f} Mts",  f"{growth:,.2f}%")
        with col4:

            try:
                preview = st.session_state.len[::-1][1]
                st.metric(":grey[*Total do Pedidos anterior*]", f"{preview:,}")
                st.divider()
                total = len(data_base)
                growth = ((total - preview) / preview) * 100
            except (IndexError, ZeroDivisionError):
                preview = 0
                total = len(data_base)
                growth = 0
            st.metric(" Total de Pedidos", f"{total:,}",  f"{growth:,.2f}%")
        st.markdown('---')
        col1, col2 = st.columns(2)
        with col1:
            fig_bar = px.bar(data_base.groupby("Categorias")["Qtd"].sum().sort_values(ascending=False).reset_index()
                             , x="Categorias", y="Qtd",
                             title="Produtos mais vendidos", text='Qtd', color='Qtd')
            fig_bar.update_traces(textposition='outside')
            st.plotly_chart(fig_bar, use_container_width=True)
        with col2:
            import plotly.graph_objects as go

            cores = [
                # Tons de Azul
                "#e3f2fd",  # Azul muito claro
                "#bbdefb",  # Azul claro
                "#90caf9",  # Azul suave
                "#64b5f6",  # Azul médio
                "#2196f3",  # Azul padrão
                "#1565c0",  # Azul escuro
                "#0d47a1",  # Azul profundo

                # Tons de Vermelho
                "#ffebee",  # Vermelho muito claro
                "#ffcdd2",  # Vermelho claro
                "#ef9a9a",  # Vermelho suave
                "#e57373",  # Vermelho médio
                "#f44336",  # Vermelho padrão
                "#c62828",  # Vermelho escuro
                "#8b0000",  # Vermelho profundo
                "#4a0000"  # Vermelho quase vinho
            ]

            fig = go.Figure(data=[go.Pie(title='Percentagem de cada categoria',
                labels=data_base['Categorias'],
                values=data_base['Valor'],
                hole=0.5,
                marker=dict(colors=cores),  # aplica cores fixas
                pull=[0, 0.1, 0, 0.3]
            )])
            fig.update_traces(textposition='inside', textinfo='percent')
            st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            fig_line = px.line(data_base, x="Data", y="Valor", color="Categorias",
                               markers=True, title="Evolução Diária")
            st.plotly_chart(fig_line, use_container_width=True)
        with col2:

            receita = data_base.groupby("Categorias")["Valor"].sum().sort_values(ascending=False).reset_index()
            figh = px.bar(receita, x="Valor", y="Categorias", orientation="h",
                          title="Produtos por Receita", text="Valor")
            figh.update_traces(textposition='inside')
            st.plotly_chart(figh, use_container_width=True)
        st.markdown('---')
        group_lis = st.multiselect('Verificar o Valor Total em:', options=data_base.columns, default='Data')
        grouped = data_base.groupby(group_lis)['Valor'].sum()
        df_grouped = pd.DataFrame(grouped)
        df_ = df_grouped.rename(columns={'Valor': 'Valor total'})
        with st.expander(''):
            st.dataframe(df_)

        st.markdown('---')

        cat = st.multiselect('Selecione a(s) Categoria(s) para análise', options=data_base['Categorias'].unique(),)


        df_filt = data_base.query('Categorias == @cat')
        col1, col2, col3 = st.columns(3)
        with col1:
            sum_cat = df_filt['Valor'].sum()
            total = data_base['Valor'].sum()
            per_cat = (sum_cat / total) * 100
            st.metric(f"Total de Vendas de "+", ".join(cat), f"{df_filt['Valor'].sum():,.2f} Mts",
                      f"{per_cat:.2f}% dos produtos")

        with col2:
            qtd_total = df_filt['Qtd'].sum()
            total = data_base['Qtd'].sum()
            per_cat = (qtd_total / total) * 100
            st.metric("Qtd Vendidas", f"{qtd_total:,.2f} Unidades", f"{per_cat:,.2f}% das unidades")

        with col3:
            total = df_filt['Valor'].max()
            st.metric("Máximo de venda em Dia", f"{total:,.2f} Mts", f"{growth:,.2f}%")
        st.dataframe(df_filt)
except:
    st.warning('Adicione produtos a carrinha e no banco de dados para ter as analises dessa secção...')
    st.empty()

try:
    with tabi:
        data_base = pd.DataFrame(st.session_state.banco_dados)
        st.dataframe(data_base)
        button = st.button('Exportar dados em Excel')
        if button:
            placeholder = st.empty()
            placeholder.success(f"Novo Banco de Dados arquivado com sucesso ✅")
            sleep(1.5)
            placeholder.empty()
except:
    st.empty()

with tabo:
    placeholder = st.empty()
    placeholder.info('Desenvolvido por Ginélio Hermilio 🤠')
    sleep(5)
    placeholder.empty()



















