import ast

from odoo import fields, models


class AccountFinancialReport(models.Model):
    _inherit = "account.financial.report"

    account_domain = fields.Char(
        string="Dominio de Cuentas (Multi-Compañía)",
        help="Dominio Python para resolver las cuentas dinámicamente. "
        "Si se deja vacío se infiere de las cuentas ya cargadas.",
    )

    def _get_dynamic_accounts(self, companies=None):
        """Devuelve account.account para este reporte.
        :param companies: recordset de res.company. Si es None usa self.env.companies.
        """
        self.ensure_one()
        if self.type != "accounts":
            return self.account_ids

        if companies is None:
            companies = self.env.companies

        Account = self.env["account.account"]
        domain = None

        # 1) Dominio explícito
        if self.account_domain:
            try:
                domain = ast.literal_eval(self.account_domain)
                if not isinstance(domain, list):
                    domain = None
            except (ValueError, SyntaxError):
                domain = None

        # 2) Inferido de los códigos ya cargados
        if domain is None:
            codes = sorted(set(self.account_ids.mapped("code")))
            if not codes:
                return self.account_ids
            domain = []
            for i, code in enumerate(codes):
                if i:
                    domain.insert(0, "|")
                domain.append(("code", "=", code))

        # 3) Filtro por compañías
        if "company_ids" in Account._fields:  # Odoo 18
            domain = domain + [("company_ids", "in", companies.ids)]
        elif "company_id" in Account._fields:  # Odoo <= 17
            domain = domain + [
                "|",
                ("company_id", "=", False),
                ("company_id", "in", companies.ids),
            ]

        return Account.search(domain)

    def action_refresh_accounts(self):
        """Botón individual (en la ficha del reporte)."""
        for report in self:
            if report.type == "accounts":
                report.account_ids = [(6, 0, report._get_dynamic_accounts().ids)]
        return True
