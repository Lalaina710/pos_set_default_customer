# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PosConfigInherit(models.Model):
    _inherit = 'pos.config'

    default_partner_id = fields.Many2one(
        'res.partner',
        string="Client par défaut",
        domain="[('customer_rank','>',0),('active','=',True),"
               "'|',('company_id','=',False),('company_id','=',company_id)]",
        help="Client automatiquement pré-sélectionné à l'ouverture d'une nouvelle "
             "commande POS. Modification réservée aux managers PdV.",
    )


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _load_pos_data_domain(self, data):
        domain = super()._load_pos_data_domain(data)
        config = self.env['pos.config'].browse(data['pos.config']['data'][0]['id'])
        if config.default_partner_id:
            return ['|', ('id', '=', config.default_partner_id.id)] + domain
        return domain


class ResConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_default_partner_id = fields.Many2one(
        'res.partner',
        related="pos_config_id.default_partner_id",
        readonly=False,
        string="Default Customer",
        groups="point_of_sale.group_pos_manager",
    )
