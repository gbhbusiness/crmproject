# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.
import random
from datetime import datetime, timedelta,timezone
from unicodedata import category

import pytz
from odoo import api, fields, models, tools
from markupsafe import  Markup


class ChatbotDiscussChannel(models.Model):
    _inherit = "discuss.channel"

    wa_chatbot_id = fields.Many2one(
        comodel_name="whatsapp.chatbot", string="Whatsapp Chatbot"
    )
    child_wa_chatbot = fields.Many2one("whatsapp.chatbot", string="Child WhatsApp Chatbot")
    message_ids = fields.One2many(
        "mail.message",
        "res_id",
        domain=lambda self: [
            ("wa_chatbot_id", "!=", False),
            ("wa_chatbot_id", "=", self.wa_chatbot_id.id),
        ],
        string="Messages",
    )
    script_sequence = fields.Integer(string="Sequence", default=1)
    is_chatbot_ended = fields.Boolean(string="Inactivate Chatbot")


    def _convert_time_to_utc(self, date_time, from_timezone):
        local = pytz.timezone(from_timezone).localize(date_time, is_dst=None)
        return local.astimezone(pytz.utc)

    def chatbot_activate(self):
        channels = self.search([])
        for rec in channels:
            if rec.is_chatbot_ended:
                rec.is_chatbot_ended = False
                rec.wa_chatbot_id = rec.wa_chatbot_id.id

    def _update_dynamic_template_value(self, current_script,booking, action=False):
        if current_script.action_id.dynamic_selection == 'search':
            body = tools.html2plaintext(fields.first(self.message_ids).body)
            dynamic_booking_value_dict = {}
            dynamic_booking_value = []
            # dynamic_description_booking_value = False
            reschedule = False
            if current_script.action_id.dynamic_send_template_id.is_category_template:

                # dynamic_description_value =False
                category  = self.env[current_script.action_id.dynamic_model_id.model].search([])
                for cat in category:
                    if len(cat.name)<=24:
                        dynamic_booking_value.append(cat.name)
                    else:
                        dynamic_booking_value.append(cat.name[0:24])
                # dynamic_booking_value = [i.name for i in
                #                          self.env[current_script.action_id.dynamic_model_id.model].search([])][0:9]
                dynamic_description_value = [i.name[:50] for i in
                                         self.env[current_script.action_id.dynamic_model_id.model].search([])][0:9]

                dynamic_booking_value_dict.update(zip(dynamic_booking_value,dynamic_description_value))



            elif current_script.action_id.dynamic_send_template_id.is_sub_cat_template:
                category = self.env[current_script.action_id.dynamic_model_id.model].search([]).filtered(lambda x:x.name[:24].strip() == body).name
                sub_cat = self.env[current_script.action_id.dynamic_model_id.model].search(
                    [('name', '=', category)]).services_ids[0:9]
                for subcat in sub_cat:
                    if len(subcat.name) <= 24:
                        dynamic_booking_value.append(subcat.name)
                    else:
                        dynamic_booking_value.append(subcat.name[0:24])

                dynamic_description_value =[i.name[:50] for i in  self.env[current_script.action_id.dynamic_model_id.model].search([('name','=',category)]).services_ids][0:9]
                dynamic_booking_value_dict.update(zip(dynamic_booking_value, dynamic_description_value))

            elif current_script.action_id.dynamic_send_template_id.is_project_template:
                projects =  self.env[current_script.action_id.dynamic_model_id.model].search([])
                for project in projects:
                    if len(project.name) <= 24:
                        dynamic_booking_value.append(project.name)
                    else:
                        dynamic_booking_value.append(project.name[0:24])
                dynamic_description_value = [i.name[:50] for i in
                                         self.env[current_script.action_id.dynamic_model_id.model].search(
                                             [])][0:9]
                dynamic_booking_value_dict.update(zip(dynamic_booking_value, dynamic_description_value))

            elif current_script.action_id.dynamic_send_template_id.is_tower_template:
                project_name = self.env[current_script.action_id.dynamic_model_id.model].search([]).filtered(lambda x:x.name[:24].strip() == body).name
                towers = self.env[current_script.action_id.dynamic_model_id.model].search(
                                             [('name', '=', project_name)]).tower_ids
                for tower in towers:
                    if len(tower.name)<= 24:
                        dynamic_booking_value.append(tower.name)
                    else:
                        dynamic_booking_value.append(tower.name[0:24])
                dynamic_description_value = [i.name[:50] for i in
                                         self.env[current_script.action_id.dynamic_model_id.model].search(
                                             [('name', '=', project_name)]).tower_ids][0:9]
                dynamic_booking_value_dict.update(zip(dynamic_booking_value, dynamic_description_value))

            if not reschedule:
                current_script.action_id.dynamic_send_template_id.wa_interactive_ids.write(
                    {'interactive_list_ids': [(5, 0, 0)] + [(
                        0, 0, {'main_title': current_script.action_id.dynamic_template_list_title,
                               'title_ids': [(0, 0, {'title': i,'description':j}) for i,j in zip(dynamic_booking_value_dict.keys(),dynamic_booking_value_dict.values())]})]})
            return current_script.action_id.dynamic_send_template_id

    def _get_dynamic_model_values(self, current_script, booking, previous_script, mail_message):
        if booking and current_script and previous_script:
            body = tools.html2plaintext(mail_message.body)
            if current_script.receive_action_id.dynamic_field_id and previous_script.action_id.dynamic_send_template_id.is_category_template:
                category =  self.env[previous_script.action_id.dynamic_model_id.model].search([]).filtered(lambda x:x.name[:24].strip()  == body)
                dynamic_field_value = category
                booking.sudo().write({
                    current_script.receive_action_id.dynamic_field_id.name: dynamic_field_value.name
                })
            elif current_script.receive_action_id.dynamic_field_id and previous_script.action_id.dynamic_send_template_id.is_sub_cat_template:
                sub_cat = self.env[previous_script.action_id.dynamic_model_id.model].search([('name','=', booking.categories if booking.categories else body)]).services_ids.filtered(lambda x:x.name[:24].strip() == body)
                # sub_cat = self.env['helpdesk.service'].search([('name','=',body)])
                booking.sudo().write({
                    current_script.receive_action_id.dynamic_field_id.name: sub_cat.name
                })
            elif current_script.receive_action_id.dynamic_field_id and previous_script.action_id.dynamic_send_template_id.is_project_template:
                # sub_cat = self.env['helpdesk.service'].search([('name','=',body)])
                project = self.env[previous_script.action_id.dynamic_model_id.model].search([]).filtered(
                    lambda x: x.name[:24].strip() == body)
                # project = self.env[previous_script.action_id.dynamic_model_id.model].search(
                #             [(previous_script.action_id.dynamic_field_id.name, '=', body)])
                booking.sudo().write({
                    current_script.receive_action_id.dynamic_field_id.name: project.name
                })
            elif current_script.receive_action_id.dynamic_field_id and previous_script.action_id.dynamic_send_template_id.is_tower_template:
                project =  self.env[previous_script.action_id.dynamic_model_id.model].search([('name','=',booking.project)]).tower_ids.filtered(lambda x:x.name[:24].strip() == body)
                # project =  self.env['project.tower'].search([('name','=',body)])
                # project = self.env[previous_script.action_id.dynamic_model_id.model].search(
                #             [(previous_script.action_id.dynamic_field_id.name, '=', body)])
                booking.sudo().write({
                    current_script.receive_action_id.dynamic_field_id.name: project.name
                })


            return booking
    def _get_active_bot(self, wa_account_id, channel, received_message):
        child_bot_script = wa_account_id.wa_chatbot_id.mapped('step_type_ids').filtered(lambda x: x.step_call_type == 'chatbot' and x.message == tools.html2plaintext(received_message))
        if child_bot_script:
            child_chatbot = child_bot_script[0].child_wa_chatbot_id if len(child_bot_script) > 1 else child_bot_script.child_wa_chatbot_id
            channel.child_wa_chatbot = child_chatbot.id
            channel.script_sequence = 1
        if channel.child_wa_chatbot:
            chatbot = channel.child_wa_chatbot
        else:
            chatbot = wa_account_id.wa_chatbot_id
        if received_message in ['Main Menu', 'Main menu']:
            channel.sudo().write({'child_wa_chatbot': False})
            chatbot = wa_account_id.wa_chatbot_id
        return chatbot

    def _notify_thread(self, message, msg_vals=False, **kwargs):
        res = super(ChatbotDiscussChannel, self)._notify_thread(
            message, msg_vals=msg_vals, **kwargs
        )
        booking_id = self.env['helpdesk.order']
        dummy_booking_id = self.env['helpdesk.order'].sudo().search(
            [('partner_id', '=', message.author_id.id), ('state', 'not in', ['cancel', 'confirm'])])
        if self.env.context.get('stop_recur'):
            return res
        if message:
            wa_account_id = self.wa_account_id
            user_partner = (
                    wa_account_id.notify_user_ids and wa_account_id.notify_user_ids[0] or []
            )
            mail_message_id = message
            partner_id = mail_message_id.author_id
            chatbot = self._get_active_bot(wa_account_id, self, tools.html2plaintext(mail_message_id.body))
            if wa_account_id and user_partner and chatbot and self:
                message.update({"wa_chatbot_id": chatbot.id})
                if not self.is_chatbot_ended:
                    message_script = (
                        self.env["whatsapp.chatbot"]
                        .search([("id", "=", chatbot.id)])
                        .mapped("step_type_ids")
                        .filtered(
                            lambda l: l.message
                                      == tools.html2plaintext(mail_message_id.body)
                        )
                    )
                    current__chat_seq_script = (
                        self.env["whatsapp.chatbot"]
                        .search([("id", "=", chatbot.id)])
                        .mapped("step_type_ids")
                        .filtered(lambda l: l.sequence == self.script_sequence)
                    )

                    if not message_script and tools.html2plaintext(mail_message_id.body) == 'Confirm':
                        helpdesk_order = self.env['helpdesk.order'].sudo().search([('partner_id','=',partner_id.id),('state','not in',['confirm','cancel'])])
                        helpdesk_order.action_confirm()
                    if not message_script and tools.html2plaintext(mail_message_id.body) == 'Cancel':
                        helpdesk_order = self.env['helpdesk.order'].sudo().search([('partner_id','=',partner_id.id),('state','not in',['confirm','cancel'])])
                        helpdesk_order.action_cancel()
                    # if not message_script and current__chat_seq_script.is_chatbot_ended:
                    #    self.is_chatbot_ended = True

                    if message_script:
                        if len(message_script) > 1 and message_script.parent_id:
                            channel_script = message_script.filtered(
                                lambda x: x.sequence == self.script_sequence).parent_id
                            if channel_script:
                                current__chat_seq_script = message_script.filtered(
                                    lambda x: x.parent_id == channel_script)
                            else:
                                chatbot_script_lines = message_script
                        else:
                            chatbot_script_lines = message_script
                    elif  mail_message_id and not message_script and current__chat_seq_script and current__chat_seq_script.get_image_script:
                        if mail_message_id.attachment_ids:
                            for attachment in mail_message_id.attachment_ids:
                                helpdesk_order = self.env['helpdesk.order'].sudo().search([('partner_id','=',partner_id.id),('state','not in',['confirm','cancel'])])
                                helpdesk_order.sudo().write({
                                    'attachment_ids':  [(4, attachment.id)],
                                })
                                mail_message_id.update({
                                    'body': 'Image Received'
                                })

                                chatbot_script_lines = self.wa_chatbot_id.mapped('step_type_ids').filtered(
                                    lambda l: l.sequence == current__chat_seq_script.sequence + current__chat_seq_script.next_sq_number)
                        else:
                            chatbot_script_lines = current__chat_seq_script

                    elif current__chat_seq_script:
                        if self._context.get('parent_message_id'):
                            if self._context.get('parent_message_id') and self._context.get(
                                    'parent_message_id').wa_template_id:
                                current__chat_seq_script = chatbot.step_type_ids.filtered(lambda
                                                                                              l: l.action_id.dynamic_send_template_id == self._context.get(
                                    'parent_message_id').wa_template_id and l.sequence == self.script_sequence)
                                if not current__chat_seq_script:
                                    temp_script = chatbot.step_type_ids.filtered(lambda
                                                                                      l: l.action_id.dynamic_send_template_id == self._context.get(
                                        'parent_message_id').wa_template_id)
                                    channel_script = chatbot.step_type_ids.filtered(
                                        lambda x: x.sequence == self.script_sequence).parent_id
                                    current__chat_seq_script = temp_script.filtered(
                                        lambda x: x.parent_id == channel_script)
                                next_script = current__chat_seq_script.sequence + current__chat_seq_script.next_sq_number
                                chatbot_script_lines = chatbot.step_type_ids.filtered(
                                    lambda l: l.sequence == next_script)
                            else:
                                chatbot_script_lines = chatbot.step_type_ids.filtered(lambda l: l.sequence == current__chat_seq_script.sequence + current__chat_seq_script.next_sq_number)
                        else:
                            chatbot_script_lines = current__chat_seq_script
                    else:
                        chatbot_script_lines = chatbot.step_type_ids[0]

                    for chat in chatbot_script_lines:
                        if chat.sequence >= self.script_sequence:
                            self.write(
                                {
                                    "wa_chatbot_id": chat.whatsapp_chatbot_id.id
                                    if chatbot
                                       == chat.whatsapp_chatbot_id
                                    else False,
                                    "script_sequence": chat.sequence,
                                }
                            )
                        elif (
                                current__chat_seq_script
                                and current__chat_seq_script.parent_id
                                and current__chat_seq_script.parent_id == chat.parent_id
                        ):
                            self.write(
                                {
                                    "wa_chatbot_id": chat.whatsapp_chatbot_id.id,
                                    "script_sequence": chat.sequence,
                                }
                            )
                        else:
                            first_script = (
                                self.env["whatsapp.chatbot"]
                                .search([("id", "=", self.wa_chatbot_id.id)])
                                .mapped("step_type_ids")
                                .filtered(lambda l: l.sequence == 1)
                            )
                            if first_script:
                                self.write(
                                    {
                                        "wa_chatbot_id": chat.whatsapp_chatbot_id.id,
                                        "script_sequence": first_script.sequence,
                                    }
                                )
                            else:
                                self.write(
                                    {
                                        "wa_chatbot_id": chat.whatsapp_chatbot_id.id if wa_account_id and chatbot == chat.whatsapp_chatbot_id
                                        else False,
                                        "script_sequence": chat.sequence,
                                    })

                        if chat.step_call_type in ["template", "interactive"]:
                            template = chat.template_id
                            if template:
                                whatsapp_composer = (
                                    self.env["whatsapp.composer"]
                                    .with_user(user_partner.id)
                                    .with_context(
                                        {
                                            "active_id": partner_id.id,
                                            "is_chatbot": True,
                                            "wa_chatbot_id": self.wa_chatbot_id.id,
                                        }
                                    )
                                    .create(
                                        {
                                            "phone": partner_id.mobile,
                                            "wa_template_id": template.id,
                                            "res_model": template.model_id.model,
                                        }
                                    )
                                )
                                new_message = whatsapp_composer.with_context({'stop_recur': True})._send_whatsapp_template()


                        elif chat.step_call_type == "message":
                            self.with_context({'stop_recur': True}).with_user(user_partner.id).message_post(
                                body=chat.answer,
                                message_type="whatsapp_message",
                            )
                        elif chat.step_call_type == "action":
                            # booking_id = chatbot.booking_ids.filtered(lambda
                            #                                                                   x: x.appointment_booker_id.id == partner_id.id and x.whatsapp_booking_state == 'draft')


                            if chat.step_call_type == "action" and (
                                    chat.action_id and chat.action_id.is_custom_action) or (
                                    chat.receive_action_id and chat.receive_action_id.is_custom_action):
                                if (not (
                                        chat.action_id.dynamic_selection and chat.action_id.dynamic_working_selection
                                        and chat.action_id.dynamic_model_id and chat.action_id.dynamic_field_id)
                                        and chat.action_id.is_custom_action and chat.action_id.dynamic_send_template_id):
                                    mail_message_id.sudo().write(
                                        {'wa_template_id': chat.action_id.dynamic_send_template_id.id})
                                    whatsapp_composer = (
                                        self.env["whatsapp.composer"]
                                        .with_user(user_partner.id)
                                        .with_context(
                                            {
                                                "active_id": partner_id.id,
                                                "is_chatbot": True,
                                                "wa_chatbot_id": self.wa_chatbot_id.id,
                                            }
                                        )
                                        .create(
                                            {
                                                "phone": partner_id.mobile,
                                                "wa_template_id": chat.action_id.dynamic_send_template_id.id,
                                                "res_model": chat.action_id.dynamic_send_template_id.model_id.model,
                                            }
                                        )
                                    )
                                    new_message = whatsapp_composer.with_context({'stop_recur': True})._send_whatsapp_template()



                                elif not mail_message_id.booking_id or self._context.get('parent_message_id').booking_id:
                                    if chat.action_id.dynamic_action_selection not in ['reschedule', 'cancel']:
                                        if not dummy_booking_id:
                                            booking_id |= self.env['helpdesk.order'].sudo().create({
                                                'partner_id': partner_id.id,
                                                'user_id': fields.first(wa_account_id.notify_user_ids).id,
                                            })
                                            mail_message_id.sudo().write({'booking_id':booking_id.id})

                                        else:
                                            mail_message_id.sudo().write({'booking_id': dummy_booking_id.id})
                                            # chatbot.booking_ids = [(4, booking_id.id)]

                                if chat.receive_action_id.dynamic_working_selection == 'receive':
                                    last_message = {}
                                    self._get_dynamic_model_values(chat, dummy_booking_id, current__chat_seq_script,
                                                                   mail_message_id)
                                    # vals)
                                    if chat.receive_action_id.dynamic_send_template_id:
                                        pass
                                        # message_values.update({
                                        #     "body": tools.html2plaintext(
                                        #         chat.receive_action_id.dynamic_send_template_id.body_html)
                                        # })
                                        # self._send_wa_template(wa_account_id, channel, partner_id,
                                        #                        chat.receive_action_id.dynamic_send_template_id,
                                        #                        message_values, partner_id, chat)

                                    next_script = chatbot.step_type_ids.filtered(
                                        lambda l: l.sequence == chat.sequence + chat.next_sq_number)
                                    if next_script.is_question_script:
                                        chat_answer = next_script.answer
                                        pass
                                        # message_values.update({'body': chat_answer})
                                        # self._send_wa_message(wa_account_id, channel, message_values)
                                        # channel.sudo().write({
                                        #     'script_sequence': next_script.sequence
                                        # })
                                    if next_script.step_call_type in ["template", "interactive"]:
                                        template = next_script.template_id
                                        if template:
                                            whatsapp_composer = (
                                                self.env["whatsapp.composer"]
                                                .with_user(user_partner.id)
                                                .with_context(
                                                    {
                                                        "active_id": partner_id.id,
                                                        "is_chatbot": True,
                                                        "wa_chatbot_id": self.wa_chatbot_id.id,
                                                    }
                                                )
                                                .create(
                                                    {
                                                        "phone": partner_id.mobile,
                                                        "wa_template_id": template.id,
                                                        "res_model": template.model_id.model,
                                                    }
                                                )
                                            )
                                            new_message = whatsapp_composer.with_context(
                                                {'stop_recur': True})._send_whatsapp_template()
                                if chat.receive_action_id.dynamic_working_selection == 'action':
                                    if chat.receive_action_id.dynamic_selection == 'reschedule':
                                        if chat.receive_action_id.dynamic_action_selection == 'reschedule':
                                            if self._context.get('parent_message_id') and self._context.get(
                                                    'parent_message_id').booking_id:
                                                self._context.get('parent_message_id').booking_id.action_rescheduled()

                                if chat.action_id.dynamic_working_selection == 'send':
                                    if not booking_id and self._context.get('parent_message_id').booking_id :
                                        booking_id = self._context.get('parent_message_id').booking_id
                                            # message_values.update({
                                            #     "body": tools.html2plaintext(
                                            #         template.body_html)
                                            # })
                                            # self._send_wa_template(wa_account_id, channel, partner_id, template,
                                            #                        message_values, values[0], chat)
                                    else:
                                        template = self._update_dynamic_template_value(chat, dummy_booking_id)
                                        if template and template.body and template.body != "":
                                            whatsapp_composer = (
                                                self.env["whatsapp.composer"]
                                                .with_user(user_partner.id)
                                                .with_context(
                                                    {
                                                        "active_id": partner_id.id,
                                                        "is_chatbot": True,
                                                        "wa_chatbot_id": self.wa_chatbot_id.id,
                                                    }
                                                )
                                                .create(
                                                    {
                                                        "phone": partner_id.mobile,
                                                        "wa_template_id": chat.action_id.dynamic_send_template_id.id,
                                                        "res_model": chat.action_id.dynamic_send_template_id.model_id.model,
                                                    }
                                                )
                                            )
                                            whatsapp_composer.with_context(
                                                {'stop_recur': True})._send_whatsapp_template()


                                if chat.action_id.dynamic_working_selection == 'action':
                                    if chat.receive_action_id.dynamic_selection == 'reschedule':
                                        if chat.receive_action_id.dynamic_action_selection == 'reschedule':
                                            if self._context.get('parent_message_id').dummy_booking_id:
                                                self._context.get('parent_message_id').booking_id.action_rescheduled()
                                    if chat.action_id.dynamic_selection == 'cancel':
                                        if chat.action_id.dynamic_action_selection == 'cancel':
                                            if self.dynamic_booking_id:
                                                booking_dict = self.dynamic_booking_id.action_cancel(
                                                    is_whatsapp=True)
                                                if isinstance(booking_dict, type({})) and booking_dict.get(
                                                        'ValidationError'):
                                                    last_message = booking_dict.get('ValidationError')
                                                else:
                                                    last_message = (
                                                        "Thank you, Your Appointment is Cancelled."
                                                        "We will contact you accordingly")
                                                self.with_context({'stop_recur': True}).with_user(
                                                    user_partner.id).message_post(
                                                    body=last_message,
                                                    message_type="whatsapp_message",
                                                )
                                                # message_values.update({'body': last_message})
                                                # self._send_wa_message(wa_account_id, channel, message_values)

                                    if chat.action_id.dynamic_action_selection == 'confirm':
                                        if booking_id.is_rescheduled_booking:
                                            booking_dict = dummy_booking_id.with_context(
                                                by_pass_wa=True).confirm_booking(is_whatsapp=True)
                                            if isinstance(booking_dict, type({})) and booking_dict.get(
                                                    'ValidationError'):
                                                last_message = booking_dict.get('ValidationError')
                                            else:
                                                whatsapp_composer = self.env['whatsapp.composer'].with_user(
                                                    user_partner.id).create(
                                                    {
                                                        'phone': dummy_booking_id.partner_id.mobile,
                                                        'wa_template_id': chat.action_id.dynamic_send_template_id.id,
                                                        'res_model': chat.action_id.dynamic_send_template_id.model_id.model,
                                                    }
                                                )
                                                whatsapp_composer._send_whatsapp_template()
                                            #     last_message = (
                                            #         "Thank you for your confirmation for Reschedule. "
                                            #         "Admin will contact you accordingly")
                                            # self.with_context({'stop_recur': True}).with_user(
                                            #     user_partner.id).message_post(
                                            #     body=last_message,
                                            #     message_type="whatsapp_message",
                                            # )

                                            # message_values.update({'body': last_message})
                                            # self._send_wa_message(wa_account_id, channel, message_values)
                                        else:
                                            booking_id_dict = booking_id.confirm_booking(is_whatsapp=True)
                                            next_chat = False
                                            if isinstance(booking_id_dict, type({})) and booking_id_dict.get(
                                                    'ValidationError'):
                                                last_message = booking_id_dict.get('ValidationError')
                                            else:
                                                next_chat = chatbot.step_type_ids.filtered(
                                                    lambda l: l.sequence == chat.sequence + chat.next_sq_number)
                                                last_message = "Thank you for your confirmation."
                                                # if not booking_id.is_free_booking:
                                                #     last_message += ' You will Receive a Payment Link in a While'
                                                if next_chat.step_call_type == "message":
                                                    self.with_context({'stop_recur': True}).with_user(
                                                        user_partner.id).message_post(
                                                        body=next_chat.answer,
                                                        message_type="whatsapp_message",
                                                    )
                                            # message_values.update({'body': next_chat.answer or last_message})
                                            # self._send_wa_message(wa_account_id, channel, message_values)
                                    if chat.action_id.dynamic_action_selection in ['reschedule', 'cancel']:
                                        if chat.action_id.dynamic_send_template_id.is_value_template:
                                            booking_ids = dummy_booking_id.search(
                                                [('partner_id', '=', partner_id.id),
                                                 ('state', '=', 'confirm'),
                                                 ])
                                            for booking in booking_ids:
                                                template = self._update_dynamic_template_value(chat, booking,
                                                                                               action=chat.action_id.dynamic_action_selection)
                                                if template and template.body:
                                                    whatsapp_composer = (
                                                        self.env["whatsapp.composer"]
                                                        .with_user(user_partner.id)
                                                        .with_context(
                                                            {
                                                                "active_id": partner_id.id,
                                                                "is_chatbot": True,
                                                                "wa_chatbot_id": self.wa_chatbot_id.id,
                                                            }
                                                        )
                                                        .create(
                                                            {
                                                                "phone": partner_id.mobile,
                                                                "wa_template_id": chat.action_id.dynamic_send_template_id.id,
                                                                "res_model": chat.action_id.dynamic_send_template_id.model_id.model,
                                                            }
                                                        )
                                                    )
                                                    new_message = whatsapp_composer.with_context(
                                                        {'stop_recur': True})._send_whatsapp_template()
                                                    # new_message.mail_message_id.parent_id = message.id
                                                    # new_message.mail_message_id.booking_id = booking.id
                                            if not booking_ids:
                                                if chatbot.end_template_id:
                                                    pass
                                                    # self._send_wa_template(wa_account_id, channel, partner_id,
                                                    #                        chatbot.end_template_id,
                                                    #                        message_values, partner_id, chat)

                                                else:
                                                    last_message = ('There is no booking found. Please Contact '
                                                                    'administrator')
                                                    self.with_context({'stop_recur': True}).with_user(
                                                        user_partner.id).message_post(
                                                        body=last_message, message_type="whatsapp_message"
                                                    )
                            if chat.action_id.binding_model_id.model == "crm.lead":
                                lead_message = (
                                        "Dear "
                                        + partner_id.name
                                        + ", We are pleased to inform you that your lead has been successfully generated. Our team will be in touch with you shortly."
                                )
                                self.with_context({'stop_recur': True}).with_user(user_partner.id).message_post(
                                    body=lead_message, message_type="whatsapp_message"
                                )
                                self.env["crm.lead"].with_user(
                                    user_partner.id
                                ).sudo().create(
                                    {
                                        "name": partner_id.name + " WA ChatBot Lead ",
                                        "partner_id": partner_id.id,
                                        "email_from": partner_id.email
                                        if partner_id.email
                                        else False,
                                        "mobile": partner_id.mobile,
                                        "user_id": user_partner.id,
                                        "type": "lead",
                                        "description": "Lead created by Chatbot for customer "
                                                       + partner_id.name,
                                    }
                                )
                            if (
                                    chat.action_id.binding_model_id.model
                                    == "helpdesk.ticket"
                            ):
                                ticket_message = (
                                        "Dear "
                                        + partner_id.name
                                        + ", We are pleased to inform you that your Ticket has been raised. Our team will be in touch with you shortly."
                                )
                                self.with_context({'stop_recur': True}).with_user(user_partner.id).message_post(
                                    body=ticket_message, message_type="whatsapp_message"
                                )
                                self.env["helpdesk.ticket"].with_user(
                                    user_partner.id
                                ).sudo().create(
                                    {
                                        "name": partner_id.name + " WA ChatBot Ticket ",
                                        "partner_id": partner_id.id,
                                        "partner_phone": partner_id.mobile,
                                        "user_id": user_partner.id,
                                        "description": "Ticket raised by Chatbot for customer "
                                                       + partner_id.name,
                                    }
                                )

                            if (
                                    chat.action_id.binding_model_id.model
                                    == "discuss.channel"
                            ) and chat.action_id.dynamic_is_chatbot_ended:
                                self.is_chatbot_ended = True
                                available_operator = False
                                active_operator = wa_account_id.wa_chatbot_id.mapped(
                                    "user_ids"
                                ).filtered(lambda user: user.im_status == "online")
                                if active_operator:
                                    wa_chatbot_channels = (
                                        wa_account_id.wa_chatbot_id.mapped(
                                            "channel_ids"
                                        )
                                    )
                                    for wa_channel in wa_chatbot_channels:
                                        operators = active_operator.filtered(
                                            lambda av_user: av_user.partner_id
                                                            not in wa_channel.channel_member_ids.partner_id
                                        )
                                        if operators:
                                            for operator in operators:
                                                available_operator = operator.partner_id
                                        else:
                                            available_operator = random.choice(active_operator).partner_id
                                    if available_operator:
                                        added_operator = (
                                            self.channel_partner_ids.filtered(
                                                lambda x: x.id == available_operator.id
                                            )
                                        )
                                        if added_operator:
                                            self.write(
                                                {
                                                    "is_chatbot_ended": True,
                                                    "wa_chatbot_id": False,
                                                }
                                            )
                                        else:
                                            self.write(
                                                {
                                                    "channel_partner_ids": [
                                                        (4, available_operator.id)
                                                    ],
                                                    "is_chatbot_ended": True,
                                                    "wa_chatbot_id": False,
                                                }
                                            )
                                        mail_channel_partner = (
                                            self.env["discuss.channel.member"]
                                            .sudo()
                                            .search(
                                                [
                                                    ("channel_id", "=", self.id),
                                                    (
                                                        "partner_id",
                                                        "=",
                                                        available_operator.id,
                                                    ),
                                                ]
                                            )
                                        )
                                        mail_channel_partner.write({"is_pinned": True})
                                        if chat.action_id.last_message_conf == 'message':
                                            last_message = chat.action_id.message
                                            self.with_context({'stop_recur': True}).with_user(
                                                user_partner.id).message_post(
                                                body=last_message,
                                                message_type="whatsapp_message",
                                            )
                                        elif chat.action_id.last_message_conf == 'template':
                                            last_message = chat.action_id.wa_template_id
                                            whatsapp_composer = self.env["whatsapp.composer"].with_user(
                                                user_partner.id).with_context({
                                                "active_id": self.id,
                                                "is_chatbot": True,
                                                "wa_chatbot_id": self.wa_chatbot_id.id,
                                            }).create({
                                                "phone": partner_id.mobile or partner_id.phone,
                                                "wa_template_id": last_message.id,
                                                "res_model": last_message.model_id.model,
                                            })
                                            whatsapp_composer.with_context(
                                                {'stop_recur': True})._send_whatsapp_template()
                                        else:
                                            last_message = "We are connecting you with one of our experts. Please wait a moment."
                                            self.with_context({'stop_recur': True}).with_user(
                                                user_partner.id).message_post(
                                                body=last_message,
                                                message_type="whatsapp_message",
                                            )
                                            user_message = (
                                                    "You are now chatting with "
                                                    + available_operator.name
                                            )
                                            self.with_context({'stop_recur': True}).with_user(
                                                user_partner.id).message_post(
                                                body=user_message,
                                                message_type="whatsapp_message",
                                            )
                                else:
                                    if chat.action_id.no_operator_conf == 'message':
                                        last_message = chat.action_id.no_operator_message
                                        self.with_context({'stop_recur': True}).with_user(
                                            user_partner.id).message_post(
                                            body=last_message,
                                            message_type="whatsapp_message",
                                        )

                                    elif chat.action_id.no_operator_conf == 'template':
                                        last_message = chat.action_id.no_operator_template
                                        whatsapp_composer = self.env["whatsapp.composer"].with_user(
                                            user_partner.id).with_context({
                                            "active_id": self.id,
                                            "is_chatbot": True,
                                            "wa_chatbot_id": self.wa_chatbot_id.id,
                                        }).create({
                                            "phone": partner_id.mobile or partner_id.phone,
                                            "wa_template_id": last_message.id,
                                            "res_model": last_message.model_id.model,
                                        })
                                        whatsapp_composer.with_context(
                                            {'stop_recur': True})._send_whatsapp_template()
                                    else:
                                        last_message = "Apologies, but there are currently no active operators available. We will connect you with one shortly."
                                        self.with_context({'stop_recur': True}).with_user(
                                            user_partner.id).message_post(
                                            body=last_message,
                                            message_type="whatsapp_message",
                                        )



                            # if (
                            #         chat.action_id.binding_model_id.model
                            #         == "discuss.channel"
                            # ):
                            #     self.is_chatbot_ended = True
                            #     available_operator = False
                            #     active_operator = chatbot.mapped(
                            #         "user_ids"
                            #     ).filtered(lambda user: user.im_status == "online")
                            #     if active_operator:
                            #         wa_chatbot_channels = (
                            #             chatbot.mapped(
                            #                 "channel_ids"
                            #             )
                            #         )
                            #         for wa_channel in wa_chatbot_channels:
                            #             operators = active_operator.filtered(
                            #                 lambda av_user: av_user.partner_id
                            #                                 not in wa_channel.channel_member_ids.partner_id
                            #             )
                            #             if operators:
                            #                 for operator in operators:
                            #                     available_operator = operator.partner_id
                            #             else:
                            #                 available_operator = random.choice(active_operator).partner_id
                            #         if available_operator:
                            #             added_operator = (
                            #                 self.channel_partner_ids.filtered(
                            #                     lambda x: x.id == available_operator.id
                            #                 )
                            #             )
                            #             if added_operator:
                            #                 self.write(
                            #                     {
                            #                         "is_chatbot_ended": True,
                            #                         "wa_chatbot_id": False,
                            #                     }
                            #                 )
                            #             else:
                            #                 self.write(
                            #                     {
                            #                         "channel_partner_ids": [
                            #                             (4, available_operator.id)
                            #                         ],
                            #                         "is_chatbot_ended": True,
                            #                         "wa_chatbot_id": False,
                            #                     }
                            #                 )
                            #             mail_channel_partner = (
                            #                 self.env["discuss.channel.member"]
                            #                 .sudo()
                            #                 .search(
                            #                     [
                            #                         ("channel_id", "=", self.id),
                            #                         (
                            #                             "partner_id",
                            #                             "=",
                            #                             available_operator.id,
                            #                         ),
                            #                     ]
                            #                 )
                            #             )
                            #             mail_channel_partner.write({"is_pinned": True})
                            #             # wait_message = "We are connecting you with one of our experts. Please wait a moment."
                            #             wait_message = chat
                            #             self.with_context({'stop_recur': True}).with_user(user_partner.id).message_post(
                            #                 body=wait_message,
                            #                 message_type="whatsapp_message",
                            #             )
                            #             user_message = (
                            #                     "You are now chatting with "
                            #                     + available_operator.name
                            #             )
                            #             self.with_context({'stop_recur': True}).with_user(user_partner.id).message_post(
                            #                 body=user_message,
                            #                 message_type="whatsapp_message",
                            #             )
                            #     else:
                            #         no_user_message = "Apologies, but there are currently no active operators available."
                            #         self.with_context({'stop_recur': True}).with_user(user_partner.id).message_post(
                            #             body=no_user_message,
                            #             message_type="whatsapp_message",
                            #         )
                            #         user_message = (
                            #             "We will connect you with one shortly."
                            #         )
                            #         self.with_context({'stop_recur': True}).with_user(user_partner.id).message_post(
                            #             body=user_message,
                            #             message_type="whatsapp_message",
                            #         )
                            # self.sudo().write({
                            #     'child_wa_chatbot': False
                            # })
        return res


class ChatbotMailMessage(models.Model):
    _inherit = "mail.message"

    wa_chatbot_id = fields.Many2one(
        comodel_name="whatsapp.chatbot", string="Whatsapp Chatbot"
    )
    booking_id = fields.Many2one(comodel_name='helpdesk.order', string='Booking id')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if self._context.get("wa_chatbot_id"):
                whatsapp_chatbot = self.env["whatsapp.chatbot"].search(
                    [("id", "=", self._context.get("wa_chatbot_id"))]
                )
                if whatsapp_chatbot:
                    vals.update(
                        {
                            "wa_chatbot_id": whatsapp_chatbot.id,
                        }
                    )
        return super(ChatbotMailMessage, self).create(vals_list)
