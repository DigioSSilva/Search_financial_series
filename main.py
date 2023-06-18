
import flet as ft
import sgs
import ipeadatapy as ip
import requests
import pandas as pd
from datetime import datetime
import creds

My_api = creds.My_api



def main(page: ft.Page):
    page.title = "Financial Series"
    page.window_height = 600
    page.window_width = 700
    #page.window_top = 200
    dict_values = {
        'FonteDados': '',
        'CodSerie': '',
        'DataInicio': '',
        'DataFim': '',
        'Categoria': '',
        'Categoria_id': '',
        'Subcategoria': '',
        'SubCategoria_id': '',
        'SubSubCategoria': '',
        'Serie_id': '',
        'Serie': '',
        
        
    }
    lista_categorias = []
    lista_subcategorias = []
    lista_subsubcategorias = []
    lista_series = []
    #Funções on change e on click
    def dropdown_changed_fontes(e):
        #Limpar todos os dados 
        Dd_Categoria.options.clear
        page.update()
        if Fontes_dados.value == "SGS Bacen":
            Dd_Categoria.options.clear()
            Dd_SubCategoria.options.clear()
            Dd_SubSubCategoria.options.clear()
            Dd_Cod_serie.options.clear()
            page.update()

        elif Fontes_dados.value == "Ipeadata":
            Dd_Categoria.options.clear()
            Dd_SubCategoria.options.clear()
            Dd_SubSubCategoria.options.clear()
            Dd_Cod_serie.options.clear()
            page.update()           

        elif Fontes_dados.value == "FRED St. Louis FED":
            Dd_Categoria.options.clear()
            Dd_SubCategoria.options.clear()
            Dd_SubSubCategoria.options.clear()
            Dd_Cod_serie.options.clear()
            page.update()

            dict_values['FonteDados'] = Fontes_dados.value
            link_category = f"https://api.stlouisfed.org/fred/category/children?category&api_key={My_api}&file_type=json"
                #Lista de categorias
                #Filtra id e Nome das categorias
            categorias = requests.get(link_category)
            categorias = categorias.json()
            categorias_download = [{'id': item['id'], 'name': item['name']} for item in categorias['categories']]
            for value in categorias_download:
                Dd_Categoria.options.append(ft.dropdown.Option(value['name']))  
                lista_categorias.append({'id': value['id'], 'name': value['name']})            
                page.update()
        print(dict_values['FonteDados'])

    def dropdown_changed_categorias(e):
        Dd_SubCategoria.options.clear()
        Dd_SubSubCategoria.options.clear()
        Dd_Cod_serie.options.clear()
        page.update()

        #Capturando o id referente a categoria selecionada
        dict_values['Categoria'] = Dd_Categoria.value
        id_select = [item['id'] for item in lista_categorias if item['name'] == dict_values['Categoria']]
        id_select = id_select[0]
        #Subcategorias
            #Filtra  id e nome das subcategorias
        link_subc = f"https://api.stlouisfed.org/fred/category/children?category_id={id_select}&api_key={My_api}&file_type=json"
        subcategorias = requests.get(link_subc)
        subcategorias = subcategorias.json()
        subcategorias_download = [{'id': item['id'], 'name': item['name']} for item in subcategorias['categories']]
        for value in subcategorias_download:
            Dd_SubCategoria.options.append(ft.dropdown.Option(value['name']))
            lista_subcategorias.append({'id': value['id'], 'name': value['name']})
            page.update()            

    def dropdown_changed_subcategorias(e):
        Dd_SubSubCategoria.options.clear()
        Dd_Cod_serie.options.clear()
        page.update()

        #Capturando o id referente a categoria selecionada
        dict_values['SubCategoria'] = Dd_SubCategoria.value
        id_select = [item['id'] for item in lista_subcategorias if item['name'] == dict_values['SubCategoria']]
        id_select = id_select[0]
        #Subcategorias
            #Filtra  id e nome das subcategorias
        link_sub_subc = f"https://api.stlouisfed.org/fred/category/children?category_id={id_select}&api_key={My_api}&file_type=json"
        sub_subcategorias = requests.get(link_sub_subc)
        sub_subcategorias = sub_subcategorias.json()
        sub_subcategorias_download = [{'id': item['id'], 'name': item['name']} for item in sub_subcategorias['categories']]
        for value in sub_subcategorias_download:
            Dd_SubSubCategoria.options.append(ft.dropdown.Option(value['name']))
            lista_subsubcategorias.append({'id': value['id'], 'name': value['name']})
            page.update()

    def dropdown_changed_subsubcategorias(e):
        Dd_Cod_serie.options.clear()
        page.update()

        #Capturando o id referente a categoria selecionada
        dict_values['SubSubCategoria'] = Dd_SubSubCategoria.value
        id_select = [item['id'] for item in lista_subsubcategorias if item['name'] == dict_values['SubSubCategoria']]
        id_select = id_select[0]
        #Subcategorias
            #Filtra  id e nome das subcategorias
            
        link_series = f"https://api.stlouisfed.org/fred/category/series?category_id={id_select}&api_key={My_api}&file_type=json"
        series = requests.get(link_series)
        series = series.json()
        series_download = [{'id': item['id'], 'name': item['title']} for item in series['seriess']]
        series_filtered = [i for i in series_download if '(DISCONTINUED)' not in i['name']]
        for value in series_filtered:
            Dd_Cod_serie.options.append(ft.dropdown.Option(value['name']))
            lista_series.append({'id': value['id'], 'name': value['name']})
            page.update()

    def changed_cod_serie(e):
        dict_values['CodSerie'] = Cod_serie.value
        print(dict_values['CodSerie'])

    def changed_data_inicio(e):
        dict_values['DataInicio'] = Inicio_serie.value
        print(dict_values['DataInicio'])

    def changed_data_fim(e):
        dict_values['DataFim'] = Fim_serie.value
        print(dict_values['DataFim'])

    def consulta_data(e):
        #Consulta SGS Bacen
        if dict_values['FonteDados'] == "SGS Bacen":
            #df=sgs.dataframe([CDI,INCC],start='02/01/2018',end='31/12/2018')
            data = sgs.time_serie(dict_values['CodSerie'], start=dict_values['DataInicio'], end=dict_values['DataFim'])
            #metadata = sgs.search_ts(dict_values['CodSerie'], language="pt")
            #print(metadata)

        elif dict_values['FonteDados'] == "Ipeadata":
            data = ip.timeseries(dict_values['CodSerie'])
            print(data.date_range)

        elif dict_values['FonteDados'] == "FRED St. Louis FED":
            fred = fp.series(dict_values['CodSerie'])
            fred = pd.DataFrame(fred.data)
            fred.index = pd.to_datetime(fred.index, format='%Y-%m-%d')
            fred.index = fred.index.strftime('%d/%m/%Y')
            ##fred = fred.filter(['date', 'value'])
            #fred['date'] = pd.to_datetime(fred['date'], format='%Y-%m-%d')
            #fred['date'] = fred['date'].dt.strftime('%d/%m/%Y')

            inicio = datetime.strptime(dict_values['DataInicio'], '%d/%m/%Y').strftime('%d/%m/%Y')
            fim = datetime.strptime(dict_values['DataFim'], '%d/%m/%Y').strftime('%d/%m/%Y')

            ##fred = pd.DataFrame(fred[['date', 'value']])
            #data = fred.loc[(fred['date'] >= inicio) & (fred['date'] <= fim)]
            data = fred[(fred.index >= inicio) & (fred.index <= fim)]
        data.to_excel("Dados_downloaded.xlsx", sheet_name= "Sheet1")



    Fontes_dados = ft.Dropdown(
        label= 'Fonte de Dados',
        autofocus= True,
        options=[
            ft.dropdown.Option("SGS Bacen"),
            ft.dropdown.Option("Ipeadata"),
            ft.dropdown.Option("FRED St. Louis FED"),
        ],
        width=500,
        on_change=dropdown_changed_fontes
    )    

    Dd_Categoria = ft.Dropdown(
        label= 'Categoria',
        autofocus= True,
        options=[
        ],
        width=500,
        on_change=dropdown_changed_categorias
    ) 

    Dd_SubCategoria = ft.Dropdown(
        label= 'Subcategoria',
        autofocus= True,
        options=[
        ],
        width=500,
        on_change=dropdown_changed_subcategorias
    )

    Dd_SubSubCategoria = ft.Dropdown(
        label= 'Sub-subcategoria',
        autofocus= True,
        options=[
        ],
        width=500,
        on_change=dropdown_changed_subsubcategorias
    )

    Dd_Cod_serie = ft.Dropdown(
        label= 'Series',
        autofocus= True,
        options=[
        ],
        width=500,
        on_change=dropdown_changed_fontes
    )


    
    Inicio_serie = ft.TextField(label='Data Início:', 
            width=145,
            on_change = changed_data_inicio
            )
    
    Fim_serie = ft.TextField(label='Data Fim:', 
            width=145,
            on_change = changed_data_fim
            )

    def route_change(route):
        page.views.clear()
        page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
            primary="#00BED3",
            primary_container="#00BED3",
            ),
        )
        page.views.append(
            ft.View(
                "/",
                [
                    #ft.Text(value= 'Buscador de Séries Financeiras', size= 20, weight= 'bold')
                    ft.AppBar(title=ft.Text("Buscador de Séries Financeiras LEME "), bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.Text(value= 'Selecione o a fonte de dados que deseja consultar:', size= 20, weight= 'bold'),
                    ft.Row(controls=[
                        Fontes_dados,
                        ],
                    ),

                    ft.Row(controls=[
                        Dd_Categoria,
                        ],
                    ),

                    ft.Row(controls=[
                        Dd_SubCategoria,
                        ],
                    ),

                    ft.Row(controls=[
                        Dd_SubSubCategoria    
                        ],
                    ),

                    ft.Row(controls=[
                        Dd_Cod_serie,
                        ]      
                    ),
                    ft.Row(controls=[
                        Inicio_serie,
                        Fim_serie,
                        ]      
                    ),
                    ft.Row(controls=[
                        ft.ElevatedButton('Download Data', on_click= consulta_data),
                        ft.ElevatedButton("Próximo", on_click=lambda _: page.go("/menu2"))
                        #ft.ElevatedButton("Consultar", on_click=lambda _: page.go("/menu2"))
                        ]      
                    ),                                        
                    #ft.TextField(label='PL', prefix_text= 'R$ ',suffix_text= ' MM'),
                   # ft.ElevatedButton("Próximo", on_click=lambda _: page.go("/store")),
                ],
            )
        )
        if page.route == "/menu2":
            page.views.append(
                ft.View(
                    "/menu2",
                    [
                        ft.AppBar(title=ft.Text("Precificação Gestão LEME "), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.Text(value= 'Passo 2: Quais os valores de CDI e Perfil', size= 20, weight= 'bold'),
                        ft.Row(controls=[
                            #Cdi,
                            
                            ]      
                        ),
                        ft.Row(controls = [
                                                 

                            ]
                        ), 
                        ft.Row(controls=[
                            ft.ElevatedButton("Próximo", on_click=lambda _: page.go("/menu3")),
                            ft.ElevatedButton("Reiniciar", on_click=lambda _: page.go("/"))
                            ]      
                        ),                       
                    ],
                )
            )
              

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main)