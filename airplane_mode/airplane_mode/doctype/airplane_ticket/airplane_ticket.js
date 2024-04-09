// Copyright (c) 2024, hemant pema and contributors
// For license information, please see license.txt

 frappe.ui.form.on("Airplane Ticket", {
 	refresh(frm) {
        frm.refresh_field("add_ons");
        frm.add_custom_button(__('Assign Seat'), function(){

            let d = new frappe.ui.Dialog({
                title: 'Enter details',
                fields: [
                    {
                        label: 'Seat Number',
                        fieldname: 'seat_number',
                        fieldtype: 'Data'
                    }
                ],
            
                size: 'small', // small, large, extra-large 
                primary_action_label: 'Assign',
                primary_action(values) {
                    frm.set_value('seat', values.seat_number);
                    frm.save();
                    d.hide();
                }
            });
            
            d.show();

          }, __('Actions'));
    },
    flight_price(frm){
        frm.trigger("update_total_amount");
    },
    update_total_amount(frm){
        let total = 0;
        for(let item of frm.doc.add_ons){
            total = total + item.amount;
        }
        frm.set_value("total_amount", frm.doc.flight_price + total);
    },
    
 });

 

 frappe.ui.form.on("Airplane Ticket Add-on Item", {
    item(frm,cdt, cdn){
        let row = frappe.get_doc(cdt,cdn); 
        let idx = row.idx;
        let item_added = row.item 
        
        if(item_added !=''){
            for(let item of frm.doc.add_ons){
                if(item.item == item_added && item.idx!=idx){
                    //console.log("Duplicate: ", row.name);
                    frm.fields_dict.add_ons.grid.grid_rows_by_docname[cdn].remove();
                    frappe.throw("Item: " + item_added + " is not unique. Add on already on the list");
                }
            }
        }
    },
    amount(frm,cdt, cdn){
        frm.trigger("update_total_amount");
    }
 })