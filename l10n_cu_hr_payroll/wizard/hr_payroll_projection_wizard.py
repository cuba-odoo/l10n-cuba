# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

# Nombres de los campos mensuales del modelo hr.payslip.projection.line
MONTH_FIELDS = [
    'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre',
]


class HrPayslipProjectionWizard(models.TransientModel):
    _name = 'hr.payslip.projection.wizard'
    _description = 'Payslip Projection Wizard'

    date_from = fields.Date(
        string='Date From', required=True, help="Start date",
        default=lambda self: fields.Date.to_string(date.today().replace(day=1)),
    )
    date_to = fields.Date(
        string='Date To', required=True, help="End date",
        default=lambda self: fields.Date.to_string(
            (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()
        ),
    )

    def action_projection(self):
        self.ensure_one()
        payslip_lines_obj = self.env["hr.payslip.line"]
        # Filtrar por compañía activa: en multi-compañía, sumar nóminas
        # de otras compañías infla los salarios proyectados de este
        # empleado con importes ajenos a su empresa.
        domain = [
            ('slip_id.state', '=', 'done'),
            ('slip_id.credit_note', '=', False),
            ('slip_id.date_from', '>=', self.date_from),
            ('slip_id.date_to', '<=', self.date_to),
            ('slip_id.company_id', '=', self.env.company.id),
        ]
        payslip_lines = payslip_lines_obj.search(domain)
        rules_code = self.env["hr.salary.rule"].search_read(
            [('appears_on_payslip', '=', True)], ['code']
        )
        employee_line_data = payslip_lines_obj.read_group(
            domain, ['employee_id'], ['employee_id']
        )

        dict_proj = {}
        for emp in employee_line_data:
            employee_id = emp['employee_id'][0]
            # Inicializamos con 0.0 (float) → Pyright no marca += float sobre int
            list_line = {rule['code']: 0.0 for rule in rules_code}
            dict_proj[employee_id] = list_line
            for line in payslip_lines.filtered(
                lambda a, eid=employee_id: a.employee_id.id == eid
            ):
                # .get + default evita KeyError si una regla antigua ya no existe
                list_line[line.code] = list_line.get(line.code, 0.0) + line.total

        for emp_id, proj_data in dict_proj.items():
            self._projection(emp_id, proj_data, self.date_from, self.date_to)

        return self.env.ref('l10n_cu_hr_payroll.hr_payslip_projection_action').read()[0]

    def _projection(self, employee_id, dict_proj, from_date, to_date):
        domain = [
            ('payslip_projection_id.employee_id', '=', employee_id),
            ('payslip_projection_id.start_date', '<=', from_date),
            ('payslip_projection_id.active', '=', True),
            ('payslip_projection_id.end_date', '>=', to_date),
        ]
        projections = self.env["hr.payslip.projection.line"].search(domain)
        if not projections:
            return

        month_field = MONTH_FIELDS[from_date.month - 1]

        for projection_line in projections:
            total = dict_proj.get(projection_line.code, 0.0)
            if month_field in projection_line._fields:
                projection_line.write({month_field: total})
