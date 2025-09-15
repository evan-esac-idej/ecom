import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from time import sleep
import os

st.set_page_config(page_title='ecom_events', layout='wide', page_icon='bar_chart')


# ---------------------------------------------------
# Função para verificar se a dependência openpyxl está instalada
# ---------------------------------------------------
try:
    import openpyxl
except ImportError:
    st.error("⚠️ A biblioteca 'openpyxl' não está instalada. Execute 'pip install openpyxl'")
    st.stop()  # para não continuar o app

# ---------------------------------------------------
# Caminhos relativos para os arquivos Excel
# ---------------------------------------------------
base_dir = os.path.dirname(__file__)  # pasta do script atual
data_base_path = os.path.join(base_dir, 'data_base', 'data.xlsx')
new_data_path = os.path.join(base_dir, 'data_base', 'new_data.xlsx')

# ---------------------------------------------------
# Função para carregar Excel com fallback para upload
# ---------------------------------------------------
def load_excel(file_path, label):
    if os.path.exists(file_path):
        try:
            return pd.read_excel(file_path)
        except Exception as e:
            st.error(f"Erro ao ler {label}: {e}")
            return None
    else:
        st.warning(f"Arquivo '{label}' não encontrado! Faça upload abaixo.")
        uploaded_file = st.file_uploader(f"Escolha o arquivo Excel para {label}", type="xlsx", key=label)
        if uploaded_file is not None:
            try:
                return pd.read_excel(uploaded_file)
            except Exception as e:
                st.error(f"Erro ao ler o arquivo enviado para {label}: {e}")
    return None

# ---------------------------------------------------
# Carregar arquivos
# ---------------------------------------------------
data_base = load_excel(data_base_path, "data.xlsx")
new_data = load_excel(new_data_path, "new_data.xlsx")

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



mob = {
    'Mesas': 1000,
    'Cadeiras': 100,
    'Kit Utensilios por Mesas': 300,
    'Piscina': 2000,
    'Decorativos': 8000,
    'Jardim': 3000
}

alim = {
    'Bolo': 1000,
    'Sobremesa': 100,
    'Salgados': 300,
    'Bifé': 2000,
    'Saladas': 8000,
    'Churrasco': 3000

}

entr = {
    'Som': 1000,
    'DJ': 100,
    'Artista ou Banda': 300,
    'Animação em Led': 2000,
    'Fogo de Artifício': 8000,
    'After Party': 3000

}

if 'len' not in st.session_state:
    st.session_state.len = [0]

if 'max' not in st.session_state:
    st.session_state.max = [0]

if 'mean' not in st.session_state:
    st.session_state.mean = [0]

if 'aval' not in st.session_state:
    st.session_state.aval = [0]

if "carrinho" not in st.session_state:
    st.session_state.carrinho = []
df = {}


tab1, tab2, tab3, tab4 = st.tabs(['👥Clientes', '📈Financeiro', '🗄️Banco de Dados', '⚙️Sobre'])
try:
    with tab1:
        col_a, col_e, col_i = st.columns(3)
        with col_a:
            for item in mob.items():

                # Caminho absoluto seguro baseado no arquivo atual
                caminho_pasta = os.path.join(os.path.dirname(__file__), 'images')
                caminho_imagem = os.path.join(caminho_pasta, f'{item[0]}.jpg')

                if os.path.exists(caminho_imagem):
                    st.image(caminho_imagem)
                else:
                    st.warning(f"Imagem não encontrada: {caminho_imagem}")

                # Número de unidades
                if item[0] in ['Jardim', 'Piscina', 'Decorativos']:
                    pr = st.number_input(f'Para adicionar **{item[0]}** Coloque o número 1', 0, 1, 0)
                else:
                    pr = st.number_input(f'Número de {item[0]}', 0, 100, 0)

                a, i = st.columns(2)
                with a:
                    button = st.button(f'Adicionar', key=f'{item[0]}')
                    if button:
                        placeholder = st.empty()
                        if pr == 0:
                            placeholder.warning(f"⚠️ O número de **{item[0]}** deve ser igual ou maior que 1.")
                            sleep(1.5)
                            placeholder.empty()
                        else:
                            df['Data'] = pd.to_datetime(datetime.now())
                            df['Categorias'] = f'{item[0]}'
                            df['Qtd'] = pr
                            df['Preço'] = item[1]
                            df['Valor'] = pr*item[1]
                            st.session_state.carrinho.append(df)

                            st.toast(f"{pr}x{item[0]} no carrinho ✅!", icon="🎉")

                with i:
                    st.write(f'Preço: {item[1]} Mts/unit')

        with col_e:
            for item in alim.items():
                caminho_pasta = os.path.join(os.path.dirname(__file__), 'images')
                caminho_imagem = os.path.join(caminho_pasta, f'{item[0]}.jpg')

                if os.path.exists(caminho_imagem):
                    st.image(caminho_imagem)
                else:
                    st.warning(f"Imagem não encontrada: {caminho_imagem}")

                # Número de unidades
                if item[0] in ['Bolo', 'Piscina', 'Decorativos']:
                    pr = st.number_input(f'Para adicionar **{item[0]}** Coloque o número 1', 0, 1, 0)
                else:
                    pr = st.number_input(f'Número de {item[0]}', 0, 100, 0)

                a,  i = st.columns(2)
                with a:
                    button = st.button(f'Adicionar', key=f'{item[0]}')
                    if button:
                        placeholder = st.empty()
                        if pr == 0:
                            placeholder.warning(f"⚠️ O número de **{item[0]}** deve ser igual ou maior que 1.")
                            sleep(1.5)
                            placeholder.empty()
                        else:
                            df['Data'] = pd.to_datetime(datetime.now())
                            df['Categorias'] = f'{item[0]}'
                            df['Qtd'] = pr
                            df['Preço'] = item[1]
                            df['Valor'] = pr*item[1]
                            st.session_state.carrinho.append(df)
                            st.toast(f"{pr}x{item[0]} no carrinho ✅!", icon="🎉")
                with i:
                    st.write(f'Preço: {item[1]} Mts/unit')
        with col_i:
            for item in entr.items():
                caminho_pasta = os.path.join(os.path.dirname(__file__), 'images')
                caminho_imagem = os.path.join(caminho_pasta, f'{item[0]}.jpg')

                if os.path.exists(caminho_imagem):
                    st.image(caminho_imagem)
                else:
                    st.warning(f"Imagem não encontrada: {caminho_imagem}")

                # Número de unidades
                if item[0] in 'SomDJArtista ou BandaFogo de ArtifícioAfter Party':
                    pr = st.number_input(f'Para adicionar **{item[0]}** Coloque o número 1', 0, 1, 0)
                else:
                    pr = st.number_input(f'Número de {item[0]}', 0, 100, 0)

                a, i = st.columns(2)
                with a:
                    button = st.button(f'Adicionar', key=f'{item[0]}')
                    if button:
                        placeholder = st.empty()
                        if pr == 0:
                            placeholder.warning(f"⚠️ O número de **{item[0]}** deve ser igual ou maior que 1.")
                            sleep(1.5)
                            placeholder.empty()
                        else:
                            df['Data'] = pd.to_datetime(datetime.now())
                            df['Categorias'] = f'{item[0]}'
                            df['Qtd'] = pr
                            df['Preço'] = item[1]
                            df['Valor'] = pr * item[1]
                            st.session_state.carrinho.append(df)
                            st.toast(f"{pr}x{item[0]} no carrinho ✅!", icon="🎉")

                with i:
                    st.write(f'Preço: {item[1]} Mts/unit')
        with st.sidebar:
            st.title('Carrinho')
            data = pd.DataFrame(st.session_state.carrinho, index=None)
            data.to_excel(new_data_path, index=False)
            select = st.selectbox('Selecione o número da linha ou index', options=data.index)
            del_button = st.button('Eliminar Item')
            if del_button:
                st.session_state.carrinho.pop(select)
                st.rerun()
            st.dataframe(data)
            st.metric(f"O Pagamento total", f"{data['Valor'].sum():,.2f} Mts")

            keep = st.button('Adicionar ao Banco de Dados')
            if keep:
                st.success('Dados adicionados ao banco de dados com Sucesso.')
                df = pd.concat([new_data, data_base], ignore_index=True)
                df.to_excel(data_base_path, index=False)
                st.dataframe(df)
                st.session_state.aval.append(data_base['Valor'].sum())
                st.session_state.mean.append(data_base['Valor'].mean())
                st.session_state.mean.append(data_base['Valor'].max())

except:
    st.empty()

with tab2:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        preview = st.session_state.aval[::-1][0]
        total = data_base['Valor'].sum()
        growth = ((total - preview) / preview) * 100
    
        st.metric("Total de Vendas", f"{data_base['Valor'].sum():,.2f} Mts",
                  f"{growth:.2f}%")
    with col2:
        preview = st.session_state.mean[::-1][0]
        total = data_base['Valor'].mean()
        growth = ((total - preview) / preview) * 100
        if preview == 0:
            growth = 0
        else:
            growth = ((total - preview) / preview) * 100
        st.metric("Média de Venda", f"{data_base['Valor'].mean():,.2f} Mts", f"{growth:,.2f}%")
    with col3:
        preview = st.session_state.max[::-1][0]
        total = data_base['Valor'].max()
        if preview == 0:
            growth = 0
        else:
            growth = ((total - preview) / preview) * 100
        st.metric("Máximo das Vendas", f"{data_base['Valor'].max():,.2f} Mts",  f"{growth:,.2f}%")
    with col4:
        preview = st.session_state.len[::-1][0]
        total = len(data_base)
        
        if preview == 0:
            growth = 0
        else:
            growth = ((total - preview) / preview) * 100
        st.metric(" Total de Pedidos", f"{len(data_base):,}",  f"{growth:,.2f}%")
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
            # Azul
            "#4e79a7",  # Azul médio
            "#6baed6",  # Azul claro
            "#2c3e50",  # Azul escuro
            # Verde
            "#59a14f",  # Verde médio
            "#8cd17d",  # Verde claro
            "#2f4f4f",  # Verde escuro
            # Cinza
            "#bab0ab",  # Cinza claro
            "#7f7f7f",  # Cinza médio
            "#4f4f4f",  # Cinza escuro
            # Vermelho frio
            "#d62728",  # Vermelho médio
            "#ff6f61",  # Vermelho claro
            "#8b0000",  # Vermelho escuro
            # Amarelo frio
            "#f1ce63",  # Amarelo médio
            "#fffacd",  # Amarelo bem claro
            "#c2b280"  # Amarelo acinzentado
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

try:
    with tab3:
        st.dataframe(data_base)
        button = st.button('Exportar dados em Excel')
        if button:
            placeholder = st.empty()
            placeholder.success(f"Novo Banco de Dados arquivado com sucesso ✅")
            sleep(1.5)
            placeholder.empty()
except:
    st.empty()
with tab4:
    st.text('Desenvolvido por Ginélio Hermilio 🤠')
    


























