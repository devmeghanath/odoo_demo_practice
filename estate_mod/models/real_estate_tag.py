from odoo import fields,models


class EstatePropertyTag(models.Model):
    _name='real.estate.property.tag'
    _description='This is for handling tags in the model'


    name=fields.Char(required=True)
    _sql_constraints=[
        ('check_name','unique(name)','tag must be unique')
        ]
