
from odoo import api, models, _
from odoo.exceptions import ValidationError


class ReportInvoice(models.AbstractModel):
    _name = 'report.l10n_cu_agr_account.report_agr_invoice'

    # #@api.multi
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.move'].browse(docids)
        # if len(docs.filtered(lambda r: r.state != 'draft')):
        #     raise ValidationError(_(u'You have selected items that are not incoming stock picking'))
        return {
            'doc_ids': docs.ids,
            'doc_model': 'account.move',
            'docs': docs,
            'orders': "invoice_date asc, number asc, id asc"
        }

