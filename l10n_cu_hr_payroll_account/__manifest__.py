# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Cuba - Nóminas con contabilidad',
    'category': 'Accounting/Accounting',    
    'description': """
Accounting Data for Cuba Payroll Rules.
==========================================
    """,
    'depends': ['hr_payroll_account_community', 'l10n_cu', 'l10n_cu_hr_payroll'],
    'author': 'Segu',
    'data': [
        'data/hr_payroll_account_data.xml',
        'views/hr_payroll_account_views.xml',
    ],
}
