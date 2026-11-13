{
    "name": "Odoo 16 Automatic Currency Rates — Cuba (BCC + El Toque)",
    "summary": """Fuentes de tasas de cambio para Cuba:
    BCC oficial y El Toque (TRMI informal)
    """,
    "version": "16.0.1.0.0",
    "category": "Accounting",
    "author": "Comunidad Cubana de Odoo",
    "license": "LGPL-3",
    "depends": [
        "om_currency_rate_update",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
    ],
}
