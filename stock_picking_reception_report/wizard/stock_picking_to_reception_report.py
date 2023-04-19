# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class StockPickingToReceptionReport(models.TransientModel):
    _name = 'stock.picking.to.reception.report'
    _description = 'Add pickings to a reception report'

    receptionreport_id = fields.Many2one('stock.reception.report', string='Reception Report', required=True, oldname="wave_id")

    # #@api.multi
    def attach_pickings(self):
        # use active_ids to add picking line to the selected batch
        self.ensure_one()
        picking_ids = self.env.context.get('active_ids')
        return self.env['stock.picking'].browse(picking_ids).write({'receptionreport_id': self.receptionreport_id.id})
