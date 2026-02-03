{
    'name': 'Cierre de Ejercicio Fiscal - Localización Cubana',
    'version': '15.0.1.1.0',
    'category': 'Accounting/Localizations',
    'summary': 'Automatiza el cierre contable anual según normas cubanas (NC-04)',
    'description': """
Módulo para cierre de ejercicio fiscal en Cuba.
- Calcula automáticamente saldos de ingresos y gastos
- Genera asiento único de cierre a cuenta 999000000 (Resultados)
- Compatible con plan de cuentas cubano NC-04
- Totalmente funcional en Odoo Community Edition
""",
    'author': 'Comunidad Cubana de Odoo',
    'website': 'https://github.com/cuba-odoo/l10n-cu',
    'license': 'LGPL-3',
    'depends': ['account', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/fiscal_year_closing_wizard_views.xml',
        'wizards/add_account_wizard_views.xml',
        'wizards/add_accounts_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}