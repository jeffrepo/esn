from odoo import api, fields, models, tools, _
import logging

class AccountMove(models.Model):
    _inherit = "account.move"

    def _post_reconcile_invoice_payment(self):
        invoice_ids = self.env["account.move"].search([("move_type","=", "out_invoice"),("state","=","draft")])
        if invoice_ids:
            for invoice in invoice_ids:
                invoice.action_post()
                payment_id = self.env["account.payment"].search([("amount","=", invoice.amount_total),("partner_id","=", invoice.partner_id.id),("state","=","posted"),("payment_type","=","inbound")])
                logging.warning(payment_id)
                if payment_id:
                    for pl in payment_id.move_id.line_ids.filtered(lambda r: r.account_id.account_type == 'asset_receivable' and not r.reconciled):
                        for il in invoice.line_ids.filtered(lambda r: r.account_id.account_type == 'asset_receivable' and not r.reconciled):
                            if (pl.debit == il.credit or pl.credit - linea_factura.debit ):
                                (pl | il).reconcile()
                                break
        return True