# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


## Esto se utiliza para procesar la información antes de exportarla, es decir, modificar, limpiar y formatear la informacion a la vez que se extrae.

class ContaDianProjPipeline(object):
    def process_item(self, item, spider):
        if item['objeto']:
            item['objeto'] = item['objeto'].replace('\n', '')
            item['objeto'] = item['objeto'].replace('\t', '')
            item['objeto'] = item['objeto'].replace('"', '')
            item['objeto'] = item['objeto'].capitalize()
        
        if item['municipio']:
            item['municipio'] = item['municipio'].replace(':', '')
            item['municipio'] = item['municipio'].strip()
        
        if item['entidad']:
            item['entidad'] = item['entidad'].capitalize()
            
        return item
