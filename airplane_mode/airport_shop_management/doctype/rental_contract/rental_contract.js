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
