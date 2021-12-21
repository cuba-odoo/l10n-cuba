<<<<<<< HEAD
# List of contributors:
# Segu S.U.R.L

=======
>>>>>>> a542a08a032458fdb0e64cc66de48d4ecf9d2a35
{
     'name': 'Cuba - Pago de Nóminas',
     'version': '0.1',
     'category': 'Human Resources',
     'summary': """
        Pago masivo de nóminas para las MIPYME en Cuba.
     """,
<<<<<<< HEAD
     'author': 'Comunidad Cubana de Odoo',
=======
     'author': 'Segu',
>>>>>>> a542a08a032458fdb0e64cc66de48d4ecf9d2a35
     'depends': ["l10n_cu", "l10n_cu_hr","l10n_cu_hr_payroll_account"],
     'data': [
          "security/ir.model.access.csv",
          "views/hr_payroll_payment_views.xml",
          "views/report_payroll_payment_template.xml",
          "reports/payroll_payment_report.xml",
          "wizard/payroll_payment_massive_wizard.xml",
     ],
}
