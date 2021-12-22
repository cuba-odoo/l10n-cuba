# List of contributors:
# Segu S.U.R.L

{
     'name': 'Cuba - RRHH',
     'version': '0.1',
     'category': 'Human Resources',
     'summary': """
        RRHH para las MIPYME en Cuba.
     """,
     'author': 'Comunidad Cubana de Odoo',
     'depends': ["hr", "date_range"],
     'auto_install': True,     
     'data': [
          "data/hr_data.xml",
          "views/assistance_cards_template.xml",
          "reports/report_assistance_cards.xml",
          "wizards/assistance_cards_wizard.xml",
          "security/ir.model.access.csv"
     ],
}
