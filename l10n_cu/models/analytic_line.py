# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    analytic_account_parent_id = fields.Many2one('account.analytic.account', compute='_compute_analytic_parent', index=True, ondelete='set null', readonly=False, store=True)
    analytic_element_id = fields.Many2one('expense.element', compute='_compute_analytic_expense_element_id', index=True, ondelete='set null', readonly=True, store=True)
    element_id = fields.Many2one('expense.element',  index=True, ondelete='set null', readonly=False, store=True)

    @api.depends('account_id')
    def _compute_analytic_parent(self):
        for record in self:
            record.analytic_account_parent_id = record.account_id.parent_id.id

    @api.depends('account_id', 'account_id.element_id')
    def _compute_analytic_expense_element_id(self):
        for record in self:
            record.analytic_element_id = record.account_id.element_id.id

    @api.constrains('account_id', 'element_id')
    def _check_element_coherence(self):
        self.flush_recordset(['analytic_element_id'])
        for line in self:
            account_element = line.account_id.element_id

            # Coherencia entre element_id manual y el de la cuenta
            if account_element and line.element_id and line.element_id != account_element:
                raise ValidationError(_(
                    "El elemento '%(line)s' no coincide con el de la cuenta '%(acc)s'.",
                    line=line.element_id.display_name, acc=line.account_id.display_name,
                ))

            # Cuentas contenedoras requieren element_id explícito
            if line.account_id.element_detailed and not line.element_id:
                raise ValidationError(_(
                    "Las cuentas contenedoras requieren un elemento de gasto en la línea."
                ))

            # Coherencia entre analytic_element_id (computado) y account_id.element_id
            if line.analytic_element_id != account_element:
                raise ValidationError(_(
                    "Inconsistencia interna: 'analytic_element_id' no coincide con "
                    "'account_id.element_id'. Refresque la línea o contacte al administrador."
                ))
