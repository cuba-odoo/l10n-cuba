# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date


class FiscalYearClosing(models.Model):
    _name = 'l10n_cu.fiscal.year.closing'
    _description = 'Cierre de Ejercicio Fiscal Cubano'
    _order = 'closing_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Referencia', required=True, default=lambda self: _('Cierre %s') % date.today().year)
    company_id = fields.Many2one('res.company', string='Compañía', required=True, default=lambda self: self.env.company)
    fiscal_year = fields.Char(string='Ejercicio Fiscal', required=True, default=lambda self: str(date.today().year))
    closing_date = fields.Date(string='Fecha de Cierre', required=True, default=lambda self: date(date.today().year, 12, 31))
    move_id = fields.Many2one('account.move', string='Asiento de Cierre', readonly=True, copy=False)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('posted', 'Cerrado'),
        ('cancelled', 'Cancelado')
    ], string='Estado', default='draft', readonly=True)
    
    # Cuentas seleccionadas para el cierre
    account_ids = fields.One2many('l10n_cu.fiscal.year.closing.account', 'closing_id', string='Cuentas para Cierre')
    
    # Resúmenes
    total_income = fields.Monetary(string='Total Ingresos', currency_field='currency_id', readonly=True, compute='_compute_totals')
    total_expense = fields.Monetary(string='Total Gastos', currency_field='currency_id', readonly=True, compute='_compute_totals')
    net_result = fields.Monetary(string='Resultado Neto', currency_field='currency_id', readonly=True, compute='_compute_totals', 
                                help='Positivo = Utilidad, Negativo = Pérdida')
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    
    # Contadores
    total_accounts = fields.Integer(string='Total Cuentas', compute='_compute_counters')
    selected_accounts = fields.Integer(string='Cuentas Seleccionadas', compute='_compute_counters')

    @api.depends('account_ids.balance', 'account_ids.account_type', 'account_ids.include_in_closing')
    def _compute_totals(self):
        """Calcula los totales basados en las cuentas seleccionadas"""
        for record in self:
            income = sum(acc.balance for acc in record.account_ids if acc.account_type == 'income' and acc.include_in_closing)
            expense = sum(acc.balance for acc in record.account_ids if acc.account_type == 'expense' and acc.include_in_closing)
            record.total_income = income
            record.total_expense = expense
            record.net_result = income - expense

    @api.depends('account_ids')
    def _compute_counters(self):
        """Calcula contadores de cuentas"""
        for record in self:
            record.total_accounts = len(record.account_ids)
            record.selected_accounts = len(record.account_ids.filtered(lambda x: x.include_in_closing))

    def action_load_suggested_accounts(self):
        """Carga automáticamente las cuentas sugeridas según patrones comunes"""
        self.ensure_one()
        
        if self.state != 'draft':
            raise UserError(_('Solo se puede cargar cuentas desde estado Borrador'))
        
        # Eliminar cuentas existentes
        self.account_ids.unlink()
        
        # Rango de fechas del ejercicio
        try:
            start_date = date(int(self.fiscal_year), 1, 1)
        except:
            raise UserError(_('El ejercicio fiscal debe ser un año válido (ej: 2025)'))
        
        # 🔑 Buscar cuentas según patrones comunes
        suggested_accounts = []
        suggested_account_ids = set()  # Para evitar duplicados
        
        # Patrón 1: Plan cubano NC-04 (sin puntos) - Ingresos 900xxxx
        accounts_900 = self.env['account.account'].search([
            ('company_id', '=', self.company_id.id),
            ('code', '=like', '900%'),
            ('deprecated', '=', False)
        ])
        for acc in accounts_900:
            if acc.id not in suggested_account_ids:
                suggested_accounts.append({
                    'closing_id': self.id,
                    'account_id': acc.id,
                    'account_type': 'income',
                    'include_in_closing': True,
                })
                suggested_account_ids.add(acc.id)
        
        # Patrón 2: Plan cubano NC-04 (sin puntos) - Gastos 822xxxx
        accounts_822 = self.env['account.account'].search([
            ('company_id', '=', self.company_id.id),
            ('code', '=like', '822%'),
            ('deprecated', '=', False)
        ])
        for acc in accounts_822:
            if acc.id not in suggested_account_ids:
                suggested_accounts.append({
                    'closing_id': self.id,
                    'account_id': acc.id,
                    'account_type': 'expense',
                    'include_in_closing': True,
                })
                suggested_account_ids.add(acc.id)
        
        # Patrón 3: Plan cubano con puntos - Ingresos 900.xxxx
        accounts_900_dot = self.env['account.account'].search([
            ('company_id', '=', self.company_id.id),
            ('code', '=like', '900.%'),
            ('deprecated', '=', False)
        ])
        for acc in accounts_900_dot:
            if acc.id not in suggested_account_ids:
                suggested_accounts.append({
                    'closing_id': self.id,
                    'account_id': acc.id,
                    'account_type': 'income',
                    'include_in_closing': True,
                })
                suggested_account_ids.add(acc.id)
        
        # Patrón 4: Plan cubano con puntos - Gastos 822.xxxx
        accounts_822_dot = self.env['account.account'].search([
            ('company_id', '=', self.company_id.id),
            ('code', '=like', '822.%'),
            ('deprecated', '=', False)
        ])
        for acc in accounts_822_dot:
            if acc.id not in suggested_account_ids:
                suggested_accounts.append({
                    'closing_id': self.id,
                    'account_id': acc.id,
                    'account_type': 'expense',
                    'include_in_closing': True,
                })
                suggested_account_ids.add(acc.id)
        
        # Patrón 5: Cuentas estándar de Odoo - Ingresos
        accounts_income = self.env['account.account'].search([
            ('company_id', '=', self.company_id.id),
            ('user_type_id.type', '=', 'income'),
            ('deprecated', '=', False),
            ('id', 'not in', list(suggested_account_ids))
        ])
        for acc in accounts_income:
            suggested_accounts.append({
                'closing_id': self.id,
                'account_id': acc.id,
                'account_type': 'income',
                'include_in_closing': False,
            })
            suggested_account_ids.add(acc.id)
        
        # Patrón 6: Cuentas estándar de Odoo - Gastos
        accounts_expense = self.env['account.account'].search([
            ('company_id', '=', self.company_id.id),
            ('user_type_id.type', '=', 'expense'),
            ('deprecated', '=', False),
            ('id', 'not in', list(suggested_account_ids))
        ])
        for acc in accounts_expense:
            suggested_accounts.append({
                'closing_id': self.id,
                'account_id': acc.id,
                'account_type': 'expense',
                'include_in_closing': False,
            })
            suggested_account_ids.add(acc.id)
        
        # Crear registros
        if suggested_accounts:
            self.env['l10n_cu.fiscal.year.closing.account'].create(suggested_accounts)
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Cuentas cargadas'),
                    'message': _('Se encontraron %s cuentas sugeridas.\nRevise y ajuste las cuentas antes de crear el asiento.') % len(suggested_accounts),
                    'type': 'success',
                    'sticky': False,
                }
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('No se encontraron cuentas'),
                    'message': _('No se encontraron cuentas con los patrones comunes.\nPuede agregar cuentas manualmente usando el botón "Agregar Cuentas".'),
                    'type': 'warning',
                    'sticky': False,
                }
            }

    def action_add_accounts(self):
        """Abre wizard para agregar cuentas manualmente (múltiples)"""
        self.ensure_one()
        
        return {
            'name': _('Agregar Cuentas Manualmente'),
            'type': 'ir.actions.act_window',
            'res_model': 'l10n_cu.add.accounts.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_closing_id': self.id,
            }
        }

    def action_calculate_balances(self):
        """Recalcula los saldos de todas las cuentas"""
        self.ensure_one()
        
        # Recalcular balances de cada cuenta
        for account_line in self.account_ids:
            account_line._compute_balance()
        
        # Recalcular totales
        self._compute_totals()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Saldos actualizados'),
                'message': _('Se recalculó el saldo de %s cuentas.') % len(self.account_ids),
                'type': 'info',
                'sticky': False,
            }
        }

    def action_create_closing_entry(self):
        """Genera el asiento contable de cierre basado en las cuentas seleccionadas"""
        self.ensure_one()
        
        if self.state != 'draft':
            raise UserError(_('Solo se puede crear el asiento desde estado Borrador'))
        
        if not self.account_ids.filtered(lambda x: x.include_in_closing):
            raise UserError(_('No hay cuentas seleccionadas para el cierre.\nPor favor, seleccione al menos una cuenta o cargue las cuentas sugeridas.'))
        
        if abs(self.total_income) < 0.01 and abs(self.total_expense) < 0.1:
            raise UserError(_('No hay movimientos en las cuentas seleccionadas para el período.\nVerifique la fecha de cierre y el ejercicio fiscal.'))

        # 🔑 Buscar cuenta de resultados
        retained_earnings_account = self.env['account.account'].search([
            ('code', '=', '999000000'),
            ('company_id', '=', self.company_id.id)
        ], limit=1)

        if not retained_earnings_account:
            retained_earnings_account = self.env['account.account'].search([
                ('code', '=like', '999%'),
                ('company_id', '=', self.company_id.id)
            ], limit=1)

        if not retained_earnings_account:
            retained_earnings_account = self.env['account.account'].search([
                ('name', 'ilike', '%resultados%'),
                ('company_id', '=', self.company_id.id)
            ], limit=1)

        if not retained_earnings_account:
            retained_earnings_account = self.env['account.account'].search([
                ('user_type_id.type', '=', 'equity'),
                ('company_id', '=', self.company_id.id)
            ], limit=1)

        if not retained_earnings_account:
            raise UserError(_(
                'No se encontró la cuenta de "Resultados" (999000000).\n\n'
                'Solución:\n'
                '1. Cree manualmente una cuenta con código 999000000\n'
                '2. O vaya a Contabilidad > Configuración > Plan de cuentas y busque "999"\n'
                '3. Asegúrese de que la cuenta exista y esté activa'
            ))

        # Obtener cuentas seleccionadas con saldo
        selected_accounts = self.account_ids.filtered(lambda x: x.include_in_closing and abs(x.balance) > 0.01)
        
        if not selected_accounts:
            raise UserError(_('No hay cuentas con saldo para cerrar.\nVerifique que las cuentas seleccionadas tengan movimientos en el período.'))

        # Líneas del asiento
        move_lines = []

        # 1. Cerrar cuentas de ingresos (débito para anular créditos)
        for acc in selected_accounts.filtered(lambda x: x.account_type == 'income'):
            if abs(acc.balance) > 0.01:
                move_lines.append((0, 0, {
                    'account_id': acc.account_id.id,
                    'debit': acc.balance,
                    'credit': 0.0,
                    'name': _('Cierre ingresos %s') % self.fiscal_year,
                }))

        # 2. Cerrar cuentas de gastos (crédito para anular débitos)
        for acc in selected_accounts.filtered(lambda x: x.account_type == 'expense'):
            if abs(acc.balance) > 0.01:
                move_lines.append((0, 0, {
                    'account_id': acc.account_id.id,
                    'debit': 0.0,
                    'credit': acc.balance,
                    'name': _('Cierre gastos %s') % self.fiscal_year,
                }))

        # 3. Diferencia a resultados acumulados
        if abs(self.net_result) > 0.01:
            move_lines.append((0, 0, {
                'account_id': retained_earnings_account.id,
                'debit': -self.net_result if self.net_result < 0 else 0.0,
                'credit': self.net_result if self.net_result > 0 else 0.0,
                'name': _('Resultado del ejercicio %s') % self.fiscal_year,
            }))

        # Validar que el asiento cuadre
        total_debit = sum(line[2]['debit'] for line in move_lines)
        total_credit = sum(line[2]['credit'] for line in move_lines)
        
        if abs(total_debit - total_credit) > 0.01:
            raise UserError(_('Error interno: El asiento no cuadra (Débito: %s, Crédito: %s). Contacte al administrador.') % 
                          (total_debit, total_credit))

        # Obtener diario de asientos varios
        journal = self.env['account.journal'].search([
            ('type', '=', 'general'),
            ('company_id', '=', self.company_id.id)
        ], limit=1)
        
        if not journal:
            raise UserError(_('No se encontró un diario de tipo "Asientos varios" para la compañía %s') % self.company_id.name)

        # ✅ MEJORA: Nombre del asiento más descriptivo
        move_ref = _('Cierre de Cuentas Nominales del año %s') % self.fiscal_year

        # Crear asiento
        move = self.env['account.move'].create({
            'date': self.closing_date,
            'journal_id': journal.id,
            'move_type': 'entry',
            'ref': move_ref,  # ✅ NOMBRE MEJORADO
            'line_ids': move_lines,
            'company_id': self.company_id.id,
        })

        self.move_id = move.id
        self.state = 'posted'

        return {
            'name': _('Asiento de Cierre'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': move.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_cancel(self):
        """Cancela el cierre (elimina el asiento)"""
        self.ensure_one()
        if self.move_id:
            if self.move_id.state == 'posted':
                self.move_id.button_draft()
            self.move_id.unlink()
        self.state = 'cancelled'
        return True