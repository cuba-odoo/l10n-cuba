# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


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
    
    # Saldos - ¡IMPORTANTE: store=True para que se guarde en DB!
    balance = fields.Monetary(string='Saldo', currency_field='currency_id', readonly=True, compute='_compute_balance', store=True, digits='Account')
    currency_id = fields.Many2one('res.currency', related='closing_id.currency_id', readonly=True)
    
    # Selección
    include_in_closing = fields.Boolean(string='Incluir en Cierre', default=True)
    
    # Estado
    state = fields.Selection(related='closing_id.state', string='Estado', readonly=True)

    @api.depends('account_id', 'closing_id.fiscal_year', 'closing_id.closing_date')
    def _compute_balance(self):
        """Calcula el saldo de la cuenta para el período del cierre - ¡CORREGIDO Y OPTIMIZADO!"""
        for record in self:
            if not record.account_id or not record.closing_id.fiscal_year:
                record.balance = 0.0
                continue
            
            try:
                # Validar año fiscal
                fiscal_year = int(record.closing_id.fiscal_year)
                start_date = fields.Date.from_string(f"{fiscal_year}-01-01")
                end_date = record.closing_id.closing_date
                
                # Buscar líneas contables del período
                domain = [
                    ('account_id', '=', record.account_id.id),
                    ('date', '>=', start_date),
                    ('date', '<=', end_date),
                    ('parent_state', '=', 'posted')
                ]
                lines = self.env['account.move.line'].search(domain)
                
                if not lines:
                    record.balance = 0.0
                    continue
                
                # Calcular saldo neto (débito - crédito)
                total_debit = sum(lines.mapped('debit'))
                total_credit = sum(lines.mapped('credit'))
                net_balance = total_debit - total_credit
                
                # Ajustar según tipo de cuenta para mostrar saldo natural
                if record.account_type == 'income':
                    # Para ingresos: el saldo natural es crédito (negativo en débito-crédito)
                    record.balance = -net_balance
                elif record.account_type == 'expense':
                    # Para gastos: el saldo natural es débito (positivo en débito-crédito)
                    record.balance = net_balance
                else:
                    record.balance = net_balance
                    
                # Redondear a 2 decimales (estándar contable)
                record.balance = round(record.balance, 2)
                    
            except Exception as e:
                record.balance = 0.0
                # Opcional: registrar en logs para debugging
                # self.env['ir.logging'].sudo().create({
                #     'name': 'Cierre Fiscal Error',
                #     'type': 'server',
                #     'level': 'WARNING',
                #     'message': f'Error calculando saldo cuenta {record.account_code}: {str(e)}',
                #     'path': 'l10n_cu_fiscal_year_closing',
                # })