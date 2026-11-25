# -*- coding: utf-8 -*-
from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _get_frontend_writable_fields(self):
        frontend_writable_fields = super()._get_frontend_writable_fields()
        frontend_writable_fields.update({'municipality_id'})
        return frontend_writable_fields

    def _get_mandatory_address_fields(self, country_sudo, **kwargs):
        mandatory_fields = super()._get_mandatory_address_fields(country_sudo, **kwargs)
        if country_sudo.code != 'CU':
            return mandatory_fields

        # Portal users cannot read system parameters. Read only this fixed key.
        fiscal_country_only = self.env['ir.config_parameter'].sudo().get_bool(
            'l10n_cu_website_sale.rquire_company_fiscal_country'
        )
        if fiscal_country_only and self.env.company.country_id.code != 'CU':
            return mandatory_fields

        return (mandatory_fields - {country_sudo._get_partner_city_field()}) | {
            'state_id', 'municipality_id',
        }
