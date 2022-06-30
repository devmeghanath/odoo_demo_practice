from odoo import fields,models


class EstatePropertyTag(models.Model):
    _name='real.estate.property.tag'
    _description='This is for handling tags in the model'


    name=fields.Char(required=True)
