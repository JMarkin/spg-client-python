# -*- coding: utf-8 -*-
import hashlib
import hmac
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
