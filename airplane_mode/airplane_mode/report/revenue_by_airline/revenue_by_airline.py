# Copyright (c) 2024, hemant pema and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):

	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	columns = [
	{
		"label": "Airline",
		"fieldname": "airline",
		"fieldtype": "Link",
		"options": "Airline",
	},
	{
		"label": "Revenue",
		"fieldname": "revenue",
		"fieldtype": "Currency",
	}
	]

	return columns


def get_data(filters=None):

	data = []
	airplane_ticket = frappe.qb.DocType("Airplane Ticket")
	airplane_flight = frappe.qb.DocType("Airplane Flight")
	airplane = frappe.qb.DocType("Airplane")
	# airline = frappe.qb.DocType("Airline")
	
	query = (
     	frappe.qb.from_(airplane_ticket)
		.join(airplane_flight)
		.on(airplane_ticket.flight == airplane_flight.name)
		.join(airplane)
		.on(airplane_flight.airplane == airplane.name)
		.select(
		airplane.airline.as_("airline"),
		airplane_ticket.total_amount
		)
	)

	ticket_items = query.run(as_dict=True)
	# group Tickets items by Airline
	airline_items = {}
	
	for ticket_item in ticket_items:
		airline_items.setdefault(ticket_item.airline, []).append(ticket_item)
	
	# frappe.errprint(airline_items)
 	# {'Emirates': [{'airline': 'Emirates', 'total_amount': 759.0}, {'airline': 'Emirates', 'total_amount': 1564.0}, {'airline': 'Emirates', 'total_amount': 1500.0}, {'airline': 'Emirates', 'total_amount': 1500.0}, {'airline': 'Emirates', 'total_amount': 1500.0}], 'Qatar': [{'airline': 'Qatar', 'total_amount': 1500.01}]}
 	# create a row for each Airline
	for airline, ticket_items in airline_items.items():
		#frappe.errprint(airline)
		#frappe.errprint(ticket_items)
		total = 0
		for item in ticket_items:
			total = total + item.total_amount

		#frappe.errprint(total)
		row = {
			"airline": airline,
			"revenue": format_currency(total)
			}
		data.append(row)
		#frappe.errprint(data)
	return data

def format_currency(value, currency="AED"):
	return frappe.format_value(value, df={"fieldtype": "Currency"}, currency=currency)