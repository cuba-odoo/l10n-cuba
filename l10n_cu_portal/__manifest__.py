{
    'name': "l10n_cu_portal",
    'summary': "Integración del portal con la dirección cubana",
    'description': """
    Módulo puente entre el Portal y la localización de dirección cubana.

    Este módulo garantiza que los usuarios del portal (clientes que acceden
    al sitio web bajo el grupo Portal) tengan sus formularios de dirección
    renderizados con los campos específicos cubanos proporcionados por
    l10n_cu_address (provincia, municipio, etc.), en lugar del layout de
    dirección genérico.

    Características principales:
    - Adapta las plantillas de dirección del portal para usar los campos
      de dirección cubanos.
    - Mantiene la experiencia del portal consistente para usuarios
      ubicados en Cuba.
    """,
    "author": "Idola Odoo Team, Comunidad cubana de Odoo",
    'category': '',
    'version': '1.0',
    'depends': ['base', 'portal', 'l10n_cu_address'],
    'data': [
        'views/portal_templates.xml',
    ],
    "assets": {
        'web.assets_frontend': [
            'l10n_cu_portal/static/src/**/*',
        ],
    },
    'installable': True,
    "auto_install": ['l10n_cu_address', 'portal'],
    "license": "AGPL-3",
}
