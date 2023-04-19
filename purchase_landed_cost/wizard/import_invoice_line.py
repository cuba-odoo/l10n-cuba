# Copyright 2014-2016 Tecnativa - Pedro M. Baeza
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3
from odoo import api, fields, models


class ImportMoveLine(models.TransientModel):
    _name = "import.move.line.wizard"
    _description = "Import supplier move line"

    supplier = fields.Many2one(
        comodel_name='res.partner', string='Supplier', required=True,
        domain="[('supplier',  '=', True)]")
    move = fields.Many2one(
        comodel_name='account.move', string="Invoice", required=True,
        domain="[('partner_id', '=', supplier), ('type', '=', 'in_move'),"
               "('state', 'in', ['open', 'paid'])]")
    move_line = fields.Many2one(
        comodel_name='account.move.line', string="Invoice line",
        required=True, domain="[('move_id', '=', move)]")
    expense_type = fields.Many2one(
        comodel_name='purchase.expense.type', string='Expense type',
        required=True)

    #@api.multi
    def action_import_move_line(self):
        self.ensure_one()
        self.env['purchase.cost.distribution.expense'].create({
            'distribution': self.env.context['active_id'],
            'move_line': self.move_line.id,
            'move_id': self.move_line.move_id.id,
            'ref': self.move_line.name,
            'expense_amount': self.move_line.price_subtotal,
            'type': self.expense_type.id,
        })
