import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from time import sleep
import os

st.set_page_config(page_title='ecom_events', layout='wide', page_icon='bar_chart')

import streamlit as st
import pandas as pd
import os

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

a, e, i = st.columns([1, 4, 1])
with e:
    st.title('Bem vindo EcomWeb Eventos')


with st.sidebar:
    op = st.selectbox('Catálogo', options=['👥 Clientes', '📈Financeiro', '🗄️Bancos de Dados'], placeholder='Home')

import os
from datetime import datetime
import pandas as pd
import streamlit as st
from time import sleep

# Exemplo dos dicionários
import streamlit as st
import pandas as pd
from datetime import datetime
from time import sleep
import os
import plotly.express as px

# -----------------------------
# Dicionários de produtos
# -----------------------------
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

# -----------------------------
# Categorias especiais
# -----------------------------
mob_especiais = ['Jardim', 'Piscina', 'Decorativos']
alim_especiais = ['Bolo']
entr_especiais = ['Som', 'DJ', 'Artista ou Banda', 'Fogo de Artifício', 'After Party']

# -----------------------------
# Inicialização do session_state
# -----------------------------
for key in ['max', 'mean', 'aval', 'carrinho']:
    if key not in st.session_state:
        st.session_state[key] = [0] if key != 'carrinho' else []

df = {}

# -----------------------------
# Colunas principais
# -----------------------------
col_a, col_e, col_i = st.columns(3)

try:
    if op == '👥 Clientes':
        # -------- MOBILIÁRIO --------
        with col_a:
            for item in mob.items():
                nome, preco = item
                img_path = os.path.join('images', f'{nome}.jpg')
                if os.path.exists(img_path):
                    st.image(img_path)
                else:
                    st.warning(f"Imagem não encontrada: {img_path}")

                # Número de unidades
                pr = st.number_input(
                    f'Para adicionar **{nome}** Coloque o número 1', 0, 1, 0
                ) if nome in mob_especiais else st.number_input(
                    f'Número de {nome}', 0, 100, 0
                )

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
                            df_item = {
                                'Data': pd.to_datetime(datetime.now()),
                                'Categorias': nome,
                                'Qtd': pr,
                                'Preço': preco,
                                'Valor': pr*preco
                            }
                            st.session_state.carrinho.append(df_item)
                            st.toast(f"{pr}x{nome} no carrinho ✅!", icon="🎉")
                with i:
                    st.write(f'Preço: {preco} Mts/unit')

        # -------- ALIMENTOS --------
        with col_e:
            for item in alim.items():
                nome, preco = item
                img_path = os.path.join('images', f'{nome}.jpg')
                if os.path.exists(img_path):
                    st.image(img_path)
                else:
                    st.warning(f"Imagem não encontrada: {img_path}")

                pr = st.number_input(
                    f'Para adicionar **{nome}** Coloque o número 1', 0, 1, 0
                ) if nome in alim_especiais else st.number_input(
                    f'Número de {nome}', 0, 100, 0
                )

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
                            df_item = {
                                'Data': pd.to_datetime(datetime.now()),
                                'Categorias': nome,
                                'Qtd': pr,
                                'Preço': preco,
                                'Valor': pr*preco
                            }
                            st.session_state.carrinho.append(df_item)
                            st.toast(f"{pr}x{nome} no carrinho ✅!", icon="🎉")
                with i:
                    st.write(f'Preço: {preco} Mts/unit')

        # -------- ENTRETENIMENTO --------
        with col_i:
            for item in entr.items():
                nome, preco = item
                img_path = os.path.join('images', f'{nome}.jpg')
                if os.path.exists(img_path):
                    st.image(img_path)
                else:
                    st.warning(f"Imagem não encontrada: {img_path}")

                pr = st.number_input(
                    f'Para adicionar **{nome}** Coloque o número 1', 0, 1, 0
                ) if nome in entr_especiais else st.number_input(
                    f'Número de {nome}', 0, 100, 0
                )

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
                            df_item = {
                                'Data': pd.to_datetime(datetime.now()),
                                'Categorias': nome,
                                'Qtd': pr,
                                'Preço': preco,
                                'Valor': pr*preco
                            }
                            st.session_state.carrinho.append(df_item)
                            st.toast(f"{pr}x{nome} no carrinho ✅!", icon="🎉")
                with i:
                    st.write(f'Preço: {preco} Mts/unit')

        # -------- SIDEBAR CARRINHO --------
        with st.sidebar:
            st.title('Carrinho')
            data = pd.DataFrame(st.session_state.carrinho)
            data.to_excel('data_base/new_data.xlsx', index=False)
            select = st.selectbox('Selecione o número da linha ou index', options=data.index)
            del_button = st.button('Eliminar Item')
            if del_button:
                st.session_state.carrinho.pop(select)
                st.rerun()
            st.dataframe(data)
            st.metric(f"O Pagamento total", f"{data['Valor'].sum():.2f} Mts")

            keep = st.button('Adicionar ao Banco de Dados')
            if keep:
                st.success('Dados adicionados ao banco de dados com Sucesso.')
                df_concat = pd.concat([new_data, data_base], ignore_index=True)
                df_concat.to_excel('data_base/data.xlsx', index=False)
                st.dataframe(df_concat)
                st.session_state.aval.append(data_base['Valor'].sum())
                st.session_state.mean.append(data_base['Valor'].mean())
                st.session_state.max.append(data_base['Valor'].max())

# ------------------------------------------------------
# Restante do código (Financeiro, Bancos de Dados, etc.)
# permanece igual, só ajustando imagens da mesma forma
# ------------------------------------------------------

except:
    st.empty()























