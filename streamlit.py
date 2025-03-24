import streamlit as st
import pandas as pd
import boto3
from PIL import Image
import requests
from io import BytesIO
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

load_dotenv()



def fetch_and_resize_image(url, size=(800, 800)):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img.resize(size, Image.LANCZOS)

def inicial():

    st.markdown("<h1 style='text-align: center;'>Classificação de Imagens dos PDXs</h1>", unsafe_allow_html=True)

    st.markdown("""
    <hr>
    <h2>🎯 Objetivos da Classificação</h2>
    <ul>
        <li><b>Notas</b> As notas devem ser dadas de 0 a 10, onde 0 é nenhum produto na loja e 10 é a loja completamente abastecida sem nenhum erro.</li>
        <li><b>Critérios</b> O critério de avaliação para dizer se uma loja é boa ou não é SIMPLISMENTE o preenchimento do espaço, ou seja, unicamente abastecimento.</li>
    </ul>
    <hr>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h2>🌟 Referências</h2>
    <p>As imagens a seguir são apenas para se utilizar de referência de lojas boas e lojas ruins</b></a>.</p>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)


def url_s3(pasta):
    aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name='us-east-2'
    )

    bucket_name = 'teste-gpt-imagem'

    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=f"{pasta}/")

    urls = []

    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']
            if key != f"{pasta}/":
                url = f"https://{bucket_name}.s3.{s3.meta.region_name}.amazonaws.com/{key}"
                urls.append(url)

    return urls

def loja_boa():
    st.markdown("<h1 style='text-align: center;'>Lojas boas com uma Classificação de nota 10:</h1>", unsafe_allow_html=True)
    fotos_boas = ["https://teste-gpt-imagem.s3.us-east-2.amazonaws.com/boas/boa_9.jpeg", "https://teste-gpt-imagem.s3.us-east-2.amazonaws.com/boas/2.jpg","https://teste-gpt-imagem.s3.us-east-2.amazonaws.com/boas/13.jpg"]
    
    col1, col2, col3 = st.columns(3)
    
    #Certifique-se de que há pelo menos 3 imagens disponíveis
    if len(fotos_boas) >= 3:
        image_urls = fotos_boas[:3]
        
        # Baixar e redimensionar todas as imagens de uma vez usando ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=3) as executor:
            resized_images = list(executor.map(
                lambda url: fetch_and_resize_image(url), 
                image_urls
            ))
        
        # Exibir as imagens já processadas
    with col1:
        st.image(resized_images[0], caption="Exemplo 1", use_container_width=True)
    with col2:
        st.image(resized_images[1], caption="Exemplo 2", use_container_width=True)
    with col3:
        st.image(resized_images[2], caption="Exemplo 3", use_container_width=True)



def loja_ruim():
    st.markdown("<h1 style='text-align: center;'>Lojas ruins com uma Classificação de nota 2:</h1>", unsafe_allow_html=True)
    fotos_ruins = ["https://teste-gpt-imagem.s3.us-east-2.amazonaws.com/ruins/queéisso.jpg", "https://teste-gpt-imagem.s3.us-east-2.amazonaws.com/ruins/ruim_12432.jpg", "https://teste-gpt-imagem.s3.us-east-2.amazonaws.com/ruins/seloco.jpg"]
    
    col1, col2, col3 = st.columns(3)
    
    # Certifique-se de que há pelo menos 3 imagens disponíveis
    if len(fotos_ruins) >= 3:
        image_urls = fotos_ruins[:3]
        
        # Baixar e redimensionar todas as imagens de uma vez usando ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=3) as executor:
            resized_images = list(executor.map(
                lambda url: fetch_and_resize_image(url), 
                image_urls
            ))
        
        # Exibir as imagens já processadas
    with col1:
        st.image(resized_images[0], caption="Exemplo 1", use_container_width=True)
    with col2:
        st.image(resized_images[1], caption="Exemplo 2", use_container_width=True)
    with col3:
        st.image(resized_images[2], caption="Exemplo 3", use_container_width=True)


def avaliacao():
    # Criar ou carregar o DataFrame (pode substituir pelo seu método de carregamento real)
    df = pd.DataFrame({
        'MAQUINA': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'FOTO': ['foto1.jpg', 'foto2.jpg', 'foto3.jpg', 'foto4.jpg', 'foto5.jpg', 'foto6.jpg', 'foto7.jpg', 'foto8.jpg', 'foto9.jpg', 'foto10.jpg'],
        'PICKLIST': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
        'URL': [
            'https://dk2a9ia2gb2sz.cloudfront.net/rotas/f730e85ec34fe81ba9c2459be2e5eed3.jpg',
            'https://dk2a9ia2gb2sz.cloudfront.net/rotas/76f38a68ba24eef8081f50feff915c66.jpg',
            'https://dk2a9ia2gb2sz.cloudfront.net/rotas/1121c88de33a47a4c94d3ff10f206098.jpg',
            'https://dk2a9ia2gb2sz.cloudfront.net/rotas/8b45a33a8610fd88d56408a831c534f9.jpg',
            'https://dk2a9ia2gb2sz.cloudfront.net/rotas/291cf569df680a87ce4626ff25208ee4.jpg',
            'https://dk2a9ia2gb2sz.cloudfront.net/rotas/69d31928c9aff6987dfd1f9bbe744a3b.jpg',
            'https://dk2a9ia2gb2sz.cloudfront.net/rotas/9a4b0312fad903e0802eaad029c0be4c.jpg',
            'https://dk2a9ia2gb2sz.cloudfront.net/rotas/58f77338a7c17a3409e78af6b56f776b.jpg',
            'https://dk2a9ia2gb2sz.cloudfront.net/rotas/693e5cbf7dba9dcfc7145f7b7e4476de.jpg',
            'https://dk2a9ia2gb2sz.cloudfront.net/rotas/ef2889d011805fe50d97e7fde85f34db.jpg'
        ]
    })
    
    # Inicializar variáveis de estado se ainda não existirem
    if 'index' not in st.session_state:
        st.session_state.index = 0
    
    # Garantir que avaliacoes seja sempre uma lista
    if 'avaliacoes' not in st.session_state or st.session_state.avaliacoes is None:
        st.session_state.avaliacoes = [None] * len(df)
    
    # Exibir o progresso
    progress = st.progress(st.session_state.index / len(df))
    st.write(f"Imagem {st.session_state.index + 1} de {len(df)}")
    
    # Mostrar a imagem atual
    if st.session_state.index < len(df):
        row = df.iloc[st.session_state.index]
        
        # Exibir a imagem em toda a largura
        st.image(row['URL'], caption=f"Foto {row['FOTO']}", width=450)#use_container_width=True
        
        # Exibir informações da imagem abaixo, em colunas para organização
        # info_col1, info_col2, info_col3 = st.columns(3)
        
        # with info_col1:
        #     st.write(f"**Máquina:** {row['MAQUINA']}")
        
        # with info_col2:
        #     st.write(f"**Picklist:** {row['PICKLIST']}")
        
        # with info_col3:
        #     st.write(f"**Data/Hora:** {row['DATAHORA_FIM']}")
        
        # Avaliação centralizada
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        
        # Obter nota atual ou usar o valor padrão
        nota_atual = 0
        if st.session_state.avaliacoes[st.session_state.index] is not None:
            nota_atual = st.session_state.avaliacoes[st.session_state.index]
        
        # Centralizar o input de nota
        col_nota = st.columns([1, 2, 1])
        with col_nota[1]:
            nota = st.number_input("Nota (0-10):", min_value=0, max_value=10, value=nota_atual, step=1, key=f"nota_{st.session_state.index}")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Botões de navegação abaixo, em uma linha
        col_btn1, col_prev, col_next, col_btn2 = st.columns([1, 1, 1, 1])
        
        with col_prev:
            # Mostra o botão sempre, mas desabilita quando estiver na primeira imagem
            disabled = st.session_state.index <= 0
            if st.button("Anterior", use_container_width=True, disabled=disabled):
                # Salvar a avaliação atual
                st.session_state.avaliacoes[st.session_state.index] = nota
                # Voltar para a imagem anterior
                st.session_state.index -= 1
                st.rerun()
        

        with col_next:
            if st.button("Próxima" if st.session_state.index < len(df) - 1 else "Finalizar", use_container_width=True):
                # Salvar a avaliação atual
                st.session_state.avaliacoes[st.session_state.index] = nota
                # Avançar para a próxima imagem
                st.session_state.index += 1
                st.rerun()
                
    
        st.warning("LEMBRE-SE - Todas as imagens devem ser avaliadas apenas no critério de quantidade disponíveis de produtos na loja")

    # Exibir resultados quando todas as imagens forem avaliadas
    else:
        st.success("Avaliação concluída!")
        
        # Criar um DataFrame com os resultados
        df_resultado = df.copy()
        df_resultado['AVALIACAO_MANUAL'] = st.session_state.avaliacoes
        
        # Exibir o DataFrame
        # st.write("Resumo das avaliações:")
        # st.dataframe(df_resultado)
        
        # Opção para baixar os resultados
        csv = df_resultado.to_csv(index=False).encode('utf-8')
        st.download_button("Baixar CSV", csv, "avaliacoes.csv", "text/csv")
        
        # Botão para reiniciar as avaliações
        if st.button("Avaliar novamente"):
            st.session_state.index = 0
            st.session_state.avaliacoes = [None] * len(df)
            st.rerun()


########################################################### EXIBIÇÃO ##########################################################
def pagina_home():
    # Inicializar o modo de classificação se não existir
    if 'modo_classificacao' not in st.session_state:
        st.session_state.modo_classificacao = False
    
    # Se o modo classificação estiver ativo, mostrar apenas a interface de classificação
    if st.session_state.modo_classificacao:
        avaliacao()
        
        # Botão para voltar à página inicial
        if st.button("Voltar à página inicial"):
            st.session_state.modo_classificacao = False
            st.rerun()
    else:
        # Exibir a página inicial normal
        inicial()
        loja_boa()
        loja_ruim()
        
        # Botão para iniciar a classificação no final da página
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>Pronto para começar?</h2>", unsafe_allow_html=True)
        
        if st.button("Começar Classificação", use_container_width=True):
            # Inicializar o estado para a classificação
            st.session_state.modo_classificacao = True
            st.session_state.index = 0
            # Avaliacoes será inicializado corretamente na função avaliacao()
            st.rerun()

def Main():
    pagina_home()

if __name__ == "__main__":
    Main()
    