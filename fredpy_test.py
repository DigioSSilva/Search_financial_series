import fredpy as fp
import requests
import pandas as pd
import creds
My_api = creds.My_api
fp.api_key = creds.My_api


#Lista de categorias
    #Filtra id e Nome das categorias
categorias = requests.get(f"https://api.stlouisfed.org/fred/category/children?category&api_key={My_api}&file_type=json")
categorias = categorias.json()
categorias = [{'id': item['id'], 'name': item['name']} for item in categorias['categories']]
#print(categorias)


#Subcategorias
    #Filtra  id e nome das subcategorias
subcategorias = requests.get(f"https://api.stlouisfed.org/fred/category/children?category_id=32991&api_key={My_api}&file_type=json")
subcategorias = subcategorias.json()
subcategorias = [{'id': item['id'], 'nome': item['name']} for item in subcategorias['categories']]
print(subcategorias)

#Sub-Subcategorias
    #Filtra  id e nome das sub-subcategorias
sub_subcategorias = requests.get(f"https://api.stlouisfed.org/fred/category/children?category_id=22&api_key={My_api}&file_type=json")
sub_subcategorias = sub_subcategorias.json()
sub_subcategorias = [{'id': item['id'], 'nome': item['name']} for item in sub_subcategorias['categories']]
#print(sub_subcategorias)

#Series
    #Filtra  id e nome das series dentro das sub-subcategorias
    
series = requests.get(f"https://api.stlouisfed.org/fred/category/series?category_id=120&api_key={My_api}&file_type=json")
series = series.json()
series = [{'id': item['id'], 'name': item['title']} for item in series['seriess']]
series_filtered = [i for i in series if '(DISCONTINUED)' not in i['name']]
#print(series_filtered)