import tkinter as tk

LENGTH_DOCKETS = 11
BASECOLOR = "gainsboro"
HIGHFONT = ("Calibre","18")
BASICFONT = ("Calibre","14")
ENTRYFONT = ("Calibre","12")
ENTRIES_NUM = 3

data_example = {
    "date":
    {
        "client": "2017/09/03",
        "required": "2017/09/04",
        "ship": "2017/09/03"
    },
    "requirements":
    {
        "labels":
         {
            "Die",
            "Print",
            "Glue"
         },
        "checklist":
        {
            True,
            True,
            False
        },
        "Supplier":
        {
            "Max & Co",
            "Ling & Co",
            "Sup & Co",
        }
    },
    "Notes":"this is for comments, if you have some wishes"
}






class MainWindow(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Delivery Accountant")
        self.master.minsize(1280,720)
        self.master.resizable(False,False)


        #search engine UI
        self.label_frame_search = tk.LabelFrame(text="Availible Dockets",height="720",width="200")
        self.label_frame_search.grid(column=0,row=0,sticky="n")
        self.search_entry = tk.Spinbox(self.label_frame_search,from_=1000,to=100000,bg=BASECOLOR,font=ENTRYFONT)
        self.search_entry.grid(column=0,row=0)
        self.list_dockets()
        
        # additional info for selected docket
        self.general_data()#draws labels and entries with data
        


    #UI labels with dockets
    def list_dockets(self,data=None):
        """
        parameter: data(list) includes list of strings to show 
        """
        if data is None:
            data = []
            for i in range(0,LENGTH_DOCKETS):
                data.append("Max and Co. - # 30041")

        #dont forget that there maybe less data than dockets!
        
        self.docket_labels = []
        for i in range(0,LENGTH_DOCKETS):
            self.docket_labels.append(tk.Label(self.label_frame_search,text=data[i],bg=BASECOLOR,font=BASICFONT).grid(column=0,row=i+1,sticky="w"))   
            #creates the label with data and packs it with grid
    
    def general_data(self, data=None):
        """Draws right side of the window with additional info"""
        if data is None:
            data = data_example
        
        #ui for the additional data
        self.label_frame_info = tk.LabelFrame(text="Advanced information",height="720",width="1040")
        self.label_frame_info.grid(column=1,row=0,sticky="n")
        self.date_lable = tk.Label(self.label_frame_info,text="Date",font=HIGHFONT)
        self.date_lable.place(x=25,y=25)
        
        #date labels
        # y offset is 40 per new widget
        x_offset = 40
        self.date_client = tk.Label(self.label_frame_info,text="client : ",font=BASICFONT)
        self.date_client.place(x=x_offset,y=65)
        self.date_required = tk.Label(self.label_frame_info,text="required : ",font=BASICFONT)
        self.date_required.place(x=x_offset,y=105)
        self.date_ship = tk.Label(self.label_frame_info,text="shipment : ",font=BASICFONT)
        self.date_ship.place(x=x_offset,y=145)

        x_offset = 150
        self.entry_client = tk.Entry(self.label_frame_info,text="client date",font=ENTRYFONT,state="readonly")
        self.entry_client.place(x=x_offset,y = 65)

        self.entry_required = tk.Entry(self.label_frame_info,text="required date",font=ENTRYFONT,state="readonly")
        self.entry_required.place(x=x_offset,y = 105)

        self.entry_ship = tk.Entry(self.label_frame_info,text="required date",font=ENTRYFONT,state="readonly")
        self.entry_ship.place(x=x_offset,y = 145)
        
        #requirements
        x_offset = 40
        y_offset = 200
        self.entries_reqs = []

        for i in range(0,ENTRIES_NUM):
            label_req = tk.Label(self.label_frame_info,text="      ",font=BASICFONT)
            label_req.place(x=x_offset,y=y_offset)
            check_box = tk.Checkbutton(self.label_frame_info,state="disabled")
            check_box.place(x=x_offset + 50 ,y=y_offset)
            entry_supplier = tk.Entry(self.label_frame_info,font=ENTRYFONT,state="readonly")
            entry_supplier.place(x=x_offset + 100 ,y=y_offset)
            self.entries_reqs.append([label_req,check_box,entry_supplier])
            y_offset+=50



    def update_data(self):
        pass





    def set_data(self,data=None):
        """
        parameter data(tuple) receives a named tuple with date info and puts into entries
        """       
        #date entries(turned off) to change them need to start edit mode
        
        




root = tk.Tk()

app = MainWindow(master=root)

root.mainloop()





        