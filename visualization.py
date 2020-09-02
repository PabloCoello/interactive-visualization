import pandas as pd
import geopandas as gpd
import numpy as np
from geopandas.tools import sjoin
import folium
from folium.plugins import MarkerCluster
from folium import IFrame
import shapely
from shapely.geometry import Point
import unicodedata
import pysal as ps
import mapclassify
import branca


class visualization():
    '''
    '''

    def __init__(self, ut, specific_conf, var_dict, threats, style='OpenStreetMap'):
        '''
        '''
        self.starting_point = self.get_starting_point(ut)
        mapa = self.base_map(style)
        for threat in threats.keys():
            print(threat)
            self.add_threat_map(mapa, threat, threats)
            
        for var in var_dict.keys():
            print(var)
            mapa = self.add_var_map(mapa, var_dict, specific_conf, layer=var)

        self.layer = mapa
        folium.LayerControl().add_to(self.layer)

    def to_html(self):
        self.layer.save('output.html')

    def base_map(self, style='OpenStreetMap'):
        '''
        '''
        toret = folium.Map(self.starting_point, zoom_start=12, tiles=style)
        return toret

    def add_threat_map(self, mapa, threat, threats):
        '''
        '''
        if len(threats[threat]['val'].unique()) > 1:
            colorscale = branca.colormap.linear.YlOrRd_09.scale(
                threats[threat]['val'].min(), threats['erosion']['val'].max())
            colorscale = colorscale.to_step(
                n=len(threats[threat]['val'].unique()))

        folium.GeoJson(threats[threat],
                       name=threat,
                       style_function=lambda x: {
            'weight': 1,
            'color': '#545453',
            'fillColor': '#9B9B9B' if len(threats[threat]['val'].unique()) == 1
            else colorscale(x['properties']['val']),
            'fillOpacity': 0.2
        },
            highlight_function=lambda x: {
            'weight': 3,
            'color': 'black',
            'fillOpacity': 1
        },
            tooltip=folium.features.GeoJsonTooltip(
            fields=['val'],
            aliases=[threat + 'risk']
        )).add_to(mapa)
        
    
    def add_markers(self, gdf, mapa, specific_conf, layer):
        width, height = 310,110
        popups, locations = [], []
        for idx, row in gdf.iterrows():
            try:
                locations.append(sum([[p.y, p.x] for p in row.geom], []))
            except:
                locations.append([row['geom'].y, row['geom'].x])
            variable = row[specific_conf['var_list'][layer]['variables']]
            name = specific_conf['var_list'][layer]['name']
            iframe = self.poptext(variable, name)
            popups.append(iframe)
            
        h = folium.FeatureGroup(name=specific_conf['var_list'][layer]['name'])
        h.add_children(MarkerCluster(locations=locations, popups=popups)).add_to(mapa)
        return mapa

    def poptext(self, variable, name):
        return "<a href=\"" + name + "\">" + variable  + "</a>"
    
    def add_var_map(self, mapa, var, specific_conf, layer):
        features = ['erosion_val', 'debrisflow_val', 'landslide_val']
        features.append(specific_conf['var_list'][layer]['variables'])
        if specific_conf['var_list'][layer]['type'] == 'lines':
            folium.Choropleth(
                var[layer][var[layer].geometry.length > 0.001],
                data=var[layer],
                columns=features,
                line_weight=1,
                line_color='black',
                legend_name=specific_conf['var_list'][layer]['name']
            ).add_to(mapa)
        else:
            mapa = self.add_markers(
                gdf=var[layer], 
                mapa=mapa,
                specific_conf=specific_conf, 
                layer=layer
                )
        return mapa

    def get_starting_point(self, ut):
        '''
        '''
        starting_point = ut.get_gdf_from_SQL('burned_area').centroid
        return [float(starting_point.y), float(starting_point.x)]

if __name__ == '__main__':
    pl = visualization(ut, specific_conf, var_dict=var,
                    threats=threats)  # , style='Stamen Toner')
    base = pl.base_map()
    pl.layer
    pl.to_html()
