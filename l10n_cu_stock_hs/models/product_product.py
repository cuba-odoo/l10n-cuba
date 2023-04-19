from odoo import models

class ProductProduct(models.Model):
    _inherit = "product.product"

    def get_hs_code_recursively(self):
        res = self.env["hs.code"]
        if self:
            self.ensure_one()
            if self.hs_code_id:
                res = self.hs_code_id
            elif self.categ_id:
                res = self.categ_id.get_hs_code_recursively()
        return res