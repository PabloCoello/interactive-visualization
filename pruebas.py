import geopandas as gpd
import pandas as pd

path = '/mnt/c/Users/pablo/OneDrive - Universidade de Santiago de Compostela/Proyectos/visualization/'

area = gpd.read_file("./data/quemado.shp")
concellos = gpd.read_file("./data/concellos_proc.shp")
concellos = concellos.rename(columns={'NAME_2':'Municipio', 'sup_quem':'Superficie quemada'})
concellos = concellos[concellos['NAME_2'].isin(['Arcos de Valdevez', 'Caminha', 'Melgaço', 'Monção', 'Paredes de Coura',
                                                'Ponte da Barca', 'Ponte de Lima', 'Valença', 'Viana do Castelo', 'Vila Nova de Cerveira'])]
df = pd.read_excel('./data/sup_quem.xlsx')
res2 = concellos.merge(df, on='NAME_2')


res = gpd.sjoin(area, concellos, how='inner', op='intersects')

concellos.to_file('./data/concellos_proc.shp')
res.to_file('./data/quemado_proc.shp')


