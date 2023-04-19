# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError, AccessError
from odoo.addons import decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)

class ProductArancel(models.Model):
    _inherit = 'product.arancel'

    order_line_ids = fields.One2many(
        'sale.order.line', 'product_arancel_id', string='Arancel')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('product_uom_qty', 'product_id')
    def _compute_weight(self):
        for line in self:
            line.weight = line.product_uom_qty * \
                line.product_id.product_tmpl_id.weight if line.product_uom_qty else 0.0
            line.net_weight = line.product_uom_qty * line.product_id.product_tmpl_id.net_weight \
                if line.product_uom_qty else 0.0

    product_arancel_id = fields.Many2one('product.arancel', related='product_id.product_tmpl_id.product_arancel_id',
                                         store=True)
    bultos = fields.Integer('Bultos', help='Cantidad de Bultos del mismo item')
    weight = fields.Float('Peso Neto', digits=dp.get_precision('Peso Neto'), compute='_compute_weight',
                          store=True, help='Peso Neto')
    net_weight = fields.Float('Peso Bruto', digits=dp.get_precision('Peso Bruto'), compute='_compute_weight',
                              store=True, help='Peso Bruto')
    # weight = fields.Float('product.template', related='product_id.product_tmpl_id.weight', store=True, help='Peso Neto')
    # weight_brute = fields.Float('product.template', related='product_id.product_tmpl_id.weight_brute', store=True,
    #                             help='Peso Bruto')
    origen = fields.Many2one('res.partner.nfm', string='Nfm',
                             ondelete='cascade', store=True, help='Nfm', default=1)

    def _prepare_invoice_line(self, **optional_values):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        """
        self.ensure_one()
        res = {}
        _logger.debug(optional_values)
        account = self.product_id.property_account_income_id or self.product_id.categ_id.property_account_income_categ_id
        if not account:
            raise UserError(
                _('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') %
                (self.product_id.name, self.product_id.id, self.product_id.categ_id.name))

        fpos = self.order_id.fiscal_position_id or self.order_id.partner_id.property_account_position_id
        if fpos:
            account = fpos.map_account(account)

        res = {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'bultos': self.bultos,
            'weight': self.weight,
            'net_weight': self.net_weight,
            'name': self.name,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'discount': self.discount,
            'price_unit': self.price_unit,
            'tax_ids': [(6, 0, self.tax_id.ids)],
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'sale_line_ids': [(4, self.id)],
        }
        if self.order_id.analytic_account_id:
            res['analytic_account_id'] = self.order_id.analytic_account_id.id

        if optional_values:
            res.update(optional_values)

        if self.display_type:
            res['account_id'] = False

        return res


class AccountInvoiceLine(models.Model):
    _inherit = 'account.move.line'

    bultos = fields.Integer('Bultos', help='Cantidad de Bultos del mismo item')
    # origen = fields.Selection(selection=[('esp*', 'España*')], help='NMF Origen', default='esp*', store=True)
    origen = fields.Many2one('res.partner.nfm', string='Nfm',
                             ondelete='cascade', store=True, help='Nfm', default=1)
