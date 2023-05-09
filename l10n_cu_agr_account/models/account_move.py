# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.addons import decimal_precision as dp


class ProductArancel(models.Model):
    _inherit = 'product.arancel'

    invoice_line_ids = fields.One2many(
        'account.move.line', 'product_arancel_id', string='Arancel')


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    @api.depends('invoice_line_ids.bultos')
    def _compute_amount_log(self):
        for rec in self:
            rec.no_bultos = sum(line.bultos for line in rec.invoice_line_ids)
            rec.weight_brute_total = sum(
                line.weight for line in rec.invoice_line_ids)
            rec.net_weight_total = sum(
                line.net_weight for line in rec.invoice_line_ids)

    no_bultos = fields.Integer(
        'No Bultos', compute='_compute_amount_log', help='Cantidad de Bultos', store=True)
    net_weight_total = fields.Float('Total Peso Neto (kg)', digits=dp.get_precision(
        'Peso Neto Total'), compute='_compute_amount_log', help='Peso neto total(Kg)', store=True)
    weight_brute_total = fields.Float('Total Peso Bruto (kg)', digits=dp.get_precision(
        'Peso Bruto Total'), compute='_compute_amount_log', help='Peso bruto total(Kg)', store=True)
    
    contract_number = fields.Char('Número de contrato')
    
    importer_company_id = fields.Many2one(
        comodel_name="res.partner",
        string="Importadora",
        domain=[
            ("company_is_importing", "=", True),
        ],
    )


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # @api.one
    @api.depends('quantity', 'product_id', 'product_id.product_tmpl_id')
    def _compute_weight_brute(self):
        for line in self:
            line.weight = line.quantity * line.product_id.product_tmpl_id.weight \
                if line.quantity else 0.0

    # @api.one
    @api.depends('quantity', 'product_id', 'product_id.product_tmpl_id')
    def _compute_net_weight(self):
        for line in self:
            line.net_weight = line.quantity * line.product_id.product_tmpl_id.net_weight \
                if line.quantity else 0.0

    product_arancel_id = fields.Many2one('product.arancel', related='product_id.product_tmpl_id.product_arancel_id',
                                         store=True)

    bultos = fields.Integer('Bultos', help='Cantidad de Bultos del mismo item')
    weight = fields.Float('Weight Brute', digits=dp.get_precision('Peso Brute'), compute=_compute_weight_brute,
                          store=True, help='Peso Brute', compute_sudo=True)
    net_weight = fields.Float('Weight Neto', digits=dp.get_precision('Peso Neto'), compute=_compute_net_weight,
                              store=True, help='Peso Neto', compute_sudo=True)

    # origen = fields.Selection(selection=[('esp*', 'España*')], help='NMF Origen', default='esp*', store=True)
    origen = fields.Many2one(
        'res.partner.nfm', string='Nfm', ondelete='cascade', store=True, help='Nfm')
