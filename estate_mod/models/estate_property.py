
from email.policy import default
from odoo import models,fields,api
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _name="estate.property"
    _description="To manage the realestate properties"

    property_type_id=fields.Many2one('estate.property.type')
    tag_ids=fields.Many2many('real.estate.property.tag',string='many2many_tags')
    offer_ids=fields.One2many('estate.property.offer','property_id',string="offer")
    name=fields.Char('Title',required=True)
    bestoffer=fields.Integer('Best Offer',compute='_computed_best_offer')
    description=fields.Char()
    expected_price=fields.Float(required=True)
    selling_price=fields.Float( copy=False)
    bedrooms=fields.Integer('Bedrooms',default=2)
    living_area=fields.Integer()
    facades=fields.Integer()
    garage=fields.Boolean()
    available_from=fields.Date(copy=False,default=lambda self: fields.Datetime.today())
    active=fields.Boolean(default=True)
    garden=fields.Boolean()
    salesman=fields.Char('Salesman',default=lambda self:self.env.user.name)
    buyer=fields.Char('Buyer',copy=False)
    postcode=fields.Integer()
    state=fields.Selection([('new','New'),('offer_recieved','Offer recieved'),('offer_accepted','Offer Accepted'),('cancelled','Cancelled'),('sold','Sold')],default='new',required=True)
    garden_area=fields.Integer()
    total_area=fields.Integer('Total Area',compute='_computed_area')
    garden_orientation=fields.Selection(
        selection=[('east','East'),('west','West')],
        help="this is for selecting the direction of the gardern"

    )
    accepted_in_global=fields.Integer(default=0)
    _sql_constraints=[
        ('check_expected_price','CHECK(expected_price>=0)','expected price should be a positve value'),
        ('check_selling_price','CHECK(selling_price>=0','selling price should be a positive value')
    ]



    @api.depends("living_area","garden_area")
    def _computed_area(self):
        for record in self:
            record.total_area=record.garden_area+record.living_area



    @api.depends("offer_ids.price")
    def _computed_best_offer(self):
        for record in self:
            try:
                record.bestoffer=max(record.offer_ids.mapped('price'))
            except ValueError:
                record.bestoffer=0
            # for val in record.offer_ids:
                    # newlist=[val.price]
                    # try:
                    #     max_val=max(newlist)
                    # except ValueError:
                    #     max_val=0
                    # record.bestoffer=max_val
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden !=False:
            self.garden_area=10
            self.garden_orientation='east'
        else:

            self.garden_area=False
            self.garden_orientation=False



    def action_sold(self):
        for record in self:
            if record.state=='cancelled':
                raise UserError("canecelled properties cannot sold")
            else:
                record.state='sold'
        return True
    def action_cancel(self):
        for record in self:
            if record.state=='sold':
                raise UserError("sold property cannot cancelled")
            else:
                record.state='cancelled'
    def action_fix_status(self):
        for record in self:
            record.accepted_in_global=0