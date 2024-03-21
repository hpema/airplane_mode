# Copyright (c) 2024, hemant pema and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import log, _

class FlightPassenger(Document):
	
	def before_save(self):
		frappe.msgprint(f'{self.first_name} {self.last_name or ""}')
		self.full_name = f'{self.first_name} {self.last_name or ""}'
