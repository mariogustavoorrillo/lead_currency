from odoo import tools, models, fields, api, _
from odoo.exceptions import ValidationError
import json
from odoo.tools.safe_eval import safe_eval
import requests
from datetime import date

class ResCurrency(models.Model):
    _inherit = 'res.currency'

    @api.model
    def cron_update_currency_rate(self):
        res = requests.get('https://api.bluelytics.com.ar/v2/latest')
        if res.status_code == 200:
            usd_val = res.json().get('oficial').get('value_avg')
            usd_currency = self.env.ref('base.USD')
            vals = {
                    'name': str(date.today()),
                    'currency_id': usd_currency.id,
                    'company_rate': 1 / usd_val,
                    }
            rate_id = self.env['res.currency.rate'].search([('name','=',str(date.today())),('currency_id','=',usd_currency.id)])
            if not rate_id:
                rate_id = self.env['res.currency.rate'].create(vals)
        else:
            raise ValidationError('Hubo un error')
