# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

class AccountingReport(models.TransientModel):
    _name = 'accounting.report'
    _inherit = 'accounting.report'

    # date_from = fields.Date(required=True, default=lambda self: fields.Date.to_string(date.today().replace(day=1)))
    # date_to = fields.Date(required=True, default=lambda self: fields.Date.to_string(
    #                           (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()))

    date_to = fields.Date(required=True, default=lambda self: datetime.now())
    
    display_account = fields.Selection(selection=[("all", "All"), ("not_zero", "With balance is not equal to 0")],
                                       string='Display Accounts', required=True, default='all')
    display_detail = fields.Selection(selection=[
        ('no_detail', 'No detail'),
        # ('detail_flat', 'Display children flat'),
        ('detail_with_hierarchy', 'Display children with hierarchy')
    ], string='Display details', default='no_detail')

    def _print_report(self, data):
        data['form'].update(self.read(['debit_credit', 'display_account', 'display_detail',
                                       'account_report_id', 'target_move'])[0])
        context = self._context
        if context.get('efc', 'False') == 'pl':
            return self.env.ref('l10n_cu_reports.action_ncc_accounting_pdf_reports_report_pl').\
            report_action(self, data=data, config=False)
        elif context.get('efc', 'False') == 'bs':
            return self.env.ref('l10n_cu_reports.action_ncc_accounting_pdf_reports_report_bs'). \
            report_action(self, data=data, config=False)
        elif context.get('efc', 'False') == 'ege':
            return self.env.ref('l10n_cu_reports.action_ncc_accounting_pdf_reports_report_ege'). \
            report_action(self, data=data, config=False)
        else:
            return self.env.ref('l10n_cu_reports.action_ncc_accounting_pdf_reports_report_ei'). \
                report_action(self, data=data, config=False)

