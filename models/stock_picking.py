from odoo import api, fields, models, tools, _


class StockPicking(models.Model):
    _inherit = "stock.picking"

    team_id = fields.Many2one('crm.team',
        string="Equipo de ventas",
        store=True, readonly=False)
