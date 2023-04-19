# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    'name': 'Product Weight Brute',
    'version': '15.0.1.0.0',
    'category': 'Product',
    'summary': "Product Weight Brute",
    'author': 'TecKISA, Orlando Martinez Bao',
    'license': 'AGPL-3',
    'depends': [
        'product', 'stock',
        ],
    'data': [
        'views/product_weight_brute_view.xml',
        # 'security/ir.model.access.csv'
    ],
    'installable': True,
    'auto_install': False
}
