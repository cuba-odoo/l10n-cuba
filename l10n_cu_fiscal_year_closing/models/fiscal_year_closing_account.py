# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class FiscalYearClosingAccount(models.Model):
    _name = 'l10n_cu.fiscal.year.closing.account'
    _description = 'Cuentas para Cierre de Ejercicio Fiscal'
    _order = 'account_type desc, account_code'

    closing_id = fields.Many2one('l10n_cu.fiscal.year.closing', string='Cierre', required=True, ondelete='cascade')
    account_id = fields.Many2one('account.account', string='Cuenta', required=True, ondelete='cascade')
    account_code = fields.Char(related='account_id.code', string='Código', readonly=True, store=True)
    account_name = fields.Char(related='account_id.name', string='Nombre', readonly=True, store=True)
    account_type = fields.Selection([
        ('income', 'Ingreso'),
        ('expense', 'Gasto'),
        ('other', 'Otro')
    ], string='Tipo', required=True, default='other')
    
    # Saldos
    balance = fields.Monetary(string='Saldo', currency_field='currency_id', readonly=True, compute='_compute_balance')
    currency_id = fields.Many2one('res.currency', related='closing_id.currency_id', readonly=True)
    
    # Selección
    include_in_closing = fields.Boolean(string='Incluir en Cierre', default=True)
    
    # Estado
    state = fields.Selection(related='closing_id.state', string='Estado', readonly=True)

    @api.depends('account_id', 'closing_id.fiscal_year', 'closing_id.closing_date')
    def _compute_balance(self):
        """Calcula el saldo de la cuenta para el período del cierre"""
        for record in self:
            if not record.account_id or not record.closing_id.fiscal_year:
                record.balance = 0.0
                continue
            
            try:
                start_date = fields.Date.from_string(f"{record.closing_id.fiscal_year}-01-01")
                end_date = record.closing_id.closing_date
                
                domain = [
                    ('account_id', '=', record.account_id.id),
                    ('date', '>=', start_date),
                    ('date', '<=', end_date),
                    ('parent_state', '=', 'posted')
                ]
                lines = self.env['account.move.line'].search(domain)
                
                balance = sum(lines.mapped('debit')) - sum(lines.mapped('credit'))
                
                # Ajustar según tipo de cuenta
                if record.account_type == 'income':
                    record.balance = -balance
                elif record.account_type == 'expense':
                    record.balance = balance
                else:
                    record.balance = balance
                    
            except Exception as e:
                record.balance = 0.0