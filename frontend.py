import tkinter as tk
import tkinter.ttk as ttk
from backend import partners_list, partner_info, get_delivery, get_recent, neat_time, submit_delivery
import datetime
import time
# import logging
# to start logging the parts of the app

LENGTH_DOCKETS = 11
BASECOLOR = "gainsboro"
SECONDARYCOLOR = "snow2"
HIGHFONT = ("Open Sans", "18")
BASICFONT = ("Open Sans", "14")
ENTRYFONT = ("Open Sans", "12")


class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.master.title("Delivery Accountant")
        self.master.minsize(1440, 1080)
        self.master.resizable(True, True)

        # draws searching engine
        self.search_engine()
        # additional info for dates
        self.draw_dates(535, 10)
        self.draw_notes(535, 200)
        self.customer_info = self.draw_info("Customer", pos_x=230, pos_y=10)
        self.vendor_info = self.draw_info("Vendor", pos_x=230, pos_y=200)
        self.draw_tasks(10, pos_x=230, pos_y=390)
        self.delivery_info(pos_x=850, pos_y=10)
        self.draw_menu()
        self.update_customer_combobox()
        self.update_vendor_combobox()
        # self.update_data()

    def search_engine(self):
        # search engine UI
        self.label_frame_search = tk.LabelFrame(
            text="Search", height="720", width="200")
        self.label_frame_search.place(x=25, y=10)
        self.search_entry = tk.Entry(
            self.label_frame_search, bg=BASECOLOR, font=ENTRYFONT)
        self.search_entry.grid(column=0, row=0)
        data, dockets = get_recent()
        self.list_dockets(data=data, dockets=dockets)

    def draw_menu(self):
        """Creates menue in the app"""
        self.menubar = tk.Menu(self.master)

        self.editmenu = tk.Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="New Customer", command=None)
        self.editmenu.add_command(label="New Vendor", command=None)
        self.editmenu.add_command(
            label="New Delivery", command=lambda: self.set_active)

        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        self.menubar.add_command(label="Reports", command=None)
        self.master.config(menu=self.menubar)
    # UI labels with dockets

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
        for i in range(0, len(data)):
            if i % 2 == 0:
                font_list = SECONDARYCOLOR
            else:
                font_list = BASECOLOR

            label = tk.Label(
                self.label_frame_search, text=data[i],
                bg=font_list)
            label.grid(column=0, row=i+1)
            label.bind("<Double-Button-1>", self.update_by_docket)
            self.docket_labels.append(label)

            # creates the label with data and packs it with grid

    def delivery_info(self, pos_x, pos_y):
        """
        draws delivery information of the form
        """
        self.label_frame_delivery = tk.LabelFrame(
            self.master, text="Delivery Info", height="350", width="300")
        self.label_frame_delivery.place(x=pos_x, y=pos_y)
        self.deliver_address = tk.Label(
            self.label_frame_delivery, text="Delivery Address")
        self.deliver_address.grid(column=0, row=0)
        self.entry_del_address = tk.Entry(
            self.label_frame_delivery, width="25")
        self.entry_del_address.grid(column=1, row=0)

    def draw_info(self, name, pos_x, pos_y, labels=True):
        """
        :parameter: labels: (bool) show the requirement of label of entry
        :parameter: name: whos info is going to showed up
        :return: (list) returns two lists that have information about state
        """
        label_frame = tk.LabelFrame(
            self.master, text="{} Info".format(name),
            height="350", width="300")
        label_frame.place(x=pos_x, y=pos_y)

        # TODO backend method that returns all customers
        combobox = ttk.Combobox(label_frame, values=[], font=ENTRYFONT)
        combobox.grid(column=0, row=0)
        if name == "Customer":
            combobox.bind("<<ComboboxSelected>>", self.update_customer_info)
        elif name == "Vendor":
            combobox.bind("<<ComboboxSelected>>", self.update_vendor_info)
        name_label = tk.Label(
            label_frame, text="{} Name".format(name), font=BASICFONT)
        name_label.grid(column=0, row=1, sticky="w")

        address_label = tk.Label(label_frame, text="Address", font=BASICFONT)
        address_label.grid(column=0, row=2, sticky="w")

        phone_label = tk.Label(label_frame, text="Phone", font=BASICFONT)
        phone_label.grid(column=0, row=4, sticky="w")

        contact_label = tk.Label(label_frame, text="Contact", font=BASICFONT)
        contact_label.grid(column=0, row=5, sticky="w")

        name = None
        address = None
        phone = None
        contact = None
        # if need lbels than it is going to draw labels, if not draw entries
        if labels:

            name = tk.Label(label_frame, text="")
            name.grid(column=1, row=1)

            address = tk.Label(label_frame, text="")
            address.grid(column=1, row=2)

            phone = tk.Label(label_frame, text="")
            phone.grid(column=1, row=4)

            contact = tk.Label(label_frame, text="")
            contact.grid(column=1, row=5)
        else:
            name = tk.Entry(label_frame)
            name.grid(column=1, row=1)

            address = tk.Entry(label_frame)
            address.grid(column=1, row=2)

            phone = tk.Entry(label_frame)
            phone.grid(column=1, row=4)

            contact = tk.Entry(label_frame)
            contact.grid(column=1, row=5)

        return [[name_label, address_label, phone_label, contact_label],
                [combobox, name, address, phone, contact]]

    def draw_dates(self, pos_x, pos_y):
        # ui for date widget
        self.label_frame_dates = tk.LabelFrame(
            text="About Dates", height="130", width="300")
        self.label_frame_dates.place(x=pos_x, y=pos_y)

        # date labels

        self.date_client = tk.Label(
            self.label_frame_dates, text="Client", font=BASICFONT)
        self.date_client.grid(column=0, row=0, sticky="w")
        self.date_required = tk.Label(
            self.label_frame_dates, text="Requested", font=BASICFONT)
        self.date_required.grid(column=0, row=1, sticky="w")
        self.date_ship = tk.Label(
            self.label_frame_dates, text="Shipment", font=BASICFONT)
        self.date_ship.grid(column=0, row=2, sticky="w")

        self.entry_client = ttk.Entry(self.label_frame_dates, font=ENTRYFONT)
        self.entry_client.grid(column=1, row=0, sticky="w")

        self.entry_required = ttk.Entry(self.label_frame_dates, font=ENTRYFONT)
        self.entry_required.grid(column=1, row=1, sticky="w")

        self.entry_ship = ttk.Entry(self.label_frame_dates, font=ENTRYFONT)
        self.entry_ship.grid(column=1, row=2, sticky="w")

    def draw_tasks(self, length, pos_x, pos_y):
        """
        draws tasks in this format Task:
            goal(string)  |  checkbox(bool)  |  target date(date)
        :parameter: length: (integer) tells how any tasks to draw

        """
        self.tasks = []
        self.label_frame_tasks = tk.LabelFrame(
            text="Tasks", height="130", width="300")
        self.label_frame_tasks.place(x=pos_x, y=pos_y)

        for i in range(0, length):
            entry = tk.Entry(self.label_frame_tasks, width="75")
            entry.grid(column=0, row=i)

            check_button = tk.Checkbutton(self.label_frame_tasks)
            check_button.grid(column=1, row=i)

            date = tk.Entry(self.label_frame_tasks, width="20")
            date.grid(column=2, row=i)
            self.tasks.append([entry, check_button, date])

    def draw_notes(self, pos_x, pos_y):

        self.notes_frame = tk.LabelFrame(
            text="Notes", height="130", width="300")
        self.notes_frame.place(x=pos_x, y=pos_y)
        self.notes = tk.Text(
            self.notes_frame, font=ENTRYFONT, width=31, height=5)
        self.notes.grid(column=0, row=0)

    def update_customer_info(self, event):
        data = partner_info(self.customer_info[1][0].get(), "customers")
        for n, d in enumerate(data):
            self.customer_info[1][n+1].configure(text=d)
        # return [[name_label, address_label, phone_label, contact_label],
        # [combobox, name, address, phone, contact]]

    def update_customer_combobox(self):
        """
        updates info on customer frame
        """
        self.customer_info[1][0].configure(
            values=partners_list(db_name="customers"))

    def update_vendor_combobox(self):
        self.vendor_info[1][0].configure(values=partners_list("vendors"))

    def update_vendor_info(self, event):
        data = partner_info(self.vendor_info[1][0].get(), "vendors")
        for n, d in enumerate(data):
            self.vendor_info[1][n+1].configure(text=d)

    def update_by_docket(self, event):
        # this method parses widget text because of the explained below
        """
            found intersting bug(probably just the thing that not all people know) in python
            if you bind label(may work with other widgets) in a loop(which uses range(0,somenumber))
            with the callback the last value of i or other iterator will be passed to function!
        """

        self.set_active()
        # docket, customer, vendor, completed_tasks, date_client, date_require,
        # date_shipment, tasks, note, delivery address
        data = get_delivery(int(event.widget["text"].split(" ")[2]))
        # update customer info
        self.customer_info[1][0].current(
            self.customer_info[1][0]["values"].index((data[1],)))
        self.update_customer_info(None)
        # none instead of event as update does
        # not depend on event variables
        # update vendor info
        self.vendor_info[1][0].current(
            self.vendor_info[1][0]["values"].index((data[2],))
        )
        self.update_vendor_info(None)
        # update dates
        self.insert_dates(data[4:7])

        # update tasks dont forget that
        # at some point it should turn from bytes -> tuple -> string

        # for num, task in enumerate(data[7]):
        #    self.tasks[num][0] = data[7]  # and point to 1 part
        #    self.tasks[num][1] = data[7]  # and point to 2 part
        #    self.tasks[num][2] = data[7]  # and point to 3 part
        # update notes
        self.update_notes(data[8])
        # update delivery address
        self.update_delivery_address(data[9])
        self.readonly_mode()

    def update_notes(self, text):
        self.notes.delete(1.0, tk.END)
        self.notes.insert(1.0, text)

    def update_delivery_address(self, text):
        self.entry_del_address.delete(0, tk.END)
        self.entry_del_address.insert(0, text)

    def readonly_mode(self):
        self.entry_client.configure(state="readonly")
        self.entry_del_address.configure(state="readonly")
        self.entry_required.configure(state="readonly")
        self.entry_ship.configure(state="readonly")
        for i in self.tasks:
            i[0].configure(state="readonly")
            i[1].configure(state="readonly")
            i[2].configure(state="readonly")
        self.notes.configure(state="readonly")

    def read_delivery_entries(self):
        data = []
        data.append(self.customer_info[1][0].get())
        data.append(self.vendor_info[1][0].get())
        done_tasks = True
        tasks = []
"""
        for task, done, date in self.tasks:
            if not task.get() and not task.get().isspace() and done.variable == 0:
                done_tasks = False
            tasks.append((task.get(), done.variable, date.get()))
"""
        data.append(done_tasks)
        data.append(self.entry_client["text"])
        data.append(self.entry_required["text"])
        data.append(self.entry_ship["text"])
        data.append(bytes(tasks, "utf-8"))
        data.append(self.note.get())
        data.append(self.entry_del_address.get())
        submit_delivery(data)

    def time_format(self, time_str):
        time_str = time_str.split("/")
        return datetime.datatime(time)
        # need time format !

    def insert_dates(self, dates):
        self.entry_client.delete(0, tk.END)
        self.entry_ship.delete(0, tk.END)
        self.entry_required.delete(0, tk.END)

        self.entry_client.insert(0, neat_time(dates[0]))
        self.entry_required.insert(0, neat_time(dates[1]))
        self.entry_ship.insert(0, neat_time(dates[2]))

    def set_active(self):
        self.entry_client.configure(state="normal")
        self.entry_del_address.configure(state="normal")
        self.entry_required.configure(state="normal")
        self.entry_ship.configure(state="normal")
        for i in self.tasks:
            i[0].configure(state="normal")
            # i[1].configure(state="normal")
            i[2].configure(state="normal")
        self.notes.configure(state="normal")


root = tk.Tk()
app = MainWindow(master=root)
root.mainloop()
