/* @odoo-module */

import { threadActionsRegistry } from "@mail/core/common/thread_actions";
import { AgentListPanel } from "@whatsapp_extended/js/agents/agent_list";
import { TemplateListPanel } from "@whatsapp_extended/js/templates/template_list";

import { useChildSubEnv } from "@odoo/owl";

import { _t } from "@web/core/l10n/translation";

threadActionsRegistry.add("agent-list", {
    component: AgentListPanel,

    condition(component) {
        return (
            component.thread.type === 'whatsapp' && component.thread?.model === "discuss.channel" &&
            (!component.props.chatWindow || component.props.chatWindow.isOpen)
        );
    },
    panelOuterClass: "o-discuss-AgentListPanel",
    icon: "fa fa-fw fa-user",
    iconLarge: "fa fa-fw fa-lg fa-user",
    name: _t("Client"),
    nameActive: _t("Hide Agent List"),
    sequence: 20,
    setup(action) {
        useChildSubEnv({
            pinMenu: {
                open: () => action.open(),
                close: () => {
                    if (action.isActive) {
                        action.close();
                    }
                },
            },
        });
    },
    toggle: true,
});

threadActionsRegistry.add("template-list", {
    component: TemplateListPanel,
    condition(component) {
        return (
            component.thread.type === 'whatsapp' && component.thread?.model === "discuss.channel" &&
            (!component.props.chatWindow || component.props.chatWindow.isOpen)
        );
    },
    panelOuterClass: "o-discuss-TemplateListPanel",
    icon: "fa fa-fw fa-file",
    iconLarge: "fa fa-fw fa-lg fa-file",
    name: _t("Templates"),
    nameActive: _t("Hide Template List"),
    sequence: 20,
    setup(action) {
        useChildSubEnv({
            pinMenu: {
                open: () => action.open(),
                close: () => {
                    if (action.isActive) {
                        action.close();
                    }
                },
            },
        });
    },
    toggle: true,
});
