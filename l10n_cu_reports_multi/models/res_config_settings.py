from odoo import _, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    def action_refresh_all_financial_reports(self):
        """Recorre todos los account.financial.report de tipo 'accounts'
        y recalcula account_ids para todas las compañías del usuario."""
        companies = self.env.user.company_ids
        reports = self.env["account.financial.report"].search(
            [("type", "=", "accounts")]
        )

        updated = 0
        for report in reports:
            accounts = report._get_dynamic_accounts(companies=companies)
            report.account_ids = [(6, 0, accounts.ids)]
            updated += 1

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Estados financieros actualizados"),
                "message": _(
                    "Se actualizaron %(n)s reportes con las cuentas de %(c)s compañías."
                )
                % {"n": updated, "c": len(companies)},
                "type": "success",
                "sticky": False,
                "next": {"type": "ir.actions.act_window_close"},
            },
        }
