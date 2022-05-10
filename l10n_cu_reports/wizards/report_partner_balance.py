
from odoo import fields, models, api,_

class PartnerBalanceWizard(models.TransientModel):
    """
        This wizard will provide the partner balance report by periods, between any two dates.
    """
    _inherit = 'account.common.partner.report'
    _name = 'account.partner.balance'
    _description = 'Print Account Partner Balance'
    
    display_partner = fields.Selection(string='Display Partners', default='non-zero_balance',
                                       selection=[('non-zero_balance', 'With balance is not equal to 0'),
                                                  ('all', 'All Partners')])
    result_selection = fields.Selection(default='customer_supplier', selection=[('customer', 'Receivable Accounts'),
                                                                                ('supplier', 'Payable Accounts'),
                                                                                ('customer_supplier',
                                                                                 'Receivable and Payable Accounts')])

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        active_model = self._context.get('active_model')
        active_ids = self._context.get('active_ids', [])

        if active_model == 'account.account' and active_ids and len(active_ids) == 1:
            internal_type = self.env[active_model].browse(active_ids).internal_type
            if internal_type == 'receivable':
                res['result_selection'] = 'customer'
            elif internal_type == 'payable':
                res['result_selection'] = 'supplier'

        return res

    def _print_report(self, data):
        model = self.env.context.get('active_model')
        if model == 'account.account':
            docs = self.env[model].browse(self.env.context.get('active_ids'))
        else:
            docs = self.env["account.account"].search([])

        data['ids'] = docs.ids
        data = self.pre_print_report(data)
        data['form'].update({'display_partner': self.display_partner})

        return self.env.ref('l10n_cu_reports.action_report_partner_balance').report_action(self, data=data)
