import tkinter as tk
import tkinter.ttk as ttk
from request_data import request_by_docket, request_partner_info, request_partners, request_recent
import datetime
# from pdf_writer import report_open_tasks
from tkcalendar import DateEntry


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
        self.duedate_dockets()
        self.delivery_info(pos_x=6, pos_y=0, span_x=1, span_y=1)
        self.draw_menu()
        self.btn_submit = ttk.Button(text="submit")
        self.btn_submit.grid(column=0, row=11, columnspan=2,
                             rowspan=2, sticky="NESW")

    def duedate_dockets(self):
        # search engine UI
        self.label_frame_search = tk.LabelFrame(
            text="Search")
        self.label_frame_search.grid(
            column=0, row=0, columnspan=2, rowspan=6, pady=10, padx=10, sticky="NESW")
        self.search_entry = tk.Entry(
            self.label_frame_search, bg=BASECOLOR, font=ENTRYFONT)
        self.search_entry.bind("<Return>", self.update_dockets_list)
        self.search_entry.grid(column=0, row=0)
        data = request_recent()
        self.list_dockets(data=data)

    def draw_menu(self):
        """Creates menue in the app"""
        self.menubar = tk.Menu(self.master)

        self.editmenu = tk.Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(
            label="New Customer", command=lambda: self.new_partner(CUSTOMER))
        self.editmenu.add_command(
            label="New Vendor", command=lambda: self.new_partner(VENDOR))
        self.editmenu.add_command(
            label="New Delivery", command=self.new_delivery)

        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

       # self.menubar.add_command(label="Report", command=report_open_tasks)
        self.menubar.add_command(label="Test database", command=self.db_test)
        self.master.config(menu=self.menubar)
    # UI labels with dockets

    # def db_test(self):
    #    create_tables()

    def update_dockets_list(self, event):
        num = self.search_entry.get()
        self.update_by_docket(event, docket=int(num))
        self.list_dockets(data=request_recent())

    def new_delivery(self):
        pass

    def list_dockets(self, data=None, dockets=None):
        """
        parameter: data(list) includes list of strings to show
        """
        """if data is None:
            data = []
            for i in range(0, LENGTH_DOCKETS):
                data.append("Max and Co. \n # 30041")
        """
        # dont forget that there maybe less data than dockets!

        self.docket_labels = []
        font_list = None
        for i, obj in enumerate(data):
            if i % 2 == 0:
                font_list = SECONDARYCOLOR
            else:
                font_list = BASECOLOR
            # concatincates dict wit empty string
            text = ""
            for k, v in obj.items():
                text = text + str(k)+" : "+str(v)+"\n"
            label = tk.Label(
                self.label_frame_search, text=text,
                bg=font_list)
            label.grid(column=0, row=i+1, sticky="NESW")
            label.bind("<Double-Button-1>", self.update_by_docket)
            self.docket_labels.append(label)

            # creates the label with data and packs it with grid

    def delivery_info(self, pos_x, pos_y, span_x, span_y):
        """
        draws delivery information of the form
        """
        self.label_frame_delivery = tk.LabelFrame(
            self.master, text="Delivery Info")
        self.label_frame_delivery.grid(
            column=pos_x, row=pos_y, columnspan=2, sticky="NEW", padx=10, pady=10)
        self.deliver_address = tk.Label(
            self.label_frame_delivery, text="Delivery Address")
        self.deliver_address.grid(column=0, row=0)
        self.entry_del_address = tk.Entry(
            self.label_frame_delivery, width=30)
        self.entry_del_address.grid(column=1, row=0)

    def update_by_docket(self, event, docket=None):
        # this method parses widget text because of the explained below
        """
            found intersting bug(probably just the thing that not all people know) in python
            if you bind label(may work with other widgets) in a loop(which uses range(0,somenumber))
            with the callback the last value of i or other iterator will be passed to function!
        """

        self.set_active()
        self.clear_tasks()

        # docket, customer, vendor, completed_tasks, date_client, date_require,
        # date_shipment, tasks, note, delivery address
        data = None
        if docket is None:
            docket = int(event.widget["text"].split("\n")[0].split(" ")[2])
            data = request_by_docket(docket)
        else:
            data = request_by_docket(docket)
        if data is None:
            # create a message that will say that something wrong was inputed
            self.clear_entries()
            self.clear_by_partner(CUSTOMER)
            self.clear_by_partner(VENDOR)
            self.clear_tasks()

        else:
            print(data)
            def func(): return update_docket(docket, self.read_tasks())
            self.btn_submit.configure(command=func)
            # fields in dictionary are the same as fields in docket
            # update customer info
            self.customer_info[1][0].current(
                self.customer_info[1][0]["values"].index((data["customer"])))
            self.update_customer_info(None)
            # none instead of event as update does
            # not depend on event variables
            # update vendor info
            self.vendor_info[1][0].current(
                self.vendor_info[1][0]["values"].index((data["vendor"]))
            )
            self.update_vendor_info(None)
            # update dates

            self.insert_dates(
                [data["date_client"], data["date_request"], data["date_shipmet"]])

            # update tasks dont forget that
            # at some point it should turn from bytes -> tuple -> string

            self.update_tasks(data["tasks"])
            # update notes
            self.update_notes(data["note"])
            # update delivery address
            self.update_delivery_address(data["delivery_address"])
        self.readonly_mode()

    def update_delivery_address(self, text):
        self.entry_del_address.delete(0, tk.END)
        self.entry_del_address.insert(0, text)

    def readonly_mode(self):
        pass

    def read_delivery_entries(self):
        # self.update_dockets_list()
        pass

    def set_active(self):
        pass


def time_format(time_str):
    time_str = time_str.split("/")
    return datetime.datetime(
        year=2000+int(time_str[2]), month=int(time_str[0]), day=int(time_str[1])
    ).strftime("%m/%d/%Y")


root = tk.Tk()
app = MainWindow(master=root)
root.mainloop()
