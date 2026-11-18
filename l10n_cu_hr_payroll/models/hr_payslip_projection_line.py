# -*- coding: utf-8 -*-

from odoo import api, fields, models


class HrPayslipProjectionLine(models.Model):
    _name = 'hr.payslip.projection.line'
    _description = "Payslip Projection Line"

    payslip_projection_id = fields.Many2one("hr.payslip.projection", "Payslip Projection")
    sequence = fields.Integer("Sequence")
    code = fields.Char("Code", required=True)
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

    @api.depends('enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
                 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre')
    def _compute_total(self):
        for res in self:
            res.total = (
                res.enero + res.febrero + res.marzo + res.abril + res.mayo +
                res.junio + res.julio + res.agosto + res.septiembre +
                res.octubre + res.noviembre + res.diciembre
            )
