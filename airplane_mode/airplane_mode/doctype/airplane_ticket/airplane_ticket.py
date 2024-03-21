# Copyright (c) 2024, hemant pema and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AirplaneTicket(Document):
	
	def before_validate(self):
		total = 0
		for line in self.add_ons:
			total = total + line.amount

		self.total_amount = self.flight_price + total

	def validate(self):
		pass