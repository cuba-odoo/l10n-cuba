# -*- coding: utf-8 -*-
from collections import defaultdict
from typing import Optional, Tuple

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class AccountAccount(models.Model):
    _inherit = 'account.account'
    
    account_type = fields.Selection(readonly=False, compute='_compute_account_type', precompute=False)
    expense_element_detailed = fields.Boolean(string='Expense element detailed?', 
        compute='_compute_expense_element_detailed',readonly=False )
    
    @api.depends('group_id', 'group_id.expense_element_detailed')
    def _compute_expense_element_detailed(self):
        for record in self:
            record.expense_element_detailed=record.group_id.expense_element_detailed   
    
    @api.depends('code', 'group_id', 'group_id.account_type')
    def _compute_account_type(self):
        super()._compute_account_type()
        for record in self:
            if record.group_id.account_type:
                record.account_type = record.group_id.account_type

    @api.depends('account_type', 'group_id', 'group_id.reconcile', 'group_id.account_type')
    def _compute_reconcile(self):
        grouped   = self.filtered(lambda a: a.group_id.account_type)
        ungrouped = self - grouped
        super(AccountAccount, ungrouped)._compute_reconcile()
        for account in grouped:
            account.reconcile = account.group_id.reconcile


class AccountAccountTag(models.Model):
    _inherit = 'account.account.tag'

    nature = fields.Selection([
        ('D', 'Debitable Account'), ('A', 'Creditable Account')])

class AccountChartTemplate(models.Model):
    _inherit = "account.chart.template"
    

    def _create_records_with_xmlid(self, model, template_vals, company):   
        if model=='account.group':     
            for record, vallist in template_vals:
                # vallist["parent_id"] = record.parent_id.id2
                vallist["note"] = record.note
                vallist["account_type"] = record.account_type
                vallist["reconcile"] = record.reconcile 
                vallist["expense_element_detailed"] = record.expense_element_detailed 
                vallist["group_template_id"] = record.get_external_id().get(record.id)
                vallist["chart_template_id"] = record.chart_template_id.id
                if record.parent_id:
                    vallist["group_template_parent_id"] = record.parent_id.get_external_id().get(record.parent_id.id)

        res= super()._create_records_with_xmlid(model,template_vals,company)
        return res
    
    def _create_bank_journals(self, company, acc_template_ref):
        '''
        This function creates bank journals and their account for each line
        data returned by the function _get_default_bank_journals_data.

        :param company: the company for which the wizard is running.
        :param acc_template_ref: the dictionary containing the mapping between the ids of account templates and the ids
            of the accounts that have been generated from them.

        Adding code parameter    
        '''
        self.ensure_one()
        bank_journals = self.env['account.journal']
        # Create the journals that will trigger the account.account creation
        for acc in self._get_default_bank_journals_data():
            bank_journals += self.env['account.journal'].create({
                'name': acc['acc_name'],
                'type': acc['account_type'],
                'company_id': company.id,
                'currency_id': acc.get('currency_id', self.env['res.currency']).id,
                'sequence': 10,
                'code' : acc.get('code','BNK'),
            })

        return bank_journals

    @api.model
    def _get_default_bank_journals_data(self):
        """ Returns the data needed to create the default bank journals when
        installing this chart of accounts, in the form of a list of dictionaries.
        The allowed keys in these dictionaries are:
            - acc_name: string (mandatory)
            - account_type: 'cash' or 'bank' (mandatory)
            - currency_id (optional, only to be specified if != company.currency_id)
            - addning journal code
        """
        default_journals=super()._get_default_bank_journals_data()
        journals_to_create=default_journals + [{'acc_name': 'Fondo para cambios', 'account_type': 'cash', 'code':'FCAMB'}, 
                {'acc_name': 'Fondo para pagos menores', 'account_type': 'cash', 'code':'FPMEN'},
                {'acc_name': 'Extraído para nómina', 'account_type': 'cash', 'code':'FNOM'},
                {'acc_name': 'Sellos', 'account_type': 'cash', 'code':'FSELL'},
                {'acc_name': 'Tarjetas prepagadas', 'account_type': 'cash', 'code':'FPREP'},
                {'acc_name': 'Otros valores en caja', 'account_type': 'cash', 'code':'FOTROS'}]
        return journals_to_create[1:]

class AccountGroupTemplate(models.Model):
    _inherit = "account.group.template"

    reconcile = fields.Boolean(string='Allow Reconciliation')   
    expense_element_detailed = fields.Boolean()
    account_type = fields.Selection(
        selection=[
            ("asset_receivable", "Receivable"),
            ("asset_cash", "Bank and Cash"),
            ("asset_current", "Current Assets"),
            ("asset_non_current", "Non-current Assets"),
            ("asset_prepayments", "Prepayments"),
            ("asset_fixed", "Fixed Assets"),
            ("liability_payable", "Payable"),
            ("liability_credit_card", "Credit Card"),
            ("liability_current", "Current Liabilities"),
            ("liability_non_current", "Non-current Liabilities"),
            ("equity", "Equity"),
            ("equity_unaffected", "Current Year Earnings"),
            ("income", "Income"),
            ("income_other", "Other Income"),
            ("expense", "Expenses"),
            ("expense_depreciation", "Depreciation"),
            ("expense_direct_cost", "Cost of Revenue"),
            ("off_balance", "Off-Balance Sheet"),
        ],
        string="Type", required=False, help="Account Type is used for information purpose, to generate country-specific legal reports, and set the rules to close a fiscal year and generate opening entries."
    )
    note = fields.Text("Content and Usage")


class AccountGroup(models.Model):
    _inherit = "account.group"

    chart_template_id = fields.Many2one('account.chart.template', string='Chart Template', index=True, ondelete='set null')
    parent_id = fields.Many2one('account.group', compute='_compute_parent', index=True, ondelete='set null', readonly=False, store=True)
    reconcile = fields.Boolean(string='Allow Reconciliation',
        compute='_compute_reconcile', store=True, readonly=False,
        help="Check this box if accounts belonging this account group allows invoices & payments matching of journal items."
    )
    expense_element_detailed = fields.Boolean(string='Expense element detailed?')
    active = fields.Boolean(default=True)
    account_type = fields.Selection(
        selection=[
            ("asset_receivable", "Receivable"),
            ("asset_cash", "Bank and Cash"),
            ("asset_current", "Current Assets"),
            ("asset_non_current", "Non-current Assets"),
            ("asset_prepayments", "Prepayments"),
            ("asset_fixed", "Fixed Assets"),
            ("liability_payable", "Payable"),
            ("liability_credit_card", "Credit Card"),
            ("liability_current", "Current Liabilities"),
            ("liability_non_current", "Non-current Liabilities"),
            ("equity", "Equity"),
            ("equity_unaffected", "Current Year Earnings"),
            ("income", "Income"),
            ("income_other", "Other Income"),
            ("expense", "Expenses"),
            ("expense_depreciation", "Depreciation"),
            ("expense_direct_cost", "Cost of Revenue"),
            ("off_balance", "Off-Balance Sheet"),
        ],
        string="Type", required=False, help="Account Type is used for information purpose, to generate country-specific legal reports, and set the rules to close a fiscal year and generate opening entries."
    )
    note = fields.Text("Content and Usage")
    group_template_id = fields.Char()
    group_template_parent_id = fields.Char()

    def init(self):
        self.env.cr.execute("""
            CREATE INDEX IF NOT EXISTS account_group_company_template_idx
            ON account_group (company_id, chart_template_id);
        """)

    def _parent_store_update(self):
        """Override intencional del mixin ``_parent_store``.

        PyDev marca este método con ``method-hidden`` porque sobreescribe un
        método "privado" del mixin. Es intencional: el mixin asume un único
        ``parent_id`` en el recordset y la carga del plan contable crea grupos
        con padres mixtos (padres e hijos en el mismo ``create``). Agrupamos
        por padre antes de delegar.
        """
        if not self:
            return
        by_parent = defaultdict(lambda: self.env['account.group'])
        for record in self:
            by_parent[record.parent_id.id] |= record
        for records in by_parent.values():
            if records:
                super(AccountGroup, records)._parent_store_update()

    @api.constrains('code_prefix_start', 'code_prefix_end',
                'chart_template_id', 'company_id')
    def _constraint_prefix_overlap(self):
        self.flush_model()
        if not self:
            return

        # Agrupar por (company, chart_template): 1 búsqueda por scope
        by_scope = defaultdict(lambda: self.env['account.group'])
        for group in self:
            if not group.code_prefix_start or not group.code_prefix_end:
                continue
            by_scope[(group.company_id.id, group.chart_template_id.id)] |= group

        for (company_id, template_id), groups in by_scope.items():
            scope = self.search([
                ('company_id', '=', company_id),
                ('chart_template_id', '=', template_id),
                ('code_prefix_start', '!=', False),
                ('code_prefix_end', '!=', False),
            ])
            for group in groups:
                for other in scope:
                    if other.id == group.id:
                        continue
                    if self._ranges_overlap_partially(group, other):
                        raise ValidationError(_(
                            "Los grupos de cuentas '%(a)s' y '%(b)s' se solapan "
                            "parcialmente. Deben ser disjuntos o estar uno "
                            "contenido en el otro.",
                            a=group.display_name,
                            b=other.display_name,
                        ))

    @api.constrains('code_prefix_start', 'code_prefix_end')
    def _constraint_prefix_numeric(self):
        """Exige que los prefijos sean numéricos.

        `_adapt_accounts_for_account_groups` usa `cast(code_prefix_end as int)`
        en SQL. Un prefijo no numérico ('130.', 'A01') hace fallar el cast
        en PostgreSQL y rompe el recálculo de group_id en todas las cuentas.
        Esta validación cierra esa clase de fallos en el origen.
        """
        for group in self:
            for field_name in ('code_prefix_start', 'code_prefix_end'):
                value = getattr(group, field_name)
                if value and not value.isdigit():
                    raise ValidationError(_(
                        "El prefijo '%(value)s' del campo %(field)s debe ser numérico. "
                        "El grupo '%(name)s' no puede tener prefijos no numéricos porque "
                        "el cálculo de asignación cuenta→grupo usa comparación numérica.",
                        value=value,
                        field=field_name,
                        name=group.display_name,
                    ))

    @staticmethod
    def _to_interval(start, end) -> Optional[Tuple[int, int]]:
        DEPTH = 10
        if not isinstance(start, str) or not isinstance(end, str):
            return None
        if not start or not end:
            return None
        if not (start.isdigit() and end.isdigit()):
            return None
        return (
            int(start.ljust(DEPTH, '0')),
            int(end.ljust(DEPTH, '9')),
        )

    @classmethod
    def _ranges_overlap_partially(cls, a, b) -> bool:
        a_iv = cls._to_interval(a.code_prefix_start, a.code_prefix_end)
        b_iv = cls._to_interval(b.code_prefix_start, b.code_prefix_end)
        if a_iv is None or b_iv is None:
            return False

        a_start, a_end = a_iv
        b_start, b_end = b_iv

        if (a_start <= b_start and a_end >= b_end) or \
           (b_start <= a_start and b_end >= a_end):
            return False
        if a_end < b_start or b_end < a_start:
            return False
        return True

    @api.depends('group_template_parent_id')
    def _compute_parent(self):
        if not self.filtered('group_template_parent_id'):
            return
        company_ids = self.company_id.ids
        if not company_ids:
            return
        relevant_templates = set(self.mapped('group_template_parent_id')) - {False}
        if not relevant_templates:
            return
        record_parents = self.search([
            ('company_id', 'in', company_ids),
            ('group_template_id', 'in', list(relevant_templates)),
        ])
        # Índice O(n): clave (group_template_id, company_id) → registro padre
        parent_map = {
            (it.group_template_id, it.company_id.id): it
            for it in record_parents
        }
        for record in self.filtered('group_template_parent_id'):
            parent = parent_map.get(
                (record.group_template_parent_id, record.company_id.id)
            )
            if parent and record.parent_id != parent:
                record.parent_id = parent.id

    @api.depends('account_type')
    def _compute_reconcile(self):
        for group in self:
            group.reconcile = group.account_type in ('asset_receivable', 'liability_payable')

    def unlink(self):
        if self:
            self.write({'parent_id': False})
        return super(AccountGroup, self).unlink()
 
    def _adapt_parent_account_group(self):
        if not self:
            return
        super()._adapt_parent_account_group()
        self.flush_model()
        company_ids = self.company_id.ids
        if not company_ids:
            return

        all_groups = self.search([('company_id', 'in', company_ids)])
        parent_map = {
            (it.group_template_id, it.company_id.id): it
            for it in all_groups if it.group_template_id
        }
        self_templates = set(self.mapped('group_template_id')) - {False}
        to_reassign = all_groups.filtered(
            lambda g: g in self
            or (g.group_template_parent_id and g.group_template_parent_id in self_templates)
        )

        # 1) Reasignar padre por lote (1 write por padre, no por registro)
        by_parent_id = defaultdict(list)
        for record in to_reassign.filtered('group_template_parent_id'):
            parent = parent_map.get(
                (record.group_template_parent_id, record.company_id.id)
            )
            if parent and record.parent_id != parent:
                by_parent_id[parent.id].append(record.id)

        for parent_id, record_ids in by_parent_id.items():
            self.browse(record_ids).write({'parent_id': parent_id})

        # 2) Refrescar parent_path agrupando por padre
        self.invalidate_model(['parent_id'])
        by_parent = defaultdict(lambda: self.env['account.group'])
        for record in to_reassign:
            by_parent[record.parent_id.id] |= record
        for records in by_parent.values():
            if records:
                records._parent_store_update()

    def _adapt_accounts_for_account_groups(self, account_ids=None):
        """Ensure consistency between accounts and account groups.
        Find and set the most specific group matching the code of the account.
        The most specific is the one with the longest prefixes and with the starting
        prefix being smaller than the account code and the ending prefix being greater.
        """
        company_ids = account_ids.company_id.ids if account_ids else self.company_id.ids
        account_ids = account_ids.ids if account_ids else []
        if not company_ids and not account_ids:
            return
        self.flush_model()
        self.env['account.account'].flush_model()

        account_where_clause = ''
        where_params = [tuple(company_ids)]
        if account_ids:
            account_where_clause = 'AND account.id IN %s'
            where_params.append(tuple(account_ids))

        self._cr.execute(f'''
            WITH candidates_account_groups AS (
                                SELECT
                    account.id AS account_id,
					account.code,
					ARRAY_AGG(agroup.id ORDER BY cast(agroup.code_prefix_end as int)- cast(agroup.code_prefix_start as int), agroup.id) AS group_ids
                FROM account_account account
                LEFT JOIN account_group agroup
                    ON agroup.code_prefix_start <= LEFT(account.code, char_length(agroup.code_prefix_start))
                    AND agroup.code_prefix_end >= LEFT(account.code, char_length(agroup.code_prefix_end))
                    AND agroup.company_id = account.company_id
                WHERE account.company_id IN %s {account_where_clause}
                GROUP BY account.id
            )
            UPDATE account_account
            SET group_id = rel.group_ids[1]
            FROM candidates_account_groups rel
            WHERE account_account.id = rel.account_id
        ''', where_params)
        self.env['account.account'].invalidate_model(['group_id'])
        self.env['account.account'].modified(['group_id'])   