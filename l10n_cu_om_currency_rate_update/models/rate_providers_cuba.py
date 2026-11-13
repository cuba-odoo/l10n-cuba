from datetime import datetime, timezone
from urllib.parse import quote

import requests

from odoo.exceptions import UserError

from odoo.addons.om_currency_rate_update.models.rate_providers import (
    PROVIDERS,
    TIMEOUT,
    RateProvider,
)


# ---------------------------------------------------------------------------
# Proveedor: Banco Central de Cuba (BCC)
# ---------------------------------------------------------------------------
class BccProvider(RateProvider):
    """Tasas oficiales del BCC.

    El endpoint devuelve CUP por 1 unidad de moneda: ``"USD": 24`` significa
    1 USD = 24 CUP. Por eso la base es CUP y la tasa se invierte.
    Excepción: el JPY se publica al revés y se marca con ``(*)`` en el nombre.
    """

    code = "bcc"
    name = "Banco Central de Cuba"
    url = "https://api.bc.gob.cu/v1/tasas-de-cambio/activas"

    def fetch(self):
        data = self._get_json(self.url)
        tasas = data.get("tasas") if isinstance(data, dict) else None
        if not tasas:
            raise UserError(
                self.company.env._(
                    "%(provider)s no devolvió tasas.", provider=self.name
                )
            )

        variant = self.company.rate_bcc_tasa or "tasaOficial"
        day, rates = None, {}
        for tasa in tasas:
            if tasa.get("estado") and tasa["estado"] != "ACTIVA":
                continue
            code = tasa.get("codigoMoneda")
            value = tasa.get(variant)
            if not code or value is None:
                continue
            try:
                value = float(value)
            except (TypeError, ValueError):
                continue
            if value <= 0:
                continue

            inverted = "(*)" in (tasa.get("nombreMoneda") or "")
            rates[code] = value if inverted else 1.0 / value

            if day is None and tasa.get("fechaDia"):
                day = datetime.strptime(tasa["fechaDia"][:10], "%Y-%m-%d").date()

        if not rates:
            raise UserError(
                self.company.env._(
                    "%(p)s sin tasas para %(v)s.", p=self.name, v=variant
                )
            )
        return day or datetime.now(timezone.utc).date(), "CUP", rates


# ---------------------------------------------------------------------------
# Proveedor: El Toque (TRMI — tasa informal)
# ---------------------------------------------------------------------------
class ElToqueProvider(RateProvider):
    """Tasa Representativa del Mercado Informal (TRMI) de El Toque.

    - Endpoint: ``GET https://tasas.eltoque.com/v1/trmi?date_from=...&date_to=...``
    - Requiere token Bearer (registro gratuito en dev.eltoque.com).
    - La respuesta es ``{"tasas": {"USD": 490.0, "ECU": 540.0, ...}}``
      donde los valores están en **CUP por 1 unidad** de la moneda.
    - El Toque usa ``ECU`` para el euro; se mapea a ``EUR``.
    """

    code = "eltoque"
    name = "El Toque (TRMI)"
    needs_key = True
    key_field = "rate_eltoque_token"
    url = "https://tasas.eltoque.com/v1/trmi"

    def _get_json(self, url, headers=None, **params):
        """Igual que el del módulo base pero acepta cabeceras (Authorization)."""
        try:
            response = requests.get(
                url,
                params=params,
                headers=headers or {},
                timeout=TIMEOUT,
            )
        except requests.RequestException as error:
            raise UserError(
                self.company.env._(
                    "%(provider)s could not be reached: %(error)s",
                    provider=self.name,
                    error=self._hide_key(str(error)),
                )
            ) from error

        if response.status_code == 401:
            raise UserError(
                self.company.env._("El Toque: token inválido o caducado (HTTP 401).")
            )

        try:
            return response.json()
        except ValueError as error:
            raise UserError(
                self.company.env._(
                    "%(provider)s answered with an unexpected"
                    " response (HTTP %(status)s).",
                    provider=self.name,
                    status=response.status_code,
                )
            ) from error

    def fetch(self):
        token = self._get_key()
        if not token:
            raise UserError(
                self.company.env._("Introduce el token de El Toque en los ajustes.")
            )

        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        date_from = quote(f"{today} 00:00:01", safe="")
        date_to = quote(f"{today} 23:59:01", safe="")
        url = f"{self.url}?date_from={date_from}&date_to={date_to}"

        data = self._get_json(
            url,
            headers={"Authorization": f"Bearer {token}"},
        )

        tasas = data.get("tasas") if isinstance(data, dict) else None
        if not tasas:
            raise UserError(
                self.company.env._(
                    "%(provider)s no devolvió tasas.", provider=self.name
                )
            )

        mapping = {"ECU": "EUR"}
        rates = {}
        for code, value in tasas.items():
            code = mapping.get(code, code)
            try:
                value = float(value)
            except (TypeError, ValueError):
                continue
            if value > 0:
                rates[code] = 1.0 / value  # CUP por unidad -> unidades por CUP

        day = None
        if data.get("date"):
            try:
                day = datetime.strptime(data["date"], "%Y-%m-%d").date()
            except ValueError:
                return
        return day or datetime.now(timezone.utc).date(), "CUP", rates


# ---------------------------------------------------------------------------
# Registro de ambos proveedores
# ---------------------------------------------------------------------------
PROVIDERS[BccProvider.code] = BccProvider
PROVIDERS[ElToqueProvider.code] = ElToqueProvider
