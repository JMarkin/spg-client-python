# -*- coding: utf-8 -*-
from spg_client import Card
from spg_client.spg_requests import BaseRequest
from spg_client.spg_responses import EMoneyTransferResponse


class EMoneyTransfer(BaseRequest):
    response_class = EMoneyTransferResponse
    method = 'POST'
    path = '/emoney_transfer'

    _mac_fields = [
        'ServiceId', 'OrderId', 'PAN', 'EMonth', 'EYear', 'Amount', 'Description', 'CustomFields',
        'Phone'
    ]

    _mac_val_or_ignore_fields = []

    def __init__(self, order_id: str or int, card: Card, amount: float, description:str,custom_field:str,phone:str):
        """
        Шаг 4 в 3ds
        Args:
            order_id : Уникальный идентификатор транзакции в системе
            Партнера cтрока, 6-19 цифр

            card (Card):  Данные карты
            amount (float): сумма к оплате
                1-14 цифр, может
                содержать
                десятичный
                разделитель в виде
                точки
            description(str): Описание транзакции
                cтрока, до 1000
                символов

            custom_field(str): доп параметры
                cтрока, до 1000
                символов

            phone(str): Телефон
                В МН формате (без пробелов):
                +79991231212
                +375227775511
                до 20 цифр, впереди
                ‘+’



        """
        self.order_id = order_id
        self.card = card
        self.amount = amount
        self.description = description
        self.custom_field = custom_field
        self.phone = phone

    def _params(self):
        return {
            'OrderId': self.order_id,
            'PAN': self.card.pan,
            'EMonth': self.card.month,
            'EYear': self.card.year,
            'Description': self.description,
            'CustomFields': self.custom_field,
            'Phone': self.phone,
        }
