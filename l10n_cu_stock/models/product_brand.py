# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ProductBrand(models.Model):
    _name = 'product.brand'
    _description = 'Product Brands'
    _order = "sequence,id"

    sequence = fields.Integer(string='Sequence')
    name = fields.Char(string='Brand Name', translate=True, required=True)
    logo = fields.Binary(string='Logo', required=True)
    active = fields.Boolean(string='Active', default=True)
    brand_description = fields.Text(string='Description', translate=True)
    brand_product_ids = fields.One2many('product.template','product_brand_id', string='Brand Products',)
    products_count = fields.Integer(string='Number of products', compute='_get_products_count')

    @api.depends('brand_product_ids')
    def _get_products_count(self):
        ''' Product count brandwise '''
        self.products_count = len(self.brand_product_ids)

    def get_brand_product(self):
        ''' Brand page redirector '''
        result = {
            "type": "ir.actions.act_window",
            "res_model": "product.template",
            "domain": [['product_brand_id', '=', self.id]],
            "name": "Products",
            'view_mode': 'kanban,tree,form',
        }
        return result