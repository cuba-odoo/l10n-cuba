# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class ResCountry(models.Model):
    _inherit = 'res.country'

    def get_website_sale_countries(self, mode='billing'):
        if mode == 'shipping':
            return self.sudo().search([])
        return self.sudo().search([])

    # def get_website_sale_states(self, mode='billing'):
    #     if mode == 'shipping':
    #         def_stage_id = self.env['res.country.state'].search([('name', 'in', ('La Habana','Mayabeque','Artemisa'))])
    #         def_stage_id = self.env['res.country.state'].search([('name', '=', 'La Habana')])

    #         if def_stage_id:
    #             return def_stage_id
    #     return self.sudo().state_ids
