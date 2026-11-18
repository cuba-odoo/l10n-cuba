# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class L10nCuWebsiteSale(WebsiteSale):

    def _l10n_cu_validate_fiscal_country(self):
        """Devuelve el parámetro de configuración que controla si la lógica de campos
        obligatorios específica de Cuba (municipality_id en lugar de city) debe
        aplicarse únicamente cuando el país fiscal de la compañía del sitio web
        sea Cuba.

        Cuando este parámetro está activado, se toma el país fiscal de la compañía
        como fuente de verdad para decidir si aplican las reglas de dirección
        cubanas. Cuando está desactivado (comportamiento por defecto), las reglas
        se aplican únicamente basándose en el país de destino seleccionado por el
        cliente, sin importar el país fiscal de la compañía.
        """
        return request.env['ir.config_parameter'].sudo()._get_param(
            'l10n_cu_website_sale.rquire_company_fiscal_country'
        )

    def _get_mandatory_delivery_address_fields(self, country_sudo):
        mandatory_fields = super()._get_mandatory_delivery_address_fields(country_sudo)

        check_fiscal_country = self._l10n_cu_validate_fiscal_country()

        # En Odoo, los addons específicos de país o región suelen asumir que
        # el país fiscal de la compañía coincide con el país que se está
        # validando, para así aplicar sus restricciones o validaciones. Sin
        # embargo, esta suposición no siempre se cumple: la compañía de un
        # sitio web puede estar registrada en España y aun así realizar
        # entregas en Cuba. En ese escenario, basarse únicamente en el país
        # fiscal dejaría sin exigir el municipality_id en las direcciones de
        # entrega cubanas. Este parámetro permite sobrescribir ese
        # comportamiento para poder seguir aplicando la validación específica
        # de Cuba en función del país de destino, independientemente del país
        # fiscal de la compañía.
        if bool(check_fiscal_country) and request.website.sudo().company_id.country_id.code != 'CU':
            return mandatory_fields

        if country_sudo.code == 'CU':
            mandatory_fields |= {'municipality_id'}
            mandatory_fields.remove('city')

        return mandatory_fields

    def _get_mandatory_billing_address_fields(self, country_sudo):
        """Extend mandatory fields to add the vat in case the website and the customer are from cuba"""
        mandatory_fields = super()._get_mandatory_billing_address_fields(country_sudo)

        check_fiscal_country = self._l10n_cu_validate_fiscal_country()

        # Ver _get_mandatory_delivery_address_fields: el país fiscal de la
        # compañía no siempre representa los países que realmente atiende el
        # sitio web, por lo que esta validación puede omitirse mediante
        # configuración para seguir exigiendo los campos obligatorios
        # específicos de Cuba.
        if bool(check_fiscal_country) and request.website.sudo().company_id.country_id.code != 'CU':
            return mandatory_fields

        if country_sudo.code == 'CU':
            mandatory_fields |= {'municipality_id'}
            mandatory_fields.remove('city')

        return mandatory_fields

    def _prepare_address_form_values(self, order_sudo, partner_sudo, *args, address_type, **kwargs):
        rendering_values = super()._prepare_address_form_values(
            order_sudo, partner_sudo, *args, address_type=address_type, **kwargs
        )
        rendering_values.update({
            'municipality_id': partner_sudo.municipality_id.id,
            'state_municipalities': partner_sudo.state_id.municipality_ids,
        })
        return rendering_values

    @http.route(['/shop/l10n_cu/state_infos/<model("res.country.state"):state>'], type="json", auth="public", methods=["POST"], website=True, )
    def l10n_cu_state_infos(self, state, **kw):
        municipalities = request.env['res.municipality'].sudo().search([('state_id', '=', state.id)])
        return {'municipalities': [(c.id, c.name, c.code) for c in municipalities]}
