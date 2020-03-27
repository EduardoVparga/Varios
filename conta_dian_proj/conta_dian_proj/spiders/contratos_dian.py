## Este es elc codigo principal, es la spider, que directamente se encarga de extraer la información.

from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from selenium.common.exceptions import NoSuchElementException
from scrapy.http import Request


from time import sleep

class ContratosDianSpider(Spider):
    name = 'contratos_dian'
    allowed_domains = ['www.contratos.gov.co']

    def start_requests(self):
        yield Request('https://www.contratos.gov.co/consultas/inicioConsulta.do',
                      callback= self.parse)


    def parse(self, response):

        self.driver = webdriver.Firefox()
        self.driver.get('https://www.contratos.gov.co/consultas/inicioConsulta.do')

     ## Se puede midificar la "key" a eviar segun la empresa que se necesite, yo recomiendo primero entrara a la pagina, ver exactamente como la pagina nombra la entidad
     ## copiar y pegar ese nombre dentro de las comillas y correr el codigo ejemplo: para buscar a la DIAN el nombre que maneja la pagina es
     ## DIRECCIÓN DE IMPUESTOS Y ADUANAS NACIONALES (DIAN) entonces
     # self.driver.find_element_by_css_selector('#findEntidad').send_keys("DIRECCIÓN DE IMPUESTOS Y ADUANAS NACIONALES (DIAN)")

        self.driver.find_element_by_css_selector('#findEntidad').send_keys("INSTITUTO NACIONAL DE VÍAS (INVIAS)")

        sleep(1)
        self.driver.find_element_by_css_selector('#ui-id-1').click()
        sleep(1)
        self.driver.find_element_by_css_selector('#ctl00_ContentPlaceHolder1_imgBuscar').click()


        while True:
            try:

                sel = Selector(text= self.driver.page_source)

                for n in range(2, 52):

                    index = sel.xpath("/html/body/div[3]/div/div/center/div/div/form/table/tbody/tr[" + str(n) + "]/td[1]/text()").extract_first()

                    n_proceso = sel.xpath("/html/body/div[3]/div/div/center/div/div/form/table/tbody/tr[" + str(n) + "]/td[2]/a/text()").extract_first()

                    tipo_proceso = sel.xpath("/html/body/div[3]/div/div/center/div/div/form/table/tbody/tr[" + str(n) + "]/td[3]/text()").extract_first()

                    estado = sel.xpath("/html/body/div[3]/div/div/center/div/div/form/table/tbody/tr[" + str(n) + "]/td[4]/text()").extract_first()

                    entidad = sel.xpath("/html/body/div[3]/div/div/center/div/div/form/table/tbody/tr[" + str(n) + "]/td[5]/text()").extract_first()

                    objeto = sel.xpath("/html/body/div[3]/div/div/center/div/div/form/table/tbody/tr[" + str(n) + "]/td[6]/text()").extract_first()

                    departamento = sel.xpath("/html/body/div[3]/div/div/center/div/div/form/table/tbody/tr[" + str(n) + "]/td[7]/b/text()").extract_first()
                    municipio = sel.xpath("/html/body/div[3]/div/div/center/div/div/form/table/tbody/tr[" + str(n) + "]/td[7]/text()").extract_first()

                    cuantia = sel.xpath("/html/body/div[3]/div/div/center/div/div/form/table/tbody/tr[" + str(n) + "]/td[8]/text()").extract_first()

                    tipo_fecha = sel.xpath("/html/body/div[3]/div/div/center/div/div/form/table/tbody/tr[" + str(n) + "]/td[9]/b/text()").extract_first()
                    fecha = sel.xpath("/html/body/div[3]/div/div/center/div/div/form/table/tbody/tr[" + str(n) + "]/td[9]/text()").extract_first()

                    yield {'index' : index,
                           'n_proceso' : n_proceso,
                           'tipo_proceso' : tipo_proceso,
                           'estado' : estado,
                           'entidad' : entidad,
                           'objeto' : objeto,
                           'departamento' : departamento,
                           'municipio' : municipio,
                           'cuantia' : cuantia,
                           'tipo_fecha' : tipo_fecha,
                           'fecha' : fecha}

                    control = sel.xpath("/html/body/div[3]/div/div/center/div/div/form/p/text()").extract_first()
                    control = control.split('r')
                    control = control[0].split('\t')

                    if (index == control[-1]) == True:
                        raise NoSuchElementException()
                        break

                next_page = self.driver.find_element_by_xpath('//a[text()="Siguiente"]')
                sleep(1)
                next_page.click()
                sleep(2)

            except NoSuchElementException:
                self.driver.quit()
                break
