# -*- coding: utf-8 -*-
{
    'name': "l10n_cu_website_sale",
    'summary': "Improve eCommerce in Cuba, adding support for addresses and municipalities.",
    'description': """
        The `l10n_cu_website_sale` module is designed to enhance eCommerce in Cuba, facilitating the management of 
        addresses and the integration of municipalities in the purchasing process.
        It provides a structure adapted to local needs, allowing companies to offer a more precise and personalized 
        shopping experience.
        This module is essential to optimize online sales, ensuring that addresses are handled appropriately 
        according to the Cuban context.
    """,
    "author": "Idola Odoo Team, Comunidad cubana de Odoo",
    'category': 'Website/Website',
    'version': '2.0',
    'depends': ['base', 'website_sale', 'l10n_cu_address'],
    'data': [
        'data/ir_model_fields.xml',
        'views/delivery_carrier_views.xml',
    ],
    'installable': True,
    "auto_install": ['l10n_cu_address', 'website_sale'],
    "license": "AGPL-3",
}
