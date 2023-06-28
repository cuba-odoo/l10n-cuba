# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class PayrollPaymentMassiveWizard(models.TransientModel):
    _name = 'hr.payroll.payment.massive.wizard'
    _description = 'Payroll Payment Massive'

    name = fields.Char("Name", required=True)
    date = fields.Date("Date", required=True, default=fields.Datetime.now())
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 compute='_compute_from_lines')
    journal_id = fields.Many2one('account.journal', readonly=False, store=True,
                                 compute='_compute_journal_id',
                                 domain="[('type', 'in', ('bank', 'cash'))]")
    # == Fields given through the context ==
    line_ids = fields.Many2many('hr.payslip', 'hr_payslip_payment_register_rel', 'wizard_id', 'line_id',
                                string="Journal items", readonly=True, copy=False, )

    @api.depends('line_ids')
    def _compute_from_lines(self):
        ''' Load initial values from the account.moves passed through the context. '''
        for wizard in self:
            # batches = wizard._get_batches()
            # batch_result = batches[0]
            # wizard_values_from_batch = wizard._get_wizard_values_from_batch(batch_result)
            #
            # if len(batches) == 1:
            #     # == Single batch to be mounted on the view ==
            #     wizard.update(wizard_values_from_batch)
            #
            #     wizard.can_edit_wizard = True
            #     wizard.can_group_payments = len(batch_result['lines']) != 1
            # else:
            #     # == Multiple batches: The wizard is not editable  ==

            if wizard.line_ids:
                wizard.update({
                    'company_id': wizard.line_ids[0].company_id.id,
                })

                # wizard.can_edit_wizard = False
                # wizard.can_group_payments = any(len(batch_result['lines']) != 1 for batch_result in batches)

    @api.depends('company_id')
    def _compute_journal_id(self):
        for wizard in self:
            domain = [
                ('type', 'in', ('bank', 'cash'))
            ]
            journal = self.env['account.journal'].search(domain, limit=1)
            wizard.journal_id = journal

    @api.model
    def default_get(self, fields_list):
        # OVERRIDE
        res = super().default_get(fields_list)

        if 'line_ids' in fields_list and 'line_ids' not in res:

            # Retrieve moves to pay from the context.

            if self._context.get('active_model') == 'hr.payslip':
                lines = self.env['hr.payslip'].browse(self._context.get('active_ids', []))
            elif self._context.get('active_model') == 'hr.payslip.run':
                lines = self.env['hr.payslip.run'].browse(self._context.get('active_ids', [])).slip_ids
            else:
                raise UserError(_(
                    "The register payment wizard should only be called on account.move or account.move.line records."
                ))

            # Keep lines having a residual amount to pay.
            available_lines = self.env['hr.payslip']
            for line in lines:
                if line.state != 'done':
                    raise UserError("Solo puedes registrar el pago de las nóminas confirmadas.")

                if line.total_on_payable:
                    raise UserError("El total a pagar de la nómina %s debe ser superior a 0." % line.name)

                # if line.account_internal_type not in ('receivable', 'payable'):
                #     continue
                # if line.currency_id:
                #     if line.currency_id.is_zero(line.amount_residual_currency):
                #         continue
                # else:
                #     if line.company_currency_id.is_zero(line.amount_residual):
                #         continue
                available_lines |= line

            # Check.
            if not available_lines:
                raise UserError(_(
                    "You can't register a payment because there is nothing left to pay on the selected journal items."))
            if len(lines.company_id) > 1:
                raise UserError(_("You can't create payments for entries belonging to different companies."))
            # if len(set(available_lines.mapped('account_internal_type'))) > 1:
            #     raise UserError(
            #         _("You can't register payments for journal items being either all inbound, either all outbound."))

            res['line_ids'] = [(6, 0, available_lines.ids)]

        return res

    def action_create_payments(self):
        values = {'name': self.name, 'date': self.date, 'journal_id': self.journal_id.id,
                  'payslip_line_ids': self.line_ids.ids}
        payroll_payment_id = self.env["hr.payslip.payment"].create(values)

        return {
            'view_type': 'form',
            'res_id': payroll_payment_id.id,
            'view_mode': 'form',
            'res_model': 'hr.payslip.payment',
            'type': 'ir.actions.act_window'
        }
