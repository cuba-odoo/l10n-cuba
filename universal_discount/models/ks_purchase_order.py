from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import json


class KSGlobalDiscountPurchases(models.Model):
    _inherit = "purchase.order"

    ks_global_discount_type = fields.Selection([('percent', 'Percentage'), ('amount', 'Amount')],
                                               string='Universal Discount Type', readonly=True,
                                               states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                               default='percent')
    ks_global_discount_rate = fields.Float('Universal Discount', readonly=True,
                                           states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    ks_amount_discount = fields.Monetary(string='Universal Discount', readonly=True, compute='_amount_all',
                                         track_visibility='always', store=True)
    ks_enable_discount = fields.Boolean(compute='ks_verify_discount')

    @api.depends('company_id.ks_enable_discount')
    def ks_verify_discount(self):
        for rec in self:
            rec.ks_enable_discount = rec.company_id.ks_enable_discount

    @api.depends('order_line.price_total', 'ks_global_discount_type', 'ks_global_discount_rate')
    def _amount_all(self):
        ks_res = super(KSGlobalDiscountPurchases, self)._amount_all()
        for rec in self:
            if not ('global_tax_rate' in rec):
                rec.ks_calculate_discount()
        return ks_res

    def _prepare_invoice(self):
        ks_res = super(KSGlobalDiscountPurchases, self)._prepare_invoice()
        ks_res['ks_global_discount_type'] = self.ks_global_discount_type
        ks_res['ks_global_discount_rate'] = self.ks_global_discount_rate
        return ks_res

    def action_view_invoice(self, invoices=False):
        ks_res = super(KSGlobalDiscountPurchases, self).action_view_invoice()
        for rec in self:
            hh = ks_res['context']
            jj = str(hh).replace("'", '"')
            dic = json.loads(jj)
            dic['default_ks_global_discount_rate'] = rec.ks_global_discount_rate
            dic['default_ks_global_discount_type'] = rec.ks_global_discount_type
            context_str = json.dumps(dic)
            ks_res['context'] = context_str
            # ks_res['context']['default_ks_global_discount_rate'] = rec.ks_global_discount_rate
            # ks_res['context']['default_ks_global_discount_type'] = rec.ks_global_discount_type
        return ks_res

    # #@api.multi
    def ks_calculate_discount(self):
        for rec in self:
            if rec.ks_global_discount_type == "amount":
                rec.ks_amount_discount = rec.ks_global_discount_rate if rec.amount_untaxed > 0 else 0
            elif rec.ks_global_discount_type == "percent":
                if rec.ks_global_discount_rate != 0.0:
                    rec.ks_amount_discount = (rec.amount_untaxed + rec.amount_tax) * rec.ks_global_discount_rate / 100
                else:
                    rec.ks_amount_discount = 0
            elif not rec.ks_global_discount_type:
                rec.ks_amount_discount = 0
                rec.ks_global_discount_rate = 0
            rec.amount_total = rec.amount_tax + rec.amount_untaxed - rec.ks_amount_discount

    @api.constrains('ks_global_discount_rate')
    def ks_check_discount_value(self):
        if self.ks_global_discount_type == "percent":
            if self.ks_global_discount_rate > 100 or self.ks_global_discount_rate < 0:
                raise ValidationError('You cannot enter percentage value greater than 100.')
        else:
            if self.ks_global_discount_rate < 0 or self.ks_global_discount_rate > self.amount_untaxed:
                raise ValidationError(
                    'You cannot enter discount amount greater than actual cost or value lower than 0.')
