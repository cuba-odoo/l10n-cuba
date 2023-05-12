# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleCU(WebsiteSale): 

    @http.route(['/shop/address'], type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def address(self, **kw):
        result = super(WebsiteSaleCU, self).address(**kw)
        res_municipality_id = request.website.sale_get_order().partner_id.res_municipality_id
        state_id = request.website.sale_get_order().partner_id.state_id
        city = request.website.sale_get_order().partner_id.city
        if result.qcontext.get('mode',()) == ('edit', 'shipping'):
            res_municipality_id = request.website.sale_get_order().partner_shipping_id.res_municipality_id
            state_id = request.website.sale_get_order().partner_shipping_id.state_id
            city = request.website.sale_get_order().partner_shipping_id.city
        result.qcontext['res_municipality_id'] =res_municipality_id
        result.qcontext['state_id'] = state_id
        result.qcontext['city'] = city
        if 'submitted' not in kw and kw.get('is_profile',) and kw.get('is_profile',) == "True":
            result.qcontext.update({"response_template": "co_theme.co_address"})
            result.template = "co_theme.co_address"
        if 'submitted' in kw and request.httprequest.method == "POST" and kw.get('is_profile',):
            result.location = "/my/home"
        return result
