# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

#        This field respond to the necessity of see the value of the net rule to pay in the slip
    total = fields.Float(string='Total')
#        This field respond to the necessity of obtain a domain who registry the slip who value is <= 0.0
    total_on_payable = fields.Boolean(string='Not Payable', store=True)

    def refund_sheet(self):
        """Se cancela la nomina origen para que no sea tomada en cuenta (el origen y la rectificativa.)."""
        res = super(HrPayslip, self).compute_sheet()
        self.write({'state': 'cancel'})
        return res

    def action_payslip_done(self):
        """No es necesario hacer un cron porque estamos hablando de dias trabajados, que es algo irrelevante
        desde el punto de visa contable.
        """
        res = super(HrPayslip, self).action_payslip_done()
        salary_rule_09 = self.env.ref('l10n_cu_hr_payroll.hr_payroll_rules_09_dias')
        for line in self.line_ids:
            if line.code == salary_rule_09.code:
                holiday_status_cl = self.env.ref('hr_holidays.holiday_status_cl')
                res = {'name': "Asignando vacaciones a %s" % line.employee_id.name, 'number_of_days': line.total,
                           'employee_id': line.employee_id.id, 'holiday_status_id': holiday_status_cl.id}
                allocation = self.env["hr.leave.allocation"].create(res)
                allocation.action_confirm()
                allocation.action_validate()

        return res

    def compute_sheet(self):
        res = super(HrPayslip, self).compute_sheet()
        for slip in self:
            for line in slip.line_ids:
                if line.salary_rule_id.code == 'NET':
                    slip.total = line.total
            if slip.total <= 0.0:
                slip.total_on_payable = True
            else:
                slip.total_on_payable = False
            # if slip.state == 'draft':
            #     slip.state = 'calculate'
        return res

    @api.model
    def get_inputs(self, contracts, date_from, date_to):
        # Override
        res = []
        structure_ids = contracts.get_all_structures()
        rule_ids = self.env['hr.payroll.structure'].browse(structure_ids).get_all_rules()
        sorted_rule_ids = [id for id, sequence in sorted(rule_ids, key=lambda x: x[1])]
        inputs = self.env['hr.salary.rule'].browse(sorted_rule_ids).mapped('input_ids')

        for contract in contracts:
            for input in inputs:
                amount = 0
                domain = [
                    ('rule_input_id.code', '=', input.code), ('employee_id', '=', contract.employee_id.id)]

                other_inputs = self.env["hr.payroll.other.input"].search(domain, limit=1)
                if other_inputs:
                    if other_inputs.start_date:
                        domain.append(('start_date', '<=', date_from))
                    if other_inputs.end_date:
                        domain.append(('end_date', '<=', date_to))

                    other_inputs = self.env["hr.payroll.other.input"].search(domain, limit=1)
                    amount = other_inputs.amount

                input_data = {
                    'name': input.name,
                    'code': input.code,
                    'contract_id': contract.id,
                    'amount': amount
                }
                res += [input_data]
        return res

class HrPayslipRun(models.Model):
    _inherit = "hr.payslip.run"
    _order = "date_start desc"

    qty_payslip = fields.Integer('Quantity Prepayslip', compute="_compute_qty_payslip", store=False, translate=True)
    total = fields.Float(string='Total', store=True)

    def _compute_qty_payslip(self):
        self.ensure_one()
        self.qty_payslip = len(self.slip_ids)

    def calculate_slips_total(self):
        for sheet in self:
            sheet.total = 0.0
            for line in sheet.slip_ids:
                line.compute_sheet()
                if line.total:
                    sheet.total += line.total

            # if sheet.state == 'draft':
            #     sheet.state = 'calculate'

class HrPayrollOtherInput(models.Model):
    _name = 'hr.payroll.other.input'
    _description = "Payroll Other Input"

    employee_id = fields.Many2one("hr.employee", "Employee")
    rule_input_id = fields.Many2one("hr.rule.input", "Code", required=True)
    amount = fields.Float("Amount", required=True)
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")