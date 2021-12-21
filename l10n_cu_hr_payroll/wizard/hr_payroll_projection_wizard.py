# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools
from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta
import babel

class HrPayslipProjectionWizard(models.TransientModel):
    _name = 'hr.payslip.projection.wizard'

    date_from = fields.Date(string='Date From', required=True, help="Start date",
                            default=lambda self: fields.Date.to_string(date.today().replace(day=1)))
    date_to = fields.Date(string='Date To', required=True, help="End date",
                          default=lambda self: fields.Date.to_string(
                              (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()),
                          states={'draft': [('readonly', False)]})

    def action_projection(self):
        self.ensure_one()
        payslip_lines_obj = self.env["hr.payslip.line"]
        domain = [('slip_id.state', '=', 'done'), ('slip_id.credit_note', '=', False),
                  ('slip_id.date_from', '>=', self.date_from), ('slip_id.date_to', '<=', self.date_to)]
        payslip_lines = payslip_lines_obj.search(domain)
        rules_code = self.env["hr.salary.rule"].search_read([], ['code'])
        employee_line_data = payslip_lines_obj.read_group(domain, ['employee_id'], ['employee_id'])

        dict_proj = {}
        for emp in employee_line_data:
            employee_id = emp['employee_id'][0]
            list_line = {}
            for rule in rules_code:
                list_line[rule['code']] = 0

            dict_proj[employee_id] = list_line
            for line in payslip_lines.filtered(lambda a: a.employee_id.id == employee_id):
                list_line[line.code] += line.total

        for emp in dict_proj:
            self._projection(emp, dict_proj[emp], self.date_from, self.date_to)

        # tree_view_id = self.env.ref('l10n_cu_hr_payroll.hr_payslip_projection_view_tree').id
        # form_view_id = self.env.ref('l10n_cu_hr_payroll.hr_payslip_projection_view_form').id
        # action = {
        #     'type': 'ir.actions.act_window',
        #     'view_mode': 'tree,form',
        #     'name': 'Proyecciones',
        #     'res_model': 'hr.payslip.projection',
        #     'target': 'current',
        #     'views': [[tree_view_id, "tree"], [form_view_id, "form"]],
        # }
        # return action

        action = self.env.ref('l10n_cu_hr_payroll.hr_payslip_projection_action').read()[0]
        return action

    def _projection(self, employee_id, dict_proj, from_date, to_date):
        domain = [('payslip_projection_id.employee_id', '=', employee_id),
                  ('payslip_projection_id.start_date', '<=', from_date.strftime("%Y-%m-%d")),
                  ('payslip_projection_id.active', '=', True),
                  ('payslip_projection_id.end_date', '>=', to_date.strftime("%Y-%m-%d"))]
        projections = self.env["hr.payslip.projection.line"].search(domain)

        for projection_line in projections:
            total = dict_proj[projection_line.code]

            fields_projection = projection_line.fields_get()
            ttyme = datetime.combine(fields.Date.from_string(from_date), time.min)
            locale = self.env.context.get('lang') or 'en_US'
            month = tools.ustr(babel.dates.format_date(date=ttyme, format='MMMM', locale=locale))

            for key, val in fields_projection.items():
                if month == key:
                    projection_line.write({key: total})
