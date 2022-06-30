import datetime
from datetime import timedelta
from email.policy import default
from odoo import models,fields,api
from odoo.exceptions import UserError



class EstatePropertyOffer(models.Model):
    _name='estate.property.offer'
    _description="this is a offer storing segment"



    create_date=fields.Datetime()
    price=fields.Float()
    status=fields.Selection([('accepted','Accepted'),('refused','Refused')],copy=False)
    partner_id=fields.Many2one('res.partner' ,required=True)
    property_id=fields.Many2one('estate.property',required=True)
    validity=fields.Integer('Validity',default=7)
    date_deadline=fields.Date('Dead line',compute='_compute_validity',inverse='_inverse_validity' ,store=True)
    accepted=fields.Integer(default=0)


    _sql_constraints=[
        ('check_offer_price','CHECK(price>=0)','offer price mustbe a positive value')
        ]

    @api.depends("validity")
    def _compute_validity(self):
        for record in self:
            if record.create_date:

                record.date_deadline=(record.create_date).date()+timedelta(days=record.validity)
            # else:
            #     record.date_deadline=datetime.date.today()
    def _inverse_validity(self):
        for record in self:
            if record.date_deadline is True:
                record.validity=(record.date_deadline-(record.create_date).date()).days


    @api.depends('status')
    def action_accept(self):
        for record in self:
                if record.property_id.accepted_in_global==0:

                    record.status='accepted'
                    record.property_id.accepted_in_global=1
                    print('----------->',record.property_id.accepted_in_global)
                    record.property_id.selling_price=record.price
                    record.property_id.buyer=record.partner_id.name
                else:
                    raise UserError('already accepted')

        return True

    def action_reffuse(self):
        for record in self:
            if self.status=='accepted':
                record.property_id.accepted_in_global=0
            record.status="refused"
        return True




