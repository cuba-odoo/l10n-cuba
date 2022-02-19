# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class AccountingReport(models.TransientModel):
    _name = 'accounting.report'
    _inherit = 'accounting.report'

    def _print_report(self, data):
        data['form'].update(self.read(['debit_credit', 'display_account', 'display_detail',
                                       'account_report_id', 'target_move'])[0])
        context = self._context
        if context.get('efe', '') == '5920-04':
            if context.get('type', '') == 'xlsx':
                return self.env.ref('l10n_cu_reports_xlsx.action_ncc_accounting_xls_reports_report_bs'). \
                    report_action(self, data=data, config=False)
            else:
                return self.env.ref('l10n_cu_reports.action_ncc_accounting_pdf_reports_report_bs'). \
                    report_action(self, data=data, config=False)
        elif context.get('efe', '') == '5921-04':
            if context.get('type', '') == 'xlsx':
                return self.env.ref('l10n_cu_reports_xlsx.action_ncc_accounting_xls_reports_report_pl'). \
                    report_action(self, data=data, config=False)
            else:
                return self.env.ref('l10n_cu_reports.action_ncc_accounting_pdf_reports_report_pl'). \
                    report_action(self, data=data, config=False)
        elif context.get('efe', '') == '5924-04':
            if context.get('type', '') == 'xlsx':
                return self.env.ref('l10n_cu_reports_xlsx.action_ncc_accounting_xls_reports_report_ege'). \
                    report_action(self, data=data, config=False)
            else:
                return self.env.ref('l10n_cu_reports.action_ncc_accounting_pdf_reports_report_ege'). \
                    report_action(self, data=data, config=False)
        elif context.get('efe', '') == '5926-04':
            if context.get('type', '') == 'xlsx':
                return self.env.ref('l10n_cu_reports_xlsx.action_ncc_accounting_xls_reports_report_evab'). \
                    report_action(self, data=data, config=False)
            else:
                return self.env.ref('l10n_cu_reports.action_ncc_accounting_pdf_reports_report_evab'). \
                    report_action(self, data=data, config=False)
        else:
            return False
