# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
   
    analytic_account_parent_id = fields.Many2one('account.analytic.account', compute='_compute_analytic_parent', index=True, ondelete='set null', readonly=False, store=True)
    analytic_element_id = fields.Many2one('expense.element', compute='_compute_analytic_expense_element_id', index=True, ondelete='set null', readonly=False, store=True)
    element_id = fields.Many2one('expense.element',  index=True, ondelete='set null', readonly=False, store=True)
   
    @api.depends('account_id')
    def _compute_analytic_parent(self):
        for record in self:
            record.analytic_account_parent_id = record.account_id.parent_id.id

    @api.depends('account_id')
    def _compute_analytic_expense_element_id(self):
        for record in self:
            record.analytic_element_id = record.account_id.element_id.id       
            
            