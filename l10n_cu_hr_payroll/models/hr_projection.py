# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import date


class HrPayslipProjection(models.Model):
    _name = 'hr.payslip.projection'
    _description = "Payslip Projection"

    _sql_constraints = [
        (
            "employee_period_unique",
            "unique(employee_id, start_date, end_date)",
            "Este empleado ya tiene una proyección para este período.",
        )
    ]

    def init(self):
        """Elimina el índice parcial legado que creaba una versión
        anterior del módulo mediante init().

        Ese índice (``hr_payslip_projection_emp_period_active_unique``)
        solo aplicaba a ``active = true`` y coexistía con la constraint
        de ``_sql_constraints``, mostrando mensajes de error SQL crudos
        en lugar del mensaje amigable en español.

        Esta función es idempotente: se puede ejecutar múltiples veces
        sin efecto. Una vez eliminado el índice, no se vuelve a crear.
        """
        self.env.cr.execute("""
            DROP INDEX IF EXISTS hr_payslip_projection_emp_period_active_unique
        """)

    name = fields.Char('Name', compute="_compute_name", store=True)
    employee_id = fields.Many2one("hr.employee", required=True)
    start_date = fields.Date(
        "Start Date", required=True,
        default=lambda self: str(date.today().year) + '-01-01',
    )
    end_date = fields.Date(
        "End Date", required=True,
        default=lambda self: str(date.today().year) + '-12-31',
    )
    payslip_projection_line_ids = fields.One2many(
        "hr.payslip.projection.line", "payslip_projection_id",
        string="Payslip Projection Line",
    )
    active = fields.Boolean("Active", default=True)

    @api.depends('employee_id', 'start_date', 'end_date')
    def _compute_name(self):
        for rec in self:
            rec.name = "%s  [%s - %s]" % (
                rec.employee_id.name or '',
                fields.Date.to_string(rec.start_date),
                fields.Date.to_string(rec.end_date),
            )

    def action_export_rules(self):
        for res in self:
            rules_ids = self._get_rules(res.employee_id)
            existing_codes = [line.code for line in res.payslip_projection_line_ids]
            commands = [
                (0, 0, rule) for rule in rules_ids
                if rule.get('code') not in existing_codes
            ]
            if commands:
                res.write({'payslip_projection_line_ids': commands})
        return

    def _get_rules(self, employee_id):
        res = []
        structure_ids = employee_id.contract_ids.get_all_structures()
        rule_ids = self.env['hr.payroll.structure'].browse(structure_ids).get_all_rules()

        rules = self.env['hr.salary.rule'].browse(
            [id for id, sequence in sorted(rule_ids, key=lambda x: x[1])]
        ).filtered(lambda l: l.appears_on_payslip)

        for rule in rules:
            res.append({
                'sequence': rule.sequence,
                'code': rule.code,
            })
        return res
