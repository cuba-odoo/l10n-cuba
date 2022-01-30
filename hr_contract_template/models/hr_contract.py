# -*- coding: utf-8 -*-
from odoo import fields, models, api

class HrContract(models.Model):
    _inherit = 'hr.contract'

    contract_template_id = fields.Many2one("hr.contract.template", "Contract Template")
    print_template = fields.Boolean("Print Template", default=0)

    @api.onchange("contract_template_id")
    def onchange_contract_template(self):
        if self.contract_template_id:
            self.job_id = self.contract_template_id.name and self.contract_template_id.name.id
            self.struct_id = self.contract_template_id.struct_id and self.contract_template_id.struct_id.id
            # self.department_id = self.contract_template_id.department_id and self.contract_template_id.department_id.id
            self.journal_id = self.contract_template_id.journal_id and self.contract_template_id.journal_id.id
            self.wage = self.contract_template_id.wage