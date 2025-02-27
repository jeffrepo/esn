from odoo import api, fields, models, tools, _
from datetime import date
import logging

class AccountMove(models.Model):
    _inherit = "account.move"

    def _update_invoice_dates(self):
        invoice_ids = self.env["account.move"].sudo().search([("move_type","=","out_invoice"),("state","=","draft"),("company_id","=",1)])
        if invoice_ids:
            for invoice in invoice_ids:
                if invoice.line_ids[0].sale_line_ids:
                    invoice.write({"invoice_date": invoice.line_ids[0].sale_line_ids.order_id.date_order.date()})
        return True
        
    def _post_reconcile_invoice_payment(self):
        invoice_ids = self.env["account.move"].sudo().search([("move_type","=","out_invoice"),("state","=","draft"),("company_id","=",1)],limit=2000)
        logging.warning(len(invoice_ids))
        if invoice_ids:
            contador = 0
            for invoice in invoice_ids:
                invoice.write({"invoice_date": invoice.line_ids[0].sale_line_ids.order_id.date_order.date()})
                invoice.action_post()
                payment_id = self.env["account.payment"].sudo().search([("partner_id","=", invoice.partner_id.id),("state","=","posted"),("ref","=", invoice.invoice_origin), ("company_id","=",1)])
                contador += 1
                logging.warning(contador)
                if payment_id:
                    for pl in payment_id.move_id.line_ids.filtered(lambda r: r.account_id.account_type == 'asset_receivable' and not r.reconciled):
                        for il in invoice.line_ids.filtered(lambda r: r.account_id.account_type == 'asset_receivable' and not r.reconciled):
                            if (pl.debit == il.credit or pl.credit - linea_factura.debit ):
                                (pl | il).reconcile()
                                break
            return True
