{
    "name": "Cuba - Reportes Multi-Compañía",
    "version": "18.0.1.0.0",
    "category": "Accounting/Localizations",
    "summary": "Resuelve dinámicamente las cuentas de account.financial.report "
    "para múltiples compañías + botón de refresco en Ajustes.",
    "author": "Comunidad Cubana de Odoo",
    "depends": [
        "accounting_pdf_reports",
        "l10n_cu_reports",
    ],
    "data": [
        "data/account_financial_report_es_data.xml",
        "data/account_financial_report_er_data.xml",
        "data/account_financial_report_domain_evab_data.xml",
        "views/account_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "license": "LGPL-3",
    "installable": True,
}
