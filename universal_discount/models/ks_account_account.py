from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class Company(models.Model):
    _inherit = "res.company"

    ks_enable_discount = fields.Boolean(string="Activate Universal Discount")
    ks_sales_discount_account = fields.Many2one('account.account', string="Sales Discount Account")
    ks_purchase_discount_account = fields.Many2one('account.account', string="Purchase Discount Account")


class KSResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ks_enable_discount = fields.Boolean(string="Activate Universal Discount", related='company_id.ks_enable_discount', readonly=False)
    ks_sales_discount_account = fields.Many2one('account.account', string="Sales Discount Account", related='company_id.ks_sales_discount_account', readonly=False)
    ks_purchase_discount_account = fields.Many2one('account.account', string="Purchase Discount Account", related='company_id.ks_purchase_discount_account', readonly=False)
