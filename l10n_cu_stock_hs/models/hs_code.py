# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HSCode(models.Model):
    _name = "hs.code"
    _description = "H.S. Code"
    _order = "code"
    _rec_name = "code"


    code = fields.Char('Code', size=64, required=True, index=True)
    description = fields.Char('Description', size=2048, required=True, translate=True, index=True)
    parent_id = fields.Many2one('hs.code', 'Parent Hs. code', domain=[('type', '=', 'view')],
                                index=True, ondelete='cascade')
    child_id = fields.One2many('hs.code', 'parent_id', string='Child Hs code')

    active = fields.Boolean(default=True)
    UM = fields.Many2one('uom.uom', string='UM')
    general_duty = fields.Integer(string='General Duty')
    nmf_duty = fields.Integer(string='NMF duty')
    type = fields.Selection([('view', 'View'), ('normal', 'Normal')], ' H.S Type')

    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self._default_company_id(),
    )
    product_categ_ids = fields.One2many(
        comodel_name="product.category",
        inverse_name="hs_code_id",
        string="Product Categories",
        readonly=True,
    )
    product_tmpl_ids = fields.One2many(
        comodel_name="product.template",
        inverse_name="hs_code_id",
        string="Products",
        readonly=True,
    )
    product_categ_count = fields.Integer(compute="_compute_product_categ_count")
    product_tmpl_count = fields.Integer(compute="_compute_product_tmpl_count")

    @api.model
    def _default_company_id(self):
        return False
        
    @api.depends("product_categ_ids")
    def _compute_product_categ_count(self):
        for code in self:
            code.product_categ_count = len(code.product_categ_ids)

    @api.depends("product_tmpl_ids")
    def _compute_product_tmpl_count(self):
        for code in self:
            code.product_tmpl_count = len(code.product_tmpl_ids)

    @api.depends("code", "description")
    def name_get(self):
        res = []
        for this in self:
            name = this.code
            if this.description:
                name += " " + this.description
            name = len(name) > 55 and name[:55] + "..." or name
            res.append((this.id, name))
        return res

    _sql_constraints = [
        (
            "code_company_uniq",
            "unique(code, company_id)",
            "This code already exists for this company !",
        )
    ]

    @api.model
    def create(self, vals):
        if vals.get("code"):
            vals["code"] = vals["code"].replace(" ", "")
        return super().create(vals)

    def write(self, vals):
        if vals.get("code"):
            vals["code"] = vals["code"].replace(" ", "")
        return super().write(vals)