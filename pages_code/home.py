import streamlit as st

# if 'current_page' not in st.session_state:
#     st.session_state.p_df_filtrado = None
# elif st.session_state.current_page != 'Início':
#     st.session_state.p_df_filtrado = None
# st.session_state.current_page = 'Início'


def home_page():
    st.title('👋 Página inicial')

    if st.session_state.get('current_page') != 'Início':
        st.session_state['p_df_filtrado'] = None
        st.session_state["p_filters_applied"] = False
        st.session_state['current_page'] = 'Início'

    st.markdown("# Bem-vindo(a) ao py_ri_ufsc_web!")

    st.html('<h2>👀 Visão geral</h2>')

    st.text("Esta é uma ferramenta voltada para exploração e coleta de metadados presentes no Repositório Institucional da Universidade Federal de Santa Catarina.")

    st.html('<h2>📑 Páginas</h2>')

    st.html('<h3>🔍 Registros 🔎</h3>')

    st.text('Nossa página mais completa, onde você conseguirá analisar a quantidade de registros ao decorrer dos anos aplicando uma variedade enorme de filtros. Além de visualizar aqui no site, você pode levar esse resultado "para casa", baixando um relatório da sua consulta em PDF ou até mesmo realizando o download dos registros filtrados em uma planilha!')

    st.html('<h3>💬 Assuntos 📊</h3>')

    st.text('Quem não gosta de saber quais são os tópicos mais discutidos no momento? E se desse para visualizar esses assuntos mais abordados por campus, centro, curso, tipo de registro (como TCCs, Teses ou Dissertações)? E se eu quiser ver qual o assunto mais abordado nos metadados desde que a UFSC começou a armazenar trabalhos no RI UFSC? Tudo isso é possível por meio desta página!')

    st.html('<h3>📤 Metadados 🗃️</h3>')

    st.text('Essa página é para os amantes de dados, que gostam de levar tudo que puderem para analisar "em casa"... Não precisa mais ser programador para acessar e baixar os metadados do RI UFSC! Resolvemos esse empecilho e também facilitamos a vida de todos os analistas, cientistas e engenheiros de dados que gostariam de trabalhar com os dados dos trabalhos da UFSC! Nesta página você pode aplicar filtros, escolher quais metadados levar dos registros e fazer o download no formato que mais lhe agradar, temos planilha (xlsx), CSV, JSON e até PARQUET para os programadores amantes de rapidez e agilidade.')

    st.html('<h2>🚧 Construção</h2>')

    st.text('Este é o resultado de um Projeto de Fim de Curso do aluno Igor Caetano de Souza, que está se tornando Engenheiro de Controle e Automação pela Universidade Federal de Santa Catarina.')

    st.html('<p>O site implementa uma interface web integrada a uma biblioteca Python chamada <i>py_ri_ufsc</i>, a qual tem os metadados do RI UFSC coletados e tratados, prontos para serem consultados e analisados da forma mais prática, eficaz e segura.</p>')

    st.html('<h2>💪 Motivação</h2>')

    st.html('<p>A ideia principal do projeto é dar acesso aos metadados de forma mais simples, rápida e sem sobrecarregar os servidores do site do RI UFSC. Além disso, por meio desta aplicação web, democratizamos o acesso e análise desses dados para qualquer pesquisador interessado, mesmo sem nenhuma noção de Python ou programação!</p>')   

    st.html('<h2>❗ Aviso</h2>')

    st.warning("Esta página ainda está em construção e terá a explicação de todo processo de Extração, Transformação e Armazenamento dos Metadados do RI UFSC, desde sua coleta até sua chegada aqui no site. Ademais terá informações pertinentes sobre todas as consultas que podem ser realizadas neste ambiente.")

    st.success("Espero que gostem e...")
    st.markdown('#### Façam bom proveito! :)')
