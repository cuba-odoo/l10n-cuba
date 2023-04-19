# -*- coding: utf-8 -*-


from odoo import fields, models, api, _


class FamRecambio(models.Model):
    _name = 'product.fam.recambio'
    _description = 'Familia Recambio SAP'
    _rec_name = 'code'

    code = fields.Char('Code', size=64, required=True, index=True)
    name = fields.Char('Name', size=2048, required=True, translate=True, index=True)
    product_ids = fields.One2many('product.template', 'product_fam_recambio_id', string='Familia Recambio SAP')


class Material(models.Model):
    _name = 'product.material'
    _description = 'Material SAP'
    _rec_name = 'code'

    code = fields.Char('Code', size=64, required=True, index=True)
    name = fields.Char('Name', size=2048, required=True, translate=True, index=True)
    product_ids = fields.One2many('product.template', 'product_material_id', string='Material SAP')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_fam_recambio_id = fields.Many2one(
        'product.fam.recambio',
        string='Familia Recambio',
        help='Select fam recambio for this product'
    )
    product_material_id = fields.Many2one(
        'product.material',
        string='Material',
        help='Select material for this product'
    )



