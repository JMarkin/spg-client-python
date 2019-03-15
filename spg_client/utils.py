# -*- coding: utf-8 -*-
import hashlib
import hmac
import re
import sys
from xml.etree import ElementTree as ET

from spg_client.exceptions import InvalidMacError, InvalidPanError


def dict_to_etree(d):
    def _to_etree(d, root):
        if not d:
            pass
        elif isinstance(d, str):
            root.text = d
        elif isinstance(d, dict):
            for k, v in d.items():
                assert isinstance(k, str)
                if k.startswith('#'):
                    assert k == '#text' and isinstance(v, str)
                    root.text = v
                elif k.startswith('@'):
                    assert isinstance(v, str)
                    root.set(k[1:], v)
                elif isinstance(v, list):
                    for e in v:
                        _to_etree(e, ET.SubElement(root, k))
                else:
                    _to_etree(v, ET.SubElement(root, k))
        else:
            assert d == 'invalid type', (type(d), d)

    assert isinstance(d, dict) and len(d) == 1
    tag, body = next(iter(d.items()))
    node = ET.Element(tag)
    _to_etree(body, node)
    return node


def dict_to_xml_str(d: dict):
    return ET.tostring(dict_to_etree(d))


def parse_xml(string_content):
    return ET.fromstring(string_content)


def mac_part(item):
    if item is None:
        return '-'
    else:
        string = str(item)
        return "{0}{1}".format(len(string), string)


def calculate_mac(secret_key, *items):
    mac = hmac.new(
        secret_key.encode(),
        msg="".join(mac_part(i) for i in items).encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    if sys.version_info > (3,):
        return mac.hex()
    else:
        return mac.encode('hex')


def check_mac_equivalence(spg, calculated):
    if spg != calculated:
        raise InvalidMacError(spg)


def is_pan_valid(pan):
    """
    Проверка PAN по алгоритму mod 10
    :param pan: str
    :returns: bool
    """
    digits_input = reversed([int(digit) for digit in str(pan)])
    digits_output = []
    for index, digit in enumerate(digits_input, start=1):
        if index % 2 == 0:  # check if even четный
            digit = digit * 2
            if digit > 9:
                digit = digit - 9
        digits_output.append(digit)
    check = sum(digits_output) % 10 == 0
    if not check:
        raise InvalidPanError
    return check


def transliterate(string):
    """
        https://gist.github.com/aruseni/1685075
    """
    capital_letters = {u'А': u'A',
                       u'Б': u'B',
                       u'В': u'V',
                       u'Г': u'G',
                       u'Д': u'D',
                       u'Е': u'E',
                       u'Ё': u'E',
                       u'З': u'Z',
                       u'И': u'I',
                       u'Й': u'Y',
                       u'К': u'K',
                       u'Л': u'L',
                       u'М': u'M',
                       u'Н': u'N',
                       u'О': u'O',
                       u'П': u'P',
                       u'Р': u'R',
                       u'С': u'S',
                       u'Т': u'T',
                       u'У': u'U',
                       u'Ф': u'F',
                       u'Х': u'H',
                       u'Ъ': u'',
                       u'Ы': u'Y',
                       u'Ь': u'',
                       u'Э': u'E', }

    capital_letters_transliterated_to_multiple_letters = {u'Ж': u'Zh',
                                                          u'Ц': u'Ts',
                                                          u'Ч': u'Ch',
                                                          u'Ш': u'Sh',
                                                          u'Щ': u'Sch',
                                                          u'Ю': u'Yu',
                                                          u'Я': u'Ya', }

    lower_case_letters = {u'а': u'a',
                          u'б': u'b',
                          u'в': u'v',
                          u'г': u'g',
                          u'д': u'd',
                          u'е': u'e',
                          u'ё': u'e',
                          u'ж': u'zh',
                          u'з': u'z',
                          u'и': u'i',
                          u'й': u'y',
                          u'к': u'k',
                          u'л': u'l',
                          u'м': u'm',
                          u'н': u'n',
                          u'о': u'o',
                          u'п': u'p',
                          u'р': u'r',
                          u'с': u's',
                          u'т': u't',
                          u'у': u'u',
                          u'ф': u'f',
                          u'х': u'h',
                          u'ц': u'ts',
                          u'ч': u'ch',
                          u'ш': u'sh',
                          u'щ': u'sch',
                          u'ъ': u'',
                          u'ы': u'y',
                          u'ь': u'',
                          u'э': u'e',
                          u'ю': u'yu',
                          u'я': u'ya', }

    for cyrillic_string, latin_string in capital_letters_transliterated_to_multiple_letters.items():
        string = re.sub(r"%s([а-я])" % cyrillic_string, r'%s\1' % latin_string, string)

    for dictionary in (capital_letters, lower_case_letters):

        for cyrillic_string, latin_string in dictionary.items():
            string = string.replace(cyrillic_string, latin_string)

    for cyrillic_string, latin_string in capital_letters_transliterated_to_multiple_letters.items():
        string = string.replace(cyrillic_string, latin_string.upper())

    return string


def ascii_or_translite(s):
    """ Нужно для отправки строк """
    try:
        return s.encode('ascii')
    except:
        return transliterate(s)
