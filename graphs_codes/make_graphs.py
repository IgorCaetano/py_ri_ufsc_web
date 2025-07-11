import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from collections import Counter
from typing import Any
from .utils import normalize_years_total,normalize_years_by_group
from py_ri_ufsc.get_metadata.filters import filter_subjects
from py_ri_ufsc.common.for_strings import format_text

from .utils import STOPWORDS_PT,STOPWORDS_UFSC

def plot_line_by_year(df: pd.DataFrame, year_col='year',) -> Any:
        year_range = (int(df['year'].min()),int(df['year'].max()))
        counts_by_year_df = normalize_years_total(df, year_col=year_col, year_range=year_range)
        fig = px.line(
            counts_by_year_df,
            x='year',
            y='count',
            markers=True,
            title='Quantidade total de Registros por Ano',
            labels={'year': 'Ano', 'count': 'Número de Registros'},
            template='plotly_white'
        )
        fig.update_layout(xaxis=dict(tickmode='linear', tickangle=-45))
        fig.update_traces(marker=dict(size=8, color='#007bff'), line=dict(width=2.5, color='#007bff'))
        return fig

def plot_line_by_year_and_gender(df: pd.DataFrame) -> Any:
    year_range = (int(df['year'].min()),int(df['year'].max()))
    df_gender = df[['year', 'gender_name']].copy()
    df_gender['year'] = df_gender['year'].astype(int)
    df_gender['gender_name'] = df_gender['gender_name'].replace({
        'F': 'Feminino', 'M': 'Masculino',
        'F,M': 'Feminino,Masculino', 'M,F': 'Masculino,Feminino',
        '': 'Não identificado'
    })
    df_gender = df_gender.assign(gender=df_gender['gender_name'].str.split(','))
    df_gender = df_gender.explode('gender')
    gender_counts = normalize_years_by_group(df_gender, year_col='year', group_col='gender', year_range=year_range)

    color_map = {'Feminino': '#9d3f96', 'Masculino': '#3f7f96', 'Não identificado': "#00FF0D"}
    fig = px.line(
        gender_counts,
        x='year',
        y='count',
        color='gender',
        markers=True,
        title='Quantidade de Registros por Ano e Gênero de autores',
        labels={'year': 'Ano', 'count': 'Número de Registros', 'gender': 'Gênero'},
        template='plotly_white',
        color_discrete_map=color_map
    )
    fig.update_layout(legend_title_text='Gênero dos autores', xaxis=dict(tickmode='linear', tickangle=-45))
    fig.update_traces(marker=dict(size=8), line=dict(width=2.5))
    return fig


def plot_language_pie(df: pd.DataFrame) -> Any:
    lang_counts = df['language'].replace('', 'Não identificado').value_counts()
    color_map = {
        'por': "#832929", 'eng': '#3f7f96', 'Não identificado': '#00FF0D',
        'fra': "#8F1F85", 'ita': "#25BAFF", 'spa': "#9B8922",
        'deu': "#AC7522", 'mul': "#0014C9", 'zxx': "#585858",
        'bzs': "#B4B4B4", 'por;eng': "#665015"
    }
    cores_modernas = lang_counts.index.map(color_map)
    fig = go.Figure(data=[go.Pie(
        labels=lang_counts.index,
        values=lang_counts.values,
        hole=.4,
        pull=[0.05 if i == 0 else 0 for i in range(len(lang_counts.index))],
        marker_colors=cores_modernas,
        insidetextorientation='radial'
    )])
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>Registros: %{value}<br>Porcentagem: %{percent}<extra></extra>",
        textfont_size=22
    )
    fig.update_layout(
        title={
            'text': '<b>Distribuição por Idioma</b>',
            'y': 0.95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top', 'font': {'size': 20}
        },
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        annotations=[dict(text='<b>Idiomas</b>', x=0.5, y=0.5, font_size=22, showarrow=False)],
        uniformtext_minsize=10, uniformtext_mode='hide'
    )
    return fig

def plot_gender_pie(df: pd.DataFrame) -> Any:
    df_gender_pizza = df['gender_name'].fillna('').astype(str).str.replace(' ', '').replace('', 'NI')
    df_gender_pizza = df_gender_pizza.str.split(',').explode()
    df_gender_pizza = df_gender_pizza.replace({'F': 'Feminino', 'M': 'Masculino', 'NI': 'Não identificado'})
    gender_counts = df_gender_pizza.value_counts().reset_index()
    gender_counts.columns = ['gender_label', 'count']

    color_map = {
        'Feminino': '#9d3f96', 'Masculino': '#3f7f96', 'Não identificado': '#00FF0D'
    }
    cores_ordenadas = gender_counts['gender_label'].map(color_map)
    fig = go.Figure(data=[go.Pie(
        labels=gender_counts['gender_label'],
        values=gender_counts['count'],
        hole=.4,
        pull=[0.05 if i == 0 else 0 for i in range(len(gender_counts.index))],
        marker_colors=cores_ordenadas,
        insidetextorientation='radial'
    )])
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>Registros: %{value}<br>Porcentagem: %{percent}<extra></extra>",
        textfont_size=22
    )
    fig.update_layout(
        title={
            'text': '<b>Distribuição por Gênero</b>',
            'y': 0.95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top', 'font': {'size': 20}
        },
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        annotations=[dict(text='<b>Gênero</b>', x=0.5, y=0.5, font_size=22, showarrow=False)],
        uniformtext_minsize=10, uniformtext_mode='hide'
    )
    return fig




def plot_top_subjects(
    df: pd.DataFrame,
    col_subjects: str = "subjects",
    top_n: int = 30,
    show_just_words: bool = False,
    remove_course_words: bool = False,
    stopwords_pt: set = STOPWORDS_PT,
    stopwords_ufsc: set = STOPWORDS_UFSC,
    format_text_func = format_text) -> tuple[pd.DataFrame,Any]:
    """
    Gera gráfico dos top assuntos (ou palavras) de um DataFrame.

    Parâmetros:
    - df: DataFrame contendo os dados
    - col_subjects: coluna que contém os assuntos (separados por ;)
    - top_n: número de itens mais frequentes a mostrar
    - show_just_words: se True, divide expressões compostas em palavras individuais
    - remove_course_words: se True, remove palavras relacionadas à UFSC
    - stopwords_pt: conjunto de palavras irrelevantes (português)
    - stopwords_ufsc: conjunto de palavras irrelevantes da UFSC
    - format_text_func: função usada para normalizar/verificar palavras (ex: format_text)

    Retorna:
    - fig: gráfico plotly com os assuntos
    - df_top: DataFrame com os assuntos e suas frequências
    """
    stopwords_pt = stopwords_pt or set()
    stopwords_ufsc = stopwords_ufsc or set()
    format_text_func = format_text_func or (lambda x, special_treatment=False: x)

    # Extrai assuntos
    assuntos_series = (
        df[col_subjects]
        .dropna()
        .astype(str)
        .str.split(';')
        .explode()
        .str.strip()
    )
    assuntos_series = assuntos_series[assuntos_series != ""]

    if show_just_words:
        assuntos_series = (
            assuntos_series
            .str.lower()
            .str.split()
            .explode()
            .str.strip()
        )
        assuntos_series = assuntos_series[
            (assuntos_series != "") & (~assuntos_series.isin(stopwords_pt))
        ]
        if remove_course_words:
            assuntos_series = [
                w for w in assuntos_series
                if len(w) > 1 and format_text_func(w, special_treatment=True) not in stopwords_ufsc
            ]
    elif remove_course_words:
        assuntos_series = (
            assuntos_series
            .str.lower()
            .str.strip()
        )
        assuntos_series = assuntos_series[
            (assuntos_series != "") & (~assuntos_series.isin(stopwords_pt))
        ]
        assuntos_series = [
            w for w in assuntos_series
            if len(w) > 1 and format_text_func(w, special_treatment=True) not in stopwords_ufsc
        ]

    contagem = Counter([
        item.upper()[:-1] if item and item[-1] in [',', ';', '.'] else item.upper()
        for item in assuntos_series
    ])

    df_top = (
        pd.Series(contagem)
        .nlargest(top_n)
        .reset_index()
        .rename(columns={'index': 'assunto', 0: 'frequencia'})
    )

    fig = px.bar(
        df_top.sort_values("frequencia"),
        x="frequencia",
        y="assunto",
        orientation="h",
        labels={"frequencia": "Frequência nos registros", "assunto": "Assunto"},
        color="frequencia",
        color_continuous_scale="Blues",
        title=f"Top {top_n} Assuntos"
    )
    fig.update_layout(yaxis=dict(tickfont=dict(size=10)))

    return df_top, fig

def plot_top_courses_by_year_and_subject(
    df: pd.DataFrame,
    subjects: list[str],
    match_all: bool = False,
    filter_subjects_func = filter_subjects) -> tuple[pd.DataFrame,Any]:
    """
    Gera gráfico dos Top 3 cursos por ano para os assuntos especificados.

    Parâmetros:
    - df: DataFrame contendo colunas 'subjects', 'year' e 'course'
    - subjects: lista de assuntos a serem filtrados
    - match_all: se True, todos os assuntos devem estar presentes
    - filter_subjects_func: função que aplica o filtro nos dados

    Retorna:
    - fig: gráfico plotly
    - df_resultado: DataFrame usado no gráfico
    """
    df = df.copy()
    if filter_subjects_func:
        df = filter_subjects_func(df=df, subjects=subjects, match_all=match_all)
    
    df = df[df['year'].notna() & (df['year'] != "")]
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df = df.dropna(subset=['year'])
    df = df[df['course'].notna() & (df['course'] != "")]

    if df.empty:
        return pd.DataFrame(),None

    grouped = df.groupby(['year', 'course']).size().reset_index(name='frequencia')
    top_cursos_ano = (
        grouped
        .sort_values(['year', 'frequencia'], ascending=[True, False])
        .groupby('year')
        .head(3)
    )

    anos = top_cursos_ano['year'].unique()
    cursos = top_cursos_ano['course'].unique()
    grid_completo = pd.MultiIndex.from_product([anos, cursos], names=["year", "course"]).to_frame(index=False)
    top_cursos_ano = pd.merge(grid_completo, top_cursos_ano, on=["year", "course"], how="left").fillna(0)
    top_cursos_ano['frequencia'] = top_cursos_ano['frequencia'].astype(int)

    fig = px.bar(
        top_cursos_ano,
        x="year",
        y="frequencia",
        color="course",
        barmode="group",
        labels={"frequencia": "Frequência", "year": "Ano", "course": "Curso"},
        title=f"Top 3 Cursos por ano com assunto{'s' if len(subjects) > 1 else ''}: {', '.join(subjects)}"
    )

    fig.update_layout(xaxis=dict(type='category'))

    return top_cursos_ano, fig
