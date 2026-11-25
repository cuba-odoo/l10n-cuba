
# l10n-cuba
## Localización cubana para Odoo 20.0

### Migración en desarrollo

Se verificó la instalación de ocho módulos en una base nueva de Odoo 20. La actualización desde Odoo 19 y la generación de informes PDF y XLSX con datos contables siguen pendientes. El módulo de bancos requiere adaptar el catálogo a la API bancaria de Odoo 20. Contratos, ausencias y nómina requieren resolver las dependencias `hr_contract` y `hr_payroll`.

Repositorio de código del proyecto de localización cubana para el software de gestión integral Odoo. 

Mantenido por la Comunidad Cubana de Odoo (https://cco-web.odoo.com), con participación de entidades estatales miembros oficiales de la comunidad cubana de Odoo.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Addons disponibles
----------------
addon | versión | resumen
--- | --- | ---
[l10n_cu](l10n_cu/) | 20.0.1.0.0 | Contabilidad y localización base.
[l10n_cu_address](l10n_cu_address/) | 20.0.1.0.0 | Provincias y municipios cubanos.
[l10n_cu_banks](l10n_cu_banks/) | 20.0.1.0.0 | Catálogo de sucursales bancarias.
[l10n_cu_fiscal_year_closing](l10n_cu_fiscal_year_closing/) | 20.0.1.1.0 | Cierre de ejercicio fiscal.
[l10n_cu_hr](l10n_cu_hr/) | 20.0.1.0.0 | Recursos humanos.
[l10n_cu_hr_contract](l10n_cu_hr_contract/) | 20.0.1.0.0 | Contratos de empleados.
[l10n_cu_hr_holidays](l10n_cu_hr_holidays/) | 20.0.1.0.0 | Control de ausencias.
[l10n_cu_hr_payroll_enterprise](l10n_cu_hr_payroll_enterprise/) | 20.0.1.1.0 | Nómina cubana para Odoo Enterprise.
[l10n_cu_portal](l10n_cu_portal/) | 20.0.1.0.0 | Direcciones cubanas en el portal.
[l10n_cu_pos](l10n_cu_pos/) | 20.0.1.0.0 | Adaptaciones del punto de venta.
[l10n_cu_reports](l10n_cu_reports/) | 20.0.1.0.0 | Estados financieros según las Normas Cubanas de Información Financiera.
[l10n_cu_website_sale](l10n_cu_website_sale/) | 20.0.2.0.0 | Direcciones y municipios en la tienda.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Dependencias de informes

- `accounting_pdf_reports` de [Odoo Mates](https://github.com/odoomates/odooapps).
- `report_xlsx` de [OCA reporting-engine](https://github.com/OCA/reporting-engine).

## Licencias

Este repositorio esta bajo la licencia [GPL-3.0](LICENSE).

----

CCO,  o [Comunidad Cubana de Odoo ](https://cco-web.odoo.com), tiene como misión el soporte y desarrollo colaborativo de funcionalidades para Odoo con el fin de promover y diversificar su uso.

----

## Próximos cambios.

Desarrollo de módulos como Activos Fijos. y otros necesarios para el mejor control de las entidades y pymes del pais. Tambien se desarrolla los modulos de Tesorería y control del gasto del presupuesto segun las normas del MFP .para las UPs. 

## 2025
