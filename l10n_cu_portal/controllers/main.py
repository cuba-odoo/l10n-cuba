# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal


class L10nCuPortal(CustomerPortal):

    def _prepare_address_form_values(
        self, partner_sudo, address_type='billing', use_delivery_as_billing=False, callback='', **kwargs
    ):
        rendering_values = super()._prepare_address_form_values(
            partner_sudo, address_type=address_type, use_delivery_as_billing=use_delivery_as_billing, callback=callback, **kwargs
        )
        rendering_values.update({
            'municipality_id': partner_sudo.municipality_id.id,
            'state_municipalities': rendering_values['state'].municipality_ids,
        })
        return rendering_values

    def _validate_address_values(self, address_values, partner_sudo, *args, **kwargs):
        invalid_fields, missing_fields, messages = super()._validate_address_values(
            address_values, partner_sudo, *args, **kwargs
        )
        municipality_id = address_values.get('municipality_id')
        if municipality_id:
            state_id = address_values.get('state_id', partner_sudo.state_id.id)
            country_id = address_values.get('country_id', partner_sudo.country_id.id)
            municipality = request.env['res.municipality'].sudo().browse(municipality_id).exists()
            if not municipality or (municipality.state_id.id, municipality.state_id.country_id.id) != (
                state_id, country_id
            ):
                invalid_fields.add('municipality_id')
                messages.append(self.env._("Select a municipality in the selected province."))
        return invalid_fields, missing_fields, messages

    @http.route(['/shop/l10n_cu/state_infos/<model("res.country.state"):state>'], type="jsonrpc", auth="public", methods=["POST"], website=True, )
    def l10n_cu_state_infos(self, state, **kw):
        municipalities = request.env['res.municipality'].sudo().search([('state_id', '=', state.id)])
        return {'municipalities': [(c.id, c.name, c.code) for c in municipalities]}
