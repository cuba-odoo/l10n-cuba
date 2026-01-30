# Cierre de Ejercicio Fiscal - Localización Cubana (Odoo 15 CE)

Módulo para automatizar el cierre contable anual según normas cubanas (Plan de Cuentas LC CCO).

## ✨ Características

- ✅ Carga automática de cuentas sugeridas (900xxxx para ingresos, 822xxxx para gastos)
- ✅ Selección múltiple de cuentas (como en otros reportes de Odoo)
- ✅ Cálculo automático de saldos en tiempo real
- ✅ Prevención de duplicados al agregar cuentas
- ✅ Generación de asiento único de cierre a cuenta 999000000 (Resultados)
- ✅ Historial completo de todos los cierres realizados
- ✅ Totalmente funcional en Odoo Community Edition
- ✅ Nombre del asiento descriptivo: "Cierre de Cuentas Nominales del año [año]"

## 📥 Instalación

1. Descarga el módulo y colócalo en tu carpeta de addons de Odoo (`/mnt/extra-addons/`)
2. Reinicia el servidor Odoo: `sudo service odoo restart`
3. Actualiza la lista de aplicaciones (Apps → 🔁)
4. Busca "Cierre de Ejercicio Fiscal" e instálalo

## 🚀 Uso

1. Ve a **Contabilidad → Configuración → Cierre de Ejercicio Fiscal**
2. Selecciona el ejercicio fiscal y fecha de cierre (por defecto: año anterior, 31/12)
3. Haz clic en **"Iniciar Cierre"**
4. En el formulario del cierre:
   - Haz clic en **"Cargar Cuentas Sugeridas"** para buscar automáticamente cuentas 900xxxx y 822xxxx
   - O haz clic en **"Agregar Cuentas"** para seleccionar manualmente varias cuentas a la vez
   - Ajusta la selección (marca/desmarca "Incluir" según necesites)
   - Haz clic en **"Calcular Saldos"** para ver los totales actualizados
   - Haz clic en **"Crear Asiento de Cierre"** para generar el asiento contable
5. El asiento se crea en el diario "Asientos varios" con referencia **"Cierre de Cuentas Nominales del año [año]"**

## 📊 Resultado Final

Al ejecutar el cierre contable con este módulo, obtendrás:

### ✅ Estado final de las cuentas
| Cuenta | Antes del cierre | Después del cierre | Estado |
|--------|------------------|---------------------|--------|
| **Cuentas de ingresos**<br>(900.xxxx / 900xxxx) | Saldo acumulado del año | **0.00 CUP** | ✅ Cerradas |
| **Cuentas de gastos**<br>(822.xxxx / 822xxxx) | Saldo acumulado del año | **0.00 CUP** | ✅ Cerradas |
| **Cuentas de gastos**<br>(855.xxxx / 855xxxx) | Saldo acumulado del año | **0.00 CUP** | ✅ Cerradas |
| **Cuenta de resultados**<br>(999.000000 / 999000000) | 0.00 CUP | **Utilidad/Pérdida neta** | ✅ Actualizada |

### 💡 Beneficios prácticos para contadores cubanos
- **⏱️ Ahorro de tiempo**: Cierre completo en menos de 2 minutos (vs. 30+ minutos manualmente)
- **✅ Precisión garantizada**: Elimina errores de cálculo y omisión de cuentas
- **🔍 Transparencia total**: Lista visible de todas las cuentas incluidas en el cierre
- **🔄 Reversibilidad segura**: Cancelación con un clic si se detecta error
- **📄 Auditoría simplificada**: Registro completo con fecha, usuario y detalle de cuentas

### 📋 Ejemplo práctico de cierre 2025


### ⚠️ Notas importantes post-cierre
1. **No es necesario "reabrir" cuentas**: Odoo gestiona automáticamente los saldos por período fiscal
2. **Reportes del nuevo año**: Al generar reportes para 2026, las cuentas nominales comenzarán desde cero automáticamente
3. **Histórico preservado**: Los movimientos del año 2025 permanecen accesibles para consultas y auditorías
4. **Cuenta 999.000000**: Acumulará resultados de todos los ejercicios hasta su distribución formal

## 📊 Estructura del asiento generado

| Cuenta | Débito | Crédito | Concepto |
|--------|--------|---------|----------|
| Todas cuentas de ingresos (900xxxx) | X | 0 | Cierre ingresos [año] |
| Todas cuentas de gastos (822xxxx) | 0 | X | Cierre gastos [año] |
| 999000000 - Resultados | Utilidad/Pérdida | | Resultado del ejercicio [año] |

## ⚠️ Notas importantes

- **No es necesario "reabrir" cuentas al año siguiente**: Odoo gestiona automáticamente los saldos por período
- El asiento de cierre **debe crearse una sola vez por ejercicio**
- Para anular el cierre: usa el botón "Cancelar cierre" (elimina el asiento generado)
- Si no existe la cuenta 999000000, créala manualmente en Contabilidad → Configuración → Plan de cuentas

## 🔧 Configuración recomendada

### Crear cuenta de resultados (si no existe)
1. Ve a **Contabilidad → Configuración → Plan de cuentas**
2. Haz clic en **Crear**
3. Rellena:
   - **Código**: `999000000`
   - **Nombre**: `Resultados`
   - **Tipo de cuenta**: `Patrimonio` (Equity)
   - **Compañía**: Tu compañía
4. Guarda

### Patrones de búsqueda de cuentas
El módulo busca automáticamente cuentas con estos patrones:
- **Ingresos**: `900%` y `900.%` (ej: 90000001, 900.000001)
- **Gastos**: `822%` y `822.%` (ej: 822005001, 822.005001)
- **Resultados**: `999%` (ej: 999000000, 999.000000)

## 🌐 Compatibilidad

- ✅ Odoo 15 Community Edition
- ✅ Plan de cuentas cubano LC de la CCO
- ✅ Cualquier configuración de cuentas (flexible)
- ✅ Multi-compañía
- ✅ Multi-moneda

## 📜 Licencia

LGPL-3 - Libre para uso, modificación y distribución en entornos Open Source.

## 👥 Contribuciones

¡Bienvenidas! Este módulo forma parte del proyecto de localización cubana de Odoo:
https://github.com/cuba-odoo/l10n-cu

### Cómo contribuir
1. Haz fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nombre-feature`)
3. Haz commit de tus cambios (`git commit -am 'Añadir feature'`)
4. Haz push a la rama (`git push origin feature/nombre-feature`)
5. Crea un Pull Request

## 🐛 Reportar errores

Si encuentras algún problema o tienes sugerencias de mejora, por favor:
1. Ve a https://github.com/cuba-odoo/l10n-cu/issues
2. Haz clic en "New Issue"
3. Describe el problema con detalle

## 📞 Soporte

Para soporte técnico o consultas:
- Email: scnetisla@gmail.com
- Telegram: https://t.me/odoodevcubacuba_odoo_comunidad @hcalvofernandez
- GitHub Discussions: https://github.com/cuba-odoo/l10n-cu/discussions

## 📱 Capturas de pantalla

### Interfaz principal del cierre
![Interfaz del módulo](https://i.imgur.com/placeholder1.png)

### Lista de cuentas con saldos
![Lista de cuentas](https://i.imgur.com/placeholder2.png)

### Asiento de cierre generado
![Asiento generado](https://i.imgur.com/placeholder3.png)

## 📚 Documentación adicional  ( en proceso)

- [Guía rápida de uso](docs/GUÍA_RÁPIDA.md)
- [Manual para contadores](docs/MANUAL_CONTADORES.md)
- [FAQ - Preguntas frecuentes](docs/FAQ.md)
- [Changelog](docs/CHANGELOG.md)

## 🙏 Agradecimientos

Este módulo fue desarrollado gracias a la colaboración de:
- Comunidad Cubana de Odoo
- ConLeyet SRL - Empresa de Privada, de Aplicaciones Informáticas y Servicios de Contabilidad
- Todos los contribuidores del proyecto l10n-cu

## 🇨🇺 Hecho con ❤️ para la comunidad cubana de Odoo

---

**Versión**: 15.0.1.1.0  
**Última actualización**: Enero 2026  
**Estado**: Producción - Estable