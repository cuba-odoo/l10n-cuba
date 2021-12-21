{
     'name': 'Cuba - Accounting PDF Reports',
     'version': '0.1',
     'category': 'Generic Modules/Reporting',
     'summary': """
        Proformas Estados Financieros para las MIPYME en Cuba.
     """,
     'author': 'Segu',
     'depends': ["accounting_pdf_reports", "l10n_cu"],
     'data': [
          "data/account_financial_report_es.xml",
          "data/account_financial_report_er.xml",
          "data/account_financial_report_ege.xml",
          # "data/account_financial_report_ei.xml",
          "reports/report_financial.xml",
          "reports/report_partner_balance.xml",
          "views/account_views.xml",
          "views/report_partnerbalance_template.xml",
          "views/report_financial_layout.xml",
          "views/report_financial_templates.xml",
          "wizards/account_report.xml",
          "wizards/report_partner_balance.xml",
          "security/ir.model.access.csv"
     ],
     # 'auto_install': True,
}
