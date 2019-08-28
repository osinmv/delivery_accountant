import sqlite3
import datetime
import time


CUSTOMER = "Customers"
VENDOR = "Vendor"
CUSTOMER_DB = "customers"
VENDOR_DB = "vendors"

# docket INTEGER,date_client INTEGER,date_require INTEGER, date_shipment INTEGER, requirements BLOB, notes TEXT

# connection = sqlite3.connect("delivery.db")

# crsr = connection.cursor()
# crsr.execute("""
#            CREATE TABLE deliveries (
#            docket INTEGER PRIMARY KEY, customer TEXT, vendor TEXT, completed_tasks INTEGER,
#            date_client INTEGER, date_require INTEGER, date_shipmet INTEGER, tasks BLOB, note TEXT
#            );
#            """)
# crsr.execute("""CREATE TABLE customers (name TEXT, address TEXT, phone TEXT, contact TEXT); """)

"""
DO NOT FORGET TO ADD CONTEXT MANAGER, SO IF SOMETHING HAPPENS THE DB IS SAFE AND ALSO BACKUPS!!11!!1!1

"""
DATABASEPATH = "deliveries.db"

def create_tables():
    with sqlite3.connect(DATABASEPATH) as conn:
        crsr = conn.cursor()
        crsr.execute("""CREATE TABLE "deliveries" (
                        "docket"    INTEGER PRIMARY KEY ,
                        "customer"  TEXT,
                        "vendor"    TEXT,
                        "completed_tasks"   INTEGER,
                        "date_client"   TEXT,
                        "date_request"  TEXT,
                        "date_shipmet"  TEXT,
                        "tasks" TEXT,
                        "note"  TEXT,
                        "delivery_address"  TEXT,
                        "closed"    INTEGER,
                        PRIMARY KEY("docket")
                    );""")
        crsr.execute("""CREATE TABLE customers (name TEXT, address TEXT, phone TEXT, contact TEXT);""")
        crsr.execute("""CREATE TABLE vendors (name TEXT, address TEXT, phone TEXT, contact TEXT);""")
        crsr.execute("INSERT INTO customers VALUES (?,?,?,?)",("-","-","-","-"))
        crsr.execute("INSERT INTO vendors VALUES (?,?,?,?)",("-","-","-","-"))
        conn.commit()
        
def partners_list(db_name):
    """
    returns customer list for dropdownmenu
    """
    list_cust = None
    with sqlite3.connect(DATABASEPATH) as conn:
        conn.row_factory = generator
        crsr = conn.cursor()
        if db_name == CUSTOMER_DB:
            crsr.execute("""SELECT name FROM customers BYORDER;""")
        elif db_name == VENDOR_DB:
            crsr.execute("""SELECT name FROM vendors BYORDER;""")
        list_cust = crsr.fetchall()
    return list_cust

def update_docket(docket,tasks):
    with sqlite3.connect(DATABASEPATH) as conn:
        crsr = conn.cursor()
        crsr.execute("""UPDATE deliveries SET tasks=?,completed_tasks=? WHERE docket==?;""",(tasks[0],tasks[1],docket))
        conn.commit()


def partner_info(name, db_name):
    list_cust = None
    with sqlite3.connect(DATABASEPATH) as conn:
        conn.row_factory = generator
        crsr = conn.cursor()
        if db_name == CUSTOMER:
            crsr.execute("""SELECT * FROM customers WHERE name=?""", (name,))
        elif db_name == VENDOR:
            crsr.execute("""SELECT * FROM vendors WHERE name=?""", (name,))

        list_cust = crsr.fetchone()
        # supposed to be one if something happens call
    return list_cust


def select_by_customer(num=None):
    if num is None:
        num = 10
    entries = None
    with sqlite3.connect(DATABASEPATH) as conn:
        conn = sqlite3.connect("delivery.db")
        crsr = conn.cursor()
        crsr.execute(
            """SELECT docket, customer, date_client
            FROM deliveries WHERE customer=?""",
            ("Max&Co",))
        entries = crsr.fetchmany(num)

    return entries


def _check_data(data):
    for i in data:
        if i.isspace():
            raise ValueError


def submit_partner(data, db_name):
    """
    :parameter: data(list)
    :parameter: db_name(str) which table to put data in
    """
    with sqlite3.connect(DATABASEPATH) as conn:
        crsr = conn.cursor()
        if db_name == CUSTOMER:
            crsr.execute("""INSERT INTO customers VALUES (?,?,?,?)""",
                         (data[0], data[1], data[2], data[3]))
        elif db_name == VENDOR:
            crsr.execute("""INSERT INTO vendors VALUES (?,?,?,?)""",
                         (data[0], data[1], data[2], data[3]))
        conn.commit()


def get_open_tasks():
    data = None
    with sqlite3.connect(DATABASEPATH) as conn:
        conn.row_factory = generator
        crsr = conn.cursor()
        crsr.execute("""SELECT docket, customer, date_request, tasks FROM deliveries
                     WHERE completed_tasks=1 ORDER BY date_request""")
        data = crsr.fetchall()
    return data


def submit_delivery(data):
    """
    :parameters: data (list) gives entris in db order
    """
    with sqlite3.connect(DATABASEPATH) as conn:
        crsr = conn.cursor()
        crsr.execute(
            """
            INSERT INTO deliveries VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """,
            (crsr.lastrowid, data[0], data[1], data[2], data[3], data[4],
             data[5], data[6], data[7], data[8],0))
        conn.commit()


def get_delivery(docket):
    """Returns a delivery by docket number"""
    delivery = None
    with sqlite3.connect(DATABASEPATH) as conn:
        conn.row_factory = generator
        crsr = conn.cursor()
        crsr.execute("""SELECT * FROM deliveries WHERE docket=?""", (docket,))
        delivery = crsr.fetchone()
    return delivery

def generator(crsr,row):
    dictionary = {}
    for i, col in enumerate(crsr.description):
        dictionary[col[0]] = row[i]
    return dictionary

def get_recent(num=None):
    if num is None:
        num = 10
    data = []
    with sqlite3.connect(DATABASEPATH) as conn:
        conn.row_factory = generator
        crsr = conn.cursor()
        crsr.execute("""
                    SELECT docket, customer, date_shipmet, delivery_address
                    FROM deliveries ORDER BY date_shipmet DESC
                    """)
        data = crsr.fetchmany(num)
    return data
# TODO change column name to date_shipment instead of shipment


def neat_data(data):
    """
    returns list of neat strings
    data should not include blob
    !!!ESPECIALLY DONE FOR GET RECENT FUNCTION!!!
    """
    neat_data = []
    dockets = []
    for i in data:
        neat_str = "Docket# : {} \n Customer : {} \n Date Shipment {} \n Delivery Address : \n {}".format(
            i[0], i[1], i[2], i[3])
        neat_data.append(neat_str)
        dockets.append(i[0])
    return [neat_data, dockets]


def neat_time(seconds):
    date = datetime.date.fromtimestamp(seconds)
    return "{}/{}/{}".format(date.day, date.month, date.year)


def raw_time(self, time_str):
    return time.mktime(datetime.timetuple())


def parse_tasks(data):
    if data is None:
        return ["","",""]
    data = data.split("\n")
    data.remove("")
    neat_data = []
    for i in data:
        neat_data.append(i.split("|"))
    return neat_data
