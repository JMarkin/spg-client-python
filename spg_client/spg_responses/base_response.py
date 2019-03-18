# -*- coding: utf-8 -*-
from spg_client import exceptions

FIELDS_3DS_RESPONSE = ['Success', 'OrderId',
                       'Operation',
                       'ACSUrl', 'PaReq', 'ThreeDSKey',
                       'TietoTransId'
                       ]


class BaseResponse(object):
    # включается в MAC только при наличии, при отсутствии "-" в MAC не
    # ставится
    _mac_ignore_fields = ['CustomForm']
    _fields: list
    _mac_fields = []

    def __init__(self, root):
        if root.find('ErrMessage') is not None:
            raise exceptions.InvalidResponseError('{}\n ErrCode: {}'.format(
                root.find('ErrMessage').text, root.find('ErrCode').text
            )
            )
        # block, pay
        if root.find('Success').text == '3DS':
            self._fields = FIELDS_3DS_RESPONSE + ['MAC']

        if root.find('Success').text == '3DSCustomForm':
            self._fields += ['CustomForm', 'MAC']
            self._mac_ignore_fields = []

        for field in self._fields:
            if root.find(field) is not None:
                value = root.find(field).text
            else:
                value = None
            setattr(self, field, value)

    @property
    def mac_fields(self):

        if getattr(self, 'Success') == '3DS':
            self._mac_fields = FIELDS_3DS_RESPONSE
            self._fields = FIELDS_3DS_RESPONSE

        mac_fields = list(self._mac_fields)

        for field in self._mac_ignore_fields:
            if hasattr(self, field) and getattr(self, field) is None:
                mac_fields.remove(field)

        return mac_fields
