/** @odoo-module **/

import { jsonrpc } from "@web/core/network/rpc_service";

$('select[name="ticket_type_id"]').change(function(ev){
    console.log(ev);
    var ticket_type_id =  $('select[name="ticket_type_id"]').val();
    jsonrpc(
        "/helpdesk/type_info/" + ticket_type_id, {'ticket_type': ticket_type_id}
    ).then(function (data) {
        console.log("data........", data, data.services[0]);
        var selectStates = $(".service_data");
        // if (selectStates.find('input').length) {
            if (data.services.length) {
                selectStates.html('');
                $.each(data.services, function (x, y) {
                    var opt = $(
                        '<input type="checkbox" class="s_website_form_input form-check-input" name=services_ids><label>')
                    .text(y[1])
                    .attr('value', y[0])
                    .attr('data-code', y[0])
                    .attr('id', y[0]);
                    selectStates.append(opt);
                    selectStates.append("<br/>");
                    console.log("x.....", x, y);
                    console.log("data.services..........", data.services);
                });
                selectStates.parent('div').show();
            } else {
                selectStates.val('').parent('div').hide();
            }
            selectStates.data('init', 0);
    }); 
});

$('select[name="project_id"]').change(function(ev){
    console.log(ev);
    var project_id =  $('select[name="project_id"]').val();
    jsonrpc(
        "/helpdesk/project/" + project_id, {'project_id': project_id}
    ).then(function (data) {
        var selectProjects = $(".tower_data");
        if (data.towers.length) {
            selectProjects.html('');
            $.each(data.towers, function (x, y) {
                var opt = $('<option>').text(y[1])
                    .attr('value', y[0])
                    .attr('data-code', y[0]);
                selectProjects.append(opt);
                selectProjects.append("<br/>");
            });
            selectProjects.parent('div').show();
        } else {
            selectProjects.val('').parent('div').hide();
        }
        selectProjects.data('init', 0);
    }); 
});
