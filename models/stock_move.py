from odoo import api, fields, models, tools, _


class StockMove(models.Model):
    _inherit = "stock.move"

    def _search_picking_for_assignation(self):
        res = super(StockMove, self)._search_picking_for_assignation()
        res = False
        return res