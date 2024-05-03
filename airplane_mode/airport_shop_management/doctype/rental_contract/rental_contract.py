# Copyright (c) 2024, hemant pema and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import *
from frappe.query_builder import DocType
from frappe.query_builder.functions import Count
import frappe.utils
import frappe.utils.dateutils
from pypika.terms import Case
from frappe.utils.data import nowdate, getdate, now, get_datetime
from frappe.utils.background_jobs import enqueue

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
		self.paid_amount = 0
		shop = frappe.get_doc("Shop", self.shop)
		#start_date = datetime.date(self.start_date)
		#end_date = datetime.date(self.end_date)
		if self.start_date <= nowdate() and nowdate() < self.end_date:
			shop.db_set("occupied", 1)
		if self.end_date <= nowdate():
			shop.db_set("available_to_lease",1)
			shop.db_set("occupied",0)

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
        parent.db_set("total_amount_paid", parent.total_amount_paid + line.rental_amount)
        parent.db_set("outstanding_amount", parent.total_amount_due - parent.total_amount_paid)
        parent.db_set("receipt_date", line.paid_on)
        line.db_set("reminder_sent",1)
        
        #line.save()
        #frappe.db.commit()
        return line.paid_amount
    else:
        return 0

@frappe.whitelist()
def send_statements():
	frappe.errprint("flag: " + str(frappe.db.get_single_value("Airport Shop Settings", "send_out_reminders")))
	if frappe.db.get_single_value("Airport Shop Settings", "send_out_reminders"):
		frappe.sendmail()
		data = []
		parent = frappe.qb.DocType("Rental Contract")
		child = frappe.qb.DocType("Rent")
		tenant = frappe.qb.DocType("Tenant")
  
		first_day = get_first_day(nowdate())
		last_day = get_last_day(nowdate())

		query = (
			frappe.qb.from_(parent)
			.from_(child)
			.select(
			parent.full_name,
			parent.name,
			parent.shop,
			child.due_date,
			parent.full_name,
			parent.tenant,
			child.rental_amount,
			child.name.as_("rent_name")
			)
			.where(parent.name == child.parent)
			.where(parent.docstatus == 1)
			.where(child.reminder_sent == 0)
			.where(child.due_date.between(first_day,last_day))
		)
		notifications = query.run(as_dict=True)
		
		for due in notifications:
			frappe.errprint(due)
			tenant = frappe.get_doc("Tenant", due["tenant"])
			frappe.errprint(tenant.email)
   
			"""send email with payment link"""
			email_args = {
				"recipients": tenant.email,
				"sender": None,
				"subject": "Payment due on rental contract",
				"message": "Hi " + tenant.full_name + "<br /><p>You monthly rental for shop: " + due["shop"] + " of " + str(due["rental_amount"]) + " is payable by " + format_date(due["due_date"]) + ". ",
				"now": True,
				"attachments": [],
			}
			enqueue(method=frappe.sendmail, queue="short", timeout=300, is_async=True, **email_args)
			frappe.db.set_value("Rent",due["rent_name"],"reminder_sent",1)