import mysql.connector
import frappe

#connect to ofs order tables
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

#get sales doctype from erpnext
def get_sales_doctype(woocommerceids):
	salesorders = [0] * len(woocommerceids)
	for i in range(len(woocommerceids)):
		name = frappe.db.get_value('Sales Order', {'woocommerce_id': woocommerceids[i][0]}, 'name')
		salesorders[i] = name
	return salesorders

#get customer doctype from erpnext
def get_customer_doctype(salesorders):
	customers = [0] * len(salesorders)
	for i in range(len(salesorders)):
		salesdoc = frappe.get_doc('Sales Order', salesorders[i])
		customers[i] = salesdoc.customer
	return customers

#connect to ofs store table
def ofs_store_table(column_name, id):
	mydb = mysql.connector.connect(
		host="172.26.2.28",
		user="root",
		password="i5ECPIo4znoy4Ea",
		database="ofs_shg"
	)

	mycursor = mydb.cursor()
	mycursor.execute("select " + column_name + " from ofs_stores where id like " + id)
	column_data = mycursor.fetchall()
	return column_data

def get_stores(column_name, storeids):
	array = [0] * len(storeids)
	for i in range(len(storeids)):
		array[i] = ofs_store_table(column_name, storeids[i])
	return array

def get_store_doc(storename, storeid, storecode, storeaddress):
	try:
		store = frappe.get_doc('Order Monitoring', str(storename))			
		return store
	except:
		store = frappe.get_doc({				
			'doctype':'Order Monitoring', 
			'storename': storename,
			'storeid': storeid, 
			'storecode': storecode,
			'address': storeaddress
		})
		store.insert(ignore_permissions=True)
		return store
frappe.db.commit()

def populate_ofs_orders(ordernum, status, amount, woocommerceids, salesorders, customers):
	for i in range(len(status)):
		try:
			order = frappe.get_doc('Order Monitoring', str(ordernum[i][0]))
			order.status = status[i][0]
			order.save()
		except:
			order = frappe.get_doc({
				'doctype':'Order Monitoring', 
				'orderid': ordernum[i][0],
				'status': status[i][0], 
				'orderamount': amount[i][0],
				'woocommerceid': woocommerceids[i][0],
				'salesorder': salesorders[i],
				'customer': customers[i]
			})
			order.insert(ignore_permissions=True)
	frappe.db.commit()

def main():
	ordernum = table_from_ofs("order_number", "2021-08-03")
	status = table_from_ofs("status_text", "2021-08-03")
	amount = table_from_ofs("total_gross", "2021-08-03")
	woocommerceids = table_from_ofs("woocommerce_post_id", "2021-08-03")
	salesorders = get_sales_doctype(woocommerceids)
	customers = get_customer_doctype(salesorders)

	#getstore
	storeids = table_from_ofs("store_id", "2021-08-03")
	storenames = get_stores("store_name", storeids)
	storecodes = get_stores("code", storeids)
	storeaddresses = get_stores("address", storeids)
	
	populate_ofs_orders(ordernum, status, amount, woocommerceids, salesorders, customers)
