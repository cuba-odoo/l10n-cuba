from odoo import api, fields, models, _, Command


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    municipality_ids = fields.Many2many('res.municipality', 'delivery_carrier_mun_rel', 'carrier_id',
                                        'municipality_id', 'Municipalities')

    @api.onchange('municipality_ids')
    def onchange_municipalities(self):
        self.state_ids = [(6, 0, self.state_ids.ids + self.municipality_ids.mapped('state_id.id'))]

    @api.onchange('state_ids')
    def onchange_states(self):
        super(DeliveryCarrier, self).onchange_states()
        self.municipality_ids -= self.municipality_ids.filtered(
            lambda state: state._origin.id not in self.state_ids.res_municipality_id.ids
        )

    def _match_address(self, partner):
        match = super(DeliveryCarrier, self)._match_address(partner)
        if self.municipality_ids and partner.res_municipality_id not in self.municipality_ids:
            return False
        return match
