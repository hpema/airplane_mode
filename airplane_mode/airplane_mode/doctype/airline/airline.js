// Copyright (c) 2024, hemant pema and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airline", {
	refresh(frm) {
        const web_link = frm.doc.website;
        frm.add_web_link(web_link, "Visit Website");
	}
});
