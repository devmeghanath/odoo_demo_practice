from tomlkit import string
from odoo import fields,models


class EstatePropertyType(models.Model):
    _name='estate.property.type'
    _rec_name='type'
    _description='This is for defining property type'


    type=fields.Char(required=True, string='Type')