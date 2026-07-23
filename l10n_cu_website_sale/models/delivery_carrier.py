from odoo import api, fields, models, _, Command


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    municipality_ids = fields.Many2many('res.municipality', 'delivery_carrier_mun_rel', 'carrier_id',
                                        'municipality_id', 'Municipalities')

    @api.onchange('state_ids')
    def _onchange_state_ids(self):
        self.municipality_ids -= self.municipality_ids.filtered(
            lambda state: state._origin.id not in self.state_ids.municipality_ids.ids
        )

    def _match_address(self, partner):
        match = super(DeliveryCarrier, self)._match_address(partner)
        if self.municipality_ids and partner.municipality_id not in self.municipality_ids:
            return False
        return match
