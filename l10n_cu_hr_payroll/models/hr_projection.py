# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from datetime import date

class HrPayslipProjection(models.Model):
    _name = 'hr.payslip.projection'
    _description = "Payslip Projection"

    _sql_constraints = [
        (
            "employee_id_unique",
            "unique(employee_id)",
            "This employee is already used!",
        )
    ]

    name = fields.Char('Name', compute="_compute_name", store=True)
    employee_id = fields.Many2one("hr.employee", required=True)
    start_date = fields.Date("Start Date", required=True, default=lambda self: str(date.today().year) + '-01-01')
    end_date = fields.Date("End Date", required=True, default=lambda self: str(date.today().year) + '-12-31')
    payslip_projection_line_ids = fields.One2many("hr.payslip.projection.line", "payslip_projection_id", string="Payslip Projection Line")
    active = fields.Boolean("Active", default=True)

    @api.depends('employee_id', 'start_date', 'end_date')
    def _compute_name(self):
        self.ensure_one()
        self.name = "%s  [%s - %s]" % (self.employee_id.name or '', fields.Date.to_string(self.start_date), fields.Date.to_string(self.end_date))

    def action_export_rules(self):
        for res in self:
            rules_ids = self._get_rules(res.employee_id)
            projection_line = self.payslip_projection_line_ids
            rules_code = [r.code for r in projection_line]
            for r in rules_ids:
                if r.get('code') not in rules_code:
                    rules = self.payslip_projection_line_ids.browse([])
                    res.payslip_projection_line_ids += rules.new(r)

        return

    def _get_rules(self, employee_id):
        res = []
        structure_ids = employee_id.contract_ids.get_all_structures()
        rule_ids = self.env['hr.payroll.structure'].browse(structure_ids).get_all_rules()

        rules = self.env['hr.salary.rule'].browse(id for id, sequence in sorted(rule_ids, key=lambda x: x[1])).filtered(
            lambda l: l.appears_on_payslip == True
        )

        for rule in rules:
            projection_line_data = {
                'sequence': rule.sequence,
                'code': rule.code,
            }
            res += [projection_line_data]

        return res

class HrPayslipProjectionLine(models.Model):
    _name = 'hr.payslip.projection.line'
    _description = "Payslip Projection Line"

    payslip_projection_id = fields.Many2one("hr.payslip.projection", "Payslip Projection")
    sequence = fields.Integer("Sequence")
    code = fields.Char("Code", required="True")
    enero = fields.Float("Enero")
    febrero = fields.Float("Febrero")
    marzo = fields.Float("Marzo")
    abril = fields.Float("Abril")
    mayo = fields.Float("Mayo")
    junio = fields.Float("Junio")
    julio = fields.Float("Julio")
    agosto = fields.Float("Agosto")
    septiembre = fields.Float("Septiembre")
    octubre = fields.Float("Octubre")
    noviembre = fields.Float("Noviembre")
    diciembre = fields.Float("Diciembre")
    total = fields.Float("Total", compute="_compute_total")

    @api.depends('enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre',
                 'octubre', 'noviembre', 'diciembre')
    def _compute_total(self):
        for res in self:
            total = res.enero + res.febrero + res.marzo + res.abril + res.mayo + res.junio + res.julio + \
                    res.agosto + res.septiembre + res.octubre + res.noviembre + res.diciembre
            res.total = total