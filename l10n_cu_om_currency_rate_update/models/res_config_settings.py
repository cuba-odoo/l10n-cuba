from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    rate_bcc_tasa = fields.Selection(related="company_id.rate_bcc_tasa", readonly=False)

    rate_eltoque_token = fields.Char(
        related="company_id.rate_eltoque_token",
        readonly=False,
        groups="base.group_system",
    )
