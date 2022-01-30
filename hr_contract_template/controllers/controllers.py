# -*- coding: utf-8 -*-
# from odoo import http


# class L10nCuContractTemplate(http.Controller):
#     @http.route('/l10n_cu_contract_template/l10n_cu_contract_template/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/l10n_cu_contract_template/l10n_cu_contract_template/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('l10n_cu_contract_template.listing', {
#             'root': '/l10n_cu_contract_template/l10n_cu_contract_template',
#             'objects': http.request.env['l10n_cu_contract_template.l10n_cu_contract_template'].search([]),
#         })

#     @http.route('/l10n_cu_contract_template/l10n_cu_contract_template/objects/<model("l10n_cu_contract_template.l10n_cu_contract_template"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('l10n_cu_contract_template.object', {
#             'object': obj
#         })
