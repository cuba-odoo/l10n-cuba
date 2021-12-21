# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    other_input_id = fields.One2many('hr.payroll.other.input', 'employee_id', 'Other Inputs',
                                     help="Entradas específicas al trabajador. Ej. Para pagarle vacaciones acumuladas o "
                                          "prestaciones sociales. Descuentos o retenciones al trabajador.")
