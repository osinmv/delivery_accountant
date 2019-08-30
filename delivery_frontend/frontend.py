import tkinter as tk
import tkinter.ttk as ttk
#from request_data import request_by_docket, request_partner_info, request_partners, request_recent
import datetime
from backend import get_recent, partners_list, get_delivery, submit_partner, submit_delivery, update_docket, close_docket
from pdf_writer import report_open_tasks
from tkcalendar import DateEntry
from frames.dates import Date
from frames.delivery_info import Delivery_Info
from frames.menu import Menu
from frames.notes import Note
from frames.partner_info import Partner
from frames.search_dockets import Docket_Search
from frames.tasks import Tasks
import json
CUSTOMER = "Customers"
VENDOR = "Vendor"
CUSTOMER_DB = "customers"
VENDOR_DB = "vendors"
# import logging
# to start logging the parts of the app

LENGTH_DOCKETS = 11
BASECOLOR = "gainsboro"
SECONDARYCOLOR = "snow2"
HIGHFONT = ("Open Sans", "12")
BASICFONT = ("Open Sans", "12")
ENTRYFONT = ("Open Sans", "12")


class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Delivery Accountant")
        self.master.minsize(1440, 1080)
        self.master.resizable(True, True)
        self.menu = Menu(self.master, self.new_delivery,
                         self.new_partner, report_open_tasks)
        # column=0, row=0, columnspan=2, rowspan=6, pady=10, padx=10, sticky="NESW")
        self.search_dockets = Docket_Search(
            self.master, get_recent(), self.update_by_docket, 0, 0, 2, 6)

        self.customer = Partner(
            self.master, CUSTOMER, CUSTOMER_DB, pos_x=2, pos_y=0, span_x=2, span_y=2)
        self.customer.update_partners(event=None)
        self.vendor = Partner(self.master, VENDOR, VENDOR_DB,
                              pos_x=2, pos_y=2, span_x=2, span_y=2)
        self.vendor.update_partners(event=None)

        self.dates = Date(self.master, pos_x=4, pos_y=0, span_x=2, span_y=2)
        self.notes = Note(self.master, pos_x=4, pos_y=2, span_x=2, span_y=2)
        self.tasks = Tasks(self.master, pos_x=2, pos_y=4,
                           span_x=4, span_y=4, length=10)
        self.delivery_info = Delivery_Info(
            self.master, pos_x=6, pos_y=0, span_x=2, span_y=1)

        self.btn_submit = ttk.Button(text="Submit")
        self.btn_submit.grid(column=0, row=11, columnspan=2,
                             rowspan=2, sticky="NESW")
        self.btn_close_docket = ttk.Button(text="Close Docket")
        self.btn_close_docket.grid(column=0, row=13, columnspan=2,
                                   rowspan=2, sticky="NESW")

    def close_docket(self):
        close_docket(self.delivery_info.get_docket().split(" ")[2])

    def new_delivery(self):
        self.set_active()
        self.clear_all()
        self.btn_submit.configure(
            command=lambda: submit_delivery(self.read_delivery_entries()))

    def new_partner(self, partner):
        db = None
        if partner == CUSTOMER:
            partner = self.customer
            db = CUSTOMER_DB
        elif partner == VENDOR:
            partner = self.vendor
            db = VENDOR_DB
        partner.activate_all()
        self.btn_submit.configure(
            command=lambda: submit_partner(partner.new_partner(), db))
        partner.clear_info()

    def read_delivery_entries(self):
        data = {
            "customer": self.customer.get_partner(),
            "vendor": self.vendor.get_partner()
        }
        tasks, done = self.tasks.read_tasks()

        if done:
            done = 1
        else:
            done = 0
        data["completed_tasks"] = done
        for k, v in self.dates.read_date().items():
            data[k] = v
        data["tasks"] = tasks
        data["note"] = self.notes.read_notes()
        data["delivery_address"] = self.delivery_info.read()
        data["closed"] = 0
        self.clear_all()
        self.btn_submit.configure(command=None)
        return data

    def clear_all(self):
        self.tasks.clear_all()
        self.dates.clear_dates()
        self.vendor.clear_info()
        self.customer.clear_info()
        self.notes.clear_notes()
        self.delivery_info.clear()

    def update_by_docket(self, event):
        # this method parses widget text because of the explained below
        """
            found intersting bug(probably just the thing that not all people know) in python
            if you bind label(may work with other widgets) in a loop(which uses range(0,somenumber))
            with the callback the last value of i or other iterator will be passed to function!
        """

        self.set_active()
        self.clear_all()

        # docket, customer, vendor, completed_tasks, date_client, date_require,
        # date_shipment, tasks, note, delivery address
        data = None

        docket = int(event.widget["text"].split("\n")[0].split(" ")[2])
        data = get_delivery(docket)
        if data is None:
            # create a message that will say that something wrong was inputed
            pass
        else:
            self.btn_close_docket.configure(comman=self.close_docket)
            self.btn_submit.configure(command=lambda: update_docket(
                docket, self.tasks.read_tasks()))
            self.customer.update_info(event=None, name=data["customer"])
            self.vendor.update_info(event=None, name=data["vendor"])
            # fix shipmet to shipment in db
            self.dates.update_dates(
                [data["date_client"], data["date_request"],
                 data["date_shipment"]])
            self.tasks.update_tasks(json.loads(data["tasks"]))
            # update notes
            self.notes.update_notes(data["note"])
            # update delivery address
            self.delivery_info.update_delivery_info(
                data["delivery_address"], data["docket"])
        self.readonly_mode()

    def readonly_mode(self):
        self.customer.deactivate_all()
        self.vendor.deactivate_all()
        self.dates.deactivate_all()
        self.notes.deactivate()
        self.tasks.deactivate_all()
        self.delivery_info.deactivate()

    def set_active(self):
        self.btn_close_docket.configure(comman=None)
        self.customer.activate_all()
        self.vendor.activate_all()
        self.dates.activate_all()
        self.notes.activate()
        self.tasks.activate_all()
        self.delivery_info.activate()


root = tk.Tk()
app = MainWindow(master=root)
root.mainloop()
