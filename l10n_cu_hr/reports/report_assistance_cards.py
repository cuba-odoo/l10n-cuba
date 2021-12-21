# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class AssistanceCard(models.AbstractModel):
    _name = 'report.l10n_cu_hr.report_assistance_cards'

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        report_obj = self.env['ir.actions.report']
        report = report_obj._get_report_from_name('l10n_cu_hr.report_assistance_cards')

        docargs = {
            # 'doc_ids': docids,
            'doc_model': report.model,
            'data': data,
            'docs': docs,
            # 'lines': self.lines,
        }
        return docargs