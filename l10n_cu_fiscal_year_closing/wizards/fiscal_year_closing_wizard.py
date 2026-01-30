# -*- coding: utf-8 -*-
from odoo import models, fields, api, _  # ¡IMPORTANTE! El "_" está aquí
from datetime import date


class FiscalYearClosingWizard(models.TransientModel):
    _name = 'l10n_cu.fiscal.year.closing.wizard'
    _description = 'Asistente de Cierre de Ejercicio'

    fiscal_year = fields.Char(
        string='Ejercicio Fiscal',
        required=True,
        default=lambda self: str(date.today().year - 1)  # Por defecto año anterior
    )
    closing_date = fields.Date(
        string='Fecha de Cierre',
        required=True,
        default=lambda self: date(int(date.today().year - 1), 12, 31)
    )
    company_id = fields.Many2one(
        'res.company',
        string='Compañía',
        required=True,
        default=lambda self: self.env.company
    )

    def action_create_closing(self):
        """Crea registro de cierre y abre formulario para cálculo"""
        closing = self.env['l10n_cu.fiscal.year.closing'].create({
            'name': _('Cierre %s') % self.fiscal_year,
            'fiscal_year': self.fiscal_year,
            'closing_date': self.closing_date,
            'company_id': self.company_id.id,
        })
        
        return {
            'name': _('Cierre de Ejercicio %s') % self.fiscal_year,
            'type': 'ir.actions.act_window',
            'res_model': 'l10n_cu.fiscal.year.closing',
            'res_id': closing.id,
            'view_mode': 'form',
            'target': 'current',
        }