from odoo import fields, models
import json


class WhatsappAccountInherit(models.Model):
    _inherit = "whatsapp.account"

    wa_chatbot_id = fields.Many2one(
        comodel_name="whatsapp.chatbot",
        string="Whatsapp Chatbot",
        readonly=False,
    )

    def _process_messages(self, value):
        if "messages" not in value and value.get("whatsapp_business_api_data", {}).get(
                "messages"
        ):
            value = value["whatsapp_business_api_data"]

        for messages in value.get("messages", []):
            parent_id = False
            channel = False
            sender_name = value.get("contacts", [{}])[0].get("profile", {}).get("name")
            sender_mobile = messages["from"]
            message_type = messages["type"]
            if message_type == "location":
                if "context" in messages:
                    parent_whatsapp_message = self.env["whatsapp.message"].sudo().search(
                        [("msg_uid", "=", messages["context"].get("id"))])
                    if parent_whatsapp_message:
                        parent_id = parent_whatsapp_message.mail_message_id
                    if parent_id:
                        channel = (
                            self.env["discuss.channel"]
                            .sudo()
                            .search([("message_ids", "in", parent_id.id)], limit=1)
                        )

                if not channel:
                    channel = self._find_active_channel(
                        sender_mobile, sender_name=sender_name, create_if_not_found=True
                    )
                if channel._fields.get('dynamic_booking_id'):
                    if parent_id.booking_id:
                        channel.dynamic_booking_id = parent_id.booking_id.id
                kwargs = {
                    "message_type": "whatsapp_message",
                    "author_id": channel.whatsapp_partner_id.id,
                    "subtype_xmlid": "mail.mt_comment",
                    "parent_id": parent_id.id if parent_id else None,
                }
                if message_type == "location":
                    if messages.get('location').get("latitude") and messages.get('location').get("longitude"):
                        message = messages.get('location').get("latitude") and messages.get('location').get("longitude")
                        booking_id = self.env['calendar.event'].sudo().search(
                            [('appointment_booker_id', '=', channel.whatsapp_partner_id.id)])
                        if booking_id:
                            booking_id.sudo().write({'latitude': messages.get('location').get("latitude"),
                                                     'longitude': messages.get('location').get("longitude")})
                            self.env.cr.commit()
                            if channel.wa_chatbot_id and channel.script_sequence:
                                current_chatbot_script = channel.wa_chatbot_id.mapped("step_type_ids").filtered(
                                    lambda l: l.sequence == channel.script_sequence)
                                next_script = current_chatbot_script.sequence + current_chatbot_script.next_sq_number
                                chatbot_script_lines = channel.wa_chatbot_id.step_type_ids.filtered(
                                    lambda l: l.sequence == next_script)
                    else:
                        message = ""
                    kwargs["body"] = message
                channel.with_context({'parent_message_id': parent_id if parent_id else None}).message_post(
                    whatsapp_inbound_msg_uid=messages["id"], **kwargs)


            elif message_type == "interactive":
                if "context" in messages:
                    parent_whatsapp_message = self.env["whatsapp.message"].sudo().search(
                        [("msg_uid", "=", messages["context"].get("id"))])
                    if parent_whatsapp_message:
                        parent_id = parent_whatsapp_message.mail_message_id
                    if parent_id:
                        channel = (
                            self.env["discuss.channel"]
                            .sudo()
                            .search([("message_ids", "in", parent_id.id)], limit=1)
                        )

                if not channel:
                    channel = self._find_active_channel(
                        sender_mobile, sender_name=sender_name, create_if_not_found=True
                    )
                if channel._fields.get('dynamic_booking_id'):
                    if parent_id.booking_id:
                        channel.dynamic_booking_id = parent_id.booking_id.id
                kwargs = {
                    "message_type": "whatsapp_message",
                    "author_id": channel.whatsapp_partner_id.id,
                    "subtype_xmlid": "mail.mt_comment",
                    "parent_id": parent_id.id if parent_id else None,
                }
                if message_type == "interactive":
                    if messages.get("interactive") and messages.get("interactive").get(
                            "button_reply"
                    ):
                        message = (
                            messages.get("interactive").get("button_reply").get("title")
                        )
                    elif messages.get("interactive") and messages.get(
                            "interactive"
                    ).get("list_reply"):
                        message = (
                            messages.get("interactive").get("list_reply").get("title")
                        )
                    elif messages and messages.get('interactive') and \
                            messages.get('interactive').get(
                                'type') == 'nfm_reply':
                        message = ''
                        for messages in value.get('messages', []):

                            nfm_replay = messages.get('interactive').get("nfm_reply").get("response_json")
                            json_nfm = json.loads(nfm_replay)
                            vals_list = self.filter_json_nfm(json_nfm)
                            contact_no = sender_mobile.join("+") + sender_mobile

                            parent = self.env['res.partner'].sudo().search([('mobile', '=', contact_no)])
                            helpdesk_order = self.env['helpdesk.ticket'].sudo().search(
                                [('partner_id', '=', parent.id)]).filtered(lambda x: x.stage_id.name == "New")

                            if json_nfm.get("flow_token", False) and json_nfm.get("flow_token") != "unused":
                                flow_id = json_nfm.get("flow_token")
                                flow = self.env["wa.flows"].sudo().search([("flow_id", "=", flow_id)])
                                if flow.flow_model_id.model == "helpdesk.ticket":
                                    def sort_by_sq(e):
                                        return e.split("_")[-1]

                                    answer_list = []
                                    for i in range(0, len(vals_list.keys())):
                                        get_screen = vals_list.get("screen_" + str(i))
                                        screen_keys = list(get_screen.keys())
                                        screen_keys.sort(key=sort_by_sq)
                                        sorted_dict = {j: get_screen[j] for j in screen_keys}
                                        for k, v in sorted_dict.items():
                                            k.split("_")
                                        answer_list.extend(sorted_dict.values())

                                    register_vals = {}
                                    for count, field in enumerate(flow.field_mapping_ids):
                                        if field.mapped_field.sudo().ttype in ["char", "text","html"]:
                                            register_vals.update({
                                                field.mapped_field.name: answer_list[
                                                    count
                                                ].replace('_', ' ')
                                            })
                                        elif field.mapped_field.sudo().ttype in ["many2one"]:
                                            self.env['ir.model'].search([])
                                            register_vals.update({
                                                field.mapped_field.id: answer_list[
                                                    count
                                                ].replace('_', ' ')
                                            })

                                    if not helpdesk_order:
                                        helpdesk_ticket = helpdesk_order.sudo().create({
                                            "name":  " WA ChatBot Ticket ",
                                            "partner_id": parent.id,
                                            "partner_phone": parent.mobile,
                                            'team_id': self.env.company.team_id.id
                                        })
                                        helpdesk_ticket.response_data = answer_list
                                        helpdesk_ticket.sudo().write(register_vals)

                                    if helpdesk_order:
                                        helpdesk_order.sudo().write(
                                            register_vals
                                        )
                                    # message ="Whatsapp Flow Received"

                                    if channel.wa_chatbot_id and channel.script_sequence:
                                        current_chatbot_script = channel.wa_chatbot_id.mapped("step_type_ids").filtered(
                                            lambda l: l.sequence == channel.script_sequence)
                                        next_script = current_chatbot_script.sequence + current_chatbot_script.next_sq_number
                                        chatbot_script_lines = channel.wa_chatbot_id.step_type_ids.filtered(
                                            lambda l: l.sequence == next_script)
                                        # for chat in chatbot_script_lines:
                                        #     channel.sudo().write({
                                        #         "wa_chatbot_id": chat.whatsapp_chatbot_id.id,
                                        #         "script_sequence": chat.sequence,
                                        #     })
                                        #
                                        #     if chat.step_call_type in ["template", "interactive"]:
                                        #         template = chat.template_id
                                        #         if template:
                                        #             whatsapp_composer = (
                                        #                 self.env["whatsapp.composer"]
                                        #                 .with_user(self.notify_user_ids.id)
                                        #                 .with_context(
                                        #                     {
                                        #                         "active_id": parent.id,
                                        #                         "is_chatbot": True,
                                        #                         "wa_chatbot_id": self.wa_chatbot_id.id,
                                        #                     }
                                        #                 )
                                        #                 .create(
                                        #                     {
                                        #                         "phone": parent.mobile,
                                        #                         "wa_template_id": template.id,
                                        #                         "res_model": template.model_id.model,
                                        #                     }
                                        #                 )
                                        #             )
                                        #             new_message = whatsapp_composer.with_context(
                                        #                 {'stop_recur': True})._send_whatsapp_template()


                    else:
                        message = ""
                    kwargs["body"] = message
                channel.with_context({'parent_message_id': parent_id if parent_id else None}).message_post(
                    whatsapp_inbound_msg_uid=messages["id"], **kwargs)
            else:
                return super(WhatsappAccountInherit, self)._process_messages(value)
