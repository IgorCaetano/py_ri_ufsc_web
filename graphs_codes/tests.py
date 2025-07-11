import pandas as pd
import random

from typing import Any
from py_ri_ufsc.get_metadata.tests import generate_mock_df
from py_ri_ufsc.common.for_strings import format_text
from py_ri_ufsc.get_metadata.filters import filter_subjects
from .make_graphs import (
    plot_gender_pie,plot_language_pie,plot_line_by_year,
    plot_line_by_year_and_gender,plot_top_subjects,
    plot_top_courses_by_year_and_subject
)
from .utils import STOPWORDS_PT,STOPWORDS_UFSC

DIC_USE_YEARS = {"use":True,"values":list(range(1960,2025+1))+['']}
DIC_USE_AUTHORS = {"use":True,"values":["Silva, João", "Oliveira, Maria", "Souza, Ana", "Ferreira, Pedro",
                                        "Costa, Luana D. da", "Santos, Bruno F. dos", "Lima, Paula", "Almeida, Diego"]}
DIC_USE_ADVISORS = {"use":True,"values":['',"Pereira, Marcos A.", "Mendes, Juliana A. Souza de", "Barbosa, Carla", "Rocha, Felipe Júnior"]}
DIC_USE_GENDERS = {"use":True,"values":['F','M','F,M','']}
DIC_USE_TITLES = {"use":True,"values":['',"Análise de dados educacionais", "Estudo sobre inteligência artificial",
                                        "Impacto da pandemia na saúde pública", "Gestão financeira em pequenas empresas",
                                        "Direitos humanos e constituição", "Uso de energias renováveis",
                                        "Tecnologias assistivas na educação", "Aspectos legais da telemedicina",
                                        "Controle de qualidade em laboratórios", "Sustentabilidade na construção civil"]}
DIC_USE_COURSES = {"use":True,"values":['',"Engenharia Elétrica", "Administração", "Medicina", "Direito", "Pedagogia"]}
DIC_USE_TYPE_COURSES = {"use":True,"values":['','POS','GRAD']}
DIC_USE_TYPES = {"use":True,"values":['DISSERTAÇÃO MESTRADO','NÃO ESPECIFICADO','TCC','MONOGRAFIA','ARTIGO',
 'BOOK','OUTROS','TESE DOUTORADO','ARCHIVAL COLLECTION','VIDEO','SOUND',
 'DISSERTAÇÃO MESTRADO PROFISSIONAL','RELATÓRIO','CONFERENCE PROCEEDINGS','TESE DOUTORADO PROFISSIONAL',
 'CAP. DE LIVRO', 'TESE LIVRE DOCÊNCIA', 'WORKING PAPER','TCCP ESPECIALIZAÇÃO', 'RELATORIO PÓS-DOUTORADO', 'LIVRO', 'TESE', 'DISSERTAÇÃO',
 'RELATÓRIO ESTÁGIO EXTR', 'PLANILHA', 'TRABALHO CIENT.', 'TRANSCRIPTION', 'MAGAZINE ARTICLE', 'PORTARIA/CCB/2013', 'OFICIAL',
 'TESE MESTRADO', 'REVISTA', 'DISSERTAÇÃO DOUTORADO','ANAIS', 'DOSSIE','E-BOOK', 'RELATÓRIO TÉCNICO', 'PLANO_DE_AULA', 'DOCUMENTO',
 'PROJETO DE PESQUISA', 'TESE;DISSERTAÇÃO','APRESENTAÇÃO','RELATÓRIO TÉCNICO MESTRADO PROFISSIONAL']}
DIC_USE_DESCRIPTIONS = {"use":True,"values":['Dissertação (mestrado) - Universidade Federal de Santa Catarina, Centro Sócio Econômico, Programa de Pós-Graduação em Economia, Florianópolis, 2018.',
                        '',
                        'TCC (graduação) - Universidade Federal de Santa Catarina, Campus Curitibanos, Engenharia Florestal.',
                        'Dissertação (mestrado) - Universidade Federal de Santa Catarina, Centro de Filosofia e Ciências Humanas, Programa de Pós-Graduação em Antropologia Social, Florianópolis, 2013',
                        'Dissertação (mestrado) - Universidade Federal de Santa Catarina, Centro de Ciências Biológicas.',
                        'TCC Engenharia Civil de Infraestrutura - Universidade Federal de Santa Catarina. Campus Joinville. Engenharia de Infraestrutura.',
                        'Dissertação (mestrado) - Universidade Federal de Santa Catarina, Campus Joinville, Programa de Pós-Graduação em Engenharia e Ciências Mecânicas, Joinville, 2018.',
                        'Dissertação (mestrado profissional) - Universidade Federal de Santa Catarina, Campus Blumenau, Programa de Pós-Graduação em Matemática, Blumenau, 2023.',
                        'TCC(graduação) - Universidade Federal de Santa Catarina. Campus Curitibanos. Medicina Veterinária.',
                        'TCC (graduação) - Universidade Federal de Santa Catarina. Campus Joinville. Engenharia de Transportes e Logística.',
                        'TCC (graduação) - Universidade Federal de Santa Catarina. Campus Blumenau. Engenharia de Materiais',
                        'TCC(graduação) - Universidade Federal de Santa Catarina. Campus Curitibanos. Engenharia Florestal.',
                        'E-book confeccionado a partir das vivências do projeto de extensão/pesquisa "Desenvolv-Ninos: estimulando o desenvolvimento dos pequeninos" da Universidade Federal de Santa Catarina- Campus Araranguá.',
                        'TCC (graduação) - Universidade Federal de Santa Catarina, Campus Joinville, Engenharia Mecatrônica.',
                        'TCC (graduação) - Universidade Federal de Santa Catarina. Campus Joinville. Engenharia Naval.',
                        'TCC (graduação) - Universidade Federal de Santa Catarina. Campus Joinville. Engenharia de Infraestrutura.',
                        'Este livro possui dimensões 220mm x150mm, com 180 páginas encadernadas,costurado. O exemplar original pertence ao acervo do Laboratório de Estudos e Pesquisa Científica (LEPAC), da Universidade Federal da Paraíba – Campus I – João Pessoa/PB',
                        'TCC (graduação) - Universidade Federal de Santa Catarina. Centro de Ciências Rurais. Campus de Curitibanos. Agronomia.',
                        'TCC (graduação) - Universidade Federal de Santa Catarina. Campus Joinville. Engenharia Automotiva.',
                        'TCC (graduação) - Universidade Federal de Santa Catarina, Campus Blumenau, Engenharia de Controle e Automação.',
                        'TCC (graduação) - Universidade Federal de Santa Catarina. Campus Araranguá. Tecnologias da informação e comunicação',
                        'TCC (graduação) - Universidade Federal de Santa Catarina, Campus Curitibanos, Medicina Veterinária.',
                        'Os documentos encontram-se alocados no Arquivo e Memória Institucional (ARQMI) do Centro Federal de Educação Tecnológica de Minas Gerais - Campus I. Para mais informações acessar o endereço: https://www.arquivo.cefetmg.br/informacoes-gerais-oarqmi/ \n\nTambém, informações a respeito do documento encontram-se disponíveis no documento Fundo Escola de Aprendizes Artífices de Minas Gerais, que corresponde a um inventário de documentos oficiais relacionados à escola https://www.arquivo.cefetmg.br/wp-content/uploads/sites/104/2021/04/INVENTARIO-Fundo-1-compactado-1.pdf',
                        'Dissertação (mestrado profissional) - Universidade Federal de Santa Catarina, Campus Blumenau, Programa de Pós-Graduação em Nanociência, Processos e Materiais Avançados, Blumenau, 2022.',
                        'Dissertação (mestrado) - Universidade Federal de Santa Catarina, Campus Araranguá, Programa de Pós-Graduação em Energia e Sustentabilidade, Araranguá, 2021.',
                        'Este livro possui dimensões 185mm x135mm, com 369 páginas encadernadas costuradas. O exemplar original pertence ao  acervo do Laboratório de Estudos e Pesquisa Científica (LEPAC),  da Universidade Federal da Paraíba – Campus I – João Pessoa/PB',
                        'TCC (graduação)- Universidade Federal de Santa Catarina. Campus Curitibanos. Agronomia.',
                        'TCC (graduação) - Universidade Federal de Santa Catarina, Campus Joinville, Engenharia Naval.',
                        'TCC (graduação) - Universidade Federal de Santa Catarina, Campus Joinville, Engenharia Aeroespacial',
                        '',
                        'Dissertação (mestrado) - Universidade Federal de Santa Catarina, Centro de Filosofia e Ciências Humanas, Programa de Pós-Graduação em Antropologia Social, Florianópolis, 2013',
                        'Dissertação (mestrado) - Universidade Federal de Santa Catarina, Centro de Ciências Biológicas.',
                        'TCC (graduação) - Universidade Federal de Santa Catarina. Centro Tecnológico. Arquitetura',
                        'TCC (graduação) - Universidade Federal de Santa Catarina, Centro Tecnológico, Engenharia de Materiais.',
                        'Dissertação (mestrado) - Universidade Federal de Santa Catarina, Centro de Ciências da Saúde, Programa de Pós-Graduação em Saúde Coletiva, Florianópolis, 2013.',
                        'TCC(especialização) - Universidade Federal de Santa Catarina. Centro de Ciências da Saúde. Programa de Pós-graduação em Enfermagem. Linhas de Cuidado em Atenção Psicossocial',
                        'Este artigo encontra-se disponível no seguinte link: https://bell.unochapeco.edu.br/revistas/index.php/pedagogica/article/view/6872',
                        'Referente concessão de adicional de insalubridade a Cilene Lino de Oliveira.',
                        'TCC (graduação) - Universidade Federal de Santa Catarina, Campus Curitibanos, Engenharia Florestal.',
                        'TCC(graduação) - Universidade Federal de Santa Catarina. Centro Tecnológico. Engenharia de Controle e Automação.',
                        'Livro com 272 páginas. Disponível no seguinte link: https://gallica.bnf.fr/ark:/12148/bpt6k6549736b?rk=42918;4',
                        'Este arquivo encontra-se disponível fisicamente no acervo da Câmara Municipal de Ipiaú-BA.',
                        'TCC(graduação) - Universidade Federal de Santa Catarina.  Centro de Comunicação e Expressão. Design.',
                        'TCC (graduação) - Universidade Federal de Santa Catarina, Centro Sócio Econômico, Curso de Administração.',
                        "Organizado por Amassuru, el libro cuenta con el apoyo del Data + Feminism Lab (MIT), Women's and Gender Studies (MIT), el proyecto Datos Contra el Feminicidio, el Núcleo de Estudos de Gênero na Política Externa e Internacional (UFSC) y FES Colombia.",
                        'TCC(especialização) - Universidade Federal de Santa Catarina. Centro de Ciências da Educação. Departamento de Metodologia de Ensino. Educação na Cultura Digital.',
                        'TCC (graduação) - Universidade Federal de Santa Catarina. Centro Ciências Físicas e Matemáticas. Oceanografia',
                        'TCC(graduação) - Universidade Federal de Santa Catarina. Centro Tecnológico. Engenharia Sanitária e Ambiental.',
                        'TCC(Graduação) - Universidade Federal de Santa Catarina. Centro de Ciências da Saúde. Medicina.',
                        'Dissertação (mestrado) - Universidade Federal de Santa Catarina, Centro de Filosofia e Ciências Humanas. Programa de Pós-Graduação em Sociologia Política.',
                        'TCC (graduação) - Universidade Federal de Santa Catarina, Centro Sócio Econômico, Curso de Serviço Social.',
                        'Tese (doutorado) - Universidade Federal de Santa Catarina, Centro de Ciências Biológicas, Programa de Pós-Graduação em Neurociências, Florianópolis, 2018.',
                        '']}
DIC_USE_SUBJECTS = {"use":True,"values":["educação;tecnologia", "inteligência artificial;aprendizado de máquina",
                                        "saúde pública;covid-19", "finanças;empreendedorismo",
                                        "direitos humanos;constituição", "meio ambiente;sustentabilidade",
                                        "acessibilidade;inclusão", "tecnologia;medicina",
                                        "qualidade;ciência", "engenharia;sustentabilidade"]}
DIC_USE_SETSPECS = {"use":True,"values":['col_123456789_170541', 'col_123456789_79531', 'col_123456789_856', 'col_123456789_75030', 'col_123456789_140034', 'col_123456789_82371', 'col_123456789_7443', 'col_123456789_7448',
                                        'col_123456789_133779', 'col_123456789_154090', 'col_123456789_93473', 'col_123456789_163293', 'col_123456789_162909', 'col_123456789_7436', 'col_123456789_116633', 'col_123456789_231924',
                                        'col_123456789_156547', 'col_123456789_99518', 'col_123456789_100436', 'col_123456789_7447', 'col_123456789_1772', 'col_123456789_138303', 'col_123456789_234336', 'col_123456789_98963',
                                        'col_123456789_7515', 'col_123456789_112819', 'col_123456789_195580', 'col_123456789_154949', 'col_123456789_7480', 'col_123456789_182374', 'col_123456789_263527', 'col_123456789_166330',
                                        'col_123456789_126454', 'col_123456789_7493', 'col_123456789_124305', 'col_123456789_7439', 'col_123456789_75127', 'col_123456789_7483', 'col_123456789_81311', 'col_123456789_135862',
                                        'col_123456789_231692', 'col_123456789_174124', 'col_123456789_74648', 'col_123456789_214164', 'col_123456789_140254', 'col_123456789_138780', 'col_123456789_162913', 'col_123456789_153754',
                                        'col_123456789_252492',  'col_123456789_172197', 'col_123456789_201413',  'col_123456789_103512', 'col_123456789_114969', 'col_123456789_122482', 'col_123456789_195787', 'col_123456789_204789',
                                        'col_123456789_183391', 'col_123456789_242001', 'col_123456789_240457', 'col_123456789_220094','col_123456789_164995', 'col_123456789_170165', 'col_123456789_155827', 'col_123456789_221862',
                                        'col_123456789_163385', 'col_123456789_140878', 'col_123456789_1856','col_123456789_193039', 'col_123456789_105306','col_123456789_1671', 'col_123456789_147199', 'col_123456789_78570',
                                        'col_123456789_104649', 'col_123456789_182067', 'col_123456789_143920', 'col_123456789_249470', 'col_123456789_175009', 'col_123456789_231544', 'col_123456789_178873', 'col_123456789_116498',
                                        'col_123456789_202700', 'col_123456789_184908', 'col_123456789_7446', 'col_123456789_154478', 'col_123456789_181886', 'col_123456789_152387', 'col_123456789_212',
                                        'col_123456789_7445', 'col_123456789_167525', 'col_123456789_126469', 'col_123456789_142102', 'col_123456789_178045', 'col_123456789_141302', 'col_123456789_230024',
                                        'col_123456789_200694', 'col_123456789_257112', 'col_123456789_74758', 'col_123456789_257093', 'col_123456789_1204', 'col_123456789_139094', 'col_123456789_104475', 'col_123456789_160253',
                                        'col_123456789_196575', 'col_123456789_170112', 'col_123456789_152618', 'col_123456789_139925', 'col_123456789_133398', 'col_123456789_234158', 'col_123456789_182674',
                                        'col_123456789_126560', 'col_123456789_98965', 'col_123456789_238254', 'col_123456789_158993', 'col_123456789_7441', 'col_123456789_143294', 'col_123456789_137525',
                                        'col_123456789_155672', 'col_123456789_263150', 'col_123456789_194415', 'col_123456789_156387', 'col_123456789_163273', 'col_123456789_244944', 'col_123456789_259520',
                                        'col_123456789_209487', 'col_123456789_231920', 'col_123456789_169994', 'col_123456789_188618', 'col_123456789_183731', 'col_123456789_261024', 'col_123456789_195245',
                                        'col_123456789_141695', 'col_123456789_249427', 'col_123456789_123321', 'col_123456789_175746', 'col_123456789_158966', 'col_123456789_160304']}
DIC_USE_FULL_LOCATIONS = {"use":True,"values":['',"Acervos -> Campus Florianópolis -> CED (Centro de Ciências da Educação) -> História da Educação Matemática (l'Histoire de l'éducation mathématique) -> _Documentos Oficiais e Normativos....- BA",
 'Trabalhos Acadêmicos -> Trabalhos de Conclusão de Curso de Graduação -> TCC Design',
 'Acervos -> Campus Florianópolis -> CSE (Centro Socioeconômico) -> INPEAU (Instituto de Pesquisas e Estudos em Administração Universitária) -> Anais dos Colóquios Internacionais sobre Gestão Universitária -> XIII Colóquio Internacional sobre Gestão Universitária nas Américas',
 'Acervos -> Campus Florianópolis -> CFH (Centro de Filosofia e Ciências Humanas) -> Programa de Pós-Graduação em Antropologia Social da UFSC (PPGAS) -> Portarias',
  'Acervos -> Campus Florianópolis -> PROPESQ (Pró-Reitoria de Pesquisa) -> Programa de Iniciação Científica e Tecnológica da UFSC -> Seminário de Iniciação Científica e Tecnológica da UFSC -> 2021 -> Iniciação Científica - PIBIC e Programa Voluntário -> Ciências Exatas, da Terra e Engenharias -> Araranguá - Departamento de Computação (DEC)',
 'Trabalhos Acadêmicos -> Trabalhos de Conclusão de Curso de Graduação -> TCC Administração',
 'Acervos -> Campus Joinville -> Pós-Graduação Joinville -> Programa de Pós-Graduação em Engenharia e Ciências Mecânicas (Pós-ECM) -> Portarias (Pós-ECM) -> Coordenação -> Portarias 2018',
 'Acervos -> Campus Florianópolis -> CSE (Centro Socioeconômico) -> Departamento de Economia e Relações Internacionais -> Publicações técnico-científicas -> Livros',
 'Trabalhos Acadêmicos -> Trabalhos de Conclusão de Curso de Especialização -> Centro de Ciências da Educação (CED) -> TCC Especialização - Educação na Cultura Digital',
 'Acervos -> Campus Florianópolis -> PROPLAN (Pró-Reitoria de Planejamento) -> Departamento de Planejamento e Gestão da Informação - DPGI -> Cursos de Graduação',
 'Trabalhos Acadêmicos -> Trabalhos de Conclusão de Curso de Graduação -> TCC Oceanografia',
 'Trabalhos Acadêmicos -> Trabalhos de Conclusão de Curso de Graduação -> TCC Engenharia Sanitária e Ambiental',
 'Trabalhos Acadêmicos -> Trabalhos de Conclusão de Curso de Graduação -> TCC Medicina',
 'Teses e Dissertações -> Programa de Pós-Graduação em Sociologia Política',
 'Trabalhos Acadêmicos -> Trabalhos de Conclusão de Curso de Graduação -> TCC Serviço Social',
 'Teses e Dissertações -> Programa de Pós-Graduação em Neurociências',
 'Acervos -> Campus Florianópolis -> CSE (Centro Socioeconômico) -> INPEAU (Instituto de Pesquisas e Estudos em Administração Universitária) -> Anais dos Colóquios Internacionais sobre Gestão Universitária -> XV Colóquio Internacional de Gestão Universitária',
 'Acervos -> Campus Florianópolis -> CCE (Centro de Comunicação e Expressão) -> Secretaria do Centro de Comunicação e Expressão - CCE -> Portarias (CCE) -> Portarias (CCE) - 2004',
 'Teses e Dissertações -> Programa de Pós-Graduação em Ensino de Física (Mestrado Profissional)',
 'Teses e Dissertações -> Teses e dissertações do Centro Tecnológico',
 'Teses e Dissertações -> Programa de Pós-Graduação em Educação',
 'Trabalhos Acadêmicos -> Trabalhos de Conclusão de Curso de Graduação -> TCC Ciências Biológicas',
 'Acervos -> Campus Araranguá -> Centro de Ciências, Tecnologias e Saúde (CTS) do Campus Araranguá -> Departamento de Ciências da Saúde (DCS) -> Publicações técnico-científicas (DCS)',
 'Trabalhos Acadêmicos -> Trabalhos de Conclusão de Curso de Especialização -> Multidisciplinar -> TCC Especialização - Curso de Especialização em Permacultura',
 '',
 'Teses e Dissertações -> Programa de Pós-Graduação em Aquicultura',
 'Acervos -> Campus Florianópolis -> CED (Centro de Ciências da Educação) -> Coordenadoria de Apoio Administrativo -> Atos administrativos -> Portarias -> 2016',
 'Acervos -> Campus Florianópolis -> CCS (Centro de Ciências da Saúde) -> Departamento de Saúde Pública -> Telessaúde SC -> Telessaúde SC (vídeos)',
 'Teses e Dissertações -> Programa de Pós-Graduação em Engenharia de Produção',
 'Acervos -> Campus Florianópolis -> CSE (Centro Socioeconômico) -> INPEAU (Instituto de Pesquisas e Estudos em Administração Universitária) -> Anais dos Colóquios Internacionais sobre Gestão Universitária -> XIX Colóquio Internacional de Gestão Universitária',
 'Acervos -> Campus Florianópolis -> PROPESQ (Pró-Reitoria de Pesquisa) -> Programa de Iniciação Científica e Tecnológica da UFSC -> Seminário de Iniciação Científica e Tecnológica da UFSC -> 2022 -> Iniciação Científica - PIBIC e Programa Voluntário -> Ciências Exatas, da Terra e Engenharias -> Departamento de Engenharia Civil',
 'Trabalhos Acadêmicos -> Trabalhos de Conclusão de Curso de Graduação -> TCC Jornalismo',
 'Acervos -> Campus Florianópolis -> CSE (Centro Socioeconômico) -> Secretaria Administrativa do CSE -> Portarias CSE -> Portarias CSE 2023',
 'Teses e Dissertações -> Programa de Pós-Graduação em História',
 'Acervos -> Campus Florianópolis -> PROPESQ (Pró-Reitoria de Pesquisa) -> Programa de Iniciação Científica e Tecnológica da UFSC -> Divulgação Científica para a Comunidade -> Ciências da Vida -> Ciências da Vida (Vídeos)',
 'Acervos -> Campus Florianópolis -> Grupos e Núcleos Interdisciplinares -> Virtuhab/Labrestauro/MATEC -> MIX SUSTENTÁVEL -> Mix Sustentável',
 "Acervos -> Campus Florianópolis -> CED (Centro de Ciências da Educação) -> História da Educação Matemática (l'Histoire de l'éducation mathématique) -> CADERNOS ESCOLARES",
  'Acervos -> Campus Florianópolis -> PROPESQ (Pró-Reitoria de Pesquisa) -> Programa de Iniciação Científica e Tecnológica da UFSC -> Seminário de Iniciação Científica e Tecnológica da UFSC -> 2021 -> Iniciação Científica - PIBIC e Programa Voluntário -> Ciências Exatas, da Terra e Engenharias -> Araranguá - Departamento de Computação (DEC)',
 'Teses e Dissertações -> Teses e dissertações do Centro Sócio-Econômico',
 'Acervos -> Campus Florianópolis -> Biblioteca Universitária -> Materiais Iconográficos -> Tempo Editorial -> 600 Tecnologia (Ciências Aplicadas) -> Forte de Santo Antônio de Ratones',
 'Teses e Dissertações -> Programa de Pós-Graduação em Farmácia',
 'Acervos -> Campus Florianópolis -> CCE (Centro de Comunicação e Expressão) -> Jornalismo -> Rádio Ponto -> Acervo -> Radiojornalismo',
 'Trabalhos Acadêmicos -> Trabalhos de Conclusão de Curso de Graduação -> TCC Ciências Contábeis']}
DIC_USE_CAMPUS = {"use":True,"values":['','FLN','JOI','BNU','ARA','CUR']}
DIC_USE_CENTROS = {"use":True,"values":['','CCA','CCB','CCE','CCS','CCJ',
                                         'CDS','CED','CFH','CFM','CSE',
                                         'CTC','CTJ','CCR','CTE','CTS']}
DIC_USE_LANGUAGES = {"use":True,"values":['por','spa','fra','ita','eng','']}


def add_value_counts(df: pd.DataFrame, column: str, 
                     drop_duplicates: bool = True, 
                     sort_descending: bool = True) -> pd.DataFrame:
    """
    Adiciona uma coluna 'count' ao DataFrame com a contagem de ocorrências dos valores da coluna especificada.

    Parâmetros:
    - df: DataFrame de entrada
    - column: Nome da coluna a ser analisada
    - drop_duplicates: Se True, retorna apenas uma linha por valor único da coluna analisada
    - sort_descending: Se True, ordena o DataFrame pela contagem em ordem decrescente

    Retorna:
    - Um novo DataFrame com a coluna 'count' adicionada
    """
    df_copy = df.copy()
    df_copy['count'] = df_copy.groupby(column)[column].transform('count')

    if drop_duplicates:
        df_copy = df_copy[[column, 'count']].drop_duplicates()

    if sort_descending:
        df_copy = df_copy.sort_values(by='count', ascending=False).reset_index(drop=True)

    return df_copy


class WebTestRIUFSC():
    def __init__(self,
                 df : pd.DataFrame|None=None):
        self.df = df

    def test_plot_line_by_year(self,
                               df : pd.DataFrame|None = None,
                               year_col : str = 'year',
                               mock_df_lines_amount : int = 10,
                               mock_years : dict = DIC_USE_YEARS,
                               return_just_fig : bool = False) -> tuple[pd.DataFrame,Any]|Any:
        if (df is not None) and isinstance(df,pd.DataFrame):
            if 'year' not in df.keys():
                raise KeyError('Necessário coluna "year" no dataframe passado como parâmetro')
            fig = plot_line_by_year(df,year_col=year_col,year_range=(int(df['year'].min()),int(df['year'].max())))
            if not return_just_fig:
                return add_value_counts(df=df,column='year'),fig
            else:
                return fig
        elif self.df is not None and isinstance(self.df,pd.DataFrame):
            if 'year' not in self.df.keys():
                raise KeyError('Necessário coluna "year" no dataframe passado como parâmetro')
            fig = plot_line_by_year(self.df,year_col=year_col,year_range=(int(self.df['year'].min()),int(df['year'].max())))
            if not return_just_fig:
                return add_value_counts(df=self.df,column='year'),fig
            else:
                return fig
        else:
            df_mock = generate_mock_df(lines_amount=mock_df_lines_amount,
                                       years=mock_years)
            fig = plot_line_by_year(df_mock,year_col=year_col,year_range=(int(df_mock['year'].min()),int(df_mock['year'].max())))
            if not return_just_fig:
                return add_value_counts(df=df_mock,column='year'),fig
            else:
                return fig

    def test_plot_line_by_year_and_gender(self,
                               df : pd.DataFrame|None = None,
                               mock_df_lines_amount : int = 10,
                               mock_years : dict = DIC_USE_YEARS,
                               mock_genders : dict = DIC_USE_GENDERS,
                               return_just_fig : bool = False) -> tuple[pd.DataFrame,Any]|Any:
        if (df is not None) and isinstance(df,pd.DataFrame):
            if 'year' not in df.keys():
                raise KeyError('Necessário coluna "year" no dataframe passado como parâmetro')
            if 'gender_name' not in df.keys():
                raise KeyError('Necessário coluna "gender_name" no dataframe passado como parâmetro')
            fig = plot_line_by_year_and_gender(df,year_range=(int(df['year'].min()),int(df['year'].max())))
            if not return_just_fig:
                return df,fig
            else:
                return fig
        elif self.df is not None and isinstance(self.df,pd.DataFrame):
            if 'year' not in self.df.keys():
                raise KeyError('Necessário coluna "year" no dataframe passado como parâmetro')
            if 'gender_name' not in self.df.keys():
                raise KeyError('Necessário coluna "gender_name" no dataframe passado como parâmetro')
            fig = plot_line_by_year_and_gender(self.df,year_range=(int(self.df['year'].min()),int(df['year'].max())))
            if not return_just_fig:
                return self.df,fig
            else:
                return fig
        else:
            df_mock = generate_mock_df(lines_amount=mock_df_lines_amount,
                                       years=mock_years,
                                       genders=mock_genders)
            fig = plot_line_by_year_and_gender(df_mock,year_range=(int(df_mock['year'].min()),int(df_mock['year'].max())))
            if not return_just_fig:
                return df_mock,fig
            else:
                return fig

    def test_plot_language_pie(self,
                               df : pd.DataFrame|None = None,
                               mock_df_lines_amount : int = 10,
                               mock_languages : dict = DIC_USE_LANGUAGES,
                               return_just_fig : bool = False) -> tuple[pd.DataFrame,Any]|Any:
        if (df is not None) and isinstance(df,pd.DataFrame):
            if 'language' not in df.keys():
                raise KeyError('Necessário coluna "language" no dataframe passado como parâmetro')
            fig = plot_language_pie(df)
            if not return_just_fig:
                return add_value_counts(df=df,column='language'),fig
            else:
                return fig
        elif self.df is not None and isinstance(self.df,pd.DataFrame):
            if 'language' not in self.df.keys():
                raise KeyError('Necessário coluna "language" no dataframe passado como parâmetro')            
            fig = plot_language_pie(self.df)
            if not return_just_fig:
                return add_value_counts(df=self.df,column='language'),fig
            else:
                return fig
        else:
            df_mock = generate_mock_df(lines_amount=mock_df_lines_amount,
                                       languages=mock_languages)
            fig = plot_language_pie(df_mock)
            if not return_just_fig:
                return add_value_counts(df=df_mock,column='language'),fig
            else:
                return fig
        
    def test_plot_lantest_plot_gender_pieguage_pie(self,
                               df : pd.DataFrame|None = None,
                               mock_df_lines_amount : int = 10,
                               mock_genders : dict = DIC_USE_GENDERS,
                               return_just_fig : bool = False) -> tuple[pd.DataFrame,Any]|Any:
        if (df is not None) and isinstance(df,pd.DataFrame):
            if 'gender_name' not in df.keys():
                raise KeyError('Necessário coluna "gender_name" no dataframe passado como parâmetro')
            fig = plot_gender_pie(df)
            if not return_just_fig:
                return add_value_counts(df=df,column='gender_name'),fig
            else:
                return fig
        elif self.df is not None and isinstance(self.df,pd.DataFrame):
            if 'gender_name' not in self.df.keys():
                raise KeyError('Necessário coluna "gender_name" no dataframe passado como parâmetro')            
            fig = plot_gender_pie(self.df)
            if not return_just_fig:
                return add_value_counts(df=self.df,column='gender_name'),fig
            else:
                return fig
        else:
            df_mock = generate_mock_df(lines_amount=mock_df_lines_amount,
                                       genders=mock_genders)
            fig = plot_gender_pie(df_mock)
            if not return_just_fig:
                return add_value_counts(df=df_mock,column='gender_name'),fig
            else:
                return fig
        
    def test_plot_top_subjects(self,
                               top_n : int,
                               show_just_words : bool,
                               remove_course_words : bool,
                               stopwords_pt=STOPWORDS_PT,
                               stopwords_ufsc=STOPWORDS_UFSC,
                               format_text_func=format_text,
                               df : pd.DataFrame|None = None,
                               mock_df_lines_amount : int = 10,
                               mock_subjects : dict = DIC_USE_SUBJECTS,
                               return_just_fig : bool = False) -> tuple[pd.DataFrame,pd.DataFrame,Any]|Any:
        if (df is not None) and isinstance(df,pd.DataFrame):
            if 'gender_name' not in df.keys():
                raise KeyError('Necessário coluna "gender_name" no dataframe passado como parâmetro')
            df_freq,fig = plot_top_subjects(df,top_n=top_n,
                                            show_just_words=show_just_words,
                                            remove_course_words=remove_course_words,
                                            stopwords_pt=stopwords_pt,
                                            stopwords_ufsc=stopwords_ufsc,
                                            format_text_func=format_text_func)
            if not return_just_fig:
                return df,df_freq,fig
            else:
                return fig
        elif self.df is not None and isinstance(self.df,pd.DataFrame):
            if 'subjects' not in self.df.keys():
                raise KeyError('Necessário coluna "subjects" no dataframe passado como parâmetro')            
            df_freq,fig = plot_top_subjects(self.df,top_n=top_n,
                                            show_just_words=show_just_words,
                                            remove_course_words=remove_course_words,
                                            stopwords_pt=stopwords_pt,
                                            stopwords_ufsc=stopwords_ufsc,
                                            format_text_func=format_text_func)
            if not return_just_fig:
                return self.df,df_freq,fig
            else:
                return fig
        else:
            df_mock = generate_mock_df(lines_amount=mock_df_lines_amount,
                                       subjects=mock_subjects)
            df_freq,fig = plot_top_subjects(df_mock,top_n=top_n,
                                            show_just_words=show_just_words,
                                            remove_course_words=remove_course_words,
                                            stopwords_pt=stopwords_pt,
                                            stopwords_ufsc=stopwords_ufsc,
                                            format_text_func=format_text_func)
            if not return_just_fig:
                return df_mock,df_freq,fig
            else:
                return fig
        
    def test_plot_top_courses_by_year_and_subject(self,
                               subjects : list[str],
                               match_all : bool,
                               filter_subjects_func=filter_subjects,
                               df : pd.DataFrame|None = None,
                               mock_df_lines_amount : int = 10,
                               mock_subjects : dict = DIC_USE_SUBJECTS,
                               mock_years : dict = DIC_USE_YEARS,
                               mock_courses : dict = DIC_USE_COURSES,
                               return_just_fig : bool = False) -> tuple[pd.DataFrame,pd.DataFrame,Any]|Any:
        if (df is not None) and isinstance(df,pd.DataFrame):
            if 'year' not in df.keys():
                raise KeyError('Necessário coluna "gender_name" no dataframe passado como parâmetro')
            if 'course' not in df.keys():
                raise KeyError('Necessário coluna "course" no dataframe passado como parâmetro')
            if 'subjects' not in df.keys():
                raise KeyError('Necessário coluna "subjects" no dataframe passado como parâmetro')
            df_freq,fig = plot_top_courses_by_year_and_subject(df,subjects=subjects,
                                                               match_all=match_all,
                                                               filter_subjects_func=filter_subjects_func)
            if not return_just_fig:
                return df,df_freq,fig
            else:
                return fig
        elif self.df is not None and isinstance(self.df,pd.DataFrame):
            if 'year' not in self.df.keys():
                raise KeyError('Necessário coluna "gender_name" no dataframe passado como parâmetro')
            if 'course' not in self.df.keys():
                raise KeyError('Necessário coluna "course" no dataframe passado como parâmetro')
            if 'subjects' not in self.df.keys():
                raise KeyError('Necessário coluna "subjects" no dataframe passado como parâmetro')
            df_freq,fig = plot_top_courses_by_year_and_subject(self.df,subjects=subjects,
                                                               match_all=match_all,
                                                               filter_subjects_func=filter_subjects_func)
            if not return_just_fig:
                return self.df,df_freq,fig
            else:
                return fig
        else:
            df_mock = generate_mock_df(lines_amount=mock_df_lines_amount,
                                       subjects=mock_subjects,
                                       years=mock_years,
                                       courses=mock_courses)
            df_freq,fig = plot_top_courses_by_year_and_subject(df_mock,subjects=subjects,
                                                               match_all=match_all,
                                                               filter_subjects_func=filter_subjects_func)
            if not return_just_fig:
                return df_mock,df_freq,fig
            else:
                return fig
