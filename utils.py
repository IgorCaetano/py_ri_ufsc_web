import pandas as pd
import plotly.io as pio
import psutil

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
from reportlab.platypus import Image
from py_ri_ufsc.config import COMPLETED_DATA_PARQUET_FILE_PATH
from py_ri_ufsc.get_metadata.utils import get_raw_dataset


def print_ram_usage(prefix: str = ""):
    """
    Imprime o uso atual de memória RAM do sistema.

    Args:
        prefix (str): Texto opcional para incluir antes da mensagem.
    """
    mem = psutil.virtual_memory()
    used_gb = mem.used / (1024 ** 3)
    total_gb = mem.total / (1024 ** 3)
    percent = mem.percent
    print(f"{prefix}RAM usada: {used_gb:.2f} GB / {total_gb:.2f} GB ({percent}%)")

def get_ram_usage() -> float:
    return psutil.virtual_memory().used / (1024 ** 3)

def raw_dataframe_to_bytes(
        columns_to_use: list[str],
        filter_links: list[str],
        file_format: str  # 'csv', 'xlsx', 'json', 'parquet'
    ) -> BytesIO:
    
    output = BytesIO()
    drop_link_site = False

    # Garante que 'link_site' esteja presente para filtragem
    if 'link_site' not in columns_to_use:
        drop_link_site = True
        columns_to_use.append('link_site')

    # Carrega apenas as colunas necessárias
    df = get_raw_dataset(columns_to_use=columns_to_use)
    
    # Filtra pelas URLs desejadas
    df = df[df['link_site'].isin(filter_links)].copy()

    # Remove 'link_site' se não for solicitado originalmente
    if drop_link_site:
        df.drop(columns=['link_site'], inplace=True)
    
    # Exporta para o formato desejado
    file_format = file_format.lower().split()[0]
    
    if file_format == 'csv':
        df.to_csv(output, index=False,encoding='utf-8')
    elif file_format == 'xlsx':
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Dados')
        output.seek(0)
    elif file_format == 'json':
        # df.to_json(output, orient='records', force_ascii=False,indent=2)
        json_str = df.to_json(orient='records',force_ascii=False,indent=2)
        output.write(json_str.encode('utf-8'))        
    elif file_format == 'parquet':
        df.to_parquet(output, index=False)
    else:
        raise ValueError(f"Formato não suportado: {file_format}")

    df = None

    output.seek(0)

    return output

def plotly_fig_to_image(fig, width=800, height=500) -> BytesIO:
    img_bytes = pio.to_image(fig, format="png", width=width, height=height)
    return BytesIO(img_bytes)

def generate_excel_from_df(df: pd.DataFrame) -> BytesIO:
    output = BytesIO()
    # df.drop(columns=['gender_name','language'],inplace=True)
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Registros Filtrados')
    output.seek(0)
    return output

def generate_json_from_df(df: pd.DataFrame) -> BytesIO:
    output = BytesIO()
    json_str = df.to_json(orient='records', force_ascii=False, indent=2)
    output.write(json_str.encode('utf-8'))
    output.seek(0)
    return output

def generate_parquet_from_df(df: pd.DataFrame) -> BytesIO:
    output = BytesIO()
    df.to_parquet(output, index=False, engine='pyarrow')  # ou engine='fastparquet'
    output.seek(0)
    return output

def generate_csv_from_df(df: pd.DataFrame) -> BytesIO:
    output = BytesIO()
    csv_str = df.to_csv(index=False, encoding='utf-8')
    output.write(csv_str.encode('utf-8'))
    output.seek(0)
    return output

def generate_pdf_from_filtered_data(df_filtrado,
                                    filters_dict,
                                    gender_split: bool,
                                    img_fig_bytes,
                                    img_lang_bytes,
                                    img_gender_bytes) -> bytes:

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Helvetica', fontSize=11, leading=14))
    styles.add(ParagraphStyle(name='TitleH1', fontName='Helvetica-Bold', fontSize=16, leading=20, spaceAfter=6))
    styles.add(ParagraphStyle(name='TitleH2', fontName='Helvetica-Bold', fontSize=14, leading=18, spaceAfter=4, textColor=colors.HexColor('#003366')))
    styles.add(ParagraphStyle(name='TitleH3', fontName='Helvetica-Bold', fontSize=13, leading=20, spaceAfter=6))
    styles.add(ParagraphStyle(name='Info', fontName='Helvetica', fontSize=10, leading=12, spaceAfter=12))

    story = []

    # CAPA
    def draw_cover_page(canvas, doc):
        # --- Metadados do PDF ---
        canvas.setTitle("Relatório de Consulta - RI UFSC - py_ri_ufsc_web")
        canvas.setAuthor("py_ri_ufsc_web")
        canvas.setSubject("Análise de registros do Repositório Institucional da UFSC")
        canvas.setCreator("py_ri_ufsc_web (+ ReportLab)")
        canvas.setKeywords("UFSC, Relatório, Repositório Institucional, py_ri_ufsc_web")
        canvas.saveState()
        width, height = A4
        canvas.setFillColor(colors.HexColor('#003366'))
        canvas.rect(0, 0, width, height, fill=True, stroke=False)
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 22)
        canvas.drawCentredString(width / 2, height - 6 * cm, "RELATÓRIO DE CONSULTA")
        canvas.drawCentredString(width / 2, height - 7 * cm, "NOS REGISTROS FILTRADOS")
        canvas.drawCentredString(width / 2, height - 8 * cm, "DO REPOSITÓRIO INSTITUCIONAL")
        canvas.drawCentredString(width / 2, height - 9 * cm, "DA UFSC")
        canvas.setFont("Helvetica", 16)
        canvas.drawCentredString(width / 2, height - 14 * cm, "Análises usando dados provenientes da py_ri_ufsc")
        canvas.setFont("Helvetica-Oblique", 12)
        canvas.drawCentredString(width / 2, height - 16 * cm, f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        canvas.restoreState()

    story.append(PageBreak())

    # Resumo dos filtros
    story.append(Paragraph("Resumo dos Filtros".upper(), styles['TitleH1']))
    story.append(Paragraph("Filtros:", styles['TitleH2']))
    for key, value in filters_dict.items():
        # Tratar booleanos e listas
        if isinstance(value, bool):
            val_str = "Sim" if value else "Não"
        elif isinstance(value, (list, tuple, set)):
            val_str = ", ".join(str(v) for v in value) if value else "Não aplicado"
        else:
            val_str = str(value)
        story.append(Paragraph(f"<b>{key.replace('_', ' ').capitalize()}:</b> {val_str}", styles['Justify']))
    story.append(Spacer(1, 0.7*cm))

    story.append(Paragraph("Resumo dos Dados filtrados".upper(), styles['TitleH1']))
    story.append(Paragraph(f"Quantidade total de registros: <b>{len(df_filtrado)}</b>", styles['Justify']))
    story.append(Spacer(1, 0.5 * cm))

    if img_fig_bytes:
        story.append(Paragraph("Gráfico: Registros", styles['TitleH2']))
        story.append(Image(img_fig_bytes, width=16*cm, height=9*cm))
        story.append(Spacer(1, 0.5 * cm))
    # GRÁFICO DE REGISTROS POR ANO (COM OU SEM GÊNERO)    
    if gender_split:
        story.append(Paragraph("1. Distribuição por ano e gênero dos autores", styles['TitleH2']))
        df_gender = df_filtrado[['year', 'gender_name']].copy()
        df_gender['year'] = df_gender['year'].astype(int)
        df_gender['gender_name'] = df_gender['gender_name'].replace({'F': 'Feminino', 'M': 'Masculino', 'F,M':'Feminino,Masculino','M,F':'Masculino,Feminino', '': 'Não identificado'})
        df_gender = df_gender.assign(gender=df_gender['gender_name'].str.split(',')).explode('gender')
        grouped = df_gender.groupby(['year', 'gender']).size().reset_index(name='count')
        for year in sorted(grouped['year'].unique()):
            fem_amount = grouped[(grouped['year'] == year) & (grouped['gender']=='Feminino')]['count'].values
            if len(fem_amount):
                fem_amount = fem_amount[0]
            else:
                fem_amount = 0
            masc_amount = grouped[(grouped['year'] == year) & (grouped['gender']=='Masculino')]['count'].values            
            if len(masc_amount):
                masc_amount = masc_amount[0]
            else:
                masc_amount = 0
            non_specified_amount = grouped[(grouped['year'] == year) & (grouped['gender']=='Não identificado')]['count'].values
            if len(non_specified_amount):
                non_specified_amount = non_specified_amount[0]
            else:
                non_specified_amount = 0
            story.append(Paragraph(f"<b>Ano {year}</b>: {fem_amount+masc_amount+non_specified_amount} registros.", styles['Justify']))
            story.append(Paragraph(f"Feminino: {fem_amount} | Masculino: {masc_amount} | Não especificado: {non_specified_amount}", styles['Justify']))
            story.append(Spacer(1, 0.5 * cm))
            # for gender in grouped[grouped['year'] == year]['gender'].unique():
            #     count = grouped[(grouped['year'] == year) & (grouped['gender'] == gender)]['count'].values[0]
            #     story.append(Paragraph(f"{gender}: {count}", styles['Justify']))
    else:
        story.append(Paragraph("1. Distribuição por ano", styles['TitleH2']))
        year_counts = df_filtrado['year'].value_counts().sort_index()
        for year, count in year_counts.items():
            story.append(Paragraph(f"<b>{year}</b>: {count} registros.", styles['Justify']))

    story.append(Spacer(1, 0.5 * cm))

    # GRÁFICO DE PIZZA - LÍNGUA    
    story.append(Paragraph("2. Distribuição por idioma", styles['TitleH2']))
    if img_lang_bytes:
        story.append(Paragraph("Gráfico: Línguas", styles['TitleH3']))
        story.append(Image(img_lang_bytes, width=16*cm, height=9*cm))
        story.append(Spacer(1, 0.5 * cm))
    lang_counts = df_filtrado['language'].replace('', 'Não identificado').value_counts()
    total = lang_counts.sum()
    for lang, count in lang_counts.items():
        percent = round(100 * count / total, 2)
        story.append(Paragraph(f"<b>{lang}</b>: {count} registros ({percent}%).", styles['Justify']))

    story.append(Spacer(1, 0.5 * cm))

    # GRÁFICO DE PIZZA - GÊNERO
    story.append(Paragraph("3. Distribuição por gênero dos autores", styles['TitleH2']))
    if img_gender_bytes:
        story.append(Paragraph("Gráfico: Gêneros", styles['TitleH3']))
        story.append(Image(img_gender_bytes, width=16*cm, height=9*cm))
        story.append(Spacer(1, 0.5 * cm))
    df_gender_pizza = df_filtrado['gender_name'].fillna('').astype(str).str.replace(' ', '').replace('', 'NI')
    df_gender_pizza = df_gender_pizza.str.split(',').explode().replace({'F': 'Feminino', 'M': 'Masculino', 'NI': 'Não identificado'})
    gender_counts = df_gender_pizza.value_counts()
    total_gender = gender_counts.sum()
    for gender, count in gender_counts.items():
        percent = round(100 * count / total_gender, 2)
        story.append(Paragraph(f"<b>{gender}</b>: {count} registros ({percent}%).", styles['Justify']))

    story.append(Spacer(1, 1 * cm))

    doc.build(story, onFirstPage=draw_cover_page)
    buffer.seek(0)
    return buffer.read()
