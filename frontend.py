import tkinter as tk
import logging
#to start logging the parts of the app

LENGTH_DOCKETS = 11
BASECOLOR = "gainsboro"
HIGHFONT = ("Calibre","18")
BASICFONT = ("Calibre","14")
ENTRYFONT = ("Calibre","12")



data_example = {
    "date":
    {
        "client": "2017/09/03",
        "required": "2017/09/04",
        "ship": "2017/09/06"
    },
    "requirements":
    {
        "labels":
         [
            "Die",
            "Print",
            "Glue",
            "other"
         ],
        "checklist":
        [
            True,
            True,
            False,
            False
        ],
        "supplier":
        [
            "Max & Co",
            "Ling & Co",
            "Sup & Co",
            "EY"
        ]
    },
    "Notes":"this is for comments, if you have some wishes"
}






class MainWindow(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Delivery Accountant")
        self.master.minsize(1440,1080)
        self.master.resizable(True,True)


        # draws searching engine
        self.search_engine()
        # additional info for dates
        self.draw_dates()
        self.draw_notes()
        self.draw_customer_info()
        #self.general_data()
        # draws labels and entries with data
        #self.update_data()

    def search_engine(self):
        #search engine UI
        self.label_frame_search = tk.LabelFrame(text="Search",height="720",width="200")
        self.label_frame_search.place(x = 25,y=10)
        self.search_entry = tk.Entry(self.label_frame_search,bg=BASECOLOR,font=ENTRYFONT)
        self.search_entry.grid(column=0,row=0)
        self.list_dockets()

    #UI labels with dockets
    def list_dockets(self,data=None):
        """
        parameter: data(list) includes list of strings to show 
        """
        if data is None:
            data = []
            for i in range(0,LENGTH_DOCKETS):
                data.append("Max and Co. \n # 30041")

        #dont forget that there maybe less data than dockets!
        
        self.docket_labels = []
        for i in range(0,LENGTH_DOCKETS):
            self.docket_labels.append(tk.Label(self.label_frame_search,text=data[i],bg=BASECOLOR,font=BASICFONT).grid(column=0,row=i+1,sticky="w"))   
            #creates the label with data and packs it with grid
    
    def draw_customer_info(self):
        
        
        self.label_frame_customer = tk.LabelFrame(text="Customer Info",height="350",width="300")
        self.label_frame_customer.place(x=230,y = 10)
    
    def draw_vendor_info(self):
        pass
    
    def draw_dates(self):
        
        #ui for date widget
        self.label_frame_dates = tk.LabelFrame(text="About Dates",height="130",width="300")
        self.label_frame_dates.place(x=1125,y = 10)
        
        #date labels
        # y offset is 40 per new widget
        x_offset = 10
        self.date_client = tk.Label(self.label_frame_dates,text="Client : ",font=BASICFONT)
        self.date_client.place(x=x_offset,y=10)
        self.date_required = tk.Label(self.label_frame_dates,text="Required : ",font=BASICFONT)
        self.date_required.place(x=x_offset,y=40)
        self.date_ship = tk.Label(self.label_frame_dates,text="Shipment : ",font=BASICFONT)
        self.date_ship.place(x=x_offset,y=70)

        x_offset = 110
        self.entry_client = tk.Entry(self.label_frame_dates,font=ENTRYFONT)
        self.entry_client.place(x=x_offset,y = 10)

        self.entry_required = tk.Entry(self.label_frame_dates,font=ENTRYFONT)
        self.entry_required.place(x=x_offset,y = 40)

        self.entry_ship = tk.Entry(self.label_frame_dates,font=ENTRYFONT)
        self.entry_ship.place(x=x_offset,y = 70)
    
    def draw_tasks(self):
        pass
    
    def draw_notes(self):
        
        self.notes_frame = tk.LabelFrame(text="Notes",height="130",width="300")
        self.notes_frame.place(x=1125,y=600)
        self.notes = tk.Text(self.notes_frame,font=ENTRYFONT,width=31,height=5)
        self.notes.place(x=0,y=0)


    def general_data(self, data=None):
        """Draws right side of the window with additional info"""
        
        
        

        

        
        
    """def draw_requirements(self,data=None):
        Gets requiremets part of the data
        
        
        if data == None:
            data = data_example

    
        #requirements
        x_offset = 40
        y_offset = 250

        self.reqs_lable = tk.Label(self.label_frame_info,text="Requirements",font=HIGHFONT,bg=BASECOLOR)
        self.reqs_lable.place(x=x_offset,y=y_offset-40)
        self.supplier_lable = tk.Label(self.label_frame_info,text="Supplier",font=HIGHFONT,bg=BASECOLOR)
        self.supplier_lable.place(x=x_offset+250,y=y_offset-40)

        self.entries_reqs = []
        #check if all 3 categories are the same length
        for i in range(0,len(data_example["requirements"]["labels"])):
            label_req = tk.Label(self.label_frame_info,text=data["requirements"]["labels"][i],font=BASICFONT,bg=BASECOLOR)
            label_req.place(x=x_offset,y=y_offset)
            check_box = tk.Checkbutton(self.label_frame_info)
            check_box.place(x=x_offset + 150 ,y=y_offset)
            if data["requirements"]["checklist"][i]:
                check_box.select()
            check_box.configure(state="disabled")
            entry_supplier = tk.Entry(self.label_frame_info,font=ENTRYFONT,bg=BASECOLOR)
            entry_supplier.insert(0,data["requirements"]["supplier"][i])
            entry_supplier.configure(state="readonly")
            entry_supplier.place(x=x_offset + 250  ,y=y_offset)
            self.entries_reqs.append([label_req,check_box,entry_supplier])
            y_offset+=50
    """
    """
    def update_data(self,data=None):
        
        parameter data(tuple) receives a named tuple with date info and puts into entries
           
        #date entries(turned off) to change them need to start edit mode
        if data is None:
            data = data_example
        
        #filling in dates
        self.entry_client.delete(0,tk.END)
        self.entry_client.insert(0,data["date"]["client"])
        self.entry_client.configure(state="readonly")
        self.entry_required.delete(0,tk.END)
        self.entry_required.insert(0,data["date"]["required"])
        self.entry_required.configure(state="readonly")
        self.entry_ship.delete(0,tk.END)
        self.entry_ship.insert(0,data["date"]["ship"])
        self.entry_ship.configure(state="readonly")

        # filling in requirements
        self.draw_requirements()
        #filing notes
        #self.notes.delete(0,tk.END)
        self.notes.insert(tk.INSERT,data["Notes"])
    """
    
        
        




root = tk.Tk()
app = MainWindow(master=root)
root.mainloop()





        