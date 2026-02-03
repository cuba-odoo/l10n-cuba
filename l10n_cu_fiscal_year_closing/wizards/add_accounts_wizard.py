# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AddAccountsWizard(models.TransientModel):
    _name = 'l10n_cu.add.accounts.wizard'
    _description = 'Agregar Múltiples Cuentas al Cierre'

    closing_id = fields.Many2one('l10n_cu.fiscal.year.closing', string='Cierre', required=True)
    account_ids = fields.Many2many('account.account', string='Cuentas', 
                                  domain="[('company_id', '=', company_id), ('deprecated', '=', False)]")
    account_type = fields.Selection([
        ('income', 'Ingreso'),
        ('expense', 'Gasto'),
        ('other', 'Otro')
    ], string='Tipo', required=True, default='income')
    company_id = fields.Many2one('res.company', related='closing_id.company_id', readonly=True)

    @api.onchange('account_ids')
    def _onchange_account_ids(self):
        """Ajusta el tipo según las cuentas seleccionadas"""
        if self.account_ids:
            # Intentar detectar el tipo de las cuentas
            account_types = self.account_ids.mapped('user_type_id.type')
            if all(t == 'income' for t in account_types if t):
                self.account_type = 'income'
            elif all(t == 'expense' for t in account_types if t):
                self.account_type = 'expense'
            else:
                self.account_type = 'other'

    def action_add_accounts(self):
        """Agrega múltiples cuentas al cierre"""
        self.ensure_one()
        
        if not self.account_ids:
            raise UserError(_('Seleccione al menos una cuenta para agregar.'))
        
        # Verificar duplicados
        existing_accounts = self.env['l10n_cu.fiscal.year.closing.account'].search([
            ('closing_id', '=', self.closing_id.id),
            ('account_id', 'in', self.account_ids.ids)
        ])
        
        if existing_accounts:
            duplicate_names = ", ".join(existing_accounts.mapped('account_name'))
            raise UserError(_('Las siguientes cuentas ya están agregadas: %s') % duplicate_names)
        
        # Crear registros
        new_accounts = []
        for account in self.account_ids:
            new_accounts.append({
                'closing_id': self.closing_id.id,
                'account_id': account.id,
                'account_type': self.account_type,
                'include_in_closing': True,
            })
        
        self.env['l10n_cu.fiscal.year.closing.account'].create(new_accounts)
        
        return {
            'type': 'ir.actions.act_window_close',
        }