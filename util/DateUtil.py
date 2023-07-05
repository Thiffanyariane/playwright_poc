import re
import fitz
from datetime import *
from util import DiretorioUtil


def getDataValidadePdf(pasta, text_find, acrescimo, acrescimoExtra = 0):
    try:
        name_arquivo = DiretorioUtil.findUniqueFile(pasta)
        doc = fitz.open(pasta + name_arquivo)
        page = doc.load_page(0)
        text = page.get_text()
        expire_date = text.find(text_find)
        data_Validade = text[expire_date+acrescimoExtra:expire_date+acrescimo].replace('\n', ' ')
        if re.search(r'\d{2}/\d{2}/\d{4}', data_Validade) != None:
            match = re.search(r'\d{2}/\d{2}/\d{4}', data_Validade)
        else:
            match = re.search(r'\d{1}/\d{1}/\d{4}', data_Validade)
        date = datetime.strptime(match.group(), '%d/%m/%Y').date()
        doc.close()
        return date
    except:
        return None
