# List of contributors:
# Segu

{
     'name': 'Cuba - Pago de Nóminas',
     'version': '0.1',
     'category': 'Human Resources',
     'summary': """
        Pago masivo de nóminas.
     """,
     'author': 'Comunidad Cubana de Odoo',
     'depends': ["l10n_cu", "l10n_cu_hr", "l10n_cu_hr_payroll_account"],
     'data': [
          "security/ir.model.access.csv",
          "views/hr_payroll_payment_views.xml",
          "views/report_payroll_payment_template.xml",
          "reports/payroll_payment_report.xml",
          "wizard/payroll_payment_massive_wizard.xml",
     ],
     'license': 'LGPL-3',
}
