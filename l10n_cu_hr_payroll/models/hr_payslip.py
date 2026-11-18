# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    # Necesidad: ver el valor de la regla NET a pagar en la nómina
    total = fields.Float(string='Total')
    # Necesidad: dominios para registrar nóminas con valor <= 0.0
    total_on_payable = fields.Boolean(string='Not Payable', store=True)

    def refund_sheet(self):
        """Cancela la nómina origen (la rectificativa también se cancela)."""
        res = super().refund_sheet()
        self.write({'state': 'cancel'})
        return res

    def action_payslip_done(self):
        """Asigna días de vacaciones según la regla 09 (días acumulados).

        Solo se asigna en nóminas regulares, NO en rectificativas
        (`credit_note=True`), donde los importes son negativos.
        """
        res = super().action_payslip_done()

        salary_rule_09 = self.env.ref(
            'l10n_cu_hr_payroll.hr_payroll_rules_09_dias', raise_if_not_found=False
        )
        holiday_status_cl = self.env.ref(
            'hr_holidays.holiday_status_cl', raise_if_not_found=False
        )
        if not (salary_rule_09 and holiday_status_cl):
            return res

        for slip in self.filtered(lambda s: not s.credit_note):
            for line in slip.line_ids:
                if line.code == salary_rule_09.code and line.total > 0:
                    self.env["hr.leave.allocation"].create({
                        'name': "Asignando vacaciones a %s" % line.employee_id.name,
                        'number_of_days': line.total,
                        'employee_id': line.employee_id.id,
                        'holiday_status_id': holiday_status_cl.id,
                    }).action_validate()
        return res

    def compute_sheet(self):
        res = super().compute_sheet()
        for slip in self:
            net_total = 0.0
            for line in slip.line_ids:
                if line.code == 'NET':
                    net_total = line.total
            slip.total = net_total
            slip.total_on_payable = net_total <= 0.0
        return res

    @api.model
    def get_inputs(self, contracts, date_from, date_to):
        # Normalizamos a `date` (nunca `None`). Si los datos llegan
        # corruptos, preferimos fallar explícito antes que enmascarar
        # el bug sustituyéndolos por `date.today()`.
        from_d = fields.Date.to_date(date_from)
        to_d = fields.Date.to_date(date_to)
        if not from_d or not to_d:
            raise ValueError(_(
                "Rango de fechas inválido en get_inputs: %s - %s"
            ) % (date_from, date_to))

        res = []
        structure_ids = contracts.get_all_structures()
        rule_ids = self.env['hr.payroll.structure'].browse(structure_ids).get_all_rules()
        sorted_rule_ids = [id for id, sequence in sorted(rule_ids, key=lambda x: x[1])]
        inputs = self.env['hr.salary.rule'].browse(sorted_rule_ids).mapped('input_ids')

        for contract in contracts:
            for input in inputs:
                amount = 0.0
                # Delegamos el filtro de fechas al `search` de Odoo. Los
                # campos Date vacíos valen `False`, NO `None`, por lo que
                # comparar con `is None` explota con TypeError. El operador
                # `|` + `= False` de Odoo maneja correctamente los vacíos.
                other_input = self.env["hr.payroll.other.input"].search([
                    ('rule_input_id.code', '=', input.code),
                    ('employee_id', '=', contract.employee_id.id),
                    '|', ('start_date', '=', False), ('start_date', '<=', to_d),
                    '|', ('end_date', '=', False), ('end_date', '>=', from_d),
                ], limit=1)
                if other_input:
                    amount = other_input.amount

                res.append({
                    'name': input.name,
                    'code': input.code,
                    'contract_id': contract.id,
                    'amount': amount,
                })
        return res
