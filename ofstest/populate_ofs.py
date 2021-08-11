import mysql.connector
import frappe

def table_from_ofs(column_name, date):
	mydb = mysql.connector.connect(
		host="172.26.2.28",
		user="root",
		password="i5ECPIo4znoy4Ea",
		database="ofs_shg"
	)

	mycursor = mydb.cursor()
	mycursor.execute("select " + column_name + " from ofs_orders where order_date like '" + date + "%'")
	column_data = mycursor.fetchall()
	return column_data

def populate_ofs_orders(ordernum, status, amount, woocommerceids):
	for i in range(len(status)):
		try:
			order = frappe.get_doc('Order Monitoring', str(ordernum[i]))
			order.status = status[i]
			order.save()
		except:
			order = frappe.get_doc({
				'doctype':'Order Monitoring', 
				'orderid': ordernum[i],
				'status': status[i], 
				'orderamount': amount[i],
				'woocommerceid': woocommerceids[i]
			})
			order.insert(ignore_permissions=True)
	frappe.db.commit()

def main():
	ordernum = table_from_ofs("order_number", "2021-08-03")
	status = table_from_ofs("status_text", "2021-08-03")
	amount = table_from_ofs("total_gross", "2021-08-03")
	woocommerceids = table_from_ofs("woocommerce_post_id", "2021-08-03")
	populate_ofs_orders(ordernum, status, amount, woocommerceids)
