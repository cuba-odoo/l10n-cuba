# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.addons import decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    weight_neto = fields.Float(
        'Weight Neto',
        # compute='_compute_weight_neto',
        digits=dp.get_precision('Stock Weight Neto'),
        # inverse='_set_weight_neto',
        store=True,
        help="The weight neto of the contents in Kg, NOT including any packaging, etc.")

    # @api.depends('product_variant_ids', 'product_variant_ids.weight_neto')
    # def _compute_weight_neto(self):
    #     unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
    #     for template in unique_variants:
    #         template.weight_neto = template.product_variant_ids.weight_neto
    #     for template in (self - unique_variants):
    #         template.weight_neto = 0.0

    # @api.one
    # def _set_weight_neto(self):
    #     if len(self.product_variant_ids) == 1:
    #         self.product_variant_ids.weight_neto = self.weight_neto

    @api.model
    def create(self, vals):

        template = super(ProductTemplate, self).create(vals)
        if "create_product_product" not in self._context:
            template.with_context(create_from_tmpl=True).create_variant_ids()

        # This is needed to set given values to first variant after creation
        related_vals = {}
        if vals.get('weight_neto'):
            related_vals['weight_neto'] = vals['weight_neto']
        if related_vals:
            template.write(related_vals)
        return template


class ProductProduct(models.Model):
    _inherit = "product.product"


    weight_neto = fields.Float(
        'Peso Neto', digits=dp.get_precision('Stock Weight Neto'),
        help="The weight neto of the contents in Kg, NOT including any packaging, etc.")
