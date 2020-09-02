import pandas as pd
import geopandas as gpd
import numpy as np
import folium
from folium.plugins import MarkerCluster
from folium import IFrame
import shapely
from shapely.geometry import Point
import branca
import json


class visualization():
    '''
    '''

    def __init__(self):
        '''
        '''

        with open('./conf.json', 'r') as f:
            self.conf = json.load(f)

        self.starting_point = self.get_starting_point()
        mapa = self.base_map(style)

        for layer in self.conf["info_layers"].keys():
            print(layer)
            self.add_layer_map(mapa, layer)

        self.layer = mapa
        folium.LayerControl().add_to(self.layer)


    def to_html(self):
        self.layer.save(self.conf["output_path"])

    
    def get_starting_point(self):
        '''
        '''
        starting_point = gpd.read_file(self.conf["main_layer_path"]).centroid
        return [float(starting_point.y), float(starting_point.x)]


    def base_map(self):
        '''
        '''
        toret = folium.Map(
            self.starting_point, 
            zoom_start=self.conf["zoom"],
            tiles=self.conf["style"])
        return toret


    def add_layer_map(self, mapa, layer):
        '''
        '''
        layer_gdf = gpd.read_file(self.conf['info_layers'][layer]['path'])
        val = self.conf['info_layers'][layer]['val_variable']
        layer_conf = self.conf['info_layers'][layer]

        if len(layer_gdf[val].unique()) > 1:
            colorscale = branca.colormap.linear.YlOrRd_09.scale(
                layer_gdf[val].min(), layer_gdf[val].max()
            )
            colorscale = colorscale.to_step(
                n=len(layer_gdf[val].unique())
            )

        folium.GeoJson(
            layer_gdf,
            name=layer,
            style_function=lambda x: {
                'weight': layer_conf['style_function']['weight'],
                'color': layer_conf['style_function']['color'],
                'fillColor': layer_conf['style_function']['fillColor'] if len(layer_gdf[val].unique()) == 1
                else colorscale(x['properties'][val]),
                'fillOpacity': layer_conf['style_function']['fillOpacity']
            },
            highlight_function=lambda x: {
                'weight': layer_conf['highlight_function']['weight'],
                'color': layer_conf['highlight_function']['color'],
                'fillOpacity': layer_conf['highlight_function']['fillOpacity']
            },
            tooltip=folium.features.GeoJsonTooltip(
                fields=self.conf['info_layers'][layer]['values_to_display'],
                aliases=[layer]
            )).add_to(mapa)


if __name__ == '__main__':
    pl = visualization()
    pl.to_html()
