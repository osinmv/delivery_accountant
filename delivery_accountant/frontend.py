import tkinter as tk
import tkinter.ttk as ttk
from backend import partners_list, partner_info, get_delivery, get_recent
from backend import neat_time, submit_delivery, submit_partner, create_tables, update_docket
import datetime
from pdf_writer import report_open_tasks
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
        # create_tables()
        # draws searching engine
        self.duedate_dockets()
        # additional info for dates
        self.customer_info = self.draw_info(
            CUSTOMER, pos_x=2, pos_y=0, span_x=2, span_y=1)
        self.vendor_info = self.draw_info(
            VENDOR, pos_x=2, pos_y=1, span_x=2, span_y=1)
        self.draw_dates(pos_x=4, pos_y=0, span_x=2, span_y=1)
        self.draw_notes(pos_x=4, pos_y=1, span_x=2, span_y=2)
        self.draw_tasks(12, pos_x=2, pos_y=4, span_x=4, span_y=2)

        self.delivery_info(pos_x=6, pos_y=0, span_x=1, span_y=1)

        self.draw_menu()
        self.update_customer_combobox()
        self.update_vendor_combobox()
        # the only button for now in this app
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
        data, dockets = get_recent()
        self.list_dockets(data=data, dockets=dockets)

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

        self.menubar.add_command(label="Report", command=report_open_tasks)
        self.menubar.add_command(label="Test database", command=self.db_test)
        self.master.config(menu=self.menubar)
    # UI labels with dockets
    def db_test(self):

        create_tables()

    def update_dockets_list(self, event):
        num = self.search_entry.get()
        self.update_by_docket(event, docket=int(num))
        self.list_dockets(get_recent())
    def new_delivery(self):
        self.set_active()
        self.clear_entries()
        self.clear_by_partner(CUSTOMER)
        self.clear_by_partner(VENDOR)
        self.btn_submit.configure(command=self.read_delivery_entries)

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

    def draw_info(self, name, pos_x, pos_y, span_x, span_y):
        """
        :parameter: labels: (bool) show the requirement of label of entry
        :parameter: name: whos info is going to showed up
        :return: (list) returns two lists that have information about state
        """
        label_frame = tk.LabelFrame(
            self.master, text="{} Info".format(name))
        label_frame.grid(column=pos_x, row=pos_y, columnspan=span_x,
                         rowspan=span_y, pady=10, padx=10, sticky="NESW")

        # TODO backend method that returns all customers
        combobox = ttk.Combobox(label_frame, values=[], font=ENTRYFONT)
        combobox.grid(column=0, row=0, sticky="NESW")
        if name == CUSTOMER:
            combobox.bind("<<ComboboxSelected>>", self.update_customer_info)
        elif name == VENDOR:
            combobox.bind("<<ComboboxSelected>>", self.update_vendor_info)
        name_label = tk.Label(
            label_frame, text="{} Name".format(name), font=BASICFONT)
        name_label.grid(column=0, row=1, sticky="W")

        address_label = tk.Label(label_frame, text="Address", font=BASICFONT)
        address_label.grid(column=0, row=2, sticky="W")

        phone_label = tk.Label(label_frame, text="Phone", font=BASICFONT)
        phone_label.grid(column=0, row=3, sticky="W")

        contact_label = tk.Label(label_frame, text="Contact", font=BASICFONT)
        contact_label.grid(column=0, row=4, sticky="W")

        # if need lbels than it is going to draw labels, if not draw entries

        name = tk.Entry(label_frame, width=30)
        name.grid(column=1, row=1, sticky="NESW")

        address = tk.Entry(label_frame, width=30)
        address.grid(column=1, row=2, sticky="NESW")

        phone = tk.Entry(label_frame, width=30)
        phone.grid(column=1, row=3, sticky="NESW")

        contact = tk.Entry(label_frame, width=30)
        contact.grid(column=1, row=4, sticky="NESW")

        return [[name_label, address_label, phone_label, contact_label],
                [combobox, name, address, phone, contact]]

    def draw_dates(self, pos_x, pos_y, span_x, span_y):
        # ui for date widget
        self.label_frame_dates = tk.LabelFrame(
            text="About Dates")
        self.label_frame_dates.grid(
            column=pos_x, row=pos_y, columnspan=span_x, rowspan=span_y, padx=10, pady=10, sticky="NEW")

        # date labels

        self.date_client = tk.Label(
            self.label_frame_dates, text="Client", font=BASICFONT)
        self.date_client.grid(column=0, row=0, sticky="W")
        self.date_required = tk.Label(
            self.label_frame_dates, text="Requested", font=BASICFONT)
        self.date_required.grid(column=0, row=1, sticky="w")
        self.date_ship = tk.Label(
            self.label_frame_dates, text="Shipment", font=BASICFONT)
        self.date_ship.grid(column=0, row=2, sticky="w")

        self.entry_client = DateEntry(
            self.label_frame_dates, font=ENTRYFONT)
        self.entry_client.grid(column=1, row=0, sticky="w")

        self.entry_required = DateEntry(
            self.label_frame_dates, font=ENTRYFONT)
        self.entry_required.grid(column=1, row=1, sticky="w")

        self.entry_ship = DateEntry(self.label_frame_dates, font=ENTRYFONT)
        self.entry_ship.grid(column=1, row=2, sticky="w")

    def draw_tasks(self, length, pos_x, pos_y, span_x, span_y):
        """
        draws tasks in this format Task:
            goal(string)  |  checkbox(bool)  |  target date(date)
        :parameter: length: (integer) tells how any tasks to draw

        """
        self.tasks = []
        self.label_frame_tasks = tk.LabelFrame(
            text="Tasks")
        self.label_frame_tasks.grid(
            column=pos_x, row=pos_y, columnspan=span_x,
            rowspan=span_y, padx=10, pady=10)
        self.task_label = tk.Label(self.label_frame_tasks,text="Tasks")
        self.task_label.grid(column=0,row=0)
        self.done_label = tk.Label(self.label_frame_tasks,text="Done")
        self.done_label.grid(column=1,row=0)
        self.task_date_label = tk.Label(self.label_frame_tasks,text="Date")
        self.task_date_label.grid(column=2,row=0)
        self.task_date_must_label = tk.Label(self.label_frame_tasks,text="Must Date")
        self.task_date_must_label.grid(column=3,row=0)
        for i in range(0, length):
            entry = tk.Entry(self.label_frame_tasks, width="75")
            entry.grid(column=0, row=i+1)

            check = tk.BooleanVar()
            check_button = tk.Checkbutton(self.label_frame_tasks, var=check)
            check_button.grid(column=1, row=i+1)

            date = DateEntry(self.label_frame_tasks, width="25")
            date.grid(column=2, row=i+1)
            date.configure(state="readonly")
            date_must = DateEntry(self.label_frame_tasks, width="25")
            date_must.grid(column=3, row=i+1)
            date_must.configure(state="readonly")
            self.tasks.append([entry, check_button, date, check, date_must])

    def draw_notes(self, pos_x, pos_y, span_x, span_y):

        self.notes_frame = tk.LabelFrame(
            text="Notes")
        self.notes_frame.grid(column=pos_x, row=pos_y,
                              columnspan=span_x, rowspan=span_y, sticky="NESW")
        self.notes = tk.Text(
            self.notes_frame, height=9, width=35, font=ENTRYFONT)

        self.notes.grid(column=0, row=0)

    def update_customer_info(self, event):
        data = partner_info(self.customer_info[1][0].get(), CUSTOMER)
        if data is None:
            pass
        else:
            self.activate_info_entries(CUSTOMER)
            for n, d in enumerate(data):
                self.customer_info[1][n+1].delete(0, tk.END)
                self.customer_info[1][n+1].insert(0, str(d))
            self.deactivate_info_entries(CUSTOMER,include=False)
            # return [[name_label, address_label, phone_label, contact_label],
            # [combobox, name, address, phone, contact]]

    def update_customer_combobox(self):
        """
        updates info on customer frame
        """
        self.customer_info[1][0].configure(
            values=partners_list(db_name=CUSTOMER_DB))

    def update_vendor_combobox(self):
        self.vendor_info[1][0].configure(values=partners_list(VENDOR_DB))

    def update_vendor_info(self, event):
        data = partner_info(self.vendor_info[1][0].get(), VENDOR)
        if data is None:
            pass
        else:
            self.activate_info_entries(VENDOR)
            for n, d in enumerate(data):
                self.vendor_info[1][n+1].delete(0, tk.END)
                self.vendor_info[1][n+1].insert(1, str(d))
            self.deactivate_info_entries(VENDOR,include=False)

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
            docket = int(event.widget["text"].split(" ")[2])
            data = get_delivery(docket)
        else:
            data = get_delivery(docket)
        if data is None:
            # create a message that will say that something wrong was inputed
            self.clear_entries()
            self.clear_by_partner(CUSTOMER)
            self.clear_by_partner(VENDOR)
            self.clear_tasks()

        else:
            func = lambda:update_docket(docket,self.read_tasks())
            self.btn_submit.configure(command=func)

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

            self.update_tasks(data[7])
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
        self.deactivate_info_entries(CUSTOMER)
        self.deactivate_info_entries(VENDOR)
        self.entry_client.configure(state="disabled")
        self.entry_del_address.configure(state="readonly")
        self.entry_required.configure(state="disabled")
        self.entry_ship.configure(state="disabled")
        for i in self.tasks:
            if not i[0].get() and not i[0].get().isspace() and i[0].get() is not None:
                i[0].configure(state="normal")
                i[2].configure(state="readonly")
                i[1].configure(state="normal")
            else:
                if i[1] == 1:
                    i[1].configure(state="disabled")
                else:
                    i[0].configure(state="normal")
                i[0].configure(state="disabled")
                i[2].configure(state="disabled")

        self.notes.configure(state="disabled")

    def read_tasks(self):
        done_tasks = True
        tasks = ""
        for task, done, date, check, date_must in self.tasks:

            if task.get() and not task.get().isspace() and not (task.get() is None):

                if not check.get():
                    done_tasks = False
                
                if check.get():
                    check = 1
                else:
                    check = 0
                tasks = tasks + ""+task.get()+"|"+str(check)+"|"+date.get()+"|"+date_must.get()
        return [tasks, done_tasks]

    def read_delivery_entries(self):
        self.update_dockets_list()
        self.btn_submit.configure(command=None)
        self.set_active()
        data = []
        data.append(self.customer_info[1][0].get())
        data.append(self.vendor_info[1][0].get())
        tasks, done = self.read_tasks()
        data.append(done)
        data.append(time_format(self.entry_client.get()))
        data.append(time_format(self.entry_required.get()))
        data.append(time_format(self.entry_ship.get()))
        data.append(tasks)
        data.append(self.notes.get(1.0, tk.END))
        data.append(self.entry_del_address.get())
        self.readonly_mode()
        submit_delivery(data)

    def after_action_update(self):
        self.update_customer_combobox()
        self.update_vendor_combobox()

    def insert_dates(self, dates):
        self.entry_client.delete(0, tk.END)
        self.entry_ship.delete(0, tk.END)
        self.entry_required.delete(0, tk.END)

        self.entry_client.insert(0, dates[0])
        self.entry_required.insert(0, dates[1])
        self.entry_ship.insert(0, dates[2])

    def clear_tasks(self):
        for i in self.tasks:
            i[0].delete(0, tk.END)
            i[1].deselect()
            i[2].delete(0, tk.END)

    def clear_entries(self):
        self.insert_dates([0, 0, 0])
        self.entry_client.delete(0, tk.END)
        self.entry_del_address.delete(0, tk.END)
        self.entry_required.delete(0, tk.END)
        self.entry_ship.delete(0, tk.END)
        self.clear_tasks()
        self.notes.delete(1.0, tk.END)
        self.vendor_info[1][0].current(0)
        self.customer_info[1][0].current(0)

    def clear_by_partner(self, partner):
        if partner == CUSTOMER:
            for i in self.vendor_info[1]:
                i.delete(0, tk.END)
        if partner == VENDOR:
            for i in self.customer_info[1]:
                i.delete(0, tk.END)

    def set_active(self):
        self.activate_info_entries(CUSTOMER)
        self.activate_info_entries(VENDOR)
        self.entry_client.configure(state="readonly")
        self.entry_del_address.configure(state="normal")
        self.entry_required.configure(state="readonly")
        self.entry_ship.configure(state="readonly")
        for i in self.tasks:
            i[0].configure(state="normal")
            i[1].configure(state="normal")
            i[2].configure(state="readonly")
        self.notes.configure(state="normal")

    def activate_info_entries(self, partner):
        if partner == CUSTOMER:
            data = self.customer_info[1]
        elif partner == VENDOR:
            data = self.vendor_info[1]
        for i in data[1:]:
            i.configure(state="normal")
        data[0].configure(state="readonly")

    def deactivate_info_entries(self, partner,include=True):
        """
        CHANGE SIMILAR SSTATEMENTS ON THIS
        IF .... CUSOTMER:
            DATA = SELF.CUSTOMER
        FOR I IN DATA:
            ....
        """
        if include:
            if partner == CUSTOMER:
                data = self.customer_info[1]
            elif partner == VENDOR:
                data = self.vendor_info[1]
            for i in data[1:]:
                i.configure(state="disabled")
            
            data[0].configure(state="disabled")

    def update_tasks(self, text):
        if text is None:
            return None
        text = text.split("\n")
        text.remove("")
        self.clear_tasks()
        for num, obj in enumerate(text):
            obj = obj.split("|")
            self.tasks[num][0].delete(0, tk.END)
            self.tasks[num][0].insert(0, obj[0])
            self.tasks[num][3].set(int(obj[1]))
            self.tasks[num][2].delete(0, tk.END)
            self.tasks[num][2].insert(0, obj[2])
            self.tasks[num][4].delete(0, tk.END)
            self.tasks[num][4].insert(0, obj[3])

    def read_partner(self, partner):
        self.btn_submit.configure(command=None)
        data = None
        if partner == CUSTOMER:
            data = self.customer_info[1]
        elif partner == VENDOR:
            data = self.vendor_info[1]
        submit_data = []
        for i in data[1:]:
            submit_data.append(str(i.get()))
        submit_partner(submit_data, partner)
        self.clear_entries()
        self.update_customer_combobox()
        self.update_vendor_combobox()

    def new_partner(self, partner):
        self.set_active()
        self.clear_entries()
        self.readonly_mode()
        self.activate_info_entries(VENDOR)
        self.activate_info_entries(CUSTOMER)

        self.clear_by_partner(VENDOR)
        self.clear_by_partner(CUSTOMER)
        if partner == VENDOR:
            self.deactivate_info_entries(CUSTOMER)
        elif partner == CUSTOMER:
            self.deactivate_info_entries(VENDOR)
        self.btn_submit.configure(command=lambda: self.read_partner(partner))


def time_format(time_str):
    time_str = time_str.split("/")
    return datetime.datetime(
        year=2000+int(time_str[2]), month=int(time_str[0]), day=int(time_str[1])
    ).strftime("%m/%d/%Y")


root = tk.Tk()
app = MainWindow(master=root)
root.mainloop()
