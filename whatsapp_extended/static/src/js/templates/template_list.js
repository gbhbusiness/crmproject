/* @odoo-module */
import { ActionPanel } from "@mail/discuss/core/common/action_panel";

import { Dialog } from "@web/core/dialog/dialog";
import { Component, onWillStart, onWillUpdateProps, useState } from "@odoo/owl";
import { View } from "@web/views/view";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";


export class TemplateListPanel extends Component {
    static components = {
        ActionPanel,
        View,
    };
    static props = [ "className?"];
    static template = "discuss.AgentListPanel";

    setup() {
        this.store = useService("mail.store");
        this.rpc = useService("rpc");
        const buttonTemplate = "web.FormViewDialog.ToMany.buttons";
        this.TemplateListService = useState(useService("discuss.TemplateListPanel"));
        if (this.props.thread && this.props.thread.correspondent2 && this.props.thread.correspondent2.id){
            this.viewProps = {
                type: "list",
                buttonTemplate,
                context: {"partner": this.props.thread && this.props.thread.correspondent2 && this.props.thread.correspondent2.id},
                display: { controlPanel: false },
                domain: [['model_id', '=', 'res.partner'],['status','=','approved']], // add this line
                resId: this.props.thread.correspondent2.id,
                resModel: 'whatsapp.template',
            };
        }
        else{
             this.viewProps = {
                type: "list",
                buttonTemplate,
                context: {},
                display: { controlPanel: false },
                resId: false,
                resModel: 'whatsapp.template',
            };
        }
    }

    async discardRecord() {
        if (this.props.onRecordDiscarded) {
            await this.props.onRecordDiscarded();
        }
    }


    onClickUnpin(message) {
        this.TemplateListService.unpin(message);
    }


    get emptyText() {
        if (this.props.thread.type === "channel") {
            return _t("This channel doesn't have any pinned messages.");
        } else {
            return _t("This conversation doesn't have any pinned messages.");
        }
    }

    get title() {
        return _t("WhatsApp Templates");
    }
}

TemplateListPanel.props = {
    thread: { type: Object, optional: true },

    context: { type: Object, optional: true },
    mode: {
        optional: true,
        validate: (m) => ["edit", "readonly"].includes(m),
    },
    onRecordSaved: { type: Function, optional: true },
    onRecordDiscarded: { type: Function, optional: true },
    removeRecord: { type: Function, optional: true },
    resId: { type: [Number, Boolean], optional: true },
    title: { type: String, optional: true },
    viewId: { type: [Number, Boolean], optional: true },
    preventCreate: { type: Boolean, optional: true },
    preventEdit: { type: Boolean, optional: true },
    isToMany: { type: Boolean, optional: true },
    size: Dialog.props.size,
};
TemplateListPanel.defaultProps = {
    onRecordSaved: () => {},
    preventCreate: true,
    preventEdit: false,
    isToMany: false,
};
