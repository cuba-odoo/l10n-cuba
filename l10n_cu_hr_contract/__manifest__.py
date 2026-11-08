# List of contributors:
# Segu

{
     'name': 'Cuba - HR Contratos',
     'version': '18.0',
     'category': 'Human Resources',
     'summary': """
        Contratos de empleados, régimen de contribución.
     """,
     'description': 'Contratos de trabajadores - Cuba.',
     'author': 'Comunidad Cubana de Odoo',
     'depends': ['hr_contract'],
     'auto_install': True,
     'data': [
          'views/hr_contract_views.xml',
          'data/hr_contract_type_data.xml',
     ],
     'license': 'LGPL-3',
}
