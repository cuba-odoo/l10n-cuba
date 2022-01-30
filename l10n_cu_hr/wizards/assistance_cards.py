from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import fields, models, api,_

class HrAssistanceCardsWizard(models.TransientModel):
    _name = 'hr.assistance.cards.wizard'
    _description = 'Hr Assistance Cards Wizard'

    start_date = fields.Date("Start Date", default=lambda self: fields.Date.to_string(date.today().replace(day=1)),
                             required=True)
    end_date = fields.Date("End Date", required=True, default=lambda self: fields.Date.to_string(
                              (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()))

    def print_report(self, data = {}):
        data['start_date'] = self.start_date
        data['end_date'] = self.end_date
        return self.env.ref('l10n_cu_hr.action_report_report_assistance_cards').report_action(self, data=data)
