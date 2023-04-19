# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class StockReceptionReport(models.Model):
    _inherit = ['mail.thread']
    _name = "stock.reception.report"
    _description = "Reception Report"
    _order = "name desc"

    @api.model
    def _get_default_picking_type(self):
        return self.env['stock.picking.type'].search([
            ('code', '=', 'incoming'), ('warehouse_id.company_id', 'in',
                                        [self.env.context.get('company_id', self.env.user.company_id.id),
                                         False])], limit=1).id

    name = fields.Char(
        string='Reception Report Name', default='New',
        copy=False, required=True,
        help='Name of the Reception Report')
    FechaRecepcion = fields.Date('Fecha Recepción', required=True, default=fields.Date.today)
    user_id = fields.Many2one(
        'res.users', string='Responsible', track_visibility='onchange',
        help='Person responsible for this reception report')
    picking_ids = fields.One2many(
        'stock.picking', 'receptionreport_id', string='Pickings',
        help='List of picking associated to this reception report')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], default='draft',
        copy=False, track_visibility='onchange', required=True)
    partner_id = fields.Many2one(
        'res.partner', 'Partner',
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]})
    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env['res.company']._company_default_get('stock.reception.report'),
        index=True, required=True,
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]})
    picking_type_id = fields.Many2one(
        'stock.picking.type', 'Operation Type',
        default=_get_default_picking_type, required=True)

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('picking.reception.report') or '/'
        return super(StockReceptionReport, self).create(vals)

    def confirm_picking(self):
        return self.write({'state': 'done'})

    def cancel_picking(self):
        return self.write({'state': 'cancel'})

    def print_picking(self):
        return self.env.ref('stock_picking_reception_report.action_reception_report2').report_action(self)

    def done(self):
        pickings = self.mapped('picking_ids').filtered(lambda picking: picking.state not in ('cancel', 'done'))
        if any(picking.state not in ('assigned') for picking in pickings):
            raise UserError(_(
                'Some pickings are still waiting for goods. Please check or force their availability before setting this batch to done.'))
        for picking in pickings:
            picking.message_post(
                body="<b>%s:</b> %s <a href=#id=%s&view_type=form&model=stock.reception.report>%s</a>" % (
                    _("Transferred by"),
                    _("Reception Report"),
                    picking.receptionreport_id.id,
                    picking.receptionreport_id.name))

        picking_to_backorder = self.env['stock.picking']
        picking_without_qty_done = self.env['stock.picking']
        for picking in pickings:
            if all([x.qty_done == 0.0 for x in picking.move_line_ids]):
                # If no lots when needed, raise error
                picking_type = picking.picking_type_id
                if (picking_type.use_create_lots or picking_type.use_existing_lots):
                    for ml in picking.move_line_ids:
                        if ml.product_id.tracking != 'none':
                            raise UserError(
                                _('Some products require lots/serial numbers, so you need to specify those first!'))
                # Check if we need to set some qty done.
                picking_without_qty_done |= picking
            elif picking._check_backorder():
                picking_to_backorder |= picking
            else:
                picking.action_done()
        self.write({'state': 'done'})
        if picking_without_qty_done:
            view = self.env.ref('stock.view_immediate_transfer')
            wiz = self.env['stock.immediate.transfer'].create({
                'pick_ids': [(4, p.id) for p in picking_without_qty_done],
                'pick_to_backorder_ids': [(4, p.id) for p in picking_to_backorder],
            })
            return {
                'name': _('Immediate Transfer?'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'stock.immediate.transfer',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'res_id': wiz.id,
                'context': self.env.context,
            }
        if picking_to_backorder:
            return picking_to_backorder.action_generate_backorder_wizard()
        return True

    def _track_subtype(self, init_values):
        if 'state' in init_values:
            return 'stock_picking_reception_report.mt_reception_report_state'
        return super(StockReceptionReport, self)._track_subtype(init_values)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    receptionreport_id = fields.Many2one(
        'stock.reception.report', string='Reception Report', oldname="wave_id",
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        help='Reception Report associated to this picking', copy=False)
