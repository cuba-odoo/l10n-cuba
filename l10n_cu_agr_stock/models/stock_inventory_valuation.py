# -*- coding: utf-8 -*-

from odoo import fields, models, tools
from odoo.addons import decimal_precision as dp
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class StockInventoryValuation(models.Model):
    _name = 'stock.inventory.valuation'
    _description = 'Wizard for select payload to inventory valuation'

    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    
    company_id = fields.Many2one('res.company', string='company')
    
    location_id = fields.Many2one('stock.location', string='Location', domain="[('usage','=','internal'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    
    stock_valuation_ids = fields.Many2many('stock.valuation.layer', string='Stock Valuation')
    
    line_ids = fields.One2many('stock.inventory.valuation.line', 'valuation_id', string='Lines')

    def action_search_info_stock(self):
        _logger.debug("action_search_info_stock")
        self.stock_valuation_ids = False
        filter = [
            "|",
            ('stock_move_id.location_id', 'in', self.location_id.ids),
            ('stock_move_id.location_dest_id', 'in', self.location_id.ids),
            "&",
            ('company_id', '=', self.company_id.id),
        ]
        if (self.date_from):
            filter.append(('create_date', '>=', self.date_from))
        if (self.date_to):
            filter.append(('create_date', '<=', self.date_to))
        
        
        _logger.debug(filter)
        res = super(StockInventoryValuation, self)
        valuation_ids = self.env['stock.valuation.layer'].search(filter)
        self.stock_valuation_ids = valuation_ids
        product_ids = self.stock_valuation_ids.mapped('product_id.id')
        _logger.debug(product_ids)
       
        update = []
        p_date = dict()
        sums = {
            'qty_started' : 0,
            'unit_cost_started' : 0,
            'qty_in' : 0,
            'unit_cost_in' : 0,
            'qty_out' : 0,
            'unit_cost_out' : 0,
            'qty_adjustment' : 0,
            'unit_cost_adjustment' : 0,
            'qty_real' : 0,
            'unit_cost_real' : 0,
        }
        items = dict()
        # 
             
        for val in valuation_ids:
            _logger.debug(val.product_id.display_name)
            _logger.debug(val.quantity)
            _logger.debug(val.value)
            
            if (val.product_id.id not in items.keys()):
                items[val.product_id.id] = {
                    'valuation_id' : self.id,
                    'product_id' : val.product_id.id,
                }
                p_date[val.product_id.id] = datetime.now()
                
                items[val.product_id.id].update(sums)
                _logger.debug(val.create_date)
                _logger.debug(p_date[val.product_id.id])

            if (val.create_date < p_date[val.product_id.id]):
                p_date[val.product_id.id] = val.create_date
                # items[val.product_id.id]['qty_started'] = items[val.product_id.id]['qty_real'] - items[val.product_id.id]['qty_in'] + items[val.product_id.id]['qty_out'] #+ items[val.product_id.id]['qty_adjustment']
                # items[val.product_id.id]['unit_cost_started'] = items[val.product_id.id]['unit_cost_real'] - items[val.product_id.id]['unit_cost_in'] + items[val.product_id.id]['unit_cost_out'] #+ items[val.product_id.id]['unit_cost_adjustment']
                items[val.product_id.id]['qty_started'] = abs(val.quantity)
                items[val.product_id.id]['unit_cost_started'] = abs(val.value)
                
            if val.stock_move_id.location_dest_id.usage == 'inventory' or val.stock_move_id.location_id.usage == 'inventory':
                items[val.product_id.id]['qty_adjustment'] += abs(val.quantity)
                items[val.product_id.id]['unit_cost_adjustment'] += abs(val.value)
            
            if (val.stock_move_id.location_id.usage == 'supplier'):
                items[val.product_id.id]['qty_in'] += abs(val.quantity)
                items[val.product_id.id]['unit_cost_in'] += abs(val.value)

            if (val.stock_move_id.location_dest_id.usage == 'customer'):
                items[val.product_id.id]['qty_out'] += abs(val.quantity)
                items[val.product_id.id]['unit_cost_out'] += abs(val.value)

            items[val.product_id.id]['qty_real'] += float(val.quantity)
            items[val.product_id.id]['unit_cost_real'] += float(val.value)

           
            
        products = self.env['product.product'].search([('id', 'not in', product_ids)])
        for p in products:
            items[p.id] = {
                'valuation_id' : self.id,
                'product_id' : p.id,
            }
            items[p.id].update(sums)


        for key in items.keys():
            line = items[key]
            update.append((0,0,line))
            
        res.update({'line_ids':update})
        return res
       
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



class StocInventoryValuationWizard(models.Model):
    _name = 'stock.inventory.valuation.line'
    _description = 'Stock inventory valuation line'
    
    valuation_id = fields.Many2one('stock.inventory.valuation', string='valuation')
    
    company_id = fields.Many2one('res.company', related='valuation_id.company_id')
    
    product_id = fields.Many2one('product.product', string='product')
    
    categ_id = fields.Many2one('product.category', related='product_id.categ_id')
    
    product_tmpl_id = fields.Many2one('product.template', related='product_id.product_tmpl_id')

    product_arancel_id = fields.Many2one('product.arancel', string='Partida arancelaria', related='product_id.product_arancel_id')
    
    uom_id = fields.Many2one(related='product_id.uom_id', readonly=True, required=True)
    
    qty_started = fields.Float('Qty Started')
    
    unit_cost_started = fields.Float('Unit Value Started', readonly=True)
    
    qty_in = fields.Float('Qty In')
    
    unit_cost_in = fields.Float('Unit Value In', readonly=True,
        digits=dp.get_precision('Product Price'))
    
    qty_out = fields.Float('Qty Out')
    
    unit_cost_out = fields.Float('Unit Value Out', readonly=True,
        digits=dp.get_precision('Product Price'))
        
    qty_adjustment = fields.Float('Qty adjustment')
    
    unit_cost_adjustment = fields.Float('Unit Value Adjustment', readonly=True,
        digits=dp.get_precision('Product Price'))
    
    qty_real = fields.Float('Qty Real')
    
    unit_cost_real = fields.Float('Unit Value', readonly=True,
        digits=dp.get_precision('Product Price'))
    
    description = fields.Char('Description')
    
