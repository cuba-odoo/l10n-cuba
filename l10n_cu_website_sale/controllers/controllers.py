# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from werkzeug.exceptions import Forbidden

class WebsiteSaleCU(WebsiteSale): 

    def _get_mandatory_fields_billing(self, country_id=False):
        req = super(WebsiteSaleCU, self)._get_mandatory_fields_billing()
        # req.extend(('street_number', 'lastname', 'zip', 'city_id'))
        req = ['name', 'phone','street']
        return req

    def _get_mandatory_fields_shipping(self, country_id=False):
        req = super(WebsiteSaleCU, self)._get_mandatory_fields_shipping()
        # req.extend(('email', 'lastname', 'zip', 'street_number', 'city_id'))
        req = ['name', 'phone','street']
        return req

    def _get_country_related_render_values(self, kw, render_values):
        '''
        This method provides fields related to the country to render the website sale form
        '''
        values = render_values['checkout']
        mode = render_values['mode']
        if mode[1] == 'billing':
            res = super(WebsiteSaleCU,self)._get_country_related_render_values(kw, render_values)
            countries = request.env['res.country'].sudo().search([])
            stage = request.env['res.country.state'].sudo().search([])
            res['countries'] = countries
            # res['country_states']= stage
            return res
        def_country_id = request.env['res.country'].search([('code', '=', 'CU')], limit=1)
        def_stage_id = request.env['res.country.state'].search([('country_id', '=', def_country_id.id)])

        country = request.env['res.country'].browse(def_country_id.id)
        stage = request.env['res.country.state'].browse(def_stage_id.ids)
        
        res = {
            'country': country,
            'stage':stage,
            'country_states': stage,
            'countries': country,
            'municipalities': stage.get_website_sale_municipalities(mode=mode[1]),
        }
        return res
    
    @http.route(['/shop/addme'], type='http', auth="public", website=True)
    def addme(self):
        """Enable the widget to add a partner/contact
        """
        def_country_id = request.env['res.country'].search([('code', '=', 'CU')], limit=1)
        def_stage_id = request.env['res.country.state'].search([('country_id', '=', def_country_id.id)])
        #def_stage_id = request.env['res.country.state'].search([('name', '=', 'La Habana')])

        country = request.env['res.country'].browse(def_country_id.id)
        stage = request.env['res.country.state'].browse(def_stage_id.ids)
        return request.render('co_theme.add_shipping_address', {
        'countries': country,
        'provinces': stage,
        'municipalities': stage.get_website_sale_municipalities(mode='shipping')
    })

    @http.route(['/shop/editme'], type='http', auth="public", website=True)
    def editme(self, partner_id):
        """Enable the widget to edit a partner/contact."""
        order = request.website.sale_get_order()
        contact = request.env['res.partner'].sudo().browse(int(partner_id))
        template = 'co_theme.edit_contact_form'
        if order.partner_id.id == int(partner_id):
            template = 'co_theme.edit_billing_form'
        values = {
            'contact': contact,
            'website_sale_order': order,
        }
        return request.render(template, values)
    
    @http.route(['/shop/check_address'], type='http', auth="public", website=True)
    def check_address(self, **kw):
        """Called when the form is complete and valid."""
        order = request.website.sale_get_order()
        # checking if the user is not here without order and avoid tracebacks
        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        partner_obj = request.env['res.partner'].with_context(
            show_address=1).sudo()
        values, errors = {}, {}
        partner_id = int(kw.get('partner_id', -1))
        public_partner = request.website.user_id.sudo().partner_id.id

        mode = partner_obj.check_mode(order, partner_id, public_partner)
        if not mode:
            return Forbidden()

        values = partner_obj.search([('id', '=', partner_id)])
        pre_values = self.values_preprocess(order, mode, kw)
        errors, error_msg = self.checkout_form_validate(
            mode, kw, pre_values)
        post, errors, error_msg = self.values_postprocess(
            order, mode, pre_values, errors, error_msg)
        errors.update({'error_message': error_msg} if errors else {})

        values = kw if errors else values

        if errors:
            return json.dumps({
                'partner_id': partner_id,
                'mode': mode,
                'error': errors,
                'callback': kw.get('callback'),
            })
        if mode[1] == 'shipping':
            post['type'] = 'delivery'
            post['parent_id'] = int(kw.get('parent_id'))
        partner_id = self._checkout_form_save(mode, post, kw)
        partner_obj.bind_partner(order, mode, partner_id)

        return json.dumps({
                'partner_id': partner_id,
                'mode': mode,
                'callback': kw.get('callback'),
            })

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

    @http.route(['/shop/state_infos/<model("res.country.state"):state>'], type='json', auth="public", methods=['POST'], website=True)
    def stage_infos(self, state, mode, **kw):
        return dict(
            municipalities=[(mpio.id, mpio.name, mpio.code) for mpio in state.get_website_sale_municipalities(mode=mode)],
        )
