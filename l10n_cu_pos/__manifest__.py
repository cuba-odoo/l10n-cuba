# List of contributors:
# Segu
{
    "name": "Cuba - POS",
    "summary": "Implementacion de Punto de Ventas para Cuba.",
    "category": "Point Of Sale",
    "version": "15.0",
    "author": "Comunidad Cubana de Odoo",
    "depends": ['point_of_sale', 'l10n_cu'],
    'license': 'LGPL-3',
    'assets': {
          'web.assets_backend': ['l10n_cu_pos/static/src/js/pos.js'],
          "web.assets_qweb": ["l10n_cu_pos/static/src/xml/pos.xml"]
    },
    'data': [
        "data/point_of_sale_data.xml",
        "views/res_partner_views.xml"
    ],

}
