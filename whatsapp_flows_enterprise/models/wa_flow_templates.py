from odoo import models, fields, api


class WAFlowTemplate(models.Model):
    _inherit = 'whatsapp.template'
    _description = 'Inherited whatsapp template to whatsapp flow to extend whatsapp templates with flows'

    wa_flow_id = fields.Many2one(comodel_name="wa.flows", string="Whatsapp Flows")

    def _get_button_components(self, free_text_json, template_variables_value):
        button_components = super(WAFlowTemplate, self)._get_button_components(free_text_json, template_variables_value)
        flow_button = self.button_ids.filtered(lambda x: x.button_type == 'flow')
        flow_index = {button: i for i, button in enumerate(self.button_ids)}
        if flow_button:
            for button in flow_button:
                button_components.append({
                    'type': 'button',
                    'sub_type': 'flow',
                    'index': flow_index.get(button), "parameters": [{
                        "type": "action",
                        "action": {
                            "flow_token": button.flow_id,
                        }
                    }]})
        return button_components
