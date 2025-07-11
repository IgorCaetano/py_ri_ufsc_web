import streamlit as st

from typing import Callable, Any
from py_ri_ufsc.get_metadata.utils import get_available_values_in_dataset,get_available_columns_in_dataset


@st.cache_data
def load_filter_options():
    """
    Carrega todas as opções de filtro de uma vez.
    O resultado é cacheado para execuções futuras.
    """
    # Função auxiliar para obter valores únicos e ordenados
    def get_unique_sorted_values(values: list[str]):
        # Adicionado sorted() para melhor UX nos filtros
        return sorted(set(values))

    # OBS: Para otimizar ainda mais, o ideal seria carregar o dataset
    # uma única vez aqui, em vez de chamar get_available_values_in_dataset
    # repetidamente. Veja a dica de bônus no final.
    s_p_type_options = [v.split(" (")[0] for v in get_available_values_in_dataset("type") if v.split(" (")[0].strip()]
    s_p_course_options = [v.split(" (")[0] for v in get_available_values_in_dataset("course") if v.split(" (")[0].strip()]
    s_p_lang_options = [v.split(" (")[0] for v in get_available_values_in_dataset("language") if v.split(" (")[0].strip()]
    s_p_type_course_options = [v.split(" (")[0] for v in get_available_values_in_dataset("type_course") if v.split(" (")[0].strip()]
    s_p_centro_options = [v.split(" (")[0] for v in get_available_values_in_dataset("centro") if v.split(" (")[0].strip()]
    s_p_campus_options = [v.split(" (")[0] for v in get_available_values_in_dataset("campus") if v.split(" (")[0].strip()]

    s_p_options = {
        "type": get_unique_sorted_values(s_p_type_options),
        "course": get_unique_sorted_values(s_p_course_options),
        "language": get_unique_sorted_values(s_p_lang_options),
        "type_course": get_unique_sorted_values(s_p_type_course_options),
        "centro": get_unique_sorted_values(s_p_centro_options),
        "campus": get_unique_sorted_values(s_p_campus_options),
        "available_columns": get_available_columns_in_dataset()
    }
    return s_p_options

def show_tooltip(text: str, width: int = 350):
    """
    Exibe um ícone ℹ️ com tooltip ao passar o mouse.

    Args:
        text (str): Texto que aparecerá no balão.
        width (int): Largura do balão em pixels (padrão: 250).
    """
    st.markdown(f"""
        <style>
        .tooltip {{
          position: relative;
          display: inline-block;
          cursor: pointer;
        }}

        .tooltip .tooltiptext {{
          visibility: hidden;
          width: {width}px;
          background-color: #555;
          color: #fff;
          text-align: left;
          border-radius: 6px;
          padding: 8px;
          position: absolute;
          z-index: 1;
          bottom: 125%;
          left: 50%;
          margin-left: -{width//2}px;"
          opacity: 0;
          transition: opacity 0.3s;
        }}

        .tooltip:hover .tooltiptext {{
          visibility: visible;
          opacity: 1;
        }}
        </style>

        <div class="tooltip">ℹ️
          <span class="tooltiptext">{text}</span>
        </div>
    """, unsafe_allow_html=True)

def st_with_tooltip(component_fn: Callable[..., Any], label: str, tooltip_text: str, *args, **kwargs):
    col_a, col_b = st.columns([10, 1])
    with col_a:
        value = component_fn(label, *args, **kwargs) #,key=uuid.uuid4()
    with col_b:
        show_tooltip(tooltip_text)
    return value
