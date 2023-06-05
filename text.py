# from customtkinter import *
from tkcalendar import DateEntry
from tkinter import Menu,Tk,Label,Frame,IntVar,StringVar,DoubleVar,Listbox,END,Toplevel
from models import *
from tkinter import ttk
from datetime import date
# import models
# import win32print

root = Tk()
root.geometry("1000x600")
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

trail =9-int(str(date.today()).split("-")[2])

warn = ttk.Label(master=root,text="",font=("times new roman",14))
warn.grid(row=1,column=0,columnspan=5,pady=10)

if(trail):
  warn.config(text=f"{trail} Days Trail period Remaining. Please Purchase Full Version")
else:
  warn.config(text="Trail period is OVER. Please Purchase Full Version")
  navbar.entryconfigure("Purchase",state="disabled")
  navbar.entryconfigure("Sales",state="disabled")
  navbar.entryconfigure("Cold Facility",state="disabled")
  navbar.entryconfigure("Party Name",state="disabled")


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
        
        if(data):
            all_coldFacility_data.delete(0,END)
            all_coldFacility_data.insert(END,f"Total LOTS which Not Dispatched = {data.count()}")
            for item in data:
                l = str(item).split(' | ')
                pname = session.query(PartyName).filter(PartyName.id == int(l[2].split(':')[1])).first()
                all_coldFacility_data.insert(END,f"{l[0].split('(')[1]} | {l[1]} | Purchase From:{pname.Name} | {l[3]} | Sold To:{l[11]} | {l[12]} | {l[5]}")
                
            data1 = session.query(Purchase).filter(Purchase.coldfacility_id==int(id),Purchase.Box>0)
            all_coldFacility_data.insert(END,"=========================================================")
            all_coldFacility_data.insert(END,f"Total LOTS which Not Sold = {data1.count()}")
            if(data1):
                for item in data1:
                    l = str(item).split(' | ')
                    pname = session.query(PartyName).filter(PartyName.id == int(l[2].split(':')[1])).first()
                    all_coldFacility_data.insert(END,f"{l[0]} | {l[1]} | Purchase From:{pname.Name} | {l[3]} | Sold To: None | {l[4]} | {l[5]}")                   
        
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
            all_partyName_data.insert(i,f"=========================================")           
            i+=1
            all_partyName_data.insert(i,f"Total Sales {data1.count()}")
            i+=1 
            print("++++++++++++++++++++++++++++++++++++++++++",data,"+++++++++++++++++++++++")          
            for item in data1:
                print("*************************************************",item,"*************************")
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
        
        data = session.query(Purchase).filter(Purchase.id == idPurchase).first()
        if(data):
            data.AuctionDate = auctionDateEntry.get_date()
            data.FirmName=int(firmNameVar.get().split(" | ")[0])
            data.MarkingID=markingidPurchase.get()
            data.Box=boxVar.get()
            data.AuctionRate=float(auctionRateVar.get())
            data.Rate=float(rateVar.get())
            data.weight=weightVar.get()
            data.coldfacility_id=int(coldVar.get().split(" | ")[0])
            session.commit()
            clearPurchase()
            getPurchase()
            status1["text"] = "Status: Product Edit successfully"
            status1.config(background='green',foreground='white')
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
        return
    
    elif(f!=partyNameOptions[0] and m!="" and c!=coldFacilityOptions[0]):
        data = session.query(Purchase).filter(Purchase.AuctionDate>=aFrom,Purchase.AuctionDate<=aTo,
                                              Purchase.FirmName==int(f.split(" ")[0]),
                                              Purchase.MarkingID==m,
                                              Purchase.Box>0,
                                              Purchase.coldfacility_id==int(c.split(" ")[0]))
        purchaseListInsert(data)
        return
    
    elif(f!=partyNameOptions[0] and c!=coldFacilityOptions[0]):
        data = session.query(Purchase).filter(Purchase.AuctionDate>=aFrom,Purchase.AuctionDate<=aTo,
                                              Purchase.FirmName==int(f.split(" ")[0]),
                                              Purchase.Box>0,
                                              Purchase.coldfacility_id==int(c.split(" ")[0]))
        purchaseListInsert(data)
        return
    
    elif(m!="" and c!=coldFacilityOptions[0]):
        data = session.query(Purchase).filter(Purchase.AuctionDate>=aFrom,Purchase.AuctionDate<=aTo,
                                              Purchase.MarkingID==m,
                                              Purchase.Box>0,
                                              Purchase.coldfacility_id==int(c.split(" ")[0]))
        purchaseListInsert(data)
        return
    
    elif(f!=coldFacilityOptions[0] and m!=""):
        data = session.query(Purchase).filter(Purchase.AuctionDate>=aFrom,Purchase.AuctionDate<=aTo,
                                              Purchase.MarkingID==m,
                                              Purchase.Box>0,
                                              Purchase.FirmName==int(f.split(" ")[0]))
        purchaseListInsert(data)
        return
    
    elif(f!=coldFacilityOptions[0]):
        data = session.query(Purchase).filter(Purchase.AuctionDate>=aFrom,Purchase.AuctionDate<=aTo,
                                              Purchase.Box>0,
                                              Purchase.FirmName==int(f.split(" ")[0]))
        purchaseListInsert(data)
        return
    
    elif(m!=""):
        data = session.query(Purchase).filter(Purchase.AuctionDate>=aFrom,Purchase.AuctionDate<=aTo,
                                              Purchase.Box>0,
                                              Purchase.MarkingID==m)
        purchaseListInsert(data)
        return
    elif(c!=coldFacilityOptions[0]):
        data = session.query(Purchase).filter(Purchase.AuctionDate>=aFrom,Purchase.AuctionDate<=aTo,
                                              Purchase.Box>0,
                                              Purchase.coldfacility_id==int(c.split(" ")[0]))
        purchaseListInsert(data)
        return

    else:
        data = session.query(Purchase).filter(Purchase.AuctionDate>=aFrom,Purchase.AuctionDate<=aTo,
                                              Purchase.Box>0)
        purchaseListInsert(data)
        return

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
    
def convert_to_txt():
    data = "\n".join(all_coldFacility_data.get(0, END))
    with open("Cold_Facility_Data.txt", "w") as file:
        file.write(data)
    status3["text"] = "Status: Cold Facility Data EXPORTED"
    status3.config(background='green',foreground='white')
    status3.after(3000,lambda:status3.config(text="Status:",background='white',foreground='black'))

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
    rateVar.set(value=round(float(auctionRateVar.get())*1.025,1))

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

purchaseList = Listbox(frame1,height=5)
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


# FRAME NO. 2 ==============================================================================
#===========================================================================================
#===========================================================================================

frame2 = Frame(master=root,padx=10,pady=10,borderwidth=3,relief="groove")

idSales = IntVar()

Label(frame2,text="All Sales | OR add Filters",font=("times new roman",13),anchor="w",bg="#696562",fg="white").grid(row=0,column=0,sticky="we",columnspan=10,pady=10,ipady=3,ipadx=5)


sale_soldToNameLabelFilter = ttk.Label(master=frame2,text="Sold To Name")
sale_soldToNameLabelFilter.grid(row=1,column=0,sticky="WE")
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

salesList = Listbox(frame2,height=8,width=150)
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

all_coldFacility_data = Listbox(master=frame3,height=15,width=100,font=('times new roman',12),relief="groove")
all_coldFacility_data.grid(row=1,column=3,rowspan=15,sticky="we",ipadx=10,ipady=10)

exportFile = ttk.Button(master=frame3,text="Export",command=convert_to_txt)
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