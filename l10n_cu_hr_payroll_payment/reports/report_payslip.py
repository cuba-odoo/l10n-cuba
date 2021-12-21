# -*- coding: utf-8 -*-
from odoo import api, models


def _get_line_by_code(self, payslip_id, code):
    res = self.env["hr.payslip"].browse(payslip_id)
    line = res.line_ids.search([('slip_id', '=', payslip_id), ('code', '=', code)], limit=1)
    return line.total

class ReportPayslip(models.AbstractModel):
    _name = 'report.l10n_cu_hr_payroll_payment.report_payslip'

    def _get_decimal_precision(self, code=''):
        default_digit = 2
        if code == '':
            return default_digit

        decimal_precision = self.env["decimal.precision"].search([('name', '=', code)], limit=1)
        return decimal_precision and decimal_precision.digits or 0

    def _get_line_by_code(self, payslip_payment, code):
        return _get_line_by_code(self, payslip_payment, code)

    def _get_slip(self, payslip_payment):
        """Obtienen las nominas de un pago masivo."""
        domain = [('payslip_payment_id', '=', payslip_payment.id)]

        payslip = self.env["hr.payslip"].search(domain)
        payslip_sorted = payslip.sorted(key=lambda r: r.contract_id.name, reverse=True)
        return payslip_sorted

    def _get_rules_by_cat_code_header(self, payslip_payment_id, code_arg):
        #        Usado para crear las cabeceras de las tablas.
        query = """SELECT sr.code, sr.name
                FROM hr_payslip_payment pr inner join hr_payslip ps on (ps.payslip_payment_id = pr.id)
                INNER JOIN hr_payslip_line pl on (ps.id = pl.slip_id)                
                INNER JOIN hr_salary_rule sr ON (pl.salary_rule_id = sr.id)
                INNER JOIN hr_salary_rule_category rc ON (sr.category_id = rc.id)
                WHERE pr.id = %d and rc.code = '%s' and sr.appears_on_payslip = true 
                GROUP BY sr.code, sr.name, pl.sequence
                ORDER BY pl.sequence""" % (payslip_payment_id, code_arg)

        self.env.cr.execute(query)
        result = self.env.cr.dictfetchall()
        return result

    def _get_amount_by_cat_code(self, payslip_payment_id, code_arg, emp):
        #        Usado para crear los cuerpos de las tablas con los importes.
        query = """SELECT sr.id, sr.code, sr.name, sr.appears_on_payslip, pl.sequence, pl.amount
                    FROM hr_payslip_payment pr inner join hr_payslip ps on (ps.payslip_payment_id = pr.id)
                    INNER JOIN hr_payslip_line pl on (ps.id = pl.slip_id)
                    LEFT JOIN hr_salary_rule_category AS sh on (pl.category_id = sh.id)
                    INNER JOIN hr_salary_rule sr ON (pl.salary_rule_id = sr.id)
                    INNER JOIN hr_salary_rule_category rc ON (sr.category_id = rc.id)
                    WHERE pr.id = %d and rc.code = '%s' and sr.appears_on_payslip = true 
                    and ps.employee_id = %d 
                    GROUP BY sr.id, sr.code, sr.name, pl.sequence, sr.appears_on_payslip, pl.amount
                    ORDER BY pl.sequence""" % (payslip_payment_id, code_arg, emp)

        self.env.cr.execute(query)

        result = self.env.cr.dictfetchall()
        return result

    @api.model
    def _get_report_values(self, docids, data=None):
        report_obj = self.env['ir.actions.report']
        report = report_obj._get_report_from_name('l10n_cu_hr_payroll_payment.report_payslip')
        docs = self.env["hr.payslip.payment"].browse(docids)

        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': docs,
            'get_line_by_code': self._get_line_by_code,
            'get_slip': self._get_slip,
            'get_decimal_precision': self._get_decimal_precision,
            'get_rules_by_cat_code_header': self._get_rules_by_cat_code_header,
            'get_amount_by_cat_code': self._get_amount_by_cat_code,
        }
        return docargs    
    


