# -*- coding: utf-8 -*-

from odoo import api, models, _

class ReportFinancial(models.AbstractModel):
    _inherit = 'report.accounting_pdf_reports.report_financial'

    def get_account_lines(self, data):
        lines = []
        account_report = self.env['account.financial.report'].search([('id', '=', data['account_report_id'][0])])
        child_reports = account_report._get_children_by_order()
        res = self.with_context(data.get('used_context'))._compute_report_balance(child_reports)

        for report in child_reports:
            vals = {
                'name': report.name,
                'balance': res[report.id]['balance'] * float(report.sign),
                'type': 'report',
                'sequence': report.sequence,
                'plan_anual': report.plan_anual,
                'apertura': report.apertura,
                'level': bool(report.style_overwrite) and report.style_overwrite or report.level,
                'account_type': report.type or False, #used to underline the financial report balances
            }
            if data['debit_credit']:
                vals['debit'] = res[report.id]['debit']
                vals['credit'] = res[report.id]['credit']

            if not res[report.id]['balance'] and data['display_account'] == 'not_zero':
            # if account.company_id.currency_id.is_zero(vals['debit']):
                continue

            lines.append(vals)
            if report.display_detail == 'no_detail':
                #the rest of the loop is used to display the details of the financial report, so it's not needed here.
                continue

            if res[report.id].get('account'):
                sub_lines = []
                for account_id, value in res[report.id]['account'].items():
                    #if there are accounts to display, we add them to the lines with a level equals to their level in
                    #the COA + 1 (to avoid having them with a too low level that would conflicts with the level of data
                    #financial reports for Assets, liabilities...)
                    flag = False
                    account = self.env['account.account'].browse(account_id)
                    vals = {
                        'name': account.code + ' ' + account.name,
                        'balance': value['balance'] * float(report.sign) or 0.0,
                        'type': 'account',
                        'sequence': report.sequence,
                        'plan_anual': report.plan_anual,
                        'apertura': report.apertura,
                        # 'level': (report.display_detail == 'detail_with_hierarchy' or data.get('display_detail') == 'detail_with_hierarchy') and 4,
                        'level': data.get('display_detail') == 'detail_with_hierarchy' and 4,
                        'account_type': account.internal_type,
                    }
                    if data['debit_credit']:
                        vals['debit'] = value['debit']
                        vals['credit'] = value['credit']
                        if not account.company_id.currency_id.is_zero(vals['debit']) or not account.company_id.currency_id.is_zero(vals['credit']):
                            flag = True
                    if not account.company_id.currency_id.is_zero(vals['balance']):
                        flag = True
                    if flag:
                        sub_lines.append(vals)
                lines += sorted(sub_lines, key=lambda sub_line: sub_line['name'])
        # print(lines)
        return lines

class ReportFinancialBs(models.AbstractModel):
    _name = 'report.l10n_cu_reports.report_financial_bs'
    _description = 'Balance de Situación'
    _inherit = 'report.accounting_pdf_reports.report_financial'

class ReportFinancialPl(models.AbstractModel):
    _name = 'report.l10n_cu_reports.report_financial_pl'
    _description = 'Pérdidas y Ganancias'
    _inherit = 'report.accounting_pdf_reports.report_financial'

class ReportFinancialEge(models.AbstractModel):
    _name = 'report.l10n_cu_reports.report_financial_ege'
    _description = 'Estado de Gasto por Elemento'
    _inherit = 'report.accounting_pdf_reports.report_financial'

class ReportFinancialEi(models.AbstractModel):
    _name = 'report.l10n_cu_reports.report_financial_ei'
    _description = 'Estado de Inversiones'
    _inherit = 'report.accounting_pdf_reports.report_financial'
class ReportFinancialEvab(models.AbstractModel):
    _name = 'report.l10n_cu_reports.report_financial_evab'
    _description = 'Estado de Valor Agregado Bruto'
    _inherit = 'report.accounting_pdf_reports.report_financial'