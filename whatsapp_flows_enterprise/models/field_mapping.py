from odoo import models, fields, api
import json
from odoo.exceptions import UserError


class WAFlowTemplate(models.Model):
    _name = 'field.mapping'
    _description = 'Whatsapp flow template configurations'
    _order = 'sequence, id'

    flow_id = fields.Many2one('wa.flows',string="Related Flow")
    sequence = fields.Integer(string="Sequence", default=10)
    mapped_field = fields.Many2one("ir.model.fields", string="Mapped field to insert data into.", ondelete='cascade')
