# List of contributors:
# Segu
{
    'name': 'Cuba - POS',
    'summary': 'Implementacion de Punto de Ventas para Cuba.',
    'category': 'Point Of Sale',
    'version': '18.0.1.0.0',
    'author': 'Comunidad Cubana de Odoo',
    'depends': ['point_of_sale', 'l10n_cu'],
    'license': 'LGPL-3',
    'assets': {
        'point_of_sale._assets_pos': [
            'l10n_cu_pos/static/src/js/l10n_cu_pos.js',
        ],
    },
    'data': [
        'data/point_of_sale_data.xml',
        'views/res_partner_views.xml',
    ],
}
