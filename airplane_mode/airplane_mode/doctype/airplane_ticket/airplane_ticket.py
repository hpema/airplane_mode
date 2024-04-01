# Copyright (c) 2024, hemant pema and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import random
from random import randint


class AirplaneTicket(Document):
	

	def validate(self):
		items = set()
		rows_to_remove = []

		for item in self.add_ons:
			if item.item in items:
				#frappe.msgprint(item.item + ":" + item.name)
				rows_to_remove.append(item.name)
			else:
				items.add(item.item)

		if rows_to_remove:
			for name in rows_to_remove:  # Remove in reverse order to avoid index shifting
				for item in self.add_ons:
					if item.name == name:
						#frappe.msgprint(name)
						self.add_ons.remove(item)

				#frappe.delete_doc("Airplane Ticket Add-on Item", name)
				#frappe.msgprint(name)

	def before_save(self):
		total = 0.00
		for line in self.add_ons:
			total += line.amount

		self.total_amount = float(self.flight_price) + total
	
	def before_submit(self):
		if self.status != "Boarded":
			frappe.throw('Cannot submit ticket if not boarded.')
			
	
	def before_insert(self):
		rows = ['A','B','C','D','E']
		seatnumber = str(randint(1,90))+random.choices(rows,k=1)[0]
		self.seat = seatnumber
