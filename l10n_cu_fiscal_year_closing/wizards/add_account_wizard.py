# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AddAccountWizard(models.TransientModel):
    _name = 'l10n_cu.add.account.wizard'
    _description = 'Agregar Cuenta Manualmente al Cierre'

    closing_id = fields.Many2one('l10n_cu.fiscal.year.closing', string='Cierre', required=True)
    account_id = fields.Many2one('account.account', string='Cuenta', required=True, domain="[('company_id', '=', company_id), ('deprecated', '=', False)]")
    account_type = fields.Selection([
        ('income', 'Ingreso'),
        ('expense', 'Gasto'),
        ('other', 'Otro')
    ], string='Tipo', required=True, default='income')
    company_id = fields.Many2one('res.company', related='closing_id.company_id', readonly=True)

    def action_add_account(self):
        """Agrega la cuenta seleccionada al cierre"""
        self.ensure_one()
        
        # Verificar si la cuenta ya existe
        existing = self.env['l10n_cu.fiscal.year.closing.account'].search([
            ('closing_id', '=', self.closing_id.id),
            ('account_id', '=', self.account_id.id)
        ], limit=1)
        
        if existing:
            raise UserError(_('La cuenta "%s" ya está agregada al cierre.') % self.account_id.name)
        
        # Crear registro
        self.env['l10n_cu.fiscal.year.closing.account'].create({
            'closing_id': self.closing_id.id,
            'account_id': self.account_id.id,
            'account_type': self.account_type,
            'include_in_closing': True,
        })
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Cuenta agregada'),
                'message': _('La cuenta "%s" ha sido agregada al cierre.') % self.account_id.name,
                'type': 'success',
                'sticky': False,
            }
        }