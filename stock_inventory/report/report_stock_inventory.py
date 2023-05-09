
from odoo import api, models, _
from odoo.exceptions import ValidationError


class ReportStockInvetory(models.AbstractModel):
    _name = 'report.stock_inventory.report_stock_inventory'

    # #@api.multi
    def _get_report_values(self, docids, data=None):
        docs = self.env['stock.inventory'].browse(docids)
        # if len(docs.filtered(lambda r: r.state != 'draft')):
        #     raise ValidationError(_(u'You have selected items that are not incoming stock picking'))
        return {
            'doc_ids': docs.ids,
            'doc_model': 'stock.inventory',
            'docs': docs,
            'orders': "id asc"
        }

