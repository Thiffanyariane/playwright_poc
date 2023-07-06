import re
import fitz
from datetime import *
from util import DiretorioUtil


def get_data_validade_pdf(pasta, text_find, acrescimo, acrescimo_extra=0):
    try:
        name_arquivo = DiretorioUtil.find_unique_file(pasta)
        doc = fitz.open(pasta + name_arquivo)
        page = doc.load_page(0)
        text = page.get_text()
        expire_date = text.find(text_find)
        data_validade = text[expire_date + acrescimo_extra:expire_date + acrescimo].replace('\n', ' ')
        if re.search(r'\d{2}/\d{2}/\d{4}', data_validade) is not None:
            match = re.search(r'\d{2}/\d{2}/\d{4}', data_validade)
        else:
            match = re.search(r'\d{1}/\d{1}/\d{4}', data_validade)
        date = datetime.strptime(match.group(), '%d/%m/%Y').date()
        doc.close()
        return date
    except:
        return None
