# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
# 
#################################################################################

from . import models

def post_init_hook(cr, registry):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    denomination_1 = env.ref('point_of_sale.0_01', raise_if_not_found=False)
    denomination_2 = env.ref('point_of_sale.0_02', raise_if_not_found=False)
    denomination_5 = env.ref('point_of_sale.0_05', raise_if_not_found=False)

    denominations = denomination_1 + denomination_2 + denomination_5
    denominations.write({'pos_config_ids': [(6, 0, [])]})
