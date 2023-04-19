from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

        
    hs_code_id = fields.Many2one(
        "hs.code",
        string="H.S. Code",
        # company_dependent updated from True to False in 14.0.2.0.0
        # migration scripts provided
        company_dependent=False,
        ondelete="restrict",
        help="Harmonised System Code. Nomenclature is "
        "available from the World Customs Organisation, see "
        "http://www.wcoomd.org/. You can leave this field empty "
        "and configure the H.S. code on the product category.",
    )