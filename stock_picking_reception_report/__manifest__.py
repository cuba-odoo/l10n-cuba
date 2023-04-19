# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Warehouse Management: Reception Report',
    'version': '1.0.1',
    'author': 'TecKISA',
    'category': 'Warehouse',
    'description': """
This module adds the Reception Report option in warehouse management
=================================================================
    """,
    'website': 'https://www.teckisa.com/page/warehouse',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_reception_report_views.xml',
        'data/stock_reception_report_data.xml',
        # 'wizard/stock_picking_to_reception_report_views.xml',
        'report/reception_report_layout.xml',
        'report/report_reception.xml',
        'report/report_reception_template.xml',
    ],
    'demo': [],
    'installable': True,
}
