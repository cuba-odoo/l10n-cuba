# -*- coding: utf-8 -*-
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3

{
    'name': 'AGR - Account',
    'version': '1.1',
    'category': 'Account',
    'license': 'LGPL-3',
    'author': 'TecKISA',
    'summary': '',
    'description': """
This module contains invoice AGR.
    """,
    'depends': ['account', 'portal', 'product_arancel', 'universal_discount', 'l10n_cu_stock'],
    'data': [
        'views/account_invoice_view.xml',
        'report/report_invoice_view.xml',
        'report/report_agr_invoice_template.xml',
        'report/report_agr_invoice.xml',
        'report/report_agr_invoice_eur.xml',
        'report/report_agr_invoice_consecute.xml',
        'report/agr_invoice_report_layout.xml',
        'report/agr_invoice_report_consecute_layout.xml',
        'crash/invoice_report_templates.xml',
        'crash/sale_report_templates2.xml',
    ],
    'installable': True,
}
