# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class L10nCuWebsiteSale(WebsiteSale):

    def _get_country_related_render_values(self, kw, render_values):
        """ Provide the fields related to the country to render the website sale form """

        res = super()._get_country_related_render_values(kw, render_values)
        values = render_values['checkout']
        mode = render_values['mode']
        order = render_values['website_sale_order']

        def_state_id = order.partner_id.state_id
        state = 'state_id' in values and values['state_id'] != '' and request.env['res.country.state'].browse(int(values['state_id']))
        state = state and state.exists() or def_state_id

        res.update({
            'state': state,
            'municipalities': state.get_website_sale_municipalities(mode=mode[1]),
        })

        return res

    def _get_mandatory_fields_billing(self, country_id=False):
        req = super()._get_mandatory_fields_billing(country_id=country_id)
        if country_id:
            country = request.env['res.country'].browse(country_id)
            if country.municipality_required:
                req += ['res_municipality_id']
            if not country.city_required:
                req.remove('city')

        return req

    def checkout_form_validate(self, mode, all_form_values, data):
        error, error_message = super().checkout_form_validate(mode, all_form_values, data)

        country_id = data.get("country_id")
        state_id = data.get("state_id")
        res_municipality_id = data.get("res_municipality_id")

        if not isinstance(country_id, int) or (state_id and not isinstance(state_id, int)):
            error['common'] = 'Invalid country or state ID.'
            error_message.append(_('Invalid country or state ID.'))
            return error, error_message

        country = request.env['res.country'].browse(country_id)
        state = request.env['res.country.state'].browse(state_id) if state_id else None

        if res_municipality_id and not isinstance(res_municipality_id, int):
            error["res_municipality_id"] = 'error'
            error_message.append(_('Municipality ID must be a valid integer.'))

        elif state and res_municipality_id and int(res_municipality_id) not in state.res_municipality_id.ids:
            error["res_municipality_id"] = 'error'
            error_message.append(_('Invalid Municipality. Please select a valid Municipality.'))

        if not res_municipality_id and country.municipality_required:
            error["res_municipality_id"] = 'error'
            error_message.append(_('Some required fields are empty.'))

        return error, error_message

    def _get_mandatory_fields_shipping(self, country_id=False):
        req = super()._get_mandatory_fields_shipping(country_id=country_id)
        if country_id:
            country = request.env['res.country'].browse(country_id)
            if country.municipality_required:
                req += ['res_municipality_id']
            if not country.city_required:
                req.remove('city')

        return req

    @http.route(['/shop/l10n_cu/state_infos/<model("res.country.state"):state>'], type="json", auth="public", methods=["POST"], website=True, )
    def l10n_cu_state_infos(self, state, mode, **kw):

        municipalities = state.get_website_sale_municipalities(mode=mode)
        municipality_required = state.country_id.municipality_required

        return {
            'municipalities': [(c.id, c.name, c.code) for c in municipalities],
            'municipality_required': municipality_required
        }
