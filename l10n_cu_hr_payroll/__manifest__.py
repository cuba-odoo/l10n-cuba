# List of contributors:
# Segu

{
     'name': 'Cuba - Nóminas',
     'version': '0.1',
     'category': 'Human Resources',
     # 'description': 'Nóminas para las MIPYME en Cuba.',
     'summary': """
        Nóminas - Cuba.
     """,
     'author': 'Comunidad Cubana de Odoo',
     'depends': ["l10n_cu_hr", "hr_payroll_community"],
     'data': [
          "data/hr_payroll_data.xml",
          "data/hr.salary.rule.csv",
          "security/ir.model.access.csv",
          "views/hr_payslip_views.xml",
          "views/hr_employee_views.xml",
          "views/hr_projection_views.xml",
          "views/report_projection_template.xml",
          "views/report_payslip_run_template.xml",
          "reports/hr_payroll_report.xml",
          "wizard/hr_payroll_projection_wizard.xml",
          "wizard/hr_payroll_payslips_by_employees_wizard.xml",
     ],
}
