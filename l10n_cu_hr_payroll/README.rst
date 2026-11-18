===================================
Cuba - Nóminas (l10n_cu_hr_payroll)
===================================

Módulo de nóminas para Cuba que extiende ``om_hr_payroll`` con las
estructuras, reglas salariales, proyecciones y reportes que exige la
legislación cubana vigente.

Configuración inicial
=====================

**Salario mínimo (CUP)**

En ``Ajustes → Nóminas → Salario mínimo`` o mediante el parámetro del
sistema ``l10n_cu_hr_payroll.default_min_salary``.

- Valor por defecto: **3210 CUP**
- Se usa como base de ``SALARIO_MINIMO`` y como piso de ``FTE``.
- Al instalarse el módulo se crea el ``ir.config_parameter`` con valor
  ``3210``. El admin puede modificarlo en cualquier momento.

Dependencias
============

- ``l10n_cu_hr`` — localización base de RR.HL cubana.
- ``l10n_cu_hr_contract`` — campos del contrato cubano
  (``regimen_contribution``, ``multi_job``, etc.).
- ``om_hr_payroll`` — motor de nóminas base de Odoo Mates.

Estructuras salariales
======================

El módulo crea las siguientes estructuras:

.. list-table::
   :header-rows: 1

   * - Nombre
     - Código
     - Aplica a
   * - Operativos determinados
     - ``OPERATIVAS``
     - Trabajadores operativos con contrato determinado
   * - Administrativos determinados
     - ``ADMINISTRATIVAS``
     - Administrativos con contrato determinado
   * - Operativas indeterminados
     - ``OPERATIVAS_INDETERMINADOS``
     - Operativos con contrato indefinido (incluye asignaciones)
   * - Administrativas indeterminados
     - ``ADMINISTRATIVAS_INDETERMINADOS``
     - Administrativos con contrato indefinido (incluye asignaciones)
   * - Nóminas ejecutivas
     - ``EJECUTIVAS``
     - Socios (nómina mensual)
   * - Nóminas ejecutivas anual
     - ``EJECUTIVAS ANUAL``
     - Socios (nómina anual)
   * - Utilidad
     - ``UTILIDAD``
     - Cualquier empleado (pago de utilidades)

Todas heredan de ``om_hr_payroll.structure_base`` (que el módulo
sobreescribe para dejar solo ``WORK100`` y ``NET``).

Reglas salariales — trabajadores
================================

Aplican a las estructuras ``OPERATIVAS``, ``ADMINISTRATIVAS`` y sus
variantes indeterminadas.

``BASIC`` — Salario básico
--------------------------

- **Fórmula:** ``result = contract.wage``
- **Base:** salario mensual del contrato.
- **Categoría:** BASIC

``WORK100`` — Días trabajados
-----------------------------

- **Fórmula:** ``result = worked_days.WORK100.number_of_days``
- **Base:** días efectivamente trabajados en el período.
- **Categoría:** OTROS (no afecta al neto directamente).

``SALARIO_MINIMO`` — Salario mínimo
-----------------------------------

- **Fórmula:**

  .. code-block:: python

     param = payslip.env['ir.config_parameter'].sudo().get_param(
         'l10n_cu_hr_payroll.default_min_salary')
     result = float(param) if param else 3210.0

- **Base:** parámetro del sistema (default ``3210`` CUP).
- **Categoría:** BASIC
- **Aparece en nómina:** No (regla auxiliar).

``GROSS`` — Bruto (``hr_rule_taxable``)
---------------------------------------

- **Fórmula:** ``result = (BASIC / 24) * WORK100``
- **Base:** ``BASIC`` prorrateado por días trabajados asumiendo un
  **mes laboral de 24 días**.
- **Categoría:** GROSS

``BASE_IMPOSITIVA_SS`` — Base imponible de SS
---------------------------------------------

- **Fórmula:**

  .. code-block:: python

     if contract.multi_job:
         result = 0
     else:
         regimen = contract.regimen_contribution and int(...)
         gross = regimen or GROSS
         result = gross + categories.ALW

- **Base:**
  - ``0`` si el empleado tiene más de un empleo (``multi_job``).
  - ``regimen_contribution`` si es numérico.
  - ``GROSS + ALW`` en otro caso.
- **Categoría:** BASIC
- **Aparece en nómina:** No (regla auxiliar).

``FTE`` — Utilización fuerza de trabajo
---------------------------------------

- **Fórmula:**

  .. code-block:: python

     if GROSS:
         result = (SALARIO_MINIMO if GROSS <= SALARIO_MINIMO else GROSS) * 0.05
     else:
         result = 0

- **Base:** ``max(GROSS, SALARIO_MINIMO) × 5%``
- **Categoría:** COMP (contribución empresa).

``IPT`` — Impuesto sobre ingresos personales
--------------------------------------------

- **Fórmula:** escala progresiva de dos tramos sobre
  ``salary = GROSS + ALW``:

  .. list-table::
     :header-rows: 1

     * - Tramo
       - Rango (mensual)
       - Tasa
     * - Exento
       - hasta 3,260
       - 0%
     * - Tramo 1
       - 3,260 – 9,510
       - 3%
     * - Tramo 2
       - > 9,510
       - 5% sobre excedente

  .. code-block:: python

     MIN_EXENTO = 3260
     if salary <= 3260:        result = 0
     elif salary <= 9510:      result = (salary - 3260) * 0.03
     else:                     result = (9510 - 3260) * 0.03 + (salary - 9510) * 0.05

- **Base:** ``GROSS + ALW``
- **Categoría:** DED (deducción al trabajador).
- **Nota:** Se paga dentro de los 10 primeros días hábiles del mes.

``PROVISIONES_VACACIONES`` — Provisiones de vacaciones
------------------------------------------------------

- **Fórmula:** ``result = GROSS * 0.0909``
- **Base:** 9.09% del bruto (≈ 1/11 → 1 mes de vacaciones por 11
  trabajados, asumiendo 24 días laborables).
- **Categoría:** PROV_PRESTACIONES_COMP (pasivo empresa).

``SSE`` — Seguridad Social Empresa
----------------------------------

- **Fórmula:** ``result = GROSS * 0.125``
- **Base:** 12.5% del bruto.
- **Categoría:** COMP (contribución empresa).

``PRESTACIONESE`` — Prestaciones sociales corto plazo
-----------------------------------------------------

- **Fórmula:** ``result = GROSS * 0.015``
- **Base:** 1.5% del bruto.
- **Categoría:** PROV_PRESTACIONES_COMP (pasivo empresa).

``SS_ESPECIALT`` — Seguridad Social Especial
--------------------------------------------

- **Fórmula:** ``result = BASE_IMPOSITIVA_SS * 0.05``
- **Base:** 5% de la base imponible de SS.
- **Categoría:** DED (deducción al trabajador).

``ASIG_VACACIONES`` — Asignación manual de vacaciones
-----------------------------------------------------

- **Fórmula:** ``result = inputs.ASIG_VACACIONES.amount``
- **Base:** monto ingresado en ``hr.payroll.other.input`` con código
  ``ASIG_VACACIONES``.
- **Categoría:** ALW (asignación).

``ASIG_PROVISIONES`` — Asignación manual de provisiones
-------------------------------------------------------

- **Fórmula:** ``result = inputs.ASIG_PROVISIONES.amount``
- **Categoría:** ALW.

``UTILIDAD`` — Utilidad
-----------------------

- **Fórmula:** ``result = inputs.UTILIDAD.amount``
- **Categoría:** ALW.

``TD`` — Total deducciones
--------------------------

- **Fórmula:** ``result = categories.DED``
- **Base:** suma de todas las deducciones.

``NET`` — Neto
--------------

- **Fórmula:** ``result = categories.GROSS + categories.ALW - categories.DED``
- **Base:** bruto + asignaciones − deducciones.

Reglas salariales — socios
==========================

Aplican a las estructuras ``EJECUTIVAS`` y ``EJECUTIVAS ANUAL``.

``GROSS`` — Salario bruto del socio (``hr_rule_socio_taxable``)
---------------------------------------------------------------

- **Fórmula:** ``result = contract.wage``
- **Base:** salario mensual del socio (sin prorrateo por días).
- **Categoría:** GROSS.

``IMPUESTO_DA`` — Impuesto dividendos anticipados
-------------------------------------------------

- **Fórmula:** ``result = GROSS * 0.05``
- **Base:** 5% del bruto (anticipo).
- **Categoría:** DED.
- **Nota:** Exento en el primer año.

``CE_SS`` — Contribución especial SS
------------------------------------

- **Fórmula:** ``result = BASE_IMPOSITIVA_SS * 0.20``
- **Base:** 20% de la base imponible.
- **Categoría:** DED.

``CE_SS_CP`` — Contribución especial SS Corto Plazo
---------------------------------------------------

- **Fórmula:** ``result = CE_SS * 0.015``
- **Base:** 1.5% **de la contribución** ``CE_SS``.
- **Categoría:** DED.

``TPCD`` — Total retiros a cuenta de dividendos
-----------------------------------------------

- **Fórmula:**

  .. code-block:: python

     yf = str(payslip.date_from.year) + '-01-01'
     yt = str(payslip.date_from.year) + '-12-31'
     result = payslip.env['hr.payslip.line'].get_rule_balance(
         'GROSS', employee, yf, yt)

- **Base:** suma de todos los ``GROSS`` del empleado en nóminas
  ``done`` del **año fiscal** del slip.
- **Categoría:** OTROS.

``TPAIP`` — Total tributos anticipados
--------------------------------------

- **Fórmula:**

  .. code-block:: python

     yf = str(payslip.date_from.year) + '-01-01'
     yt = str(payslip.date_from.year) + '-12-31'
     result = payslip.env['hr.payslip.line'].get_rule_balance(
         'IMPUESTO_DA', employee, yf, yt)

- **Base:** suma de todos los ``IMPUESTO_DA`` del año fiscal.
- **Categoría:** OTROS.

Escala progresiva de socios (``T1S`` .. ``T5S``)
------------------------------------------------

Cada regla calcula **solo su tramo**. Son incrementales.

.. list-table::
   :header-rows: 1

   * - Regla
     - Rango (anual)
     - Tasa
     - Fórmula
   * - ``T1S``
     - 39,120 – 75,000
     - 3%
     - ``(min(total, 75000) - 39120) * 0.03``
   * - ``T2S``
     - 75,000 – 150,000
     - 5%
     - ``(min(total, 150000) - 75000) * 0.05``
   * - ``T3S``
     - 150,000 – 250,000
     - 10%
     - ``(min(total, 250000) - 150000) * 0.10``
   * - ``T4S``
     - 250,000 – 350,000
     - 15%
     - ``(min(total, 350000) - 250000) * 0.15``
   * - ``T5S``
     - > 350,000
     - 20%
     - ``(total - 350000) * 0.20``

Donde ``total = TPCD``.

``IPAS`` — Impuesto anual de socios
-----------------------------------

- **Fórmula:** ``result = (T1S + T2S + T3S + T4S + T5S) - TPAIP``
- **Base:** suma de los 5 tramos menos los anticipos.
- **Categoría:** DED.

Parámetros del sistema
======================

.. list-table::
   :header-rows: 1

   * - Clave
     - Valor por defecto
     - Dónde se configura
   * - ``l10n_cu_hr_payroll.default_min_salary``
     - ``3210``
     - Ajustes → Nóminas → Salario mínimo

Flujo de cálculo — estructura OPERATIVA / ADMINISTRATIVA
========================================================

.. code-block:: text

   1. BASIC              = contract.wage
   2. WORK100            = días trabajados
   3. SALARIO_MINIMO     = 3210 (config)
   4. GROSS              = (BASIC / 24) × WORK100
   5. BASE_IMPOSITIVA_SS = GROSS + ALW
   6. PROVISIONES_VAC    = GROSS × 9.09%
   7. IPT                = escala 3,260 / 9,510
   8. SS_ESPECIALT       = BASE_IMPOSITIVA_SS × 5%
   9. SSE                = GROSS × 12.5%
   10. PRESTACIONESE     = GROSS × 1.5%
   11. FTE               = max(GROSS, SALARIO_MINIMO) × 5%
   12. TD                = suma de DED
   13. NET               = GROSS + ALW − DED

Flujo de cálculo — estructura EJECUTIVA (mensual)
=================================================

.. code-block:: text

   1. GROSS              = contract.wage
   2. BASE_IMPOSITIVA_SS = GROSS + ALW
   3. IMPUESTO_DA       = GROSS × 5%
   4. CE_SS              = BASE_IMPOSITIVA_SS × 20%
   5. CE_SS_CP           = CE_SS × 1.5%
   6. TD                 = suma de DED
   7. NET                = GROSS − DED

Flujo de cálculo — estructura EJECUTIVA ANUAL
=============================================

.. code-block:: text

   1. TPCD   = Σ GROSS del año fiscal
   2. TPAIP  = Σ IMPUESTO_DA del año fiscal
   3. T1S..T5S = tramos progresivos sobre TPCD
   4. IPAS   = (T1S + T2S + T3S + T4S + T5S) − TPAIP
   5. TD     = suma de DED

Proyecciones
============

El módulo añade el modelo ``hr.payslip.projection`` para proyectar
salarios anuales por empleado.

- **Modelo:** ``hr.payslip.projection``
- **Líneas:** ``hr.payslip.projection.line`` (una por código de regla,
  con 12 columnas ``enero``..``diciembre``).
- **Wizard:** ``hr.payslip.projection.wizard`` (menú
  ``Nóminas → Reportes → Ejecutar Proyecciones``).
- **Lógica:** suma las nóminas ``done`` de la compañía activa en el
  rango seleccionado, las agrupa por empleado y regla, y escribe los
  totales en el mes correspondiente a ``date_from``.

Restricción: ``unique(employee_id, start_date, end_date)`` — un
empleado puede tener varias proyecciones (una por período).

Reportes
========

- **Nóminas** (``report.l10n_cu_hr_payroll.report_payslip``):
  tabla de todas las nóminas de un ``hr.payslip.run`` con columnas por
  categoría (BASIC, BRUTO, DED, ALW, NET).
- **Proyecciones** (``report.l10n_cu_hr_payroll.report_payslip_projection``):
  tabla anual por empleado y regla.

Wizards
=======

- ``hr.payslip.projection.wizard`` — genera la proyección anual.

Modelos extendidos
==================

- ``hr.employee`` — añade ``other_input_id`` (One2many a
  ``hr.payroll.other.input``).
- ``hr.payslip`` — añade ``total`` y ``total_on_payable``; sobreescribe
  ``refund_sheet``, ``action_payslip_done``, ``compute_sheet``,
  ``get_inputs``.
- ``hr.payslip.line`` — añade ``get_rule_balance`` (suma de una regla
  en nóminas confirmadas, con filtro opcional por fechas).
- ``hr.payslip.run`` — añade ``qty_payslip``, ``total`` y el botón
  "Calcular Hoja" (solo recalcula nóminas en ``draft``).
- ``res.config.settings`` — añade ``min_salary``.

Inputs adicionales (``hr.payroll.other.input``)
===============================================

Permite inyectar montos manuales al empleado:

.. list-table::
   :header-rows: 1

   * - Código
     - Regla que lo consume
   * - ``ASIG_VACACIONES``
     - ``ASIG_VACACIONES``
   * - ``ASIG_PROVISIONES``
     - ``ASIG_PROVISIONES``
   * - ``UTILIDAD``
     - ``UTILIDAD``

El rango de vigencia (``start_date``/``end_date``) es opcional. Si se
omite, el monto aplica a cualquier período.

Aspectos técnicos a validar con especialistas
=============================================

Los siguientes puntos están implementados pero **no han sido confirmados
por un contador o asesor fiscal**. Antes de usar el módulo en producción
se recomienda revisarlos:

1. **Mes laboral de 24 días** en ``GROSS``. ¿Aplica a todos los
   regímenes?
2. **5% de FTE**. ¿Es correcto? ¿Con piso en ``SALARIO_MINIMO``?
3. **3,260 / 9,510** en ``IPT``. ¿Mensual o anual? ¿Marginal o plano?
4. **9.09%** en provisiones de vacaciones. ¿24 días laborables o 20?
5. **12.5% empresa + 5% trabajador** en SS. ¿Vigente?
6. **1.5%** en prestaciones sociales corto plazo. ¿Adicional al 12.5%
   o incluido?
7. **20%** en ``CE_SS`` de socios. ¿O es el 17.5% general?
8. **1.5% de ``CE_SS_CP``**. ¿Debe ser sobre ``CE_SS`` o sobre
   ``BASE_IMPOSITIVA_SS``?
9. **Escala anual de socios** (39,120 / 75,000 / 150,000 / 250,000 /
   350,000 con tasas 3/5/10/15/20%). ¿Vigente y correcta?
10. **Salario mínimo 3210 CUP**. ¿Vigente a la fecha?
11. Si ``IPAS < 0`` (saldo a favor del socio), ¿se devuelve o se
    arrastra al próximo año?
12. ¿Faltan deducciones? (cuota sindical, embargos, préstamos,
    pagos en especie).

Historial de cambios
====================

18.0 (2026-11)
--------------

- Corrección de ``ImportError`` en ``wizard/__init__.py``.
- Corrección de ``models/__init__.py`` (orden de imports).
- ``hr.payslip.refund_sheet``: usa ``super().refund_sheet()``.
- ``hr.payslip.action_payslip_done``: no crea asignaciones de
  vacaciones en rectificativas.
- ``hr.payslip.get_inputs``: filtra fechas con ``search`` de Odoo
  (``False`` en lugar de ``None``).
- ``hr.payslip.run.calculate_slips_total``: solo recalcula nóminas
  en ``draft``.
- ``hr.payslip.line.get_rule_balance``: acepta ``date_from``/``date_to``.
- ``hr.projection``: constraint ``unique(employee_id, start_date, end_date)``.
- Reglas salariales: ``int(regimen_contribution)`` defensivo, escala
  progresiva de socios reescrita (incremental), ``TPCD``/``TPAIP``
  filtran por año fiscal.
- CSV migrado a XML (``hr_salary_rule.xml``).
- Salario mínimo por defecto: **3210 CUP**.
- README.rst con documentación completa de la lógica de cálculo.

Autores
=======

- Comunidad Cubana de Odoo
- Contribuidor: Segu

Licencia
========

LGPL-3
