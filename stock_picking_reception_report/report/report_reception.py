
from odoo import api, models, _
from odoo.exceptions import ValidationError


class ReportReception(models.AbstractModel):
    _name = 'report.stock_picking_reception_report.report_reception'

    def _get_report_values(self, docids, data=None):
        docs = self.env['stock.reception.report'].browse(docids)
        if len(docs.filtered(lambda r: r.picking_type_id.code != 'incoming')):
            raise ValidationError(_(u'You have selected items that are not incoming stock picking'))
        return {
            'doc_ids': docs.ids,
            'doc_model': 'stock.reception.report',
            'docs': docs
        }

