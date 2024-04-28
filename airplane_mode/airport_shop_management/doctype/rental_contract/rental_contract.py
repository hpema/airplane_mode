# Copyright (c) 2024, hemant pema and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import *
from frappe.query_builder import DocType
from frappe.query_builder.functions import Count
from pypika.terms import Case
from datetime import date, timedelta

class RentalContract(Document):
	def validate(self):
		rent_amount = frappe.db.get_single_value("Airport Shop Settings", 'default_rent_amount')
		if self.rental_amount == 0 or self.rental_amount == None:
			self.rental_amount = rent_amount
			frappe.errprint(self.rental_amount)

		# Trigger print format using frappe.msgprint
		#frappe.get_print("Rent Reciept", self.name)
	def before_submit(self):
		date = frappe.utils.add_days(frappe.utils.add_months(self.start_date,1),-1)
		self.receipt_date = frappe.utils.add_months(date,1)
		self.total_amount_due = self.rental_amount*12
		self.total_amount_paid = 0 
		self.outstanding_amount = self.total_amount_due
  
	def on_submit(self):
		#print(self.name)
		Rent = frappe.qb.DocType("Rent")
		q = (
			frappe.qb.from_(Rent)
			.select(Rent.name)
			.where(Rent.parent == self.name)
		).run(as_dict=True)
		#print(q)
		for r in q:
			#print(r)
			frappe.delete_doc("Rent",r.name)
		
		date = frappe.utils.add_days(frappe.utils.add_months(self.start_date,1),-1)
		for i in range(12):
			#print(frappe.utils.add_months(date,i))
			rent = frappe.get_doc({
				"doctype": "Rent",
				"rental_amount": self.rental_amount,
				"parent": self.name,
				"parenttype": "Rental Contract",
				"parentfield": "rent_due",
				"due_date": frappe.utils.add_months(date,i),
				"idx":i+1
       			})
			rent.insert()
		#self.reload()

@frappe.whitelist()
def receive_payment(doctype, name):
    line = frappe.get_doc(doctype,name)#qb.update(doctype).,name)
    if line.paid_amount == 0:
        #line.paid_amount = line.rental_amount
        line.db_set("paid_amount",line.rental_amount)
        line.db_set("paid_on",frappe.utils.today())
        parent = frappe.get_doc(line.parenttype,line.parent)
        parent.db_set("receipt_date", line.paid_on)
        
        line.save()
        frappe.db.commit()
        return line.paid_amount
    else:
        return 0
