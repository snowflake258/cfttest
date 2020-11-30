from marshmallow.validate import OneOf
from db.enums import CountryEnum, CurrencyEnum


CountryValidator = OneOf([c.value for c in CountryEnum])
CurrencyValidator = OneOf([c.value for c in CurrencyEnum])
