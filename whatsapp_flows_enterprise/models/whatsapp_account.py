from odoo import models, fields, api, _
import requests
import json
import logging
from odoo.exceptions import UserError
from odoo.addons.whatsapp.tools.whatsapp_exception import WhatsAppError

_logger = logging.getLogger(__name__)


class WhatsappAccount(models.Model):
    _inherit = 'whatsapp.account'
    _description = 'Whatsapp account extended for adding flow operations'

    def _get_all_whatsapp_flows(self):
        if not (self.webhook_verify_token and self.callback_url):
            raise WhatsAppError(failure_type='account')

        _logger.info("Sync whatsapp flows for account %s [%s]", self.name, self.id)
        response = self._api_requests_ext("GET", f"/{self.account_uid}/flows",
                                          auth_type="bearer")
        return response.json()

    def sync_whatsapp_flows(self):
        flows = self._get_all_whatsapp_flows()
        if flows:
            for flow in flows.get('data'):
                whatsapp_flow = self.env['wa.flows'].search([('flow_id', '=', flow['id'])])
                if not whatsapp_flow:
                    self.env['wa.flows'].create({
                        'name': flow['name'],
                        'flow_state': flow['status'].lower(),
                        'flows_categories': flow['categories'][0].lower(),
                        'wa_account_id': self.id,
                        'flow_id': flow['id'],
                    })
        else:
            return

    def _create_whatsapp_flow(self, name, category):
        if not (self.webhook_verify_token and self.callback_url):
            raise WhatsAppError(failure_type='account')
        data = {
            "name": name,
            "categories": [category],
        }
        _logger.info("Create whatsapp flows for account %s [%s]", self.name, self.id)
        response = self._api_requests_ext("POST", f"/{self.account_uid}/flows", data=data,
                                          auth_type="bearer")
        return response.json()

    def _delete_whatsapp_flow(self, flow_id):
        if not (self.webhook_verify_token and self.callback_url):
            raise WhatsAppError(failure_type='account')
        data = {}
        _logger.info("Create whatsapp flows for account %s [%s]", self.name, self.id)
        response = self._api_requests_ext("DELETE", f"/{flow_id}", data=data,
                                          auth_type="bearer")
        return response.json()

    def _publish_whatsapp_flow(self, flow_id):
        if not (self.webhook_verify_token and self.callback_url):
            raise WhatsAppError(failure_type='account')
        data = {}
        _logger.info("Create whatsapp flows for account %s [%s]", self.name, self.id)
        response = self._api_requests_ext("POST", f"/{flow_id}/publish", data=data,
                                          auth_type="bearer")
        return response.json()

    def _deprecate_whatsapp_flow(self, flow_id):
        if not (self.webhook_verify_token and self.callback_url):
            raise WhatsAppError(failure_type='account')
        data = {}
        _logger.info("Create whatsapp flows for account %s [%s]", self.name, self.id)
        response = self._api_requests_ext("POST", f"/{flow_id}/deprecate", data=data,
                                          auth_type="bearer")
        return response.json()

    def slicedict(self, d, s):
        return {k: v for k, v in d.items() if k.startswith(s)}
    
    def filter_json_nfm(self, json_nfm):
        screens = self.slicedict(json_nfm, 'screen_')
        screen_list = {}
        for key, value in screens.items():
            split_key = key.split('_')
            if split_key[0] + '_' + split_key[1] in screen_list.keys():
                screen_list[split_key[0] + '_' + split_key[1]].update({
                    split_key[2] + '_' + split_key[3]: value
                })
            else:
                screen_list[split_key[0] + '_' + split_key[1]] = {
                    split_key[2] + '_' + split_key[3]: value
                }
        return screen_list