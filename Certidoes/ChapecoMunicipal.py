import re
import os
import time
import fitz
import logging
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from util import DateUtil
from util import ImageCaptchaUtil

load_dotenv()


class ChapecoMunicipal:
    def __init__(self, db_name, empresa):
        self.db_name = db_name
        self.empresa = empresa

    async def chapeco_municipal(self):
        try:
            async with async_playwright() as p:
                page = await self.create_new_page(p)
                await self.post_cnpj(page)
                await self.get_captcha(page)
                await self.gerar_nova_certidao(page)
                await self.emitir_certidao(page)
                status = self.verifica_status()
                if status:
                    print('Positiva')
                else:
                    self.get_date_validade()
                    print('Negativa')

        except Exception as ex:
            logging.error(ex)
            raise Exception

    async def create_new_page(self, p):
        try:
            os.getenv('AUTH')
            browser_url = os.getenv('BROWSER_URL')
            browser = await p.chromium.connect_over_cdp(browser_url)
            context = await browser.new_context()
            page = await context.new_page()
            return page
        except Exception as ex:
            logging.error(ex, 'create_new_page')
            raise Exception

    async def post_cnpj(self, page):
        try:
            await page.goto('https://chapeco.meumunicipio.online/tributario/servlet/hwpcgeracertidaonegativa')
            await page.fill('xpath=//*[@id="vINCTBCPFCNPJ"]', self.empresa['cnpj'])
        except Exception as ex:
            logging.error(ex, 'post_cnpj')
            raise Exception

    async def get_captcha(self, page):
        try:
            screenshot = await (await page.query_selector('//*[@id="W0054vIMGCAPTCHA"]')).screenshot()
            ImageCaptchaUtil.saveImg(screenshot, 'chapeco', self.db_name)
            token = ImageCaptchaUtil.extract_captcha_text('imgs/demo/chapeco.png')

            if token is None or token == '' or not re.match(r'^\d{4}$', token):
                logging.error("Falha ao localizar ImageCaptcha")
                raise Exception('Falha ao localizar ImageCaptcha')
            else:
                await page.fill('xpath=//*[@id="W0054vVCAPTCHA"]', token)
                await page.query_selector('xpath=//*[@id="W0054BUTTON1"]').click()

        except Exception as ex:
            logging.error(ex, 'get_captcha')
            raise Exception

    async def gerar_nova_certidao(self, page):
        try:
            get_button = await page.query_selector('xpath=//*[@id="vGRIDGERAR_0001"]')
            await get_button.click()
            iframe_selector = '#gxp0_ifrm'
            await page.wait_for_selector(iframe_selector)
            close_pop_up = await page.wait_for_selector('//*[@id="gxp0_cls"]', state='visible', timeout=5000)
            await close_pop_up.click()

        except Exception as ex:
            logging.error(ex, 'gerar_nova_certidao')
            raise Exception

    async def emitir_certidao(self, page):
        try:
            get_button = await page.query_selector('xpath=//*[@id="vGRIDIMPRIMIR_0001"]')
            await get_button.click()
            new_page = await page.wait_for_event("popup")
            time.sleep(5)
            pdf_path = self.empresa['cnpj'] + ".pdf"
            await new_page.pdf(path=pdf_path)
        except Exception as ex:
            logging.error(ex, 'emitir_certidao')
            raise Exception

    def verifica_status(self):
        try:
            doc = fitz.open(self.empresa['cnpj'] + ".pdf")
            page = doc.load_page(0)
            text = page.get_text()
            if 'Certidão Positiva de Tributos Municipais' in text:
                return True
            elif 'Negativa' in text:
                return False
        except Exception as ex:
            logging.error(ex, 'verifica_status')
            raise Exception

    def get_date_validade(self):
        try:
            validade = DateUtil.getDataValidadePdf(self.empresa['cnpj'] + ".pdf", 'Validade', 40)
            return validade
        except Exception as ex:
            logging.error(ex, 'get_date_validade')
            raise Exception
