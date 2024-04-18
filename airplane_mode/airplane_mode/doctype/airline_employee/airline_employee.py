# Copyright (c) 2024, hemant pema and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AirlineEmployee(Document):
	def before_save(self):
		if self.last_name:
			self.full_name = f'{self.first_name} {self.last_name or ""}'
		else:
			self.full_name = f'{self.first_name}'

	def before_naming(self):
		if not self.full_name:
			if self.last_name:
				self.full_name = f'{self.first_name} {self.last_name or ""}'
			else:
				self.full_name = f'{self.first_name}'
    
