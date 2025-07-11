import pandas as pd

from py_ri_ufsc.common.for_strings import format_text
from pages_code.utils import load_filter_options

STOPWORDS_PT = {
    'de', 'da', 'do', 'das', 'dos', 'e', 'a', 'o', 'as', 'os',
    'em', 'para', 'com', 'por', 'na', 'no', 'nas', 'nos',
    'um', 'uma', 'uns', 'umas', 'sobre', 'entre', 'ao', 'aos',
    'sim','não'
}

STOPWORDS_UFSC = [format_text(item,special_treatment=True)for item in load_filter_options()['course']] + \
['ufsc','sc','universidade','universidade_federal_de_santa_catarina','santa_catarina','florianopolis_sc',
 'clipping','portaria'] # clipping é para imagens, a priori, da própria universidade


def normalize_years_total(df: pd.DataFrame, year_col: str, year_range: tuple[int, int]) -> pd.DataFrame:
    """Retorna contagem por ano, preenchendo com 0 onde não houver registros."""
    all_years = pd.DataFrame({year_col: list(range(year_range[0], year_range[1] + 1))})
    actual_counts = df[year_col].value_counts().sort_index().reset_index()
    actual_counts.columns = [year_col, 'count']
    return all_years.merge(actual_counts, on=year_col, how='left').fillna(0).astype({year_col: int, 'count': int})


def normalize_years_by_group(df: pd.DataFrame,
                              year_col: str,
                              group_col: str,
                              count_col_name: str = "count",
                              year_range: tuple[int, int] = None) -> pd.DataFrame:
    """
    Garante que todos os anos dentro do intervalo desejado estejam presentes em cada grupo.

    Args:
        df (pd.DataFrame): DataFrame contendo as colunas de ano e grupo.
        year_col (str): Nome da coluna de ano.
        group_col (str): Nome da coluna de agrupamento (ex: gênero).
        count_col_name (str): Nome da coluna de contagem. Default: "count".
        year_range (tuple[int, int], optional): Intervalo desejado de anos (min, max). 
                                                Se None, será inferido dos dados.

    Returns:
        pd.DataFrame: DataFrame com todos os anos presentes para cada grupo e contagens preenchidas.
    """
    # Agrupa e conta os valores
    counts_df = df.groupby([year_col, group_col]).size().reset_index(name=count_col_name)

    # Determina intervalo de anos
    if year_range is None:
        year_min = df[year_col].min()
        year_max = df[year_col].max()
    else:
        year_min, year_max = year_range

    all_years = list(range(year_min, year_max + 1))
    all_groups = counts_df[group_col].unique()

    # Cria todas as combinações possíveis de ano e grupo
    full_index = pd.MultiIndex.from_product([all_years, all_groups], names=[year_col, group_col]).to_frame(index=False)

    # Junta com os dados reais e preenche com 0 onde faltarem
    normalized = pd.merge(full_index, counts_df, how='left', on=[year_col, group_col]).fillna(0)
    normalized[count_col_name] = normalized[count_col_name].astype(int)

    return normalized