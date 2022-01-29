# List of contributors:
# Segu

{
     'name': 'Cuba - Accounting Financial Reports',
     'version': '15.0.1.0.0',
     'category': 'Generic Modules/Reporting',
     'summary': """
        Proformas Estados Financieros (Sector Empresarial) - Cuba.
     """,
     'author': 'Comunidad Cubana de Odoo',
     'depends': ["accounting_pdf_reports", "l10n_cu"],
     'data': [
          "data/account_financial_report_es.xml",
          "data/account_financial_report_er.xml",
          "data/account_financial_report_ege.xml",
          "data/account_financial_report_evab.xml",
          "reports/report_financial.xml",
          "reports/report_partner_balance.xml",
          "views/account_views.xml",
          "views/report_partnerbalance_template.xml",
          "views/report_financial_layout.xml",
          "views/report_financial_ege_templates.xml",
          "views/report_financial_er_templates.xml",
          "views/report_financial_es_templates.xml",
          "views/report_financial_evab_templates.xml",
          "wizards/account_report.xml",
          "wizards/report_partner_balance.xml",
          "security/ir.model.access.csv"
     ],
}
