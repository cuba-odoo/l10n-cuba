# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date
from odoo.tools import formatLang


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
    account_ids = fields.One2many('l10n_cu.fiscal.year.closing.account', 'closing_id', string='Cuentas para Cierre', copy=False)
    
    # Resúmenes - ¡IMPORTANTE: store=True para que se guarden en DB!
    total_income = fields.Monetary(string='Total Ingresos', currency_field='currency_id', readonly=True, compute='_compute_totals', store=True)
    total_expense = fields.Monetary(string='Total Gastos', currency_field='currency_id', readonly=True, compute='_compute_totals', store=True)
    net_result = fields.Monetary(string='Resultado Neto', currency_field='currency_id', readonly=True, compute='_compute_totals', store=True,
                                help='Positivo = Utilidad, Negativo = Pérdida')
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    
    # Contadores
    total_accounts = fields.Integer(string='Total Cuentas', compute='_compute_counters', store=True)
    selected_accounts = fields.Integer(string='Cuentas Seleccionadas', compute='_compute_counters', store=True)

    @api.depends('account_ids.balance', 'account_ids.account_type', 'account_ids.include_in_closing')
    def _compute_totals(self):
        """Calcula los totales basados en las cuentas seleccionadas"""
        for record in self:
            if record.account_ids:
                income = sum(acc.balance for acc in record.account_ids if acc.account_type == 'income' and acc.include_in_closing)
                expense = sum(acc.balance for acc in record.account_ids if acc.account_type == 'expense' and acc.include_in_closing)
                record.total_income = income
                record.total_expense = expense
                record.net_result = income - expense
            else:
                record.total_income = 0.0
                record.total_expense = 0.0
                record.net_result = 0.0

    @api.depends('account_ids')
    def _compute_counters(self):
        """Calcula contadores de cuentas"""
        for record in self:
            record.total_accounts = len(record.account_ids)
            record.selected_accounts = len(record.account_ids.filtered(lambda x: x.include_in_closing))

    def action_load_suggested_accounts(self):
        """Carga automáticamente TODAS las cuentas nominales según NC-04 cubano oficial"""
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
        
        # 🔑 Buscar cuentas nominales según NC-04 cubano COMPLETO
        suggested_accounts = []
        suggested_account_ids = set()  # Para evitar duplicados
        
        # ========================================================================
        # PATRÓN 1: INGRESOS - Grupo 900.xxxx completo (NC-04)
        # ========================================================================
        income_patterns = [
            '900%', '900.%',  # Ingresos generales
            '901%', '901.%',  # Ventas de mercancías
            '902%', '902.%',  # Ventas de servicios
            '903%', '903.%',  # Otros ingresos operacionales
            '904%', '904.%',  # Ingresos financieros
            '905%', '905.%',  # Ingresos extraordinarios
        ]
        
        for pattern in income_patterns:
            accounts = self.env['account.account'].search([
                ('company_id', '=', self.company_id.id),
                ('code', '=like', pattern),
                ('deprecated', '=', False)
            ])
            for acc in accounts:
                if acc.id not in suggested_account_ids:
                    suggested_accounts.append({
                        'closing_id': self.id,
                        'account_id': acc.id,
                        'account_type': 'income',
                        'include_in_closing': True,
                    })
                    suggested_account_ids.add(acc.id)
        
        # ========================================================================
        # PATRÓN 2: GASTOS - TODOS los grupos 8xx.xxxx del NC-04
        # ========================================================================
        expense_patterns = [
            # Grupo 800: Gastos generales
            '800%', '800.%',
            '801%', '801.%',  # Costo de ventas
            '802%', '802.%',  # Gastos de explotación
            '803%', '803.%',  # Gastos administrativos
            '804%', '804.%',  # Gastos de ventas
            '805%', '805.%',  # Otros gastos operacionales
            
            # Grupo 814: Gastos financieros específicos
            '814%', '814.%',
            
            # Grupos adicionales de gastos (822, 826, 835, 855)
            '822%', '822.%',  # Gastos operacionales
            '826%', '826.%',  # Gastos financieros
            '835%', '835.%',  # Gastos extraordinarios
            '855%', '855.%',  # Otros gastos
            
            # Otros grupos de gastos NC-04
            '860%', '860.%',  # Depreciaciones y amortizaciones
            '861%', '861.%',  # Provisiones
            '870%', '870.%',  # Impuestos sobre resultados
            '899%', '899.%',  # Ajustes de gastos
        ]
        
        for pattern in expense_patterns:
            accounts = self.env['account.account'].search([
                ('company_id', '=', self.company_id.id),
                ('code', '=like', pattern),
                ('deprecated', '=', False)
            ])
            for acc in accounts:
                if acc.id not in suggested_account_ids:
                    suggested_accounts.append({
                        'closing_id': self.id,
                        'account_id': acc.id,
                        'account_type': 'expense',
                        'include_in_closing': True,
                    })
                    suggested_account_ids.add(acc.id)
        
        # ========================================================================
        # PATRÓN 3: Fallback por tipo de cuenta (Odoo 15 - user_type_id.type)
        # ========================================================================
        # Ingresos por tipo de cuenta (Odoo 15)
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
        
        # Gastos por tipo de cuenta (Odoo 15)
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
            
            # Contar por tipo para mensaje informativo
            income_count = sum(1 for acc in suggested_accounts if acc['account_type'] == 'income')
            expense_count = sum(1 for acc in suggested_accounts if acc['account_type'] == 'expense')
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('✓ Cuentas cargadas'),
                    'message': _(
                        'Se cargaron %s cuentas nominales según NC-04:\n'
                        '• Ingresos (900-905.xxxx): %s cuentas\n'
                        '• Gastos (800-899.xxxx): %s cuentas\n\n'
                        'ℹ️ Haga clic en "Actualizar Lista" para ver las cuentas.'
                    ) % (len(suggested_accounts), income_count, expense_count),
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
                    'message': _(
                        'No se encontraron cuentas nominales con los patrones NC-04.\n\n'
                        'Patrones buscados:\n'
                        '• Ingresos: 900.xxxx a 905.xxxx\n'
                        '• Gastos: 800.xxxx a 899.xxxx\n\n'
                        'Verifique que su plan de cuentas esté configurado según NC-04.\n'
                        'O agregue cuentas manualmente con el botón "Agregar Cuentas".'
                    ),
                    'type': 'warning',
                    'sticky': False,
                }
            }

    def action_refresh_accounts_list(self):
        """Recarga la lista de cuentas en la vista - ¡NUEVO BOTÓN!"""
        self.ensure_one()
        
        # Forzar recálculo de saldos para cuentas existentes
        for account_line in self.account_ids:
            account_line._compute_balance()
        
        self._compute_totals()
        self._compute_counters()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
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
        """Recalcula los saldos de todas las cuentas - ¡CORREGIDO FORMATO MONEDA!"""
        self.ensure_one()
        
        if not self.account_ids:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('⚠️ Sin cuentas'),
                    'message': _('No hay cuentas agregadas para calcular saldos.\n'
                               'Use "Cargar Cuentas Sugeridas" o "Agregar Cuentas" primero.'),
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
        # Recalcular balances de cada cuenta
        for account_line in self.account_ids:
            account_line._compute_balance()
        
        # Recalcular totales
        self._compute_totals()
        self._compute_counters()
        
        # ✅ CORRECCIÓN: Usar formatLang en lugar de currency_id.format()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('✓ Saldos calculados'),
                'message': _('Totales actualizados:\n'
                           '• Ingresos: %s\n'
                           '• Gastos: %s\n'
                           '• Resultado: %s') % (
                    formatLang(self.env, self.total_income, currency_obj=self.currency_id),
                    formatLang(self.env, self.total_expense, currency_obj=self.currency_id),
                    formatLang(self.env, self.net_result, currency_obj=self.currency_id)
                ),
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
        
        # Validar que los saldos estén calculados
        if self.total_income == 0.0 and self.total_expense == 0.0:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('⚠️ Saldos no calculados'),
                    'message': _('Los saldos de las cuentas no han sido calculados.\n'
                               'Haga clic en "Calcular Saldos" antes de crear el asiento.'),
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
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

        # Fallback Odoo 15
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
                '2. O vaya a Contabilidad → Configuración → Plan de cuentas y busque "999"\n'
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
            'ref': move_ref,
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