import streamlit as st
from py_ri_ufsc.get_metadata.main import get_filtered_dataset_for_main_graphs
from utils import generate_pdf_from_filtered_data,generate_excel_from_df,plotly_fig_to_image

from .utils import load_filter_options,st_with_tooltip
from graphs_codes import plot_gender_pie,plot_language_pie,plot_line_by_year,plot_line_by_year_and_gender

# if st.session_state.current_page != 'Registros':
#     st.session_state.p_df_filtrado = None

# st.session_state.current_page = 'Registros'


def registers_page():
    st.markdown("""
        <style>
            .main {
                padding-left: 5rem !important;
                padding-right: 5rem !important;
            }            
        </style>
    """, unsafe_allow_html=True)

    st.title("🔍 Análise de Registros")
    st.markdown("### Aplique filtros para gerar o gráfico:")

    if st.session_state.get('current_page',False) != 'Registros':
        st.session_state['p_df_filtrado'] = None
        st.session_state["p_filters_applied"] = False
        st.session_state['current_page'] = 'Registros'

    if "p_filters_applied" not in st.session_state:
        st.session_state["p_filters_applied"] = False

    if "p_df_filtrado" not in st.session_state:
        st.session_state.p_df_filtrado = None

    if "p_filter_options" not in st.session_state:
        with st.spinner("🔄 Carregando opções de filtro pela primeira vez..."):
            st.session_state.p_filter_options = load_filter_options()
    p_options = st.session_state.p_filter_options


    st.warning('Itens sem data no registro serão excluídos desta análise')
    # p_use_date_filter = st_with_tooltip(st.checkbox,
    #                                       "Usar filtro de datas",
    #                                       'Selecione a caixinha "Usar filtro de datas" se você quer ter somente resultados com registros que possuem datas.',
    #                                       value=True)   

    # p_exclude_empty_dates = st_with_tooltip(st.checkbox,
    #                                           "Excluir itens sem data",
    #                                           'Exclui registros que não tem sua data especificado/identificado.') 

    p_selected_year_range = st_with_tooltip(st.slider,
                                              "Ano (intervalo inclusivo)",
                                              'Selecione o ano inicial e o ano final para compor seus resultados. Os anos são inclusivos, então os anos do intervalo entrarão para os resultados também.',
                                              1960,2025,(2002,2025))
    
    with st.expander("Filtros gerais"):    
        p_selected_types = st_with_tooltip(st.multiselect,
                                             "Tipo de registro",
                                             'Escolha o tipo de registro que você gostaria de visualizar nos resultados. Exemplos mais comuns são "Artigo", "Tese", "Dissertação", "TCC", etc.',
                                             options=p_options["type"],
                                             placeholder="Sem filtro aplicado")
        p_exclude_empty_type = st_with_tooltip(st.checkbox,
                                                 "Excluir itens sem tipo",
                                                 'Exclui registros que não tem seu tipo especificado/identificado.')

        p_selected_languages = st_with_tooltip(st.multiselect,
                                                 "Idioma",
                                                 'Escolha o idioma que você gostaria de visualizar nos resultados. Exemplos mais comuns são "por" para portugês, "eng" para inglês e "spa" para espanhol.',
                                                 options=p_options["language"],
                                             placeholder="Sem filtro aplicado")
        p_exclude_empty_lang = st_with_tooltip(st.checkbox,
                                                 "Excluir itens sem idioma",
                                                 'Exclui registros que não tem seu idioma especificado/identificado.')

    with st.expander("Filtros específicos"):
        p_selected_courses = st_with_tooltip(st.multiselect,
                                               "Curso",
                                               "Escolha os cursos dos registros que deseja Excluir. Os nomes vêm do metadado 'curso' dos autores.",
                                               options=p_options["course"],
                                             placeholder="Sem filtro aplicado")        

        p_exclude_empty_course = st_with_tooltip(st.checkbox,
                                                   "Excluir itens sem curso",
                                                   "Exclui registros que não têm curso especificado/identificado.",
                                                   value=True)

        p_selected_type_courses = st_with_tooltip(st.multiselect,
                                                    "Tipo de Curso",
                                                    "Filtra por tipo de curso, como graduação (GRAD) e pós-graduação (POS).",
                                                    options=p_options["type_course"],
                                             placeholder="Sem filtro aplicado")
        
        p_exclude_empty_type_course = st_with_tooltip(st.checkbox,
                                                        "Excluir itens sem tipo de curso identificado",
                                                        "Exclui registros que não têm tipo de curso especificado/identificado.",
                                                        value=True)
        
        p_selected_centros = st_with_tooltip(st.multiselect,
                                               "Centro",
                                               "Filtra os registros por centro de ensino responsável.",
                                               options=p_options["centro"],
                                             placeholder="Sem filtro aplicado")        

        p_exclude_empty_centro = st_with_tooltip(st.checkbox,
                                                   "Excluir itens sem centro",
                                                   "Exclui registros que não têm centro especificado/identificado.",
                                                    value=True)
        
        p_selected_campuses = st_with_tooltip(st.multiselect,
                                                "Campus",
                                                "Filtra os registros por campus da universidade.",
                                                options=p_options["campus"],
                                             placeholder="Sem filtro aplicado")
        
        p_exclude_empty_campus = st_with_tooltip(st.checkbox,
                                                   "Excluir itens sem campus",
                                                   "Exclui registros que não têm campus especificado/identificado.",
                                                   value=True)
            
    with st.expander("Filtros adicionais"):
        p_selected_genders = st_with_tooltip(st.multiselect,
                                               "Gênero dos autores",
                                               "Filtra por gênero dos autores. 'F' para feminino, 'M' para masculino.",
                                               options=["F", "M"],
                                             placeholder="Sem filtro aplicado")
        
        p_include_only_selected_gender = st_with_tooltip(st.checkbox,
                                                           "Incluir itens somente do gênero selecionado",
                                                           "Inclui apenas registros onde todos os autores possuem o(s) gênero(s) selecionado(s).")
        
        p_exclude_empty_genders = st_with_tooltip(st.checkbox,
                                                 "Excluir itens sem gênero dos autores",
                                                 'Exclui registros que não tem seus gêneros de autores identificado.')

        p_title_keywords = st_with_tooltip(st.text_input,
                                             "Palavras no título (separadas por ;)",
                                             "Digite palavras-chave que devem aparecer no título dos registros. Separe com ponto e vírgula.",
                                             placeholder="Sem filtro aplicado")

        p_match_all_title_words = st_with_tooltip(st.checkbox,
                                                    "Incluir itens que apresentem TODAS as palavras",
                                                    'Quando marcado, exige que TODOS os termos/palavras listados estejam presentes no título.')
        
        p_exclude_empty_titles = st_with_tooltip(st.checkbox,
                                                 "Excluir itens sem título",
                                                 'Exclui registros que não tem seu título especificado/identificado.',
                                                 value=True)

        p_subjects_keywords = st_with_tooltip(st.text_input,
                                                "Assuntos (separadas por ;)",
                                                "Filtra por palavras que devem aparecer no campo de assunto. Separe com ponto e vírgula.",
                                             placeholder="Sem filtro aplicado")

        p_match_all_title_subjects = st_with_tooltip(st.checkbox,
                                                       "Incluir itens que apresentem TODOS os assuntos",
                                                       "Quando marcado, exige que TODOS os assuntos listados estejam presentes no registro.")
        
        p_exclude_empty_subjects = st_with_tooltip(st.checkbox,
                                                 "Excluir itens sem assuntos",
                                                 'Exclui registros que não tem seus assuntos especificados/identificados.',
                                                 value=True)

        p_author_names = st_with_tooltip(st.text_input,
                                           "Nome(s) do(s) autor(es) (separados por ;)",
                                           "Filtra registros que contenham os nomes dos autores listados. Separe com ponto e vírgula. NÃO DEIXE de inserir o primeiro nome da pessoa para buscar adequadamente.",
                                             placeholder="Sem filtro aplicado")

        p_match_all_authors = st_with_tooltip(st.checkbox,
                                                "Incluir itens que apresentem TODOS os autores",
                                                "Quando marcado, exige que TODOS os autores informados estejam no registro.",
                                                value=True)
        
        p_exclude_empty_authors = st_with_tooltip(st.checkbox,
                                                 "Excluir itens sem autores",
                                                 'Exclui registros que não tem seus autores especificados/identificados.',
                                                 value=True)

        p_advisor_names = st_with_tooltip(st.text_input,
                                            "Nome(s) do(s) orientador(es) (separados por ;)",
                                            "Filtra registros que contenham os nomes dos orientadores listados. Separe com ponto e vírgula. NÃO DEIXE de inserir o primeiro nome da pessoa para buscar adequadamente.",
                                             placeholder="Sem filtro aplicado")

        p_match_all_title_advisors = st_with_tooltip(st.checkbox,
                                                       "Incluir itens que apresentem todos os orientadores",
                                                       "Quando marcado, exige que todos os orientadores listados estejam no registro.",
                                                       value=True)
        
        p_exclude_empty_advisors = st_with_tooltip(st.checkbox,
                                                 "Excluir itens sem orientadores",
                                                 'Exclui registros que não tem seus orientadores especificados/identificados.',
                                                 value=True)


    st.markdown("#### Por favor, clique em aplicar filtros para executar a filtragem.")
    p_aplicar = st_with_tooltip(st.button,
                                  "✅ Aplicar filtros",
                                  'Clique em "Aplicar filtros" para aplicar os filtros e gerar dados filtrados.')
   
    if p_aplicar:        
        with st.spinner("Aplicando filtros..."):
            p_df_filtrado_calculado = get_filtered_dataset_for_main_graphs(
                type_filter={"use":bool(p_selected_types),"types":p_selected_types,"exclude_empty_values":p_exclude_empty_type},
                date_filter={"use": True, "date_1": p_selected_year_range[0], "date_2": p_selected_year_range[1],"exclude_empty_values":True},
                title_filter={"use": bool(p_title_keywords), "words": p_title_keywords.split(';'), "match_all": p_match_all_title_words,"exclude_empty_values":p_exclude_empty_titles},
                subjects_filter={"use": bool(p_subjects_keywords), "subjects": p_subjects_keywords.split(';'), "match_all": p_match_all_title_subjects,"exclude_empty_values":p_exclude_empty_subjects},
                authors_filter={"use": bool(p_author_names), "author_names": p_author_names.split(';'), "match_all": p_match_all_authors,"exclude_empty_values":p_exclude_empty_authors},
                advisors_filter={"use": bool(p_advisor_names), "advisor_names": p_advisor_names.split(';'), "match_all": p_match_all_title_advisors,"exclude_empty_values":p_exclude_empty_advisors},
                gender_filter={"use": bool(p_selected_genders), "genders": p_selected_genders, "just_contain": not p_include_only_selected_gender,"exclude_empty_values":p_exclude_empty_genders},
                language_filter={"use": bool(p_selected_languages), "languages": p_selected_languages, "exclude_empty_values": p_exclude_empty_lang},
                course_filter={"use": bool(p_selected_courses), "courses": p_selected_courses, "exclude_empty_values": p_exclude_empty_course},
                type_course_filter={"use": bool(p_selected_type_courses), "type_courses": p_selected_type_courses, "exclude_empty_values": p_exclude_empty_type_course},
                centro_filter={"use": bool(p_selected_centros), "centros": p_selected_centros, "exclude_empty_values": p_exclude_empty_centro},
                campus_filter={"use": bool(p_selected_campuses), "campuses": p_selected_campuses, "exclude_empty_values": p_exclude_empty_campus}
            ) # exported_columns=['language','gender_name','year'] # já botei como padrão no retorno da função get_filtered_dataset_for_main_graphs()
            
            st.session_state.p_df_filtrado = p_df_filtrado_calculado

    if st.session_state.p_df_filtrado is not None:
        p_df_para_exibir = st.session_state.p_df_filtrado
        p_amount_of_results = len(p_df_para_exibir)

        if p_amount_of_results > 0:
            st_with_tooltip(st.success,
                            f"{p_amount_of_results} resultados encontrados.",
                            "Este é o número de registros nos seus resultados.")
        else:
            st_with_tooltip(st.error,
                            f"Nenhum resultado encontrado para os filtros aplicados.",
                            "Parece que não foi encontrado nenhum registro que satisfaça seus filtros.")


        st.subheader("📈 Gráfico de Registros por Ano")

        if st.session_state.p_df_filtrado.empty:
            st.warning("Nenhum dado disponível para gerar visualizações e/ou arquivos...")
        else:            

            genero_usado = bool(p_selected_genders)
            separar_por_genero = False  # valor padrão

            if not genero_usado:
                separar_opcao = st.selectbox("Deseja separar o gráfico por gênero dos autores?", ["Não", "Sim"], index=0)
                separar_por_genero = (separar_opcao == "Sim")

            if separar_por_genero:
                fig = plot_line_by_year_and_gender(df=st.session_state.p_df_filtrado)
            else:
                fig = plot_line_by_year(df=st.session_state.p_df_filtrado)

            st.plotly_chart(fig, use_container_width=True)       

            st.divider()
            
            # ---------- GRÁFICOS DE PIZZA: LANGUAGE e GÊNERO ----------
            st.markdown("### 📊 Distribuição dos Registros por Idioma e Gênero")
            
            if st.session_state.p_df_filtrado.empty:
                st.warning("Nenhum dado disponível para gerar o gráfico.")
            else:
                col1, spacer, col2 = st.columns([1, 0.1, 1])

                with col1:
                    fig_lang = plot_language_pie(df=st.session_state.p_df_filtrado)

                    st.plotly_chart(fig_lang, use_container_width=True)            
                
                with spacer:
                    st.markdown("<div style='border-left: 1px solid #ccc; height: 100%; margin: auto;'></div>", unsafe_allow_html=True)

                with col2:
                    fig_gender = plot_gender_pie(df=st.session_state.p_df_filtrado)

                    st.plotly_chart(fig_gender, use_container_width=True)
            
            st.divider()

            filters_dict = {
                "ano": p_selected_year_range,
                "tipos": p_selected_types,
                "excluir tipos vazios": p_exclude_empty_type,
                "idiomas": p_selected_languages,
                "excluir idiomas vazios": p_exclude_empty_lang,
                "cursos": p_selected_courses,
                "excluir cursos vazios": p_exclude_empty_course,
                "tipos de curso": p_selected_type_courses,
                "excluir tipos de curso vazios": p_exclude_empty_type_course,
                "centros": p_selected_centros,
                "excluir centros vazios": p_exclude_empty_centro,
                "campi": p_selected_campuses,
                "excluir campi vazios": p_exclude_empty_campus,
                "gêneros": p_selected_genders,
                "incluir somente gêneros selecionados": p_include_only_selected_gender,
                "palavras no título": p_title_keywords,
                "palavras nos assuntos": p_subjects_keywords,
                "nomes dos autores": p_author_names,
                "nomes dos orientadores": p_advisor_names,
            }

            st.markdown("#### Aproveite para baixar os resultados em PDF para visualizá-los de outra forma ou baixar os dados utilizados em planilha (xlsx)")
            col3, spacer2, col4 = st.columns([1, 0.2, 1])

            with col3:
                insert_charts = st.checkbox("Inserir gráficos", key="insert_charts")            

                if st_with_tooltip(st.button,"Montar um relatório em PDF","Clique aqui para gerar um arquivo em PDF do seu relatório de consulta e disponibilizarmos o download posteriormente."):
                    if insert_charts:
                        st.warning("Por favor, aguarde. Estamos inserindo as imagens no documento PDF...")
                        img_gender_bytes = plotly_fig_to_image(fig_gender)
                        img_lang_bytes = plotly_fig_to_image(fig_lang)
                        img_chart_bytes = plotly_fig_to_image(fig)
                    else:
                        img_gender_bytes = None
                        img_lang_bytes = None
                        img_chart_bytes = None
                    with st.spinner("Preparando seu relatório PDF..."):

                        st.download_button("📥 Baixar relatório em PDF",
                                        data=generate_pdf_from_filtered_data(df_filtrado=st.session_state.p_df_filtrado,
                                                                    filters_dict=filters_dict,
                                                                    gender_split=separar_por_genero,
                                                                    img_fig_bytes=img_chart_bytes,
                                                                    img_lang_bytes=img_lang_bytes,
                                                                    img_gender_bytes=img_gender_bytes),
                                        file_name="relatorio.pdf",
                                        mime="application/pdf")

            with spacer2:
                st.markdown("<div style='border-left: 1px solid #ccc; height: 100%; margin: auto;'></div>", unsafe_allow_html=True)

            with col4:
                if p_amount_of_results<=5000:
                    st.warning('Arquivo leve')
                elif p_amount_of_results>5000 and p_amount_of_results<=30000:
                    st.warning('Arquivo levemente grande')
                elif p_amount_of_results>30000 and p_amount_of_results <= 50000:
                    st.warning('Arquivo relativamente grande')
                elif p_amount_of_results>50000:
                    st.warning('Arquivo grande')

                if st_with_tooltip(st.button,"Montar uma planilha com registros filtrados","Clique aqui para gerar um arquivo XLSX dos registros filtrados e disponibilizarmos o download posteriormente."):
                    with st.spinner("Preparando planilha..."):
                        st.download_button(
                            label="📥 Baixar registros filtrados numa planilha",
                            data=generate_excel_from_df(st.session_state.p_df_filtrado),
                            file_name="registros_filtrados.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
