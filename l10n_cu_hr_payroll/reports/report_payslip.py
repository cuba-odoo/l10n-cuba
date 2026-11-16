# -*- coding: utf-8 -*-
from odoo import api, models


class ReportPayslip(models.AbstractModel):
    _name = 'report.l10n_cu_hr_payroll.report_payslip'
    _description = "Report Payslip"

    def _get_decimal_precision(self, code=''):
        default_digit = 2
        if code == '':
            return default_digit
        decimal_precision = self.env["decimal.precision"].search(
            [('name', '=', code)], limit=1
        )
        return decimal_precision.digits if decimal_precision else default_digit

    def _get_line_by_code(self, payslip_id, code):
        """Devuelve el total de la regla `code` para la nómina `payslip_id`."""
        line = self.env["hr.payslip.line"].search(
            [('slip_id', '=', payslip_id), ('code', '=', code)], limit=1
        )
        return line.total if line else 0.0

    def _get_slip(self, payslip_run):
        """Obtiene las nóminas de un pago masivo.

        `hr.payslip.contract_id` es un Many2one NO obligatorio. Si por
        cualquier motivo una nómina no tiene contrato, `r.contract_id.name`
        devuelve `False`, y Python no puede comparar `False < "str"` al
        ordenar → `TypeError`. Fallback a `''` evita el crash.
        """
        domain = [('payslip_run_id', '=', payslip_run.id)]
        payslip = self.env["hr.payslip"].search(domain)
        return payslip.sorted(
            key=lambda r: r.contract_id.name or '',
            reverse=True,
        )

    def _get_rules_by_cat_code_header(self, payslip_run_id, code_arg):
        """Cabeceras de tablas del reporte de nóminas."""
        query = """
            SELECT sr.code, sr.name
              FROM hr_payslip_run pr
             INNER JOIN hr_payslip ps         ON ps.payslip_run_id = pr.id
             INNER JOIN hr_payslip_line pl    ON ps.id = pl.slip_id
             INNER JOIN hr_salary_rule sr     ON pl.salary_rule_id = sr.id
             INNER JOIN hr_salary_rule_category rc ON sr.category_id = rc.id
             WHERE pr.id = %s
               AND rc.code = %s
               AND sr.appears_on_payslip = true
             GROUP BY sr.code, sr.name, pl.sequence
             ORDER BY pl.sequence
        """
        self.env.cr.execute(query, (payslip_run_id, code_arg))
        return self.env.cr.dictfetchall()

    def _get_amount_by_cat_code(self, payslip_run_id, code_arg, emp):
        """Cuerpos de las tablas con los importes."""
        query = """
            SELECT sr.id, sr.code, sr.name, sr.appears_on_payslip,
                   pl.sequence, pl.amount
              FROM hr_payslip_run pr
             INNER JOIN hr_payslip ps         ON ps.payslip_run_id = pr.id
             INNER JOIN hr_payslip_line pl    ON ps.id = pl.slip_id
             INNER JOIN hr_salary_rule sr     ON pl.salary_rule_id = sr.id
             INNER JOIN hr_salary_rule_category rc ON sr.category_id = rc.id
             WHERE pr.id = %s
               AND rc.code = %s
               AND sr.appears_on_payslip = true
               AND ps.employee_id = %s
             GROUP BY sr.id, sr.code, sr.name, pl.sequence,
                      sr.appears_on_payslip, pl.amount
             ORDER BY pl.sequence
        """
        self.env.cr.execute(query, (payslip_run_id, code_arg, emp))
        return self.env.cr.dictfetchall()

    @api.model
    def _get_report_values(self, docids, data=None):
        report_obj = self.env['ir.actions.report']
        report = report_obj._get_report_from_name(
            'l10n_cu_hr_payroll.report_payslip'
        )
        docs = self.env["hr.payslip.run"].browse(docids)

        slips_cache = {run.id: self._get_slip(run) for run in docs}

        def _get_slip_cached(run):
            return slips_cache.get(run.id, self.env['hr.payslip'])

        return {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': docs,
            'get_line_by_code': self._get_line_by_code,
            'get_slip': _get_slip_cached,
            'get_decimal_precision': self._get_decimal_precision,
            'get_rules_by_cat_code_header': self._get_rules_by_cat_code_header,
            'get_amount_by_cat_code': self._get_amount_by_cat_code,
        }
