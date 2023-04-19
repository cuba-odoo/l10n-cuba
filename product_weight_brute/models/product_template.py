# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.addons import decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    weight_brute = fields.Float(
        'Weight Brute',
        # compute='_compute_weight_brute',
        digits=dp.get_precision('Stock Weight Brute'),
        # inverse='_set_weight_brute',
        store=True,
        help="The weight brute of the contents in Kg, including any packaging, etc.")

    # @api.depends('product_variant_ids', 'product_variant_ids.weight_brute')
    # def _compute_weight_brute(self):
    #     unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
    #     for template in unique_variants:
    #         template.weight_brute = template.product_variant_ids.weight_brute
    #     for template in (self - unique_variants):
    #         template.weight_brute = 0.0

    # @api.one
    # def _set_weight_brute(self):
    #     if len(self.product_variant_ids) == 1:
    #         self.product_variant_ids.weight_brute = self.weight_brute

    @api.model
    def create(self, vals):

        template = super(ProductTemplate, self).create(vals)
        if "create_product_product" not in self._context:
            template.with_context(create_from_tmpl=True).create_variant_ids()

        # This is needed to set given values to first variant after creation
        related_vals = {}
        if vals.get('weight_brute'):
            related_vals['weight_brute'] = vals['weight_brute']
        if related_vals:
            template.write(related_vals)
        return template


class ProductProduct(models.Model):
    _inherit = "product.product"


    weight_brute = fields.Float(
        'Weight Brute', digits=dp.get_precision('Stock Weight Brute'),
        help="The weight brute of the contents in Kg, including any packaging, etc.")
