# -*- coding: utf-8 -*-
import scrapy


class CodMunDianSpider(scrapy.Spider):
    name = 'cod_mun_dian'
    allowed_domains = ['rankia.co']
    start_urls = ['https://www.rankia.co/blog/dian/3988807-codigo-municipios-dian']

    def parse(self, response):
        municipios = response.xpath('/html/body/div[1]/div[2]/div/div[3]/div[1]/div/article/div[1]/div[1]/table/tbody/tr')
        for municipio in municipios:
            cod_municipio = municipio.xpath('.//td[2]//text()').extract_first()

            yield {'cod_municipio' : cod_municipio}
