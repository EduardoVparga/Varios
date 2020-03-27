# -*- coding: utf-8 -*-
from scrapy import Spider
from pandas import read_csv
from scrapy.http import Request
import json

cod_municipos = read_csv('codigos_municipos.csv', encoding= 'cp1252') # Debe ir la direccion donde este ubicado el archivo
cod_municipos = cod_municipos.values[2:]


class RegaliasSpider(Spider):
    name = 'regalias'
    allowed_domains = ['maparegalias.sgr.gov.co']

    def start_requests(self):
        for municipio in cod_municipos:
            url = 'http://maparegalias.sgr.gov.co/Produccion/FichaProduccion?periodosProduccion=2012,2013,2014,2015,2016,2017,2018,2019,2020&municipio='+ municipio[0]

            yield Request(url,
                          callback=self.parse,
                          meta = {'municipio': municipio[0]})

    def parse(self, response):
        municipio = response.meta['municipio']
        url = response.url.split('=')
        url = url[1].split('&')
        url = url[0].split(',')

        for n in url:
            url_1 = 'http://maparegalias.sgr.gov.co/api/produccion/GetInformacionProduccion?periodosProduccion='+ n +'&municipio=' + municipio
            yield Request(url_1,
                          headers= {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
                                    "Accept": "*/*",
                                    "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
                                    "X-Requested-With": "XMLHttpRequest"},
                          meta = {'municipio': municipio,
                                  'periodo': n},
                          callback= self.parse_production_data)

    def parse_production_data(self, response):
        municipio = response.meta['municipio']
        periodo =  response.meta['periodo']
        jsonresponse = json.loads(response.body)

        if jsonresponse['Detalles'] != []:
            for t_recurso in jsonresponse['Detalles']:
                tipo_recurso = t_recurso['TipoDeRecurso']
                valor_total_cop = t_recurso['ValorTotal']

                for recurso in t_recurso['Detalles']:
                    id_recurso = recurso['IdRecurso']
                    nombre_recurso = recurso["NombreRecurso"]
                    cantidad = recurso["Cantidad"]
                    uni_medida = recurso["UnidadDeMedida"]
                    valor_liq = recurso["ValorLiquidado"]

                    if recurso["Detalles"][0]["IdCampo"] != 'VARIOS':
                        for campo in recurso['Detalles']:
                            id_campo = campo['IdCampo']
                            nom_campo = campo['NombreCampo']
                            cant_camp = campo['Cantidad']
                            val_liq_camp = campo['ValorLiquidado']
                            url_meses = 'http://maparegalias.sgr.gov.co/api/produccion/GetProduccionCampoOMina?periodosProduccion='+ periodo +'&municipio='+ municipio +'&campoProyecto='+ id_campo +'&recursoNatural=' + id_recurso

                            yield Request(url_meses,
                                          headers= {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
                                                    "Accept": "*/*",
                                                    "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
                                                    "X-Requested-With": "XMLHttpRequest"},
                                          meta = {'municipio': municipio,
                                                  'periodo': periodo,
                                                  'tipo_recurso':tipo_recurso,
                                                  'valor_total_cop':valor_total_cop,
                                                  'nombre_recurso':nombre_recurso,
                                                  'cantidad':cantidad,
                                                  'uni_medida':uni_medida,
                                                  'valor_liq':valor_liq,
                                                  'nom_campo':nom_campo,
                                                  'cant_camp':cant_camp,
                                                  'val_liq_camp':val_liq_camp},
                                           callback= self.parse_meses_data)

                    else:
                        url_meses = 'http://maparegalias.sgr.gov.co/api/produccion/GetProduccionCampoOMina?periodosProduccion='+ periodo +'&municipio='+ municipio +'&campoProyecto=VARIOS&recursoNatural=' + id_recurso
                        yield Request(url_meses,
                                      headers= {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
                                                "Accept": "*/*",
                                                "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
                                                "X-Requested-With": "XMLHttpRequest"},
                                          meta = {'municipio': municipio,
                                                  'periodo': periodo,
                                                  'tipo_recurso':tipo_recurso,
                                                  'valor_total_cop':valor_total_cop,
                                                  'nombre_recurso':nombre_recurso,
                                                  'cantidad':cantidad,
                                                  'uni_medida':uni_medida,
                                                  'valor_liq':valor_liq,
                                                  'nom_campo':None,
                                                  'cant_camp':None,
                                                  'val_liq_camp':None},
                                       callback= self.parse_meses_data)

        else:
            yield {'municipio':municipio,
                   'periodo': periodo,
                   'tipo_recurso': None,
                   'valor_total_cop': None,
                   'nombre_recurso': None,
                   'cantidad': None,
                   'uni_medida': None,
                   'valor_liq': None,
                   'nom_campo': None,
                   'cant_camp': None,
                   'val_liq_camp': None,
                   'Enero_cant': None,
                   'Enero_val_liq_mes': None,
                   'Febrero_cant': None,
                   'Febrero_val_liq_mes': None,
                   'Marzo_cant': None,
                   'Marzo_val_liq_mes': None,
                   'Abril_cant': None,
                   'Abril_val_liq_mes': None,
                   'Mayo_cant': None,
                   'Mayo_val_liq_mes': None,
                   'Junio_cant': None,
                   'Junio_val_liq_mes': None,
                   'Julio_cant': None,
                   'Julio_val_liq_mes': None,
                   'Agosto_cant': None,
                   'Agosto_val_liq_mes': None,
                   'Septiembre_cant': None,
                   'Septiembre_val_liq_mes': None,
                   'Octubre_cant': None,
                   'Octubre_val_liq_mes': None,
                   'Noviembre_cant': None,
                   'Noviembre_val_liq_mes': None,
                   'Diciembre_cant': None,
                   'Diciembre_val_liq_mes': None}

    def parse_meses_data(self, response):
        municipio = response.meta['municipio']
        periodo = response.meta['periodo']
        tipo_recurso = response.meta['tipo_recurso']
        valor_total_cop = response.meta['valor_total_cop']
        nombre_recurso = response.meta['nombre_recurso']
        cantidad = response.meta['cantidad']
        uni_medida = response.meta['uni_medida']
        valor_liq = response.meta['valor_liq']
        nom_campo = response.meta['nom_campo']
        cant_camp = response.meta['cant_camp']
        val_liq_camp = response.meta['val_liq_camp']
        jsonresponse = json.loads(response.body)

        calendario = {'Enero': {'Cantidad': None, 'Val_liq_mes': None},
                      'Febrero': {'Cantidad': None, 'Val_liq_mes': None},
                      'Marzo': {'Cantidad': None, 'Val_liq_mes': None},
                      'Abril': {'Cantidad': None, 'Val_liq_mes': None},
                      'Mayo': {'Cantidad': None, 'Val_liq_mes': None},
                      'Junio': {'Cantidad': None, 'Val_liq_mes': None},
                      'Julio': {'Cantidad': None, 'Val_liq_mes': None},
                      'Agosto': {'Cantidad': None, 'Val_liq_mes': None},
                      'Septiembre': {'Cantidad': None, 'Val_liq_mes': None},
                      'Octubre': {'Cantidad': None, 'Val_liq_mes': None},
                      'Noviembre': {'Cantidad': None, 'Val_liq_mes': None},
                      'Diciembre': {'Cantidad': None, 'Val_liq_mes': None}}

        for mes in jsonresponse['Detalles']:
            calendario[mes['Mes']]['Cantidad'] = mes['Cantidad']
            calendario[mes['Mes']]['Val_liq_mes'] = mes['ValorLiquidado']

        yield {'municipio': municipio,
               'periodo':periodo,
               'tipo_recurso':tipo_recurso,
               'valor_total_cop':valor_total_cop,
               'nombre_recurso':nombre_recurso,
               'cantidad':cantidad,
               'uni_medida':uni_medida,
               'valor_liq':valor_liq,
               'nom_campo':nom_campo,
               'cant_camp':cant_camp,
               'val_liq_camp':val_liq_camp,
               'Enero_cant': calendario['Enero']['Cantidad'],
               'Enero_val_liq_mes': calendario['Enero']['Val_liq_mes'],
               'Febrero_cant': calendario['Febrero']['Cantidad'],
               'Febrero_val_liq_mes': calendario['Febrero']['Val_liq_mes'],
               'Marzo_cant': calendario['Marzo']['Cantidad'],
               'Marzo_val_liq_mes': calendario['Marzo']['Val_liq_mes'],
               'Abril_cant': calendario['Abril']['Cantidad'],
               'Abril_val_liq_mes': calendario['Abril']['Val_liq_mes'],
               'Mayo_cant': calendario['Mayo']['Cantidad'],
               'Mayo_val_liq_mes': calendario['Mayo']['Val_liq_mes'],
               'Junio_cant': calendario['Junio']['Cantidad'],
               'Junio_val_liq_mes': calendario['Junio']['Val_liq_mes'],
               'Julio_cant': calendario['Julio']['Cantidad'],
               'Julio_val_liq_mes': calendario['Julio']['Val_liq_mes'],
               'Agosto_cant': calendario['Agosto']['Cantidad'],
               'Agosto_val_liq_mes': calendario['Agosto']['Val_liq_mes'],
               'Septiembre_cant': calendario['Septiembre']['Cantidad'],
               'Septiembre_val_liq_mes': calendario['Septiembre']['Val_liq_mes'],
               'Octubre_cant': calendario['Octubre']['Cantidad'],
               'Octubre_val_liq_mes': calendario['Octubre']['Val_liq_mes'],
               'Noviembre_cant': calendario['Noviembre']['Cantidad'],
               'Noviembre_val_liq_mes': calendario['Noviembre']['Val_liq_mes'],
               'Diciembre_cant': calendario['Diciembre']['Cantidad'],
               'Diciembre_val_liq_mes': calendario['Diciembre']['Val_liq_mes']}
