# -*- coding: utf-8 -*-
from odoo import fields, models, api

class HrContract(models.Model):
    _inherit = 'hr.contract'

    regimen_contribution = fields.Selection([('2000','2000'),('2500','2500'),('2700','2700'),('3000','3000'),
    ('3500','3500'),('4000','4000'),('4500','4500'),('5000','5000'),('5500','5500'),('6000','6000'),('6500','6500'),
    ('7000','7000'),('7500','7500'),('8000','8000'),('8500','8500'),('9000','9000'),('9500','9500')],
                                            string='Regimen Contribution', help="Régimen de contribución para los socios.")

    multi_job = fields.Boolean("Pluriempleo")
