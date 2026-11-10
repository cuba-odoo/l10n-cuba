# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HrPayslipRun(models.Model):
    _inherit = "hr.payslip.run"
    _order = "date_start desc"

    qty_payslip = fields.Integer(
        'Quantity Prepayslip',
        compute="_compute_qty_payslip",
        store=False,
    )
    total = fields.Float(string='Total', store=True)

    @api.depends('slip_ids')
    def _compute_qty_payslip(self):
        for rec in self:
            rec.qty_payslip = len(rec.slip_ids)

    def calculate_slips_total(self):
        """Recalcula el total del run SIN tocar nóminas ya confirmadas.

        Solo se llama `compute_sheet()` sobre nóminas en estado `draft`.
        Recalcular una nómina `done` borraría sus líneas y podría cambiar
        importes históricos (rompe auditoría y cuadres contables).
        """
        for sheet in self:
            total = 0.0
            for slip in sheet.slip_ids:
                if slip.state == 'draft':
                    slip.compute_sheet()
                total += slip.total or 0.0
            sheet.total = total
