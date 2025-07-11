import streamlit as st
import traceback

from py_ri_ufsc.get_metadata.main import get_filtered_dataset_for_main_graphs

from py_ri_ufsc.get_metadata.filters import filter_subjects
from py_ri_ufsc.common.for_strings import format_text

from .utils import load_filter_options,st_with_tooltip
from graphs_codes import plot_top_courses_by_year_and_subject,plot_top_subjects
from py_ri_ufsc.get_metadata.filters import filter_subjects
from py_ri_ufsc.common.for_strings import format_text

@st.cache_data(show_spinner=False)
def get_top_subjects_fig(df,show_just_words, remove_course_words):
    return plot_top_subjects(
        df=df,
        show_just_words=show_just_words,
        remove_course_words=remove_course_words,
        format_text_func=format_text
    )

# if st.session_state.get("current_page") != 'Assuntos':
#     st.session_state.p_df_filtrado = None
# st.session_state.current_page = 'Assuntos'

def subjects_page():
    st.markdown("""
        <style>
            .main { padding-left: 5rem !important; padding-right: 5rem !important; }
        </style>
    """, unsafe_allow_html=True)

    st.title("📊 Análise de Assuntos")
    st.markdown("### Aplique filtros antes de visualizar os resultados:")

    if st.session_state.get('current_page',False) != 'Assuntos':
        st.session_state['p_df_filtrado'] = None        
        st.session_state["p_filters_applied"] = False
        st.session_state['current_page'] = 'Assuntos'

    if "p_filters_applied" not in st.session_state:
        st.session_state["p_filters_applied"] = False

    if "p_df_filtrado" not in st.session_state:
        st.session_state.p_df_filtrado = None

    if "p_filter_options" not in st.session_state:
        with st.spinner("🔄 Carregando opções de filtro pela primeira vez..."):
            st.session_state.p_filter_options = load_filter_options()
    
    p_options = st.session_state.p_filter_options


    p_use_date_filter = st_with_tooltip(st.checkbox,
        "Usar filtro de datas",
        'Selecione a caixinha "Usar filtro de datas" se você quer ter somente resultados com registros que possuem datas.',
        value=True)

    p_exclude_empty_dates = st_with_tooltip(st.checkbox,
        "Excluir itens sem data",
        'Exclui registros que não têm sua data especificada/identificada.')

    p_selected_year_range = st_with_tooltip(st.slider,
        "Ano (intervalo inclusivo)",
        'Selecione o ano inicial e o ano final para compor seus resultados.',
        1960, 2025, (2002, 2025))

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
                type_filter={"use": bool(p_selected_types), "types": p_selected_types, "exclude_empty_values": p_exclude_empty_type},
                date_filter={"use": p_use_date_filter, "date_1": p_selected_year_range[0], "date_2": p_selected_year_range[1], "exclude_empty_values": p_exclude_empty_dates},
                title_filter={"use": bool(p_title_keywords), "words": p_title_keywords.split(';'), "match_all": p_match_all_title_words, "exclude_empty_values": p_exclude_empty_titles},
                subjects_filter={"use": bool(p_subjects_keywords), "subjects": p_subjects_keywords.split(';'), "match_all": p_match_all_title_subjects, "exclude_empty_values": p_exclude_empty_subjects},
                authors_filter={"use": bool(p_author_names), "author_names": p_author_names.split(';'), "match_all": p_match_all_authors, "exclude_empty_values": p_exclude_empty_authors},
                advisors_filter={"use": bool(p_advisor_names), "advisor_names": p_advisor_names.split(';'), "match_all": p_match_all_title_advisors, "exclude_empty_values": p_exclude_empty_advisors},
                gender_filter={"use": bool(p_selected_genders), "genders": p_selected_genders, "just_contain": not p_include_only_selected_gender, "exclude_empty_values": p_exclude_empty_genders},
                language_filter={"use": bool(p_selected_languages), "languages": p_selected_languages, "exclude_empty_values": p_exclude_empty_lang},
                course_filter={"use": bool(p_selected_courses), "courses": p_selected_courses, "exclude_empty_values": p_exclude_empty_course},
                type_course_filter={"use": bool(p_selected_type_courses), "type_courses": p_selected_type_courses, "exclude_empty_values": p_exclude_empty_type_course},
                centro_filter={"use": bool(p_selected_centros), "centros": p_selected_centros, "exclude_empty_values": p_exclude_empty_centro},
                campus_filter={"use": bool(p_selected_campuses), "campuses": p_selected_campuses, "exclude_empty_values": p_exclude_empty_campus},
                exported_columns=['subjects','course']
            )

            st.session_state.p_df_filtrado = p_df_filtrado_calculado
            st.session_state["p_filters_applied"] = True

    if st.session_state.get("p_filters_applied") and st.session_state.get("p_df_filtrado") is not None:
        p_df_para_exibir = st.session_state.p_df_filtrado
        p_amount_of_results = len(st.session_state.p_df_filtrado)

        if p_amount_of_results > 0:
            st_with_tooltip(st.success,
                            f"{p_amount_of_results} resultados encontrados.",
                            "Este é o número de registros nos seus resultados.")
        else:
            st_with_tooltip(st.error,
                            f"Nenhum resultado encontrado para os filtros aplicados.",
                            "Parece que não foi encontrado nenhum registro que satisfaça seus filtros.")    

        st.subheader("📈 Gráfico dos TOP 30 Assuntos")

        if st.session_state.p_df_filtrado.empty:
            st.warning("Nenhum dado disponível para gerar visualizações e/ou arquivos...")
        else:
            p_show_just_words = st_with_tooltip(
                st.checkbox,
                "Mostrar apenas palavras",
                "Se marcado, divide expressões como 'Engenharia de Materiais' em palavras separadas e remove palavras irrelevantes ('de', 'e', 'para' etc)."
                )

            p_remove_course_words = st_with_tooltip(
                st.checkbox,
                "Remover palavras genéricas da UFSC",
                "Se marcado irá tentar remover todas as palavras que fazem menção a um determinado curso da UFSC ou da instituição em si."
                )

            st.text('Ao passar o mouse pela imagem, clique no ícone "Fullscreen" para expandir e visualizar a imagem por completo!')
            try:
                with st.spinner("Gerando gráfico..."):
                    df_top, fig = get_top_subjects_fig(st.session_state.p_df_filtrado.copy(),
                                                       p_show_just_words,
                                                       p_remove_course_words)
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error('Lamentamos, mas não foi possível gerar o gráfico devido a um erro inesperado. Se puder, compartilhe sua busca com os desenvolvedores para tornar a ferramenta melhor! :)')
            else:
                st.session_state.df_top_subjects = df_top

            if "df_top_subjects" in st.session_state:
                st.subheader("📊 Gráficos específicos por assunto")
                top_assuntos = st.session_state.df_top_subjects['assunto'].to_list()
                if top_assuntos:
                    p_desired_subject_to_analyze = st_with_tooltip(st.multiselect,
                                                                        "Escolha o top assunto que deseja analisar ao decorrer do tempo:",
                                                                        "Escolha qual dos top assuntos exibidos você gostaria de ter uma visão mais aprofundada.",
                                                                        options=top_assuntos,
                                                                        placeholder='Não selecionado',
                                                                        max_selections=1)
                    # match_all_subjects_top_courses = st_with_tooltip(st.checkbox,"Conter todos os assuntos","Marque caso queira considerar apenas registros que contenham todos os assuntos. Desmarque se quiser considerar registros que tenham apenas 1 ou mais assuntos")
                    if p_desired_subject_to_analyze:
                        df_cleaned_years = st.session_state.p_df_filtrado[(st.session_state.p_df_filtrado['year']!='') & (st.session_state.p_df_filtrado['year']!='NÃO INDENTIFICADO')]
                        amount_df_cleaned_years = len(df_cleaned_years.index)
                        amount_df_filtrado = len(st.session_state.p_df_filtrado.index)
                        if amount_df_cleaned_years != amount_df_filtrado:
                            st.warning(f"{amount_df_filtrado-amount_df_cleaned_years} registros foram removidos para geração deste gráfico por não possuírem data identificada.")
                        try:
                            # fig = plot_top_courses_by_year_and_subject(st.session_state.p_df_filtrado, p_desired_subject_to_analyze)
                            with st.spinner("Gerando gráfico..."):
                                _,fig = plot_top_courses_by_year_and_subject(df=df_cleaned_years,
                                                                        subjects=p_desired_subject_to_analyze,
                                                                        filter_subjects_func=filter_subjects)
                                st.plotly_chart(fig, use_container_width=True)
                        except Exception as e:
                            st.error('Lamentamos, mas o gráfico não pode ser gerado. Provavelmente os registros não contém valor em alguma coluna necessária (data e/ou curso).')
                            # print(e)
                            # traceback.print_exc()
