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


class VbStatement:

    def __init__(self, statement):
        self.fecha = statement[0].text
        self.ref_corrie = statement[1].text
        self.ref_origin = statement[2].text
        self.observ = statement[3].text
        self.importe = statement[4].text
        self.tipo = statement[5].text

    def validate(self):
        """Este metodo sera el encargado de validad sintacticamente el xml."""
        pass

    def getFecha(self): return self.fecha

    def getFechaFormated(self):
        date = datetime.strptime(str(self.fecha), "%d/%m/%Y")
        return date

    def getRefCorriente(self): return self.ref_corrie

    def getRefOrigen(self): return self.ref_origin

    def getObservaciones(self): return self.observ

    def getImporte(self): return self.importe

    def getTipo(self): return self.tipo

    def getImporteByTipo(self):
        sign = self.getTipo() == 'Db' and -1 or 1
        return float(self.importe) * sign


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

            except Exception as e:
                # raise exceptions.ValidationError(e.message)
                raise exceptions.ValidationError(str(e))

            if tipo_xml is None:
                raise exceptions.ValidationError("No se pudo determinar el tipo de documento.")

        return False

    def import_file(self):
        xmlfile = base64.b64decode(self.import_f)
        root = ET.fromstring(xmlfile)

        statement_header = VbStatement(root[1])
        statement_footer = VbStatement(root[-1])

        vals_list = []
        lines = root[2:-2]
        for line in lines:
            statement = VbStatement(line)
            if statement.getFecha() and statement.getObservaciones() and statement.getImporte():
                values = {
                    'date': statement.getFechaFormated(),
                    'payment_ref': statement.getObservaciones(),
                    'ref': statement.getRefOrigen(),
                    'transaction_type': statement.getTipo(),
                    'amount': statement.getImporteByTipo()

                }
                vals_list.append((0, 0, values))

        statement_vals = {
            'name': 'Extracto de ' + str(datetime.today().date()),
            'journal_id': self.env.context.get('active_id'),
            'line_ids': vals_list,
            'balance_start': statement_header.getImporte(),
            'balance_end_real': statement_footer.getImporte()
        }
        statement_id = self.env['account.bank.statement'].create(statement_vals)

        return {
            'res_id': statement_id.id,
            'view_mode': 'form',
            'res_model': 'account.bank.statement',
            'type': 'ir.actions.act_window'
        }
