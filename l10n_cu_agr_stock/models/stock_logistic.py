# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class StockLogistic(models.Model):
    _name = 'stock.logistic'
    _descriptions = "logistical data of the picking"

    NoBultos = fields.Integer('No Bultos', help='Cantidad de Bultos recibidos')
    NoLevante = fields.Char('No Levante', help='No del levante que da la Aduana')
    TipoDeclaracion = fields.Selection(selection=[('parcial', 'Parcial'), ('total', 'Total')],
                                       string='Tipo Declaracion',
                                       help='Tipo de Declaracion Parcial/Total', default='total')
    NoContenedor = fields.Char('No Contenedor')
    NoBl = fields.Char('No BL')
    NoGa = fields.Char('No GA', help='No  de Guia Aerea si aplica')
    NoRemisionEntrada = fields.Char('No Remision Entrada', copy=False, help='No Remision de entrada')
    FactProveedor = fields.Char('Fact. Proveedor', copy=False, help='No Factura de Proveedor')
    NotaInfRecepcion = fields.Text('Nota', help='Nota adicional para Informe de Recepcion')

    # picking_ids = fields.One2many('stock.picking', 'logistic_id', string='Picking ID', ondelete='cascade')
    receptionreport_ids = fields.One2many('stock.reception.report', 'logistic_id', string='Reception Report ID',
                                          ondelete='cascade')

    _sql_constraints = [
        ('NoRemisionEntrada_uniq', 'UNIQUE("NoRemisionEntrada")',
         'A No Remision Entrada can only be assigned to one picking !'),
    ]


class StockReceptionReport(models.Model):
    _inherit = 'stock.reception.report'

    logistic_id = fields.Many2one('stock.logistic',
                                  string='Logistic', delegate=True,
                                  ondelete='cascade',
                                  help='Select logistic data for this picking')


# class StockPicking(models.Model):
#     _inherit = 'stock.picking'
#
#     logistic_id = fields.Many2one('stock.logistic',
#                                   string='Logistic', delegate=True,
#                                   ondelete='cascade',
#                                   help='Select logistic data for this picking')


class ProductArancel(models.Model):
    _inherit = 'product.arancel'

    stock_move_ids = fields.One2many('stock.move', 'product_arancel_id', string='Arancel')


class StockMove(models.Model):
    _inherit = 'stock.move'

    product_arancel_id = fields.Many2one('product.arancel', related='product_tmpl_id.product_arancel_id', store=True)


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    code_num = fields.Char('Código', help='Código númerico del Depósito')


# class Incoterms(models.Model):
#     _inherit = 'stock.incoterms'

#     # #@api.multi
#     def name_get(self):
#             return [(record.id, "%s" % record.code) for record in self]