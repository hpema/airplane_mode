# Copyright (c) 2024, hemant pema and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import *

class RentalContract(Document):
	def validate(self):
		rent_amount = frappe.db.get_single_value("Airport Shop Settings", 'default_rent_amount')
		frappe.msgprint(rent_amount)
		if self.rental_amount == 0 or self.rental_amount == None:
			self.rental_amount = rent_amount

		# Trigger print format using frappe.msgprint
		#frappe.get_print("Rent Reciept", self.name)