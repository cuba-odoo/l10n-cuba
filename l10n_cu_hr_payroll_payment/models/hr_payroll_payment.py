# -*- coding: utf-8 -*-
from odoo import fields, models, api
from datetime import datetime
from odoo.exceptions import UserError
DEFAULT_DIGITS = (16, 2)

class HrPayslipPayment(models.Model):
    _name = 'hr.payslip.payment'
    _description = "Payslip Payment"

    name = fields.Char("Name", required=True)
    date = fields.Date("Date", required=True, default=fields.Datetime.now())
    payslip_line_ids = fields.One2many("hr.payslip", "payslip_payment_id", string="Payslip Line")
    payment_line_ids = fields.One2many("account.payment", "payslip_payment_id", string="Payment Line")
    journal_id = fields.Many2one('account.journal', readonly=False, store=True,
                                 compute='_compute_journal_id',
                                 domain="[('type', 'in', ('bank', 'cash'))]")
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.ref('base.main_company'))
    total = fields.Float("Total", compute="_compute_total", digits=DEFAULT_DIGITS)
    qty_paid = fields.Integer('Quantity Paid', compute="_compute_quantity_paid")
    state = fields.Selection([('draft', 'Borrador'), ('paid', 'Pago')],
                             'Status', default="draft", readonly=True, copy=False)

    @api.depends('company_id')
    def _compute_journal_id(self):
        for wizard in self:
            domain = [
                ('type', 'in', ('bank', 'cash'))
            ]
            journal = self.env['account.journal'].search(domain, limit=1)
            wizard.journal_id = journal

    def _compute_quantity_paid(self):
        for payment in self:
            count = self.env['account.payment'].search_count([('payslip_payment_id', '=', self.id)])
            payment.qty_paid = count

    def _compute_total(self):
        for res in self:
            self.total = sum([line.total for line in res.payslip_line_ids])

    def action_draft(self):
        self.state = 'draft'

    def action_paid(self):
        """ Resgistra los pagos y genera los asientos contables. """
        self.ensure_one()
        for line in self.payslip_line_ids:
            res = {'payment_type': 'outbound', 'partner_type': 'supplier', 'ref': line.number, 'date': self.date,
                   'journal_id': self.journal_id.id, 'amount': line.total, 'payslip_payment_id': self.id}
            payment = self.env["account.payment"].create(res)
            if line.employee_id.address_home_id:
                payment.write({'destination_account_id': line.employee_id.address_home_id.property_account_payable_id.id,
                               'partner_id': line.employee_id.address_home_id.id})

            if self.journal_id.type == 'bank' and not line.employee_id.bank_account_id:
                raise UserError("El empleado %s no tiene cuenta de banco asociada." % line.employee_id.name)

            if self.journal_id.type == 'bank' and line.employee_id.bank_account_id:
                payment.write({'partner_bank_id': line.employee_id.bank_account_id.id})

            if self.journal_id.type == 'cash':
                payment.write({'partner_bank_id': False})

            payment.action_post()
            line.write({'paid': True})

        self.state = 'paid'

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    payslip_payment_id = fields.Many2one('hr.payslip.payment', 'Payslip Payment', copy=False)

    def unlink(self):
        """Al eliminar el pago, cambia el atributo paid a False de la nomina origen."""
        for payment in self:
            slip = self.env["hr.payslip"].search([('number', '=', payment.ref)])
            if slip:
                slip.write({'paid': False})

        return super(AccountPayment, self).unlink()