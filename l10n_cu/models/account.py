# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

# class AccountAccount(models.Model):
#     _inherit = 'account.account'
#
#     note = fields.Text("Note")

class AccountAccountTag(models.Model):
    _inherit = 'account.account.tag'

    nature = fields.Selection([
        ('D', 'Debitable Account'), ('A', 'Creditable Account')])
