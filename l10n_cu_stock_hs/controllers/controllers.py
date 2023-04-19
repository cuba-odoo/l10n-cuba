# -*- coding: utf-8 -*-
# from odoo import http


# class L10nCuStockHs(http.Controller):
#     @http.route('/l10n_cu_stock_hs/l10n_cu_stock_hs', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/l10n_cu_stock_hs/l10n_cu_stock_hs/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('l10n_cu_stock_hs.listing', {
#             'root': '/l10n_cu_stock_hs/l10n_cu_stock_hs',
#             'objects': http.request.env['l10n_cu_stock_hs.l10n_cu_stock_hs'].search([]),
#         })

#     @http.route('/l10n_cu_stock_hs/l10n_cu_stock_hs/objects/<model("l10n_cu_stock_hs.l10n_cu_stock_hs"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('l10n_cu_stock_hs.object', {
#             'object': obj
#         })
