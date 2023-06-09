# from customtkinter import *
from tkcalendar import DateEntry
from tkinter import Menu,Tk,Label,Frame,IntVar,StringVar,DoubleVar,Listbox,END,Toplevel,Scrollbar,font
from models import *
from tkinter import ttk
from datetime import date
import openpyxl
from openpyxl.styles import PatternFill, Alignment
# import models
# import win32print


root = Tk()
root.geometry("1000x800")
root.state('zoomed')
root.title("Inventory Management System")
w = root.winfo_screenmmwidth()
h = root.winfo_screenmmheight()
style = ttk.Style()

navbar = Menu(root, font=('Arial', 20))
root.config(menu=navbar)
rootLable = ttk.Label(master=root,text="Welecome to Inventory Management System | Select from above options",font=("times new roman",20),anchor="center")
rootLable.grid(row=0,column=0,sticky="we",columnspan=8)


# Menu Tab Functions =============================================
def purchase():
    hideAllFrame()
    frame1.grid(row=0,column=0,padx=10,pady=10,sticky="WE")
def sales():
    hideAllFrame()
    frame2.grid(row=0,column=0,padx=10,pady=10,sticky="WE")
def cold_facility():
    hideAllFrame()
    frame3.grid(row=0,column=0,padx=10,pady=10,sticky="WE")
def party_name():
    hideAllFrame()
    frame4.grid(row=0,column=0,padx=10,pady=10,sticky="WE")
def hideAllFrame():
    frame1.grid_forget()
    frame2.grid_forget()
    frame3.grid_forget()
    frame4.grid_forget()
    rootLable.grid_forget()

navbar.add_command(label="Purchase",command=purchase)
navbar.add_command(label="Sales", command=sales)
navbar.add_command(label="Cold Facility", command=cold_facility)
navbar.add_command(label="Party Name", command=party_name)

# End of Menu Tab Functions ==========================================

# Trail screen================================================================

# trail =14-int(str(date.today()).split("-")[2])

warn = ttk.Label(master=root,text="",font=("times new roman",14))
warn.grid(row=1,column=0,columnspan=5,pady=10)

# if(trail):
#   warn.config(text=f"{trail} Days Trail period Remaining. Please Purchase Full Version")
# else:
#   warn.config(text="Trail period is OVER. Please Purchase Full Version")
#   navbar.entryconfigure("Purchase",state="disabled")
#   navbar.entryconfigure("Sales",state="disabled")
#   navbar.entryconfigure("Cold Facility",state="disabled")
#   navbar.entryconfigure("Party Name",state="disabled")


#=============================================================================

# Functions=================================================================
def getColdFacilityOptions():
    global coldFacilityOptions
    coldFacilityOptions = ["0 None"]
    data = session.query(ColdFacility).all()
    for item in data:
        coldFacilityOptions.append(item)

def getpartyNameOptions():
    global partyNameOptions
    data = session.query(PartyName).all()
    for item in data:
        partyNameOptions.append(item)

def clear_partyName_option():
    global defaultPartyOption
    firmNameVar.set(defaultPartyOption)
    firmNameVarFilter.set(defaultPartyOption)
    sale_soldToNameVarFilter.set(defaultPartyOption)

def clear_coldFacility_option():
    global defaultColdFacilityOption
    coldVar.set(defaultColdFacilityOption)
    firmNameVarFilter.set(defaultColdFacilityOption)
    
def purchaseListSelect(event):
    try:
        global idPurchase
        index = event.widget.curselection()
        text = str(purchaseList.get(index))
        datalist = text.split(sep=" | ")
        idPurchase=int(datalist[0].split(':')[1])
        idParty = int(datalist[2].split(':')[1])
        idCold=int(datalist[8].split(':')[1])

        data = session.query(Purchase).filter(Purchase.id==idPurchase).first()
        data1 = session.query(PartyName).filter(PartyName.id==idParty).first()
        
        if(data):
            clear_purchase_input()
            auctionDateEntry.set_date(data.AuctionDate)
            firmNameVar.set(partyNameOptions[idParty])
            markingIdEntry.insert(0,data.MarkingID)
            boxEntry.insert(0,data.Box)
            auctionRateEntry.insert(0,data.AuctionRate)
            weightEntry.insert(0,data.weight)
            coldVar.set(coldFacilityOptions[idCold])

            addSalesbtn.config(state="normal")

            purchase_info.delete(0,END)
            if(data.weight==float(0)):               
                purchase_info.insert(END,f"LOT Weight Pending")
            else:
                purchase_info.insert(END,f"Total Weight of LOT {data.weight} Kg")
            if(data.Box>0):
                purchase_info.insert(END,f"{data.Box} Box remains to sold")
            purchase_info.insert(END,f"Purchased from {data1.Name}")
    

    except:
        pass

def salesListSelect(event):
    try:
        global idSales
        index = event.widget.curselection()
        text = str(salesList.get(index))
        datalist = text.split(sep=" | ")
        idSales=int(datalist[0].split(': ')[1])

        data = session.query(Sell).filter(Sell.id==idSales).first()
        data1 = session.query(Purchase).filter(Purchase.id == data.purchase_id).first()
        data2 = session.query(PartyName).filter(PartyName.id == str(data.SellTo).split(' | ')[0]).first()
        if(data):
            clear_sales_input()
            print("==================================",data2)
            sale_soldToNameVarFilter.set(data2)
            sale_markingIdEntryFilter.insert(0,str(data.MarkingID))
            # sale_coldVarFilter.set(coldFacilityOptions[data1.coldfacility_id])
            d =""
            dd=""
            c=str(coldFacilityOptions[data1.coldfacility_id]).split(' | ')[1]
            if(data.Dispatched):
                d= ""
                dd=data.DispatchDate
            else: 
                d=" NOT"
                dd="NONE"

            sale_info.delete(0,END)
            sale_info.insert(END,f"Kept in {c} Facility")
            sale_info.insert(END,f"LOT is{d} Dispatched")
            sale_info.insert(END,f"LOT Dispatched Date: {dd}")
        
    except:
        pass

def coldListSelect(event):
    try:
        global idCold
        index = event.widget.curselection()
        text = str(coldFacilityList.get(index))
        datalist = text.split(sep=" | ")
        id = datalist[0]
        n = datalist[1]       
        idCold = int(id)
        coldFacilityEntry.delete(0,END)
        coldFacilityEntry.insert(0,n)
        data = session.query(Purchase,Sell).filter(Purchase.id==Sell.purchase_id,
                                                   Sell.Dispatched==0,
                                                   Purchase.coldfacility_id==int(id))
        ci = 1
        if(data):
            print(len(data.all()))
            # for i in data.all():
            #     print('data    ',i)
            # all_coldFacility_data.delete(0,END)
            all_coldFacility_data.delete(*all_coldFacility_data.get_children())
            # all_coldFacility_data.insert(END,f"Total LOTS which Not Dispatched = {data.count()}")

            for i in data.all():
                print(i)
                l = str(i).split(' | ')
                pname = session.query(PartyName).filter(PartyName.id == int(l[2].split(':')[1])).first()
                firmName = "No Name"
                if pname and pname.Name:
                    firmName=pname.Name
                # t_insert = "{:^15} | {:^25} | {:^15} | {:^10} | {:^15} | {:^10} | {:^25} | {:^10}"
                # t_insert = t_insert.format(
                #     l[1].split(':')[1],
                #     pname.Name,l[3].split(':')[1],
                #     l[12].split(': ')[1],
                #     l[5].split(':')[1],
                #     l[7].split(':')[1],
                #     l[11],
                #     idCold)
                # all_coldFacility_data.insert(END,t_insert)

                all_coldFacility_data.insert("", 'end', text =f"{ci}",
                                             values =(
                    l[1].split(':')[1],
                    firmName,
                    l[3].split(':')[1],
                    l[12].split(': ')[1],
                    l[5].split(':')[1],
                    l[7].split(':')[1],
                    l[11],
                    idCold
                    ))
                ci+=1
                # all_coldFacility_data.insert(END,item)
                
        data1 = session.query(Purchase).filter(Purchase.coldfacility_id==int(id),Purchase.Box>0)
        # all_coldFacility_data.insert(END,"=========================================================")
        # all_coldFacility_data.insert(END,f"Total LOTS which Not Sold = {data1.count()}")
        if(data1):
            for item in data1:
                l = str(item).split(' | ')
                pname = session.query(PartyName).filter(PartyName.id == int(l[2].split(':')[1])).first()
                all_coldFacility_data.insert("", 'end', text =f"{ci}",
                                            values =(
                    l[1].split(':')[1],
                    pname.Name,
                    l[3].split(':')[1],
                    l[4].split(':')[1],
                    l[5].split(':')[1],
                    l[7].split(':')[1],
                    "None",
                    l[8].split(':')[1]))
                ci+=1

                # all_coldFacility_data.insert(END,f"{l[1].split(':')[1]} | Purchase From:{pname.Name} | {l[3]} | Sold To: None | {l[4]} | {l[5]}")                   

        coldFacility_data_scrlbar = ttk.Scrollbar(frame3,orient ="vertical",command = all_coldFacility_data.yview)
        coldFacility_data_scrlbar.grid(row=1,column=4,rowspan=14,sticky="nsw")
        all_coldFacility_data.configure(yscrollcommand = coldFacility_data_scrlbar.set)


    except:
        pass

def partyListSelect(event):
    try:
        global idParty
        index = event.widget.curselection()
        text = str(partyNameList.get(index))
        datalist = text.split(sep=" | ")
        id = datalist[0]
        n = datalist[1]       
        idParty = int(id)
        partyNameEntry.delete(0,END)
        partyNameEntry.insert(0,n)
        data1 = session.query(Sell).filter(Sell.SellTo==int(id))
        data = session.query(Purchase).filter(Purchase.FirmName==idParty)
        i=2
        if(data):
            all_partyName_data.delete(0,END)
            all_partyName_data.insert(1,f"Total Purchase {data.count()}")           
            for item in data:
                l = str(item).split(' | ')
                all_partyName_data.insert(i,item)
                i+=1
        if(data1):
            i+=1
            all_partyName_data.insert(i,f"Total Sales {data1.count()}")
            i+=1 
            for item in data1:
                l = str(item).split(' | ')
                all_partyName_data.insert(i,item)
                i+=1
        
    except:
        pass

def addPurchase():
    if(auctionDateEntry != "" and firmNameVar.get() != "" and markingidPurchase.get() != "" and auctionRateVar != 0):
        p = Purchase(AuctionDate=auctionDateEntry.get_date(), 
                     FirmName=int(firmNameVar.get().split(" ")[0]), 
                     MarkingID=markingidPurchase.get(),
                     Box=boxVar.get(),
                     AuctionRate=float(auctionRateVar.get()),
                     Rate=float(rateVar.get()),
                     weight=float(weightVar.get()),
                     coldfacility_id = int(coldVar.get().split(" ")[0]))
                     
        session.add(p)
        session.commit()
        clearPurchase()
        getPurchase()
        status1["text"] = "Status: Product Added successfully"
        status1.config(background='green',foreground='white')
        status1.after(10000,lambda:status1.config(text="Status:",background='white',foreground='black'))
    else:
        status1["text"] = "Status: Product Not Added __Press Clear Button__"
        status1.config(background='red',foreground='white')
        status1.after(10000,lambda:status1.config(text="Status:",background='white',foreground='black'))

def editPurchase():
    if(firmNameVar.get() != "" and markingidPurchase.get() != ""):
        try:
            data = session.query(Purchase).filter(Purchase.id == idPurchase).first()
            if(data):
                data.AuctionDate = auctionDateEntry.get_date()
                data.FirmName=int(firmNameVar.get().split(" | ")[0])
                data.MarkingID=markingidPurchase.get()
                data.Box=boxVar.get()
                data.AuctionRate=float(auctionRateVar.get())
                data.Rate=float(rateVar.get())
                data.weight=weightVar.get()
                if len(coldVar.get().split(" | "))>1:
                    data.coldfacility_id=int(coldVar.get().split(" | ")[0])
                session.commit()
                clearPurchase()
                getPurchase()
                status1["text"] = "Status: Product Edit successfully"
                status1.config(background='green',foreground='white')
                status1.after(3000,lambda:status1.config(text="Status:",background='white',foreground='black'))
        except:
            status1["text"] = "Status: Fill all data, and try again!"
            status1.config(background='red',foreground='white')
            status1.after(3000,lambda:status1.config(text="Status:",background='white',foreground='black'))
        
def deletePurchase():
    if(firmNameVar.get() != "" and markingidPurchase.get() != ""):
        data = session.query(Purchase).filter(Purchase.id == idPurchase).first()
        if(data):
            session.delete(data)
            session.commit()
            clearPurchase()
            getPurchase()
            status1["text"] = "Status: Product deleted successfully"
            status1.config(background='green',foreground='white')
            status1.after(10000,lambda:status1.config(text="Status:",background='white',foreground='black'))

def clearPurchase():
    auctionDateEntry.set_date(date.today())
    clear_partyName_option()
    markingIdEntry.delete(0,END)
    boxEntry.delete(0,END)
    auctionRateEntry.delete(0,END)
    weightEntry.delete(0,END)
    weightEntry.insert(0,"0.0")
    clear_coldFacility_option()

def clear_purchase_input():
    clear_partyName_option()
    markingIdEntry.delete(0,END)
    boxEntry.delete(0,END)
    auctionRateEntry.delete(0,END)
    weightEntry.delete(0,END)
    clear_coldFacility_option()
    
def clear_sales_input():
    clear_partyName_option()
    sale_markingIdEntryFilter.delete(0,END)

def addSales():
    popup=Toplevel(frame1,padx=30,pady=30)
    popup.title("Add Sales To")
    # data = session.query(Purchase).filter(Purchase.id==idPurchase).first()

    salesToNameVar = StringVar()
    salesToNameLabel = ttk.Label(popup,text="Sold To",anchor="w")
    salesToNameLabel.grid(row=0,column=0,padx=10,pady=10,sticky="w")
    salesToNameEntry = ttk.OptionMenu(popup,salesToNameVar,defaultPartyOption,*partyNameOptions)
    salesToNameVar.set(defaultPartyOption)
    salesToNameEntry.grid(row=0,column=1,padx=10,pady=10)


    salesToBoxVar = IntVar()
    salesToBoxLabel = ttk.Label(popup,text="Box",anchor="w")
    salesToBoxLabel.grid(row=1,column=0,padx=10,pady=10,sticky="w")
    salesToBoxEntry = ttk.Entry(popup,textvariable=salesToBoxVar)
    salesToBoxEntry.grid(row=1,column=1,padx=10,pady=10)
    salesToBoxEntry.delete(0,END)
    salesToBoxEntry.insert(0,str(boxVar.get()))

    def addSalesTo():
        data = session.query(Purchase).filter(Purchase.id==idPurchase).first()
        # print(f"{salesToBoxVar.get()}=========================")
        if(salesToNameEntry != ""):
            s = Sell(MarkingID = data.MarkingID,
                     SellTo = salesToNameVar.get(),
                     Box = salesToBoxVar.get(),
                     purchase_id = data.id)
            session.add(s)
            data.Box = int(data.Box) - int(salesToBoxVar.get())
            session.commit()
            getSales()
            getPurchase()
            salesToNameVar.set(defaultPartyOption)
            salesToBoxEntry.delete(0,END)
            statusSalesTo["text"] = "Status: Sales Added Successfully"
            statusSalesTo.config(background='green',foreground='white')
            statusSalesTo.after(10000,lambda:statusSalesTo.config(text="Status:",background='white',foreground='black'))


    salesToAddbtn = ttk.Button(popup,text="ADD sales",command=addSalesTo)
    salesToAddbtn.grid(row=2,column=0,padx=20,pady=20,sticky="w")

    statusSalesTo = ttk.Label(popup,text="Status: ",anchor="w")
    statusSalesTo.grid(row=3,column=0,sticky="we",pady=5,columnspan=3)

def deleteSales():
    data = session.query(Sell).filter(Sell.id == idSales).first()
    if(data):
        session.delete(data)
        session.commit()
        getSales()
        sale_status["text"] = "Status: Sales deleted successfully"
        sale_status.config(background='green',foreground='white')
        sale_status.after(10000,lambda:sale_status.config(text="Status:",background='white',foreground='black'))

def editSales():
    if(sale_soldToNameVarFilter.get() != defaultPartyOption and sale_markingidPurchaseFilter.get() != ""):       
        data = session.query(Sell).filter(Sell.id == idSales).first()
        if(data):
            data.SellTo = sale_soldToNameVarFilter.get().split(" ")[0]
            data.MarkingID=sale_markingidPurchaseFilter.get()
            session.commit()
            clearPurchase()
            getSales()
            sale_status["text"] = "Status: Sales Edit successfully"
            sale_status.config(background='green',foreground='white')
            sale_status.after(10000,lambda:sale_status.config(text="Status:",background='white',foreground='black'))

def dispatchedSales():
    popup=Toplevel(master=frame2,padx=30,pady=30)
    popup.title("Add Dispached Info")
    data = session.query(Sell).filter(Sell.id==idSales).first()

    sale_dispatched_info_var = IntVar()
    sale_dispatched_info_Entry = ttk.Checkbutton(popup,text="Dispatched",variable=sale_dispatched_info_var)
    sale_dispatched_info_Entry.grid(row=0,column=0,pady=10,sticky="w")


    sale_dispatched_date_Label = ttk.Label(popup,text="Dispatched Date",anchor="w")
    sale_dispatched_date_Label.grid(row=1,column=0,pady=10,sticky="w")
    sale_dispatched_date_Entry = DateEntry(popup, selectmode = 'day', date_pattern="dd-mm-yyyy",state="disabled")
    sale_dispatched_date_Entry.grid(row=1,column=1,padx=10,pady=10)

    if(sale_dispatched_info_var):
        sale_dispatched_date_Entry.config(state="normal")

    def addDispatched():
        data = session.query(Sell).filter(Sell.id==idSales).first()
        if(sale_dispatched_info_var):
            data.Dispatched = sale_dispatched_info_var.get()
            data.DispatchDate = sale_dispatched_date_Entry.get_date()
            session.commit()
            status_sale_dispatched["text"] = "Status: Dispatched Added Successfully"
            status_sale_dispatched.config(background='green',foreground='white')
            status_sale_dispatched.after(10000,lambda:status_sale_dispatched.config(text="Status:",background='white',foreground='black'))

    sale_dispatched_btn = ttk.Button(popup,text="Update Dispatched Status",command=addDispatched)
    sale_dispatched_btn.grid(row=2,column=0,pady=20,sticky="w")

    status_sale_dispatched = ttk.Label(popup,text="Status: ",anchor="w")
    status_sale_dispatched.config(background='white',foreground='black')
    status_sale_dispatched.grid(row=3,column=0,sticky="we",pady=5,columnspan=3)

def purchaseListInsert(items):
    purchaseList.delete(0,END)
    i=1
    for item in items:
        purchaseList.insert(i,item)
        i+=1

def getPurchase():
    aFrom = auctionDateEntryFilter.get_date()
    aTo = auctionDateToEntryFilter.get_date()
    f = firmNameVarFilter.get()
    m = markingidPurchaseFilter.get()
    c = coldVarFilter.get()
    all = getAllCheckVar.get()
    if(all==1):
        data = session.query(Purchase).all()
        purchaseListInsert(data)
        
    
    elif(f!=partyNameOptions[0] and m!="" and c!=coldFacilityOptions[0]):
        data = session.query(Purchase).filter(Purchase.AuctionDate>=aFrom,Purchase.AuctionDate<=aTo,
                                              Purchase.FirmName==int(f.split(" ")[0]),
                                              Purchase.MarkingID==m,
                                              Purchase.Box>0,
                                              Purchase.coldfacility_id==int(c.split(" ")[0]))
        purchaseListInsert(data)
       
    
    elif(f!=partyNameOptions[0] and c!=coldFacilityOptions[0]):
        data = session.query(Purchase).filter(Purchase.AuctionDate>=aFrom,Purchase.AuctionDate<=aTo,
                                              Purchase.FirmName==int(f.split(" ")[0]),
                                              Purchase.Box>0,
                                              Purchase.coldfacility_id==int(c.split(" ")[0]))
        purchaseListInsert(data)
       
    
    elif(m!="" and c!=coldFacilityOptions[0]):
        data = session.query(Purchase).filter(Purchase.AuctionDate>=aFrom,Purchase.AuctionDate<=aTo,
                                              Purchase.MarkingID==m,
                                              Purchase.Box>0,
                                              Purchase.coldfacility_id==int(c.split(" ")[0]))
        purchaseListInsert(data)
       
    
    elif(f!=coldFacilityOptions[0] and m!=""):
        data = session.query(Purchase).filter(Purchase.AuctionDate>=aFrom,Purchase.AuctionDate<=aTo,
                                              Purchase.MarkingID==m,
                                              Purchase.Box>0,
                                              Purchase.FirmName==int(f.split(" ")[0]))
        purchaseListInsert(data)
        
    
    elif(f!=coldFacilityOptions[0]):
        data = session.query(Purchase).filter(Purchase.AuctionDate>=aFrom,Purchase.AuctionDate<=aTo,
                                              Purchase.Box>0,
                                              Purchase.FirmName==int(f.split(" ")[0]))
        purchaseListInsert(data)
       
    
    elif(m!=""):
        data = session.query(Purchase).filter(Purchase.AuctionDate>=aFrom,Purchase.AuctionDate<=aTo,
                                              Purchase.Box>0,
                                              Purchase.MarkingID==m)
        purchaseListInsert(data)

    elif(c!=coldFacilityOptions[0]):
        data = session.query(Purchase).filter(Purchase.AuctionDate>=aFrom,Purchase.AuctionDate<=aTo,
                                              Purchase.Box>0,
                                              Purchase.coldfacility_id==int(c.split(" ")[0]))
        purchaseListInsert(data)
        

    else:
        data = session.query(Purchase).filter(Purchase.AuctionDate>=aFrom,Purchase.AuctionDate<=aTo,
                                              Purchase.Box>0)
        purchaseListInsert(data)


    purchase_list_scroll = Scrollbar(frame1,orient='vertical',command=purchaseList.yview)
    purchase_list_scroll.grid(row=7,column=8,sticky="ens")
    purchaseList.configure(yscrollcommand=purchase_list_scroll.set)

def salesListInsert(items):
    salesList.delete(0,END)
    i=1
    # for item in items:
    #     salesList.insert(i,item)
    #     i+=1
    for item in items:
        d = str(item).split(' | ')
        salesList.insert(i,f"{d[0]} | {d[1]} | Sold To: {d[3]} | {d[4]} | {d[5].split(',')[0]}")
        i+=1              

def getSales():
    s = sale_soldToNameVarFilter.get()
    m = sale_markingidPurchaseFilter.get()
    all = sale_getAllCheckVar.get()
    print(s)
    if(all==1):
        data = session.query(Sell).all()
        if(data):
            salesListInsert(data)
            return

    elif(s!=defaultPartyOption and m!=""):
        data = session.query(Sell,Purchase).filter(Sell.purchase_id == Purchase.id,
                                                   Sell.SellTo==int(s.split(" ")[0]),
                                                   Sell.MarkingID==m)
        if(data):
            salesListInsert(data)      
            return
    
    elif(s!=defaultPartyOption):
        data = session.query(Sell,Purchase).filter(Sell.purchase_id == Purchase.id,
                                                   Sell.SellTo==int(s.split(" ")[0]))
        if(data):
            salesListInsert(data)      
            return
    
    elif(m!=""):
        data = session.query(Sell,Purchase).filter(Sell.purchase_id == Purchase.id,
                                                   Sell.MarkingID==m)
        if(data):
            salesListInsert(data)      
            return
        

    else:
        data = session.query(Sell).filter(Sell.Dispatched == 0)
        if(data):
            salesListInsert(data)
            return

def addColdFacility():
    if(coldFacilityEntry != ""):
        c = ColdFacility(Name=coldFacilityVar.get())                     
        session.add(c)
        session.commit()
        coldFacilityEntry.delete(0,END)
        getColdFacility()
        getColdFacilityOptions()
        global coldbox,coldboxFilter,coldVar,coldVarFilter
        coldbox = ttk.OptionMenu(frame1,coldVar,*coldFacilityOptions)
        coldboxFilter = ttk.OptionMenu(frame1,coldVarFilter,*coldFacilityOptions)
        status3["text"] = "Status: Cold Facility Added successfully"
        status3.config(background='green',foreground='white')
        status3.after(3000,lambda:status3.config(text="Status:",background='white',foreground='black'))

def deleteColdFacility():
    if(coldFacilityEntry != ""):
        data = session.query(ColdFacility).filter(ColdFacility.id == idCold).first()
        if(data):
            session.delete(data)
            session.commit()
            getColdFacility()
            getColdFacilityOptions()
            global coldbox,coldboxFilter,coldVar,coldVarFilter
            coldbox = ttk.OptionMenu(frame1,coldVar,*coldFacilityOptions)
            coldboxFilter = ttk.OptionMenu(frame1,coldVarFilter,*coldFacilityOptions)
            status3["text"] = "Status: Cold Facility deleted successfully"
            status3.config(background='red',foreground='white')
            status3.after(3000,lambda:status3.config(text="Status:",background='white',foreground='black'))

def editColdFacility():
    if(coldFacilityVar.get() != ""):       
        data = session.query(ColdFacility).filter(ColdFacility.id == idCold).first()
        if(data):
            data.Name = coldFacilityVar.get()
            session.commit()
            clearPurchase()
            getColdFacility()
            status3["text"] = "Status: Cold Facility Edit successfully"
            status3.config(background='green',foreground='white')
            status3.after(10000,lambda:status3.config(text="Status:",background='white',foreground='black'))

def getColdFacility():
    data = session.query(ColdFacility).all()
    coldListInsert(data)

def coldListInsert(items):
    coldFacilityList.delete(0,END)
    i=1
    for item in items:
        coldFacilityList.insert(i,item)
        i+=1
    
def addpartyName():
    if(partyNameEntry != ""):
        p = PartyName(Name=partyNameVar.get())                     
        session.add(p)
        session.commit()
        partyNameEntry.delete(0,END)
        getpartyName()
        getpartyNameOptions()
        global coldbox,coldboxFilter,coldVar,coldVarFilter
        coldbox = ttk.OptionMenu(frame1,coldVar,*partyNameOptions)
        coldboxFilter = ttk.OptionMenu(frame1,coldVarFilter,*partyNameOptions)
        status4["text"] = "Status: Party Name Added successfully"
        status4.config(background='green',foreground='white')
        status4.after(3000,lambda:status4.config(text="Status:",background='white',foreground='black'))

def deletepartyName():
    if(partyNameEntry != ""):
        data = session.query(PartyName).filter(PartyName.id == idParty).first()
        if(data):
            session.delete(data)
            session.commit()
            getpartyName()
            getpartyNameOptions()
            global coldbox,coldboxFilter,coldVar,coldVarFilter          # Remains edit
            coldbox = ttk.OptionMenu(frame1,coldVar,*partyNameOptions)
            coldboxFilter = ttk.OptionMenu(frame1,coldVarFilter,*partyNameOptions)
            status4["text"] = "Status: Party deleted successfully"
            status4.config(background='red',foreground='white')
            status4.after(3000,lambda:status4.config(text="Status:",background='white',foreground='black'))

def editpartyName():
    if(partyNameVar.get() != ""):       
        data = session.query(PartyName).filter(PartyName.id == idParty).first()
        if(data):
            data.Name = partyNameVar.get()
            session.commit()
            clearPurchase()                         #  To be understand
            getpartyName()
            status4["text"] = "Status: Party Edit successfully"
            status4.config(background='green',foreground='white')
            status4.after(10000,lambda:status4.config(text="Status:",background='white',foreground='black'))

def getpartyName():
    data = session.query(PartyName).all()
    partyListInsert(data)

def partyListInsert(items):
    partyNameList.delete(0,END)
    i=1
    for item in items:
        partyNameList.insert(i,item)
        i+=1
    
def set_row_background_color(sheet, row_index, color):
    fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
    for cell in sheet[row_index]:
        cell.fill = fill

def convert_to_excel():
    data = session.query(ColdFacility).filter(ColdFacility.id == idCold).first()
    sheet_name = data.Name
    try:
        workbook = openpyxl.Workbook()
        workbook.active.title = sheet_name
        
        if sheet_name in workbook.sheetnames:
            sheet = workbook[sheet_name]
        else:
            sheet = workbook.create_sheet(sheet_name)
        sheet.append(["S.No","Auction Date","Purchased From","Marking ID","BOX","Auction Rate","Weight","Sold To","Cold"])        

        sheet.column_dimensions['A'].width = 6
        sheet.column_dimensions['B'].width = 15
        sheet.column_dimensions['C'].width = 16
        sheet.column_dimensions['D'].width = 13
        sheet.column_dimensions['E'].width = 10
        sheet.column_dimensions['F'].width = 13
        sheet.column_dimensions['G'].width = 13
        sheet.column_dimensions['H'].width = 15
        sheet.column_dimensions['I'].width = 10

        all_cold = all_coldFacility_data.get_children()
        for i, item in enumerate(all_cold):
            values = all_coldFacility_data.item(item)["values"]
            SNocell = sheet.cell(row=i+2, column=1)
            SNocell.value = i+1
            SNocell.alignment = Alignment(horizontal="left")

            for j, value in enumerate(values):
                cell = sheet.cell(row=i+2, column=j+2)
                cell.value = value
                cell.alignment = Alignment(horizontal="left")

        set_row_background_color(sheet, 1, "FFFF00")
        workbook.save(f"{sheet_name}_data.xlsx")
        status3["text"] = f"Status: Data is exported in {sheet_name}_data.xlsx file."
        status3.config(background='green',foreground='white')
        status3.after(3000,lambda:status3.config(text="Status:",background='white',foreground='black'))

    except PermissionError as e:
        status3["text"] = f"Status: {sheet_name}_data.xlsx file is opened somewhere, close the file to export!"
        status3.config(background='red',foreground='white')
        status3.after(3000,lambda:status3.config(text="Status:",background='white',foreground='black'))

def getreport():
    c=session.query(ColdFacility).all()
    report.delete(0,END)
    for item in c:
        box_in_cold = session.query(Purchase).filter(Purchase.coldfacility_id == item.id)
        total_box = 0
        for lis in box_in_cold:
            if(lis.sells):
                full_string = str(lis.sells)
                dispatch_info = full_string.split(" | ")[5].split(": ")[1][:-1]
                if(dispatch_info == 'False'):
                    sold_box = int(full_string.split(" | ")[4].split(": ")[1])
                    total_box = lis.Box + sold_box
            else:
                total_box += lis.Box
        
            # total_box = lis.Box + lis.sells
        report.insert(END,f"Total No of Box in {item.Name} = {total_box}")

    unsold = session.query(Purchase).filter(Purchase.Box > 0)
    box_unsold = 0
    for item in unsold:
        box_unsold += item.Box
    unsold_box['text'] = f"Total Unsold Box = {box_unsold}"

    sold = session.query(Sell).all()
    box_sold = 0
    for item in sold:
        box_sold += item.Box
    total_sold_box['text'] = f"Total Sold Box = {box_sold}"

    weight_pen = session.query(Purchase).filter(Purchase.weight < 1)
    pending_weight['text'] = f"Total Pending weight LOTS = {weight_pen.count()}"
    
    

# FRAME NO. 1  ================================================================ 
# ============================================================================= 
# ============================================================================= 
frame1 = Frame(master=root,padx=10,pady=10,borderwidth=3,relief="groove")

# All Fields
Label(frame1,text="Add new purchase",font=("times new roman",13),anchor="w",bg="#696562",fg="white").grid(row=0,column=0,sticky="we",columnspan=8,pady=10,ipady=3,ipadx=5)

idPurchase = IntVar()
firmNameVar = StringVar()
markingidPurchase = StringVar()
boxVar = IntVar()
auctionRateVar = StringVar()
coldVar = StringVar()
defaultPartyOption = "0 None"
rateVar = DoubleVar()
weightVar = DoubleVar(value=0)
defaultColdFacilityOption = "0 None"
firmNameVarFilter = StringVar()
markingidPurchaseFilter = StringVar()
coldVarFilter = StringVar()
getAllCheckVar = IntVar()
sale_soldToNameVarFilter = StringVar()
partyNameOptions = [defaultPartyOption]
coldFacilityOptions = [defaultColdFacilityOption]

auctionDateLabel = ttk.Label(master=frame1,text="Auction Date")
auctionDateLabel.grid(row=1,column=0)
auctionDateEntry = DateEntry(master=frame1, selectmode = 'day', date_pattern="dd-mm-yyyy")
auctionDateEntry.grid(row=2,column=0)

firmNameLabel = ttk.Label(master=frame1,text="Firm Name")
firmNameLabel.grid(row=1,column=1)


getpartyNameOptions()
firmNameEntry = ttk.OptionMenu(frame1,firmNameVar,defaultPartyOption,*partyNameOptions)
clear_partyName_option()
firmNameEntry.grid(row=2,column=1,padx=3)

markingIdLabel = ttk.Label(master=frame1,text="Marking Id")
markingIdLabel.grid(row=1,column=2)
markingIdEntry = ttk.Entry(master=frame1, textvariable=markingidPurchase)
markingIdEntry.grid(row=2,column=2,padx=3)

boxLabel = ttk.Label(master=frame1,text="Box")
boxLabel.grid(row=1,column=3)
boxEntry = ttk.Entry(master=frame1, textvariable=boxVar)
boxEntry.grid(row=2,column=3,padx=3)

auctionRateLabel = ttk.Label(master=frame1,text="Auction Rate")
auctionRateLabel.grid(row=1,column=4)
auctionRateEntry = ttk.Entry(master=frame1, textvariable=auctionRateVar)
auctionRateEntry.grid(row=2,column=4,padx=3)

def update_rateVar(*args):
    print()
    rateVar.set(value=round(float(auctionRateVar.get())+2.5,1))

rateLabel = ttk.Label(master=frame1,text="Rate")
rateLabel.grid(row=1,column=5)
rateEntry = ttk.Label(master=frame1, textvariable=rateVar,background="white")
rateEntry.grid(row=2,column=5,padx=3,sticky="we")
auctionRateVar.trace("w",update_rateVar)

weightLabel = ttk.Label(master=frame1,text="Net Weight")
weightLabel.grid(row=1,column=6)
weightEntry = ttk.Entry(master=frame1, textvariable=weightVar)
weightEntry.grid(row=2,column=6,padx=3)

coldLabel = ttk.Label(master=frame1,text="Cold Facility")
coldLabel.grid(row=1,column=7,padx=3,sticky="WE")

getColdFacilityOptions()
coldbox = ttk.OptionMenu(frame1,coldVar,defaultColdFacilityOption,*coldFacilityOptions)
clear_coldFacility_option()
coldbox.grid(row=2,column=7,padx=3,sticky="WE")

# Buttons
addPurchaseBtn = ttk.Button(master=frame1,text="Add Purchase",command=addPurchase)
addPurchaseBtn.grid(row=3,column=1,sticky="WE",pady=10,padx=3)

deletePurchaseBtn = ttk.Button(master=frame1,text="Delete Purchase",command=deletePurchase)
deletePurchaseBtn.grid(row=3,column=2,sticky="WE",padx=3)

editPurchaseBtn = ttk.Button(master=frame1,text="Update Purchase",command=editPurchase)
editPurchaseBtn.grid(row=3,column=3,sticky="WE",padx=3)

clearPurchaseBtn = ttk.Button(master=frame1,text="Clear Fields",command=clearPurchase)
clearPurchaseBtn.grid(row=3,column=4,sticky="WE",padx=3)

#============================================================================================

Label(frame1,text="Search Data and Add Filters",font=("times new roman",13),anchor="w",bg="#696562",fg="white").grid(row=4,column=0,sticky="we",columnspan=8,pady=20,ipady=3,ipadx=5)

# filters
auctionDateLabelFilter = ttk.Label(master=frame1,text="Auction Date From")
auctionDateLabelFilter.grid(row=5,column=0,sticky="WE",padx=3)
auctionDateEntryFilter = DateEntry(master=frame1, selectmode = 'day', date_pattern="dd-mm-yyyy")
auctionDateEntryFilter.grid(row=6,column=0,sticky="WE",padx=3)

Label(master=frame1,text="Auction Date To").grid(row=5,column=1,sticky="WE",padx=3)
auctionDateToEntryFilter = DateEntry(master=frame1, selectmode = 'day', date_pattern="dd-mm-yyyy")
auctionDateToEntryFilter.grid(row=6,column=1,sticky="WE",padx=3)

firmNameLabelFilter = ttk.Label(master=frame1,text="Firm Name")
firmNameLabelFilter.grid(row=5,column=2,padx=3)
firmNameEntryFilter = ttk.OptionMenu(frame1,firmNameVarFilter,defaultPartyOption,*partyNameOptions)
clear_partyName_option()
firmNameEntry.grid(row=2,column=1,padx=3)
firmNameEntryFilter.grid(row=6,column=2,padx=3)

markingIdLabelFilter = ttk.Label(master=frame1,text="Marking Id")
markingIdLabelFilter.grid(row=5,column=3,padx=3)
markingIdEntryFilter = ttk.Entry(master=frame1,textvariable=markingidPurchaseFilter)
markingIdEntryFilter.grid(row=6,column=3,padx=3)

coldLabelFilter = ttk.Label(master=frame1,text="Cold Facility")
coldLabelFilter.grid(row=5,column=4,sticky="WE",padx=3)

coldboxFilter = ttk.OptionMenu(frame1,coldVarFilter,defaultColdFacilityOption,*coldFacilityOptions)
clear_coldFacility_option()
coldboxFilter.grid(row=6,column=4,sticky="WE",padx=3)

getAllCheckBox = ttk.Checkbutton(frame1,text="GET All Purchases",variable=getAllCheckVar)
getAllCheckBox.grid(row=6,column=5,sticky="WE",padx=3)

purchaseFilterBtn = ttk.Button(master=frame1,text="Filter",command=getPurchase)
purchaseFilterBtn.grid(row=6,column=6,sticky="WE",padx=3)

#==========================================================================================

purchaseList = Listbox(frame1,height=8)
purchaseList.grid(row=7,column=0,sticky="we",columnspan=8,pady=10)
purchaseList.bind('<<ListboxSelect>>',purchaseListSelect)


getPurchase()

addSalesbtn = ttk.Button(master=frame1,text="Sales To",command=addSales,state="disabled")
addSalesbtn.grid(row=8,column=0,sticky="WE",padx=3)

status1 = ttk.Label(master=frame1,text="Status: ",anchor="w",font=('times new roman',12))
status1.config(background='white',foreground='black')
status1.grid(row=9,column=0,columnspan=8,sticky="we",pady=10)

purchase_info = Listbox(master=frame1,height=3,fg="red",font=('times new roman',14))
purchase_info.grid(row=10,column=0,columnspan=8,sticky="we",ipadx=10,ipady=10)

report_frame = ttk.Frame(master=frame1,borderwidth=6,border=5)
report_frame.grid(row=0,column=9,rowspan=10,columnspan=2,sticky="n",padx=10)

ttk.Label(master=report_frame,text="Report at Glance",font=('arial',24,"bold")).grid(row=1,column=0,sticky="nsew",padx=10,pady=20)
unsold_box = ttk.Label(master=report_frame,text="Total Unsold Box = ",font=('arial',14))
unsold_box.grid(row=6,column=0,columnspan=9,sticky="nsew",pady=5)
total_sold_box = ttk.Label(master=report_frame,text="Total Sold Box = ",font=('arial',14))
total_sold_box.grid(row=7,column=0,sticky="w",pady=5)
pending_weight = ttk.Label(master=report_frame,text="Total Pending weight LOTS = ",font=('arial',14))
pending_weight.grid(row=8,column=0,sticky="w",pady=5)
report = Listbox(master=report_frame,height=6,font=('arial',14),relief="flat",width=45)
report.grid(row=2,column=0,sticky="we")
getreport()
report_refresh_btn = ttk.Button(master=report_frame,text="Refresh Report",command=getreport)
report_refresh_btn.grid(row=9,column=0,ipadx=20,ipady=3,pady=10)




# FRAME NO. 2 ==============================================================================
#===========================================================================================
#===========================================================================================

frame2 = Frame(master=root,padx=10,pady=10,borderwidth=3,relief="groove")

idSales = IntVar()

Label(frame2,text="All Sales | OR add Filters",font=("times new roman",16),anchor="w",bg="#696562",fg="white").grid(row=0,column=0,sticky="we",columnspan=10,pady=10,ipady=3,ipadx=5)


sale_soldToNameLabelFilter = ttk.Label(master=frame2,text="Sold To Name")
sale_soldToNameLabelFilter.grid(row=1,column=0,sticky="NSEW")
sale_soldToNameFilter = ttk.OptionMenu(frame2,sale_soldToNameVarFilter,defaultPartyOption,*partyNameOptions)
clear_partyName_option()
sale_soldToNameFilter.grid(row=2,column=0,sticky="WE",pady=10)


sale_markingidPurchaseFilter = StringVar()
sale_markingIdLabelFilter = ttk.Label(master=frame2,text="Marking Id")
sale_markingIdLabelFilter.grid(row=1,column=1,sticky="WE",padx=30)
sale_markingIdEntryFilter = ttk.Entry(master=frame2,textvariable=sale_markingidPurchaseFilter)
sale_markingIdEntryFilter.grid(row=2,column=1,sticky="WE",padx=30,pady=10)

# sale_coldVarFilter = StringVar()
# sale_coldLabelFilter = Label(master=frame2,text="Cold Facilit")
# sale_coldLabelFilter.grid(row=1,column=2)

# sale_coldboxFilter = OptionMenu(frame2,coldVarFilter,*coldFacilityOptions)
# sale_coldVarFilter.set(coldFacilityOptions[0])
# sale_coldboxFilter.grid(row=2,column=2,sticky="WE")

sale_getAllCheckVar = IntVar()
sale_getAllCheckBox = ttk.Checkbutton(master=frame2,text="GET All Sales",variable=sale_getAllCheckVar)
sale_getAllCheckBox.grid(row=2,column=2)
 

# Buttons
sale_FilterBtn = ttk.Button(master=frame2,text="Filter",command=getSales)
sale_FilterBtn.grid(row=2,column=3,sticky="WE")

salesList = Listbox(frame2,height=int(h*0.1),width=int(w*0.5),font=font.Font(size=10))
salesList.grid(row=3,column=0,sticky="we",columnspan=10)
salesList.bind('<<ListboxSelect>>',salesListSelect)

getSales()

sale_deleteBtn=ttk.Button(master=frame2,text="Delete Sale",command=deleteSales)
sale_deleteBtn.grid(row=4,column=0,pady=15,sticky="WE",padx=5)

# sale_editBtn=ttk.Button(master=frame2,text="Edit Sale",command=editSales)
# sale_editBtn.grid(row=4,column=1)

sale_dispatchedBtn=ttk.Button(master=frame2,text="Enter Dispached INFO",command=dispatchedSales)
sale_dispatchedBtn.grid(row=4,column=1,sticky="WE",padx=30)

sale_status = ttk.Label(master=frame2,text="Status: ",anchor="w",font=('times new roman',12))
sale_status.config(background='white',foreground='black')
sale_status.grid(row=5,column=0,columnspan=10,sticky="we",pady=10)

sale_info = Listbox(frame2,height=3,fg="red",font=('times new roman',14),relief="groove")
sale_info.grid(row=6,column=0,columnspan=10,sticky="we",ipady=10)


# FRAME NO. 3==============================================================================
# =========================================================================================
# =========================================================================================

frame3 = Frame(master=root,padx=10,pady=10,borderwidth=3,relief="groove")

# Variables
Label(master=frame3,text="Add New Cold Facility",font=("times new roman",13),anchor="w",bg="#696562",fg="white").grid(row=0,column=0,sticky="we",columnspan=3,pady=10,ipady=3,ipadx=5,padx=5)
Label(master=frame3,text="Total LOTS in Cold Facility",font=("times new roman",13),anchor="w",bg="#696562",fg="white").grid(row=0,column=3,sticky="we",columnspan=3,pady=10,ipady=3,ipadx=5,padx=5)
# ttk.Label(master=frame3,text="Add New Cold Facility").grid(row=0,column=0)

idCold = IntVar()

coldFacilityVar = StringVar()
coldFacilityLable = ttk.Label(master=frame3,text="Cold Facility Name: ")
coldFacilityLable.grid(row=1,column=0)
coldFacilityEntry = ttk.Entry(master=frame3,textvariable=coldFacilityVar)
coldFacilityEntry.grid(row=1,column=1)

# Buttons
addColdFacilityBtn = ttk.Button(master=frame3,text="Add Cold facility",command=addColdFacility)
addColdFacilityBtn.grid(row=1,column=2,sticky="WE",padx=15)

deleteColdFacilityBtn = ttk.Button(master=frame3,text="Delete Cold facility",command=deleteColdFacility)
deleteColdFacilityBtn.grid(row=2,column=2,sticky="WE",padx=15,ipadx=5)

editColdFacilityBtn = ttk.Button(master=frame3,text="Edit Cold facility",command=editColdFacility)
editColdFacilityBtn.grid(row=3,column=2,sticky="WE",padx=15)

coldFacilityList = Listbox(master=frame3,height=7)
coldFacilityList.grid(row=2,column=0,sticky="WE",columnspan=2,rowspan=5)
coldFacilityList.bind('<<ListboxSelect>>',coldListSelect)

getColdFacility()

status3 = ttk.Label(master=frame3,text="Status: ",anchor="w",font=('times new roman',12))
status3.config(background='white',foreground='black')
status3.grid(row=17,column=0,columnspan=5,sticky="we",pady=10)

# label_text_head = "{:^15} | {:^25} | {:^15} | {:^10} | {:^15} | {:^10} | {:^25} | {:^10}"
# label_text_head = label_text_head.format('Auction Date','Purchased From','Marking ID','BOX','Auction Rate','Weight','Sold To','Cold')
# ttk.Label(master=frame3,text=label_text_head,font=('times new roman',12)).grid(row=1,column=3,sticky="w")


# all_coldFacility_data = Listbox(master=frame3,height=15,width=100,font=('times new roman',12),relief="groove")
# all_coldFacility_data.grid(row=1,column=3,rowspan=14,sticky="we",ipadx=10,ipady=10)

all_coldFacility_data = ttk.Treeview(frame3, selectmode ='browse')
all_coldFacility_data.grid(row=1,column=3,rowspan=14,sticky='w',ipadx=20)


all_coldFacility_data["columns"] = ('1','2','3','4','5','6','7','8')

all_coldFacility_data.column("#0", width= 40, anchor ='se')
all_coldFacility_data.column("1", width = 90, anchor ='se')
all_coldFacility_data.column("2", width = 100, anchor ='se')
all_coldFacility_data.column("3", width = 80, anchor ='se')
all_coldFacility_data.column("4", width = 50, anchor ='se')
all_coldFacility_data.column("5", width = 80, anchor ='se')
all_coldFacility_data.column("6", width = 70, anchor ='se')
all_coldFacility_data.column("7", width = 90, anchor ='se')
all_coldFacility_data.column("8", width = 50, anchor ='center')

all_coldFacility_data.heading("#0", text ="S.No")
all_coldFacility_data.heading("1", text ="Auction Date")
all_coldFacility_data.heading("2", text ="Purchased From")
all_coldFacility_data.heading("3", text ="Marking ID")
all_coldFacility_data.heading("4", text ="BOX")
all_coldFacility_data.heading("5", text ="Auction Rate")
all_coldFacility_data.heading("6", text ="Weight")
all_coldFacility_data.heading("7", text ="Sold To")
all_coldFacility_data.heading("8", text ="Cold")

exportFile = ttk.Button(master=frame3,text="Export",command=convert_to_excel)
exportFile.grid(row=16,column=3,sticky="E",pady=10)


# FRAME NO. 4==============================================================================
# =========================================================================================
# =========================================================================================

frame4 = Frame(master=root,padx=10,pady=10,borderwidth=3,relief="groove")

# Variables
Label(master=frame4,text="Add New Party Name",font=("times new roman",13),anchor="w",bg="#696562",fg="white").grid(row=0,column=0,sticky="we",columnspan=3,pady=10,ipady=3,ipadx=5,padx=5)
Label(master=frame4,text="Total Purachase & Sales of Party",font=("times new roman",13),anchor="w",bg="#696562",fg="white").grid(row=0,column=3,sticky="we",columnspan=3,pady=10,ipady=3,ipadx=5,padx=5)
# ttk.Label(master=frame4,text="Add New Cold Facility").grid(row=0,column=0)

idParty = IntVar()

partyNameVar = StringVar()
partyNameLable = ttk.Label(master=frame4,text="Party Name: ")
partyNameLable.grid(row=1,column=0)
partyNameEntry = ttk.Entry(master=frame4,textvariable=partyNameVar)
partyNameEntry.grid(row=1,column=1)

# Buttons
addpartyNameBtn = ttk.Button(master=frame4,text="Add Party",command=addpartyName)
addpartyNameBtn.grid(row=1,column=2,sticky="WE",padx=15)

deletepartyNameBtn = ttk.Button(master=frame4,text="Delete Party",command=deletepartyName)
deletepartyNameBtn.grid(row=2,column=2,sticky="WE",padx=15,ipadx=5)

editpartyNameBtn = ttk.Button(master=frame4,text="Edit Party",command=editpartyName)
editpartyNameBtn.grid(row=3,column=2,sticky="WE",padx=15)

partyNameList = Listbox(master=frame4,height=7)
partyNameList.grid(row=2,column=0,sticky="WE",columnspan=2,rowspan=5)
partyNameList.bind('<<ListboxSelect>>',partyListSelect)

getpartyName()

status4 = ttk.Label(master=frame4,text="Status: ",anchor="w",font=('times new roman',12))
status4.config(background='white',foreground='black')
status4.grid(row=17,column=0,columnspan=5,sticky="we",pady=10)

all_partyName_data = Listbox(master=frame4,height=15,width=100,font=('times new roman',12),relief="groove")
all_partyName_data.grid(row=1,column=3,rowspan=15,sticky="we",ipadx=10,ipady=10)

#==================================================================================================
root.mainloop()