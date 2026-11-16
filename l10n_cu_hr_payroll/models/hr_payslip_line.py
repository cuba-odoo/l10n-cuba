# -*- coding: utf-8 -*-
from odoo import api, models


class HrPayslipLine(models.Model):
    _inherit = 'hr.payslip.line'

    @api.model
    def get_rule_balance(self, code, employee, date_from=None, date_to=None):
        """Suma el total de la regla `code` para el empleado en nóminas confirmadas.

        Parámetros:
        - code: código de la regla (ej. 'GROSS', 'IMPUESTO_DA').
        - employee: recordset hr.employee.
        - date_from/date_to: opcionales. Si se pasan, restringe a nóminas
          cuyo `date_from >= date_from` y `date_to <= date_to`. Necesario
          para cálculos anuales (IPAS, TPCD, TPAIP).

        Devuelve float. Si no hay líneas, retorna 0.0.
        """
        domain = [
            ('employee_id', '=', employee.id),
            ('slip_id.state', '=', 'done'),
            ('code', '=', code),
        ]
        if date_from:
            domain.append(('slip_id.date_from', '>=', date_from))
        if date_to:
            domain.append(('slip_id.date_to', '<=', date_to))
        lines = self.search(domain)
        return sum(lines.mapped('total')) if lines else 0.0
