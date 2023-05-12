# -*- coding: utf-8 -*-

import cgi
import io
from xmlrpc import client
from odoo import models, fields ,modules,tools,api,_
import base64
from PIL import Image

class ResPartner(models.Model):
    
    _inherit = 'res.partner'

    sec_benef_name= fields.Char(
        string=_('Second Beneficiary'),required=False
    )
    
    @api.model
    def check_mode(self, order, partner_id, public_partner):
        """Return mode of the address."""
        partner_obj = self.with_context(show_address=1).sudo()

        shippings = partner_obj.search([
            ('id', 'child_of', order.partner_id.commercial_partner_id.ids),
            ('id', '=', partner_id)])

        if (partner_id not in shippings.ids and
                partner_id != order.partner_id.id and partner_id > 0):
            return ()

        # ('new', 'billing') assuming by default public user
        create = 'new'
        ship = 'billing'

        if partner_id == -1 or (partner_id != order.partner_id.id and
                                partner_id > 0):
            # ('new', 'shipping') creating a new contact
            ship = 'shipping'

        if order.partner_id.id != public_partner and partner_id > 0:
            # ('edit', 'billing') editing a registered main user/contact
            create = 'edit'

        mode = (create, ship)

        return mode
    
    @api.model
    def bind_partner(self, order, mode, partner_id):
        """Binding the order with partner."""
        if not self.browse(partner_id).exists():
            return False
        current_shipping_id = order.partner_shipping_id
        extra = (lambda order, partner: None, lambda order, partner: None)
        action = {
            'billing': (
                lambda order, partner: setattr(order, 'partner_id', partner),
                lambda order, partner: order.onchange_partner_id()
            ),
            'shipping': (
                lambda order, partner: setattr(order, 'partner_shipping_id', partner),
                lambda order, partner: None
            )
        }
        action.get(mode[1], extra)[0](order, partner_id)
        action.get(mode[1], extra)[1](order, partner_id)
        if mode[1] == 'billing' and mode[0] != 'new':
            order.partner_shipping_id = current_shipping_id
        return True

    @api.model
    def _get_default_image(self):
        
        image_path = modules.get_module_resource('co_theme', 'static','src','img', 'login.png')
        im = Image.open(image_path)
        return im 