# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError

# Fields whose change may require rebuilding the account/element combinations.
AA_CHILDS_TRIGGER_FIELDS = {'element_id', 'element_detailed', 'parent_id', 'active', 'plan_id'}


class ExpenseElement(models.Model):
    _name = "expense.element"
    _description = 'Expense element'
    _parent_store = True

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    parent_id = fields.Many2one('expense.element',  index=True, ondelete='set null', readonly=False, store=True)
    parent_path = fields.Char(index=True, unaccent=False)
    child_ids = fields.One2many('expense.element', 'parent_id')
    company_id = fields.Many2one('res.company', required=True, readonly=True, default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        self._create_aa_childs()
        return res

    def _create_aa_childs(self):
        """Create/update the combined analytic accounts (container account x expense element).

        Idempotent and bidirectional. Only analytic accounts linked to an expense
        element (element_id set) are ever archived or unarchived; regular analytic
        accounts are never touched.
        - Archive combinations whose element is no longer a leaf.
        - Unarchive combinations whose element became a leaf again.
        - Create missing combinations for existing container accounts.
        - Refuse to archive combinations that have analytic lines.
        """
        if self.env.context.get('skip_aa_childs'):
            return []
        Account = self.env['account.analytic.account'].with_context(skip_aa_childs=True)
        leaf_elements = self.search([('child_ids', '=', False)])
        # active_test=False so archived combinations can be found (needed to unarchive)
        all_combined = Account.with_context(active_test=False).search([('element_id', '!=', False)])

        # 1. Archive combinations that are no longer valid
        to_deactivate = all_combined.filtered(
            lambda a: a.active and a.element_id not in leaf_elements
        )
        line_model = self.env['account.analytic.line']
        for account in to_deactivate:
            if line_model.search_count([('account_id', '=', account.id)], limit=1):
                raise ValidationError(self.env._(
                    "The analytic account '%s' cannot be archived because it has "
                    "analytic lines. Reassign or delete those lines first.",
                    account.display_name,
                ))
        if to_deactivate:
            to_deactivate.write({'active': False})

        # 2. Unarchive combinations that became valid again
        to_reactivate = all_combined.filtered(
            lambda a: not a.active and a.element_id in leaf_elements
        )
        if to_reactivate:
            to_reactivate.write({'active': True})

        # 3. Create missing combinations
        active_combined = all_combined.filtered('active')
        containers = Account.search([('element_detailed', '=', True), ('element_id', '=', False)])
        to_create = []
        for container in containers:
            existing = active_combined.filtered(lambda a: a.parent_id == container).element_id
            for element in leaf_elements - existing:
                to_create.append({
                    'name': '%s-%s' % (container.name, element.name),
                    'code': '%s.%s' % (container.code or '', element.code),
                    'element_id': element.id,
                    'parent_id': container.id,
                    'plan_id': container.plan_id.id,
                })
        if to_create:
            Account.create(to_create)
        return to_create


class AnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    element_detailed = fields.Boolean(string='Element_detailed', default=False)
    element_id = fields.Many2one('expense.element',  index=True, ondelete='set null', readonly=False, store=True)
    parent_id = fields.Many2one('account.analytic.account',  index=True, ondelete='set null', readonly=False, store=True)

    @api.constrains('parent_id', 'element_id', 'element_detailed')
    def _constraint_element_code(self):
        for record in self:
            if record.element_id and record.element_detailed:
                raise ValidationError(self.env._(
                    "An analytic account cannot be 'element detailed' and be linked "
                    "to an expense element at the same time."
                ))
            if record.element_id and record.parent_id and not record.parent_id.element_detailed:
                raise ValidationError(self.env._(
                    "A combined analytic account must belong to a container account "
                    "with 'element detailed' enabled."
                ))

    def write(self, vals):
        """Rebuild account/element combinations only when a relevant field changes."""
        res = super().write(vals)
        if not self.env.context.get('skip_aa_childs') and AA_CHILDS_TRIGGER_FIELDS & set(vals):
            self.env['expense.element']._create_aa_childs()
        return res

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        if not self.env.context.get('skip_aa_childs') and any(
            vals.get('element_detailed') or vals.get('element_id') for vals in vals_list
        ):
            self.env['expense.element']._create_aa_childs()
        return records
