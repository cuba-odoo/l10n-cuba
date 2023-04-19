# Copyright 2014-2015 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    expense_line_ids = fields.One2many(
        comodel_name="purchase.cost.distribution.expense",
        inverse_name="move_id", string="Landed costs")


class AccountInvoiceLine(models.Model):
    _inherit = 'account.move.line'

    expense_line_ids = fields.One2many(
        comodel_name="purchase.cost.distribution.expense",
        inverse_name="move_line", string="Landed costs")
