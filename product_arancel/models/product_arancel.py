# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ProductArancel(models.Model):
    _name = 'product.arancel'
    _description = 'Arancel of customs'
    _rec_name = 'code'
    _parent_name = "parent_id"
    _parent_store = True
    # _parent_order = 'code'
    _order = 'parent_left'

    code = fields.Char('Code', size=64, required=True, index=True)
    name = fields.Char('Name', size=2048, required=True, translate=True, index=True)
    parent_path = fields.Char(index=True)
    parent_id = fields.Many2one('product.arancel', 'Parent Arancel', domain=[('type', '=', 'view')], index=True, ondelete='cascade')
    child_ids = fields.One2many('product.arancel', 'parent_id', string='Child Arancel')
    parent_left = fields.Integer('Left Parent', index=1)
    parent_right = fields.Integer('Right Parent', index=1)
    uom_id = fields.Many2one('uom.uom', string='UM')
    derechos_general = fields.Integer(string='Derechos General')
    derechos_NFM = fields.Integer(string='Derechos NFM')
    type = fields.Selection([('view', 'View'), ('normal', 'Normal')], ' Arancel Type')
    product_ids = fields.One2many('product.template', 'product_arancel_id', string='Arancel Products')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_arancel_id = fields.Many2one('product.arancel', string='Arancel', domain=[('type', '=', 'normal')], help='Select arancel for this product')


