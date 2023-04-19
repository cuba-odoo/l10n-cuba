# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                   #
###############################################################################

from odoo import models, fields, api
from odoo.tools.translate import _
from logging import getLogger
from odoo.addons import decimal_precision as dp

_logger = getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = "product.product"

    net_weight = fields.Float(
        string="Net Weight",
        digits=dp.get_precision("Stock Weight"),
        help="Net Weight of the product, container excluded.",
    )

    # Explicit field, renaming it
    weight = fields.Float(string="Gross Weight")
    
    def name_get(self):
        result = []
        for this in self:
            name_result = super(ProductProduct, this).name_get()
            return_val_split = name_result[0][1].split()
            for element in return_val_split:
                if element == "[%s]" % this.default_code:
                    return_val_split.remove(element)
                result.append((this.id, ' '.join(return_val_split)))
        return result