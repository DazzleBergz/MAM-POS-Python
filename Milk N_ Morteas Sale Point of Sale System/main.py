import os
import datetime
import time
import random

d = datetime.datetime.now()
orderPending = []
orderID = ""
userType = ""
user = ""
# orderLists = {1:{"product":"fish","quantity":1,"price":100}}
orderLists = {}
item = 1
#validations
def validate():
    return input("Continue? [Y/N]")

def invalid():
    print("\n===========================")
    print("invalid Input")
    print("===========================") 

def pendings():
    orders = open("pendingOrders/ordersID.txt", "r")
    for order in orders.readlines(0):
        orderPending.append(order.replace("\n",""))
        
def generateOrderID():
    orders = open("pendingOrders/ordersID.txt", "r")
    global orderID
    if orders.read() != "":
        orderID = "S" + str(random.randint(1000, 9999))
        for order in orders.readlines(0):
            if orderID == order:
                generateOrderID()
    else:
        orderID = "S" + str(random.randint(1000, 9999))

def logout():
    global userType
    global user
    dashboard()

#end validations

#Get menu & order design
def menuDesign(choice, prices, menus, priceNames):
    
    longest = 0
    count = 0
    print("\t============="+ choice +"=============")
    for i in menus[choice]:
        if longest < len(i):
            longest = len(i)
    label = "Beverage Name"
    print("Code\tBeverage Name", end="")
    numberofS = longest - len(label) + 10
    for x in range(numberofS):
        print(" ", end="")
    for x in priceNames:
        print(x.replace("\n","") + "\t", end="")
        
    
    print()

    for i in menus[choice]:
        print("["+ str(count) +"]\t" + i, end="")
        numberofS = longest - len(i) + 10
        count += 1
        for x in range(numberofS):
            print(" ", end="")
        for i in range(len(prices)):
            print(prices[i]+"\t", end="")
        print()
    print("[X] ==> Cancel")
    return ""
    
def orderList():
    
    if len(orderLists) != 0:
        for x in orderLists:
            price = int(orderLists[x]["quantity"]) * int(orderLists[x]["price"])
            print("Item " + str(x) + ":" + "Product:" + orderLists[x]["product"] + "=> " + str(orderLists[x]["quantity"]) + ", Price:" + str(price))
    print("\n===========================")
    return ""

#End menu & orderdesign

#Start Order Taker
def receipt(total, payment):
    generateOrderID()
    print("==================================")
    print("Order ID: " + orderID)
    global d
    print("Date: "+ str(d.month)+"-"+str(d.day)+"-"+str(d.strftime("%y")))
    print("==================================")
    longest = 0
    print("Items\t"+"Product", end="")
    label = "Product"
    for x in orderLists:
        if longest < len(orderLists[x]["product"]):
            longest = len(orderLists[x]["product"])
                    
    numberofS = longest - len(label) + 10
    for x in range(numberofS):
        print(" ", end="")
    print("Qty"+"\tPrice")
    for i in orderLists:
        print(str(i) +"\t" + orderLists[i]["product"], end="")
        numberofS = longest - len(orderLists[i]["product"]) + 10
        for x in range(numberofS):
            print(" ", end="")
        print(str(orderLists[i]["quantity"]) +" \t"+ str(orderLists[i]["price"]))
    change =  payment - total
    print("==================================")
    print("Total Payment: " + str(total))
    print("Payment: " + str(payment))
    print("Change: " + str(change))
    

    date = str(d.month)+"-"+str(d.day)+"-"+str(d.strftime("%y"))
    named_tuple = time.localtime()
    times = time.strftime("%H:%M:%S", named_tuple)
    if os.path.exists("sales/"+ date +".txt"):
        saveSale = open("sales/"+ date +".txt", "a")
        saveSale.writelines("\n"+str(times)+ "\t" + str(total))
        saveSale.close()
    else:
        saveSale = open("sales/"+ date +".txt", "x")
        saveSale.write(date + " Sales\n")
        saveSale.write("Time\t Income")
        saveSale.writelines("\n"+str(times) + "\t " + str(total))
        saveSale.close()

    saveOrder = open("pendingOrders/"+ orderID +".txt", "a")
    saveOrder.write(orderID+":\n")
    for i in orderLists:
        saveOrder.write(str(i) + "=> " + orderLists[i]["product"] + ", Quantity => " + str(orderLists[i]["quantity"]) + ", Price => " + str(orderLists[i]["price"]))
    saveOrder.close()
    
    saveOrderID = open("pendingOrders/ordersID.txt", "a")
    saveOrderID.writelines(orderID+"\n")
    saveOrderID.close()

    orderLists.clear()
    global item
    item = 1
    input()

def getPayment():
    
    global orderLists
    totalPayment = 0
    print("\n===========================")
    print("[0] ==> Cancel")
    
    for x in orderLists:
        totalPayment += int(orderLists[x]["price"])
    print("Total Payment: " + str(totalPayment))
    try:
        payment = int(input("input Payment: "))
        if payment == 0:
            takeOrder()
        elif payment >= totalPayment:
            receipt(totalPayment, payment)
            choice = input("Continue?[Y/N] ")
            if choice =='Y' or choice == 'Y':
                takeOrder()
            else:
                maintransaction()
        else:
            print("Insufficient payment")
    except:
        getPayment()

def pendingOrders():
    if os.path.exists("pendingOrders/ordersID.txt"):
        pendingOrder = "Pending orders: "
        orders = open("pendingOrders/ordersID.txt", "r")
        count = 0
        for order in orders.readlines(0):
            pendingOrder = pendingOrder + " " + order
            count += 1
        print(pendingOrder.replace("\n", ""))
        orders.close()
    else:
        print("No pending orders")

        if count == 0:
            print("No pending orders")
    print("===========================")
    return ""

def getMenus():
    menus = {}
    menu = open("menu/menus.txt", "r")
    for menuA in menu.readlines():
        product = open("menu/products/"+ menuA.replace("\n","") +".txt", "r")
        menus[menuA.replace("\n","")] = []
        for products in product.readlines():
             menus[menuA.replace("\n","")].append(products.replace("\n",""))
    product.close()
    menu.close()
    return menus

def takeOrder():
    print("\n===========================")
    orderList()
    
    global item
    global orderLists
    
    menus = getMenus()
    catName = []
    prices = []
    priceNames = []
    count = 0
    
    for x in menus:
        catName.append(x.replace("\n",""))
        print("["+ str(count) +"]" + "==> "+ x.replace("\n",""))
        count += 1
    print("[X] ==> Cancel")
    print("[C] ==> Confirm Order")
    choice = input("Choose on the menu above: ")
    try:
        choice = int(choice)
        if choice < count or choice > 0:
            price = open("menu/prices/"+ catName[choice]+".txt", "r")
            for x in price.readlines():
                prices.append(x.replace("\n",""))
            priceN = open("menu/priceNames/"+ catName[choice]+".txt", "r")
            for x in priceN.readlines():
                priceNames.append(x.replace("\n",""))
        else:
            invalid()
            takeOrder()
    except:
        if choice == 'X' or choice == 'x':
            maintransaction()
        elif choice == 'C' or choice == 'c':
            getPayment()
        else:
            invalid()
            takeOrder()
        
    #display menu
    menuDesign(catName[choice], prices, menus, priceNames)
    
    print("\n===========================")
    choose = int(input("Choose your product: "))
    print("\n===========================")
    for i in range(len(priceNames)):
            print("["+ str(i) +"] ==>" + priceNames[i])
    size = int(input("Size: "))
    prices[size]
    print("\n===========================")
    quantity = int(input("Quantity: "))
    
    orderLists[item] = {
        "product" : menus[catName[choice]][choose],
        "quantity": quantity,
        "price" : prices[size]
        }
    
    item += 1
    takeOrder()

#End Order Taker

#all sales review
def takeAllSales():
    print("=============================")
    date = str(d.month)+"-"+str(d.day)+"-"+str(d.strftime("%y"))
    allSales = open("sales/"+ date +".txt", "r")
    print(allSales.read())
    print("=============================")
    input()
    allSales.close()
    maintransaction()
#end of sales revie

#orders review

def serveOrder():
    if len(orderPending) !=0:
        try:
            for i in range(len(orderPending)):
                print("["+ str(i) +"]"+" ==> " + orderPending[i])
            print("Input any button to cancel if you want to cancel")
            inp = int(input("Choose order to serve:"))

            if(inp >= 0 or inp < len(orderPending)):
                os.remove("pendingOrders/"+ orderPending[inp] +".txt")
                print("========================")
                print("Order "+orderPending[inp]+" served")
                print("========================")
                del orderPending[inp]
                if len(orderPending) !=0:
                    servedOrder = open("pendingOrders/ordersID.txt", "w")
                    for i in range(len(orderPending)):
                        servedOrder.write(orderPending[i] + "\n")
                    servedOrder.close()
                input()
            else:
                print("There are no orders...")
                maintransaction()
        except:
            maintransaction()
    else:
        maintransaction()

def reviewOrder():
    if len(orderPending) !=0:
        try:
            for i in range(len(orderPending)):
                print("["+ str(i) +"]"+" ==> " + orderPending[i])
            print("Input any button to cancel if you want to cancel")
            inp = int(input("Choose order to review:"))
            reviewedOrder = open("pendingOrders/"+ orderPending[inp] +".txt", "r")
            print(reviewedOrder.read())
            reviewedOrder.close()
            input()
            maintransaction()
        except:
                maintransaction()

    else:
        print("No Order to review...")
        input()
        maintransaction()

def OrdersControl():
    pendings()
    print("=============================")
    print("[1] ==> Serve Order")
    print("[2] ==> Review Order")
    print("[0] ==> Exit")
    try:
        choice = int(input("Input number to manage: "))
        if choice == 1:
            serveOrder()
        elif choice == 2:
            reviewOrder()
        elif choice == 0:
            maintransaction()
        else:
            print("Invalid Input")
            input()
            OrdersControl()
    except:
        print("Invalid Input")
        input()
        OrdersControl()
    print("=============================")
#orders end review

# Srart Transaction System
def maintransaction():
    global userType
    global user
    print("\n===========================")
    print("Hello " + user)
    print("=============================")
    
    pendingOrders()

    print("[1] ==> Take Order")
    print("[2] ==> Orders")
    if userType == "admin":
        print("[3] ==> Daily sales")
    print("[0] ==> Logout")
    choice =  int(input("Enter the number of your choice: "))
    
    try:
        if choice == 1:
            takeOrder()
        elif choice == 2:
            OrdersControl()
        elif choice == 0:
            logout()
        elif choice == 3 and userType =="admin":
            takeAllSales()
        else:
            invalid()
            maintransaction()
    except:
        invalid()
        maintransaction()
# End Transaction System

# Srart Login System
def accounts():
    global userType
    if userType == "admin":
        _users = open("accounts/admin_usernames.txt", "r")
        _passw = open("accounts/admin_passwords.txt", "r")
    elif userType == "cashier":
        _users = open("accounts/cashier_usernames.txt", "r")
        _passw = open("accounts/cashier_passwords.txt", "r")

    account = {}
    for username in _users.readlines(0):
        account[username.replace("\n", "")] = ""
        for passw in _passw.readlines(1):
            account[username.replace("\n", "")] = passw.replace("\n", "")
    _users.close()
    _passw.close()
    return account

def login():
    global userType
    global user
    print("\n===========================")
    account = accounts()
    userN = input("Enter Username: ")
    usernameExist = False
        
    for x in account:
        if userN == x:
            usernameExist = True
            
    if usernameExist != False:
        passwords = input("Enter passwrod: ")
        if passwords == account[userN]:
            user = userN
            maintransaction()
        else:
            print("Password Incorrect")
            take = 0
            val = validate()
            while take == 0:
                if val == 'Y' or val == 'y':
                    login()
                elif val == 'N' or val == 'n':
                    dashboard()
                else:
                    invalid()
                    login()
                       
    else:
        print("Username does\'nt Exist")
        val = validate()
        take = 0
        while take == 0:
            if val == 'Y' or val == 'y':
                login()
            elif val == 'N' or val == 'n':
                dashboard()
            else:
                invalid()
                login()

def dashboard():
    print("\n===========================")
    print("Welcome to Milk and Mortea\'s Point of Sale System")
    print("\n===========================")
    global userType
    print("1 ==> Admin")
    print("2 ==> Cashier")
    print("0 ==> Exit")
    choice = input("Enter the number of your choice: ")
    if choice == '1':
        userType = "admin"
        login()
    elif choice == '2':
        userType = "cashier"
        login()
    elif choice == '0':
        print("\n===========================")
        Echoice = input("Are you sure you want to exit? :( [Y/N]")
        if Echoice == 'N' or Echoice == 'n':
            dashboard()
        elif Echoice == 'Y' or Echoice == 'y':
            print("\n===========================")
            print("Thank you and goodbye!! Wubba Lubba dub-dub!!! :)")
            print("=============================")
            exit()
    else:
        print("Invalid Input")   
        
        
def main():
    dashboard()

main()

# End Login System
