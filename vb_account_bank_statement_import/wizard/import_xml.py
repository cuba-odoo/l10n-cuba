# -*- coding: utf-8 -*-

import os
from odoo import models, fields, api, tools, _
from odoo import exceptions
import base64
import xml.etree.ElementTree as ET
from dateutil import parser as dtparser
import pytz
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime


class AccountBankStatementImport(models.TransientModel):
    _inherit = 'account.bank.statement.import'

    import_f = fields.Binary(string='Archivo XML')
    import_file_name = fields.Char(string='Filename')

    @api.onchange('import_f')
    def _onchange_xml_file(self):
        """Validar que este correcto el xml"""
        if self.import_f:
            try:
                xmlfile = base64.b64decode(self.import_f)
            except Exception as e:
                raise exceptions.ValidationError("Error al decodificar el archivo")
            # tipo_xml = None
            # root = []
            try:
                root = ET.fromstring(xmlfile)
                tipo_xml = root.tag.split('}')[-1]
                # if root.tag.split('}')[0].find('/v4.3/') >= 0:
                #     doc_version = 4.3
            except Exception as e:
                # raise exceptions.ValidationError(e.message)
                raise exceptions.ValidationError(str(e))

            if tipo_xml is None:
                raise exceptions.ValidationError("No se pudo determinar el tipo de documento.")

        return False

    def import_file(self):
        xmlfile = base64.b64decode(self.import_f)
        root = ET.fromstring(xmlfile)

        header = root[1]
        footer = root[-1]

        balance_start_tag = header[4] #position 4 is tag importe
        balance_start = balance_start_tag.text

        balance_end_tag = footer[4] #position 4 is tag importe
        balance_end = balance_end_tag.text

        vals_list = []
        lines = root[2:-2]
        for line in lines:
            if line[0].text and line[3].text and line[4].text:
                sign = line[5].text == 'Db' and -1 or 1

                values = {
                    'date': datetime.strptime(str(line[0].text), "%d/%m/%Y"),
                    'payment_ref': line[3].text,
                    'ref': line[2].text,
                    'transaction_type': line[5].text,
                    'amount': float(line[4].text) * sign,
                    # 'currency_id': self.get_currency(field[5])
                }
                vals_list.append((0, 0, values))

        statement_vals = {
            'name': 'Extracto de ' + str(datetime.today().date()),
            'journal_id': self.env.context.get('active_id'),
            'line_ids': vals_list,
            'balance_start': balance_start,
            'balance_end_real': balance_end
        }
        statement_id = self.env['account.bank.statement'].create(statement_vals)

        return {
            'view_type': 'list',
            'res_id': statement_id.id,
            'view_mode': 'form',
            'res_model': 'account.bank.statement',
            'type': 'ir.actions.act_window'
        }

