# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HrContractTemplate(models.Model):
    _name = 'hr.contract.template'
    _description = 'Contract Template'

    name = fields.Many2one("hr.job", "Job")
    struct_id = fields.Many2one("hr.payroll.structure", "Estructura salarial")
    resource_calendar_id = fields.Many2one("resource.calendar", "Working Schedule")
    wage = fields.Float("Wage")
    body = fields.Html("Body")