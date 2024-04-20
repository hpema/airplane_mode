// Copyright (c) 2024, hemant pema and contributors
// For license information, please see license.txt

frappe.ui.form.on("Rental Contract", {
	refresh(frm) {
        if(frm.is_new()){
             frappe.db.get_single_value("Airport Shop Settings", 'default_rent_amount').then((rent_amount) => {
               if (frm.rental_amount == 0 || frm.rental_amount == null){
                   frm.set_value("rental_amount", rent_amount);
                   console.log(frm.rental_amount);
               }
            });
        }   
        
	},
});



frappe.ui.form.on("Rent Due", {
    payment_received(frm,cdt, cdn){
        let row = frappe.get_doc(cdt,cdn); 
        let idx = row.idx;
        //let item_added = row.item 
        
        //if(item_added !=''){
        //    for(let item of frm.doc.add_ons){
        //        if(item.item == item_added && item.idx!=idx){
        //            //console.log("Duplicate: ", row.name);
        //            frm.fields_dict.add_ons.grid.grid_rows_by_docname[cdn].remove();
        //            frappe.throw("Item: " + item_added + " is not unique. Add on already on the list");
        //        }
        //    }
       // }
       console.log("Burron pressed on row " + idx);
    },
   // amount(frm,cdt, cdn){
   //     frm.trigger("update_total_amount");
   // }
 })