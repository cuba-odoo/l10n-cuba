# -*- coding: utf-8 -*-
# from odoo import http


# class L10nCuStock(http.Controller):
#     @http.route('/l10n_cu_stock/l10n_cu_stock', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/l10n_cu_stock/l10n_cu_stock/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('l10n_cu_stock.listing', {
#             'root': '/l10n_cu_stock/l10n_cu_stock',
#             'objects': http.request.env['l10n_cu_stock.l10n_cu_stock'].search([]),
#         })

#     @http.route('/l10n_cu_stock/l10n_cu_stock/objects/<model("l10n_cu_stock.l10n_cu_stock"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('l10n_cu_stock.object', {
#             'object': obj
#         })
