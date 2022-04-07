# List of contributors:
# Segu

{
     'name': 'Cuba - Contabilidad Reportes',
     'version': '15.0',
     'category': 'Generic Modules/Reporting',
     'summary': """
        Proformas Estados Financieros (Sector Empresarial) - Cuba.
     """,
     'author': 'Comunidad Cubana de Odoo',
     'depends': ["accounting_pdf_reports", "report_xlsx", "l10n_cu"],
     'data': [
          "data/account_financial_report_es.xml",
          "data/account_financial_report_er.xml",
          "data/account_financial_report_ege.xml",
          "data/account_financial_report_evab.xml",
          "data/account_financial_report_5927_00.xml",
          "reports/report_financial.xml",
          "reports/report_partner_balance.xml",
          "views/account_views.xml",
          "views/report_partnerbalance_template.xml",
          "views/report_financial_layout.xml",
          "views/report_financial_ege_templates.xml",
          "views/report_financial_er_templates.xml",
          "views/report_financial_es_templates.xml",
          "views/report_financial_evab_templates.xml",
          "views/report_financial_5927_00_templates.xml",
          "wizards/account_report.xml",
          "wizards/report_partner_balance.xml",
          "security/ir.model.access.csv"
     ],
     'license': 'LGPL-3',
}
