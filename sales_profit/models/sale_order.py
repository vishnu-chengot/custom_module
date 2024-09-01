from odoo import api, fields, models
import json
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    @api.model
    def get_sale_order_info(self, orders):
        values = []        
        orders = self.env['sale.order'].sudo().search([('id', 'in', orders)])
        for order in orders:
            tax_totals_json=json.loads(order.tax_totals_json)
            margin,products = self.get_margin(order)
            invoices = self.get_inoices(order)
            values.append({'name':order.name,
                           'customer':order.partner_id.name,
                           'date_order':order.date_order,
                           'total':tax_totals_json,
                           'order_line': products,
                           'invoices': invoices,
                           'margin_value': 'True' if margin > 0 else 'False',
                           'margin': str(margin) + " " +order.currency_id.name,
                           'state' : order.state
                           })
        print("===========================================",values)
        return values
    

    def get_margin(self, order):
        margin = 0
        products = []
        for orderline in order.order_line:
            products.append({'name':orderline.product_id.name,
                             'qty':orderline.product_uom_qty,
                             'sale_price':  str(orderline.price_unit * orderline.product_uom_qty)+ " " + order.currency_id.name,
                             'cost':  str(orderline.product_id.standard_price * orderline.product_uom_qty)+ " " + order.currency_id.name,
                             'margin_value': 'True' if ((orderline.price_unit - orderline.product_id.standard_price) * orderline.product_uom_qty) > 0 else 'False',
                             'margin':  str((orderline.price_unit - orderline.product_id.standard_price) * orderline.product_uom_qty)+ " " + order.currency_id.name })
            margin = margin + ((orderline.price_unit - orderline.product_id.standard_price) * orderline.product_uom_qty)
        return margin,products
    
    def get_inoices(self, order):
        invoices = []
        for inv in order.invoice_ids:
            invoices.append({'name':inv.name,'state':'Paid' if inv.payment_state=='paid' else 'Partial','payments_due': str(inv.amount_residual) +" " + order.currency_id.name})
        if not invoices:
            return False
        return invoices