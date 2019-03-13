# -*- coding: utf-8 -*-
from spg_client.spg_responses import Ack3dsResponse
from spg_client.spg_requests import BaseRequest


class Ack3ds(BaseRequest):
    response_class = Ack3dsResponse
    method = 'POST'
    path = '/ack3ds'

    _mac_fields = [
        'ServiceId', 'OrderId', 'EmitentResponse',
    ]

    _mac_val_or_ignore_fields = []

    def __init__(self, order_id:str or int, emitent_response:dict):
        """
        Шаг 4 в 3ds
        Args:
            order_id : Уникальный идентификатор транзакции в системе
            Партнера cтрока, 6-19 цифр

            emitent_response (dict): Все параметры, полученные на
            шаге 3, упакованные в JSON, в
            виде ассоциативного массива.
            Имена параметров, полученные
            от банка эмитента, должны
            сохранятся сюда как есть.
        """
        self.order_id = order_id
        self.emitent_response = emitent_response

    def _params(self):
        return {
            'OrderId': self.order_id,
            'EmitentResponse': self.emitent_response,
        }
