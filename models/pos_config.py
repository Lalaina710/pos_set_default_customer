# -*- coding: utf-8 -*-
from odoo import fields, models


class PosConfigInherit(models.Model):
    _inherit = 'pos.config'

    default_partner_id = fields.Many2one(
        'res.partner',
        string="Client par défaut",
        domain="[('customer_rank','>',0),('active','=',True),"
               "'|',('company_id','=',False),('company_id','=',company_id)]",
        groups="point_of_sale.group_pos_manager",
        help="Client automatiquement pré-sélectionné à l'ouverture d'une nouvelle "
             "commande POS. Modification réservée aux managers PdV.",
    )


class ResConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_default_partner_id = fields.Many2one(
        'res.partner',
        related="pos_config_id.default_partner_id",
        readonly=False,
        string="Default Customer",
        groups="point_of_sale.group_pos_manager",
    )
