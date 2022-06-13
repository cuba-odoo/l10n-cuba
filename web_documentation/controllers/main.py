# Copyright 2020 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, http
from odoo.http import request


class WebsiteDocumentation(http.Controller):

    @http.route("/documentation/15.0", type='http', auth="public", methods=['GET'], website=True)
    def show_doc(self, **kw):
        return request.render("web_documentation.fiscal_localizations_15")
