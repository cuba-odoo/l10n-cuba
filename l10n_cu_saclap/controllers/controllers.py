# -*- coding: utf-8 -*-
# from odoo import http


# class L10nCuSaclap(http.Controller):
#     @http.route('/l10n_cu_saclap/l10n_cu_saclap/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/l10n_cu_saclap/l10n_cu_saclap/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('l10n_cu_saclap.listing', {
#             'root': '/l10n_cu_saclap/l10n_cu_saclap',
#             'objects': http.request.env['l10n_cu_saclap.l10n_cu_saclap'].search([]),
#         })

#     @http.route('/l10n_cu_saclap/l10n_cu_saclap/objects/<model("l10n_cu_saclap.l10n_cu_saclap"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('l10n_cu_saclap.object', {
#             'object': obj
#         })
