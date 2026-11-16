# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


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
        # aqui tengo que verificar las cuentas analiticas que referencian elementos, y desactivar las que no sean hojas    
        self._create_aa_childs()
        return res

    def _create_aa_childs(self):
        """Crea/actualiza las cuentas analíticas combinadas cuenta-elemento.

        Es idempotente y bidireccional:
        - Desactiva combinaciones cuyo elemento dejó de ser hoja.
        - Reactiva combinaciones cuyo elemento volvió a ser hoja.
        - Crea combinaciones faltantes para cuentas contenedoras existentes.
        - Se niega a desactivar combinaciones con líneas analíticas.
        """
        if self.env.context.get('skip_aa_childs'):
            return []
        leaf_elements = self.search([('child_ids', '=', False)])
        # active_test=False para encontrar también las inactivas (necesario para reactivar)
        all_combined = self.env['account.analytic.account'].with_context(
            active_test=False
        ).search([('element_id', '!=', False)])

        # 1. Desactivar las que dejaron de ser válidas
        to_deactivate = all_combined.filtered(
            lambda a: a.active and a.element_id not in leaf_elements
        )
        line_model = self.env['account.analytic.line']
        for account in to_deactivate:
            if line_model.search_count([('account_id', '=', account.id)]):
                raise ValidationError(_(
                    "No se puede desactivar la cuenta analítica '%s' porque tiene "
                    "líneas analíticas asociadas. Reasigne o elimine esas líneas primero."
                ) % account.display_name)
        to_deactivate.with_context(skip_aa_childs=True).write({'active': False})

        # 2. Reactivar las que volvieron a ser válidas
        to_reactivate = all_combined.filtered(
            lambda a: not a.active and a.element_id in leaf_elements
        )
        to_reactivate.with_context(skip_aa_childs=True).write({'active': True})

        # 3. Crear las combinaciones faltantes
        active_combined = all_combined.filtered('active')
        containers = self.env['account.analytic.account'].search(
            [('element_detailed', '=', True), ('element_id', '=', False)]
        )
        to_create = []
        for container in containers:
            existing_ids = active_combined.filtered(
                lambda a: a.parent_id == container
            ).element_id
            for element in leaf_elements - existing_ids:
                to_create.append({
                    'name': '%s-%s' % (container.name, element.name),
                    'code': '%s.%s' % (container.code, element.code),
                    'element_id': element.id,
                    'parent_id': container.id,
                    'plan_id': container.plan_id.id,
                })
        if to_create:
            self.env['account.analytic.account'].with_context(
                skip_aa_childs=True
            ).create(to_create)
        return to_create

class AnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'
    element_detailed= fields.Boolean(string='Element_detailed', default=False )
    element_id = fields.Many2one('expense.element',  index=True, ondelete='set null', readonly=False, store=True)
    parent_id = fields.Many2one('account.analytic.account',  index=True, ondelete='set null', readonly=False, store=True)

    @api.constrains('parent_id', 'element_id', 'element_detailed')
    def _constraint_element_code(self):
        for record in self:
            if record.element_id and record.element_detailed:
                raise ValidationError(_(
                    "Una cuenta analítica no puede ser 'elemento detallado' y tener "
                    "a la vez un elemento de gasto vinculado."
                ))
            if record.element_id and record.parent_id and not record.parent_id.element_detailed:
                raise ValidationError(_(
                    "Una cuenta combinada debe colgar de una cuenta contenedora "
                    "con 'element_detailed' activo."
                ))

    @api.constrains('element_id', 'element_detailed')
    def _validate_element_detailed(self):
        for record in self:
            if record.element_id and record.element_detailed:
                raise ValidationError('Invalid operation. This a analytic account has a related expense element')

    def write(self, vals):
        """ Automatically create new accounts with combination account-element """
        write_res = super(AnalyticAccount, self).write(vals)
        if not self.env.context.get('skip_aa_childs'):
            self.env['expense.element']._create_aa_childs()
        return write_res

    @api.model_create_multi
    def create(self, vals_list):
        records = super(AnalyticAccount, self).create(vals_list)
        if not self.env.context.get('skip_aa_childs'):
            self.env['expense.element']._create_aa_childs()
        return records
