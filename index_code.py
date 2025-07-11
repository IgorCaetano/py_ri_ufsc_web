import streamlit as st

from streamlit_option_menu import option_menu
from pages_code import home_page,registers_page,subjects_page,export_metadata_page

selected = option_menu(
    menu_title=None,
    options=['Início', 'Registros', 'Assuntos', 'Metadados'],
    icons=['house', 'graph-up', 'bar-chart-line-fill', 'file-earmark-arrow-down'],
    default_index=0,
    orientation="horizontal",
    styles={
    "container": {"padding": "0!important", "background-color": "#00000000", "border-radius": "5px"},
    "icon": {"color": "#6c757d", "font-size": "22px"}, 
    "nav-link": {
        "font-family": "Segoe UI, Roboto, sans-serif",
        "font-size": "16px", 
        "text-align": "left", 
        "margin":"0px", 
        "--hover-color": "#eee"
    },
    "nav-link-selected": {
        "background-color": "transparent",
        "color": "#007bff",
        "font-weight": "bold",
        "border-bottom": "2px solid #007bff"
    },
    # A cor do ícone selecionado é controlada pelo 'color' em 'nav-link-selected'
    "icon.nav-link-selected": {"color": "#007bff"} 
}
)

def main():
    if selected == 'Início':
        if 'current_page' not in st.session_state:
            st.session_state['current_page'] = 'Início'
        home_page()
    elif selected == 'Registros':
        registers_page()
    elif selected == 'Assuntos':
        subjects_page()
    elif selected == 'Metadados':        
        export_metadata_page()

if __name__=='__main__':
    main()
