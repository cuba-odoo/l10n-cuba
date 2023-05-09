
from odoo import api, models, _
from odoo.exceptions import ValidationError


class ReportStockInvetoryValuation(models.AbstractModel):
    _name = 'report.l10n_cu_agr_stock.report_stock_inventory_valuation'

    # #@api.multi
    def _get_report_values(self, docids, data=None):
        docs = self.env['stock.inventory.valuation'].browse(docids)
        # if len(docs.filtered(lambda r: r.state != 'draft')):
        #     raise ValidationError(_(u'You have selected items that are not incoming stock picking'))
        return {
            'doc_ids': docs.ids,
            'doc_model': 'stock.inventory.valuation',
            'docs': docs,
            'orders': "id asc"
        }

