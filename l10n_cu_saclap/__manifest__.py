# -*- coding: utf-8 -*-

# List of contributors:
# José Andrés Hernández Bustio <jbustio@gmail.com>

{
    'name': "Sistema Armonizado de Clasificación de Productos",

    'summary': """
        Este módulo aún no es funcional. Se encuentra en desarrollo""",

    'description': """
        Reglas Generales para la interpretación, la Nomenclatura y las Notas de Secciones, Capítulos y Subpartidas del Sistema Armanizado de Clasificación de Productos.
            - Resolución No. 67, del 25 de abril de 2016, del Jefe de la Oficina Nacional de Estadística e Información.
            - Resolución No. 5, del 8 de enero de 2018,
            - Resolución No. 84, del 24 de noviembre de 2020,
    """,

    'author': "JADIKA Soft, Comunidad cubana de Odoo",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Localization',
    'version': '14.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','product_harmonized_system','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/hs_code_menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
