from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    # rate_provider SÍ tiene default ('frankfurter') en el módulo base
    rate_provider = fields.Selection(
        selection_add=[
            ("bcc", "Banco Central de Cuba"),
            ("eltoque", "El Toque (TRMI)"),
        ],
        ondelete={"bcc": "set default", "eltoque": "set default"},
    )

    # rate_fallback_provider NO tiene default en el módulo base:
    # 'set default' provoca AssertionError al instalar. Usamos 'set null'.
    rate_fallback_provider = fields.Selection(
        selection_add=[
            ("bcc", "Banco Central de Cuba"),
            ("eltoque", "El Toque (TRMI)"),
        ],
        ondelete={"bcc": "set null", "eltoque": "set null"},
    )

    rate_bcc_tasa = fields.Selection(
        [
            ("tasaOficial", "Oficial"),
            ("tasaPublica", "Pública"),
            ("tasaEspecial", "Especial"),
        ],
        string="Tasa BCC",
        default="tasaOficial",
        help="Cuál de las tres tasas del BCC se usa.",
    )

    rate_eltoque_token = fields.Char(
        string="Token de El Toque",
        groups="base.group_system",
        help="Token Bearer para la API de El Toque (dev.eltoque.com).",
    )
