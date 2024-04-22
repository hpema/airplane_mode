// Copyright (c) 2024, hemant pema and contributors
// For license information, please see license.txt

frappe.ui.form.on("Rental Contract", {
	refresh(frm) {
        if(frm.is_new()){
             frappe.db.get_single_value("Airport Shop Settings", 'default_rent_amount').then((rent_amount) => {
               if (frm.doc.rental_amount == 0 || frm.doc.rental_amount == null){
                   frm.set_value("rental_amount", rent_amount);
                   console.log(frm.doc.rental_amount);
               }
            });
        }   
        if(frm.doc.end_date==null){
            console.log(addMonthsToDate(frm.doc.start_date, 12));
            frm.set_value("end_date",addMonthsToDate(frm.doc.start_date, 12));
        }
        frm.refresh_field("add_ons");
	},
    end_date(frm){
        if(frm.doc.end_date <= frm.doc.start_date){
            console.log("End date to be in the future of start date.")
        }else{
            let enddate = new Date(frm.doc.end_date);
            let startdate = new Date(frm.doc.startdate);

        }
    },
    start_date(frm){
            frm.set_value("end_date",addMonthsToDate(frm.doc.start_date, 12));
    },
    on_submit(frm){
        frm.reload_doc();
    }
    
});



frappe.ui.form.on("Rent", {
    payment_received(frm,cdt, cdn){
        let row = frappe.get_doc(cdt,cdn); 
        let idx = row.idx;
        frappe.call({
            method: 'airplane_mode.airport_shop_management.doctype.rental_contract.rental_contract.receive_payment',
            args: {
                doctype: cdt,
                name: cdn
            },
            // disable the button until the request is completed
            btn: $('.primary-action'),
            // freeze the screen until the request is completed
            freeze: true,
            callback: (r) => {
                if (r.message){
                    //frm.trigger("refresh");
                    frm.reload_doc();
                    //console.log(r.message);
                    //console.log(frm.fields_dict.rent_due.grid.grid_rows_by_docname[cdn]);
                    //frm.fields_dict.rent_due.grid.grid_rows_by_docname[cdn].refresh()
                    //frm.refresh();
                }else
                {
                    frappe.msgprint("Rent already paid")
                }
            },
            error: (r) => {
                // on error
                console.log("error");
            }
        })
    },
   // amount(frm,cdt, cdn){
   //     frm.trigger("update_total_amount");
   // }
 })

function addMonthsToDate(startDate, monthsToAdd) {
    // Create a new Date object from the start date
    var date = new Date(startDate);
  
    // Add the number of months to the date's month property
    date.setMonth(date.getMonth() + monthsToAdd);
    
    // Return the formatted end date string
    return formatDate(date);
  }
  
 function formatDate(date) {
    var year = date.getFullYear();
    var month = String(date.getMonth() + 1).padStart(2, '0');
    var day = String(date.getDate()).padStart(2, '0');
  
    // Return formatted date string (e.g., YYYY-MM-DD)
    return year + "-" + month + "-" + day;
  }