# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_INCOME_TYPES = {'income', 'income_other'}
_EXPENSE_TYPES = {'expense', 'expense_direct_cost', 'expense_depreciation'}


class AddAccountsWizard(models.TransientModel):
    _name = 'l10n_cu.add.accounts.wizard'
    _description = 'Agregar Múltiples Cuentas al Cierre'

    closing_id = fields.Many2one('l10n_cu.fiscal.year.closing', string='Cierre', required=True)
    account_ids = fields.Many2many(
        'account.account', string='Cuentas',
        domain="[('company_ids', '=', company_id), ('deprecated', '=', False)]"
    )
    account_type = fields.Selection([
        ('income', 'Ingreso'),
        ('expense', 'Gasto'),
        ('other', 'Otro')
    ], string='Tipo', required=True, default='income')
    company_id = fields.Many2one('res.company', related='closing_id.company_id', readonly=True)

    @api.onchange('account_ids')
    def _onchange_account_ids(self):
        if not self.account_ids:
            return
        # account_type replaces user_type_id.type since Odoo 16
        types = self.account_ids.mapped('account_type')
        if all(t in _INCOME_TYPES for t in types if t):
            self.account_type = 'income'
        elif all(t in _EXPENSE_TYPES for t in types if t):
            self.account_type = 'expense'
        else:
            self.account_type = 'other'

    def action_add_accounts(self):
        self.ensure_one()
        if not self.account_ids:
            raise UserError(_('Seleccione al menos una cuenta para agregar.'))

        existing = self.env['l10n_cu.fiscal.year.closing.account'].search([
            ('closing_id', '=', self.closing_id.id),
            ('account_id', 'in', self.account_ids.ids)
        ])
        if existing:
            names = ', '.join(existing.mapped('account_name'))
            raise UserError(_('Las siguientes cuentas ya están agregadas: %s') % names)

        self.env['l10n_cu.fiscal.year.closing.account'].create([
            {
                'closing_id': self.closing_id.id,
                'account_id': account.id,
                'account_type': self.account_type,
                'include_in_closing': True,
            }
            for account in self.account_ids
        ])
        return {'type': 'ir.actions.act_window_close'}
