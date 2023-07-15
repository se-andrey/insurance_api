from tortoise import fields
from tortoise.models import Model


class Tariff(Model):
    id = fields.IntField(pk=True)
    date_tariff = fields.DateField()
    cargo_type = fields.CharField(max_length=200)
    rate = fields.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        table = "tariff"
