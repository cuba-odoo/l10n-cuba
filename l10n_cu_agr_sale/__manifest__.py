# -*- coding: utf-8 -*-
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3

{
    'name': 'AGR Sales',
    'version': '1.2',
    'category': 'Sales',
    'license': 'LGPL-3',
    'author': 'TecKISA',
    'summary': '',
    'description': """
This module contains all the common features of Sales Management and eCommerce. Personalización de la Oferta para AGR.
    """,
    'depends': ['l10n_cu_agr_account', 'portal', 'product_arancel'],
    'data': [
        'views/sale_views.xml',
        # 'report/sale_report_templates.xml',
        'report/sale_report.xml',
        'report/report_agr_sale.xml',
    ],
    'installable': True,
    'auto_install': False,
}
