// Copyright (c) 2024, hemant pema and contributors
// For license information, please see license.txt

 frappe.ui.form.on("Airplane Ticket", {
 	refresh(frm) {
        console.log("Form refresh");
    },
 });

 frappe.ui.form.on("Airplane Ticket Add-on Item", {
    item: function(frm,cdt, cdn){
        let row = frappe.get_doc(cdt,cdn); 
        let idx = row.idx;
        let item_added = row.item 
        
        if(item_added !=''){
            $.each(frm.doc.add_ons,  function(i,  d) {
                if(d.item == item_added && d.idx!=idx){
                    frm.fields_dict.add_ons.grid.grid_rows_by_docname[cdn].remove();
                    frappe.throw("Item: " + item_added + " is not unique. Add on already on the list");
                }
            });
        }
    },
    amount: function(frm,cdt, cdn){
        let row = frappe.get_doc(cdt,cdn); 
        let total = 0;
        $.each(frm.doc.add_ons,  function(i,  d) {
            total = total + d.amount;
            console.log(d.amount, total);
        });
        console.log(total);
        console.log(frm.doc.flight_price);
        console.log(frm.doc.total_amount);
        frm.set_value("total_amount", frm.doc.flight_price + total);
    }
 })