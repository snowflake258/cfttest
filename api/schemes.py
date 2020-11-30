from marshmallow import Schema, fields, validates, pre_load, ValidationError
from marshmallow.validate import Range
from datetime import datetime
from api.validators import CountryValidator, CurrencyValidator


class LimitSchema(Schema):
    country = fields.String(required=True, validate=CountryValidator)
    currency = fields.String(required=True, validate=CurrencyValidator)
    max_sum_per_month = fields.Decimal(required=True, validate=Range(min=1))


class TransferSchema(Schema):
    sum = fields.Decimal(required=True, validate=Range(min=1))
    country = fields.String(required=True, validate=CountryValidator)
    currency = fields.String(required=True, validate=CurrencyValidator)
    limit_id = fields.Integer(required=True)

    def __init__(self, limit, transfers):
        super().__init__()

        self.__limit = None
        self.__transfers = None

        self.__limit = limit
        self.__transfers = transfers

    @validates('sum')
    def validate_sum(self, value):
        if self.__limit is None or self.__transfers is None:
            return

        allowed_sum = self.__get_allowed_sum_for_transfer(self.__limit, self.__transfers)
        if value > allowed_sum:
            raise ValidationError(f'Your can\' tranfer {value} {self.__limit["currency"]}. '
                                  f'You have reached the limit for this month. '
                                  f'Limit - {self.__limit["max_sum_per_month"]}. '
                                  f'Allowed sum for transfer - {allowed_sum}.')

    @validates('currency')
    def validate_currency(self, value):
        if self.__limit is None:
            return

        if value != self.__limit['currency']:
            raise ValidationError(f'Incorrect currency. You must use {self.__limit["currency"]}.')

    @validates('limit_id')
    def validate_limit(self, value):
        if not self.__limit is not None:
            raise ValidationError(f'Limit with \'id\' equals {value} doesn\'t exists.')

    @staticmethod
    def __get_allowed_sum_for_transfer(limit, transfers):
        month_sum = 0
        current_month = datetime.now().date().month

        for item in transfers:
            if item['time'].date().month == current_month:
                month_sum += item['sum']

        return limit['max_sum_per_month'] - month_sum
