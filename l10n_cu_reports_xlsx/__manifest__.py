# List of contributors:
# Segu

{
     'name': 'Cuba - Contabilidad XLSX reportes',
     'version': '15.0.1.0.0',
     'category': 'Generic Modules/Reporting',
     'summary': """
        Proformas Estados Financieros XLSX (Sector Empresarial) - Cuba.
     """,
     'author': 'Comunidad Cubana de Odoo',
     'depends': ["l10n_cu_reports", "report_xlsx"],
     'data': [
          "reports/report_financial.xml",
          "wizards/account_report.xml",
     ],
     'license': 'LGPL-3',
}
