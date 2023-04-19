# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = "product.template"

    origin_country_id = fields.Many2one(
        comodel_name="res.country",
        string="Country of Origin",
        help="Country of origin of the product i.e. product " "'made in ____'.",
    )

    net_weight = fields.Float(
        string="Net Weight",
        related="product_variant_ids.net_weight",
        digits=dp.get_precision("Stock Weight"),
        help="Net Weight of the product, container excluded.",
        readonly=False,
    )

    # Analizar si es necesario
    # Explicit field, renaming it
    weight = fields.Float(string="Gross Weight")

    product_brand_id = fields.Many2one(
        'product.brand', string='Brand', help='Select a brand for this product')
