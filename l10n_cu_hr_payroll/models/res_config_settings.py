# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    min_salary = fields.Char(string='Salario mínimo', config_parameter='l10n_cu_hr_payroll.default_min_salary')

