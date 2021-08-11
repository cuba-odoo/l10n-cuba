# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HSCode(models.Model):
    _inherit = "hs.code"

    @api.model
    def create(self, vals):
        if vals.get("local_code"):
            vals["local_code"] = vals["local_code"].replace(" ", "")
        return super().create(vals)

    def write(self, vals):
        if vals.get("local_code"):
            vals["local_code"] = vals["local_code"].replace(" ", "")
        return super().write(vals)
