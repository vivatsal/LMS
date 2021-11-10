from logging import exception;
from tkinter import *;
from tkinter import messagebox;
import mysql.connector;
from tkcalendar import Calendar
from data import options
import tkinter.font as font

root = Tk()

root.title("LMS")

root.iconbitmap("C:/Users/user/desktop/New folder/icon.ico")

root.resizable(0, 0)

def backto():
    frame.pack_forget()
    button1.place(x = "225", y="125", width="200", height="60")
    button2.place(x = "225", y="250", width="200", height="60")

def submit():

    if len(e_name.get())<2 or len(e_dob.get())<2 or len(e_phone.get())<2 or len(e_password.get())<5:
        messagebox.showwarning("Error", "Invalid Input")

    elif e_password.get() != e_confirm.get(): 
        messagebox.showwarning("Error","Passwords Don't Match.")

    else:
        try: 
            mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="college")
            c = mydb.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS DATA(NAME VARCHAR(255), DOB VARCHAR(255), PHONE INT, PASSWORD VARCHAR(255), REG INT AUTO_INCREMENT, PRIMARY KEY(REG))""")
            c.execute("""ALTER TABLE DATA AUTO_INCREMENT = 100""")
            sql = ("INSERT INTO DATA(NAME, DOB, PHONE, PASSWORD) VALUES(%s, %s, %s, %s)")
            val = (e_name.get(), e_dob.get(), e_phone.get(), e_password.get())
            c.execute(sql, val)
            print(c.rowcount, "record inserted.")
            c.execute("""SELECT * FROM DATA WHERE REG = (SELECT MAX(REG) FROM DATA)""")
            global conn
            conn = c.fetchone()
            for x in conn:
                print(x)
            mydb.commit()
            mydb.close()
            dest_butt.grid_forget()
            newlabel = Label(frame, text="Your Login Credentials are: ", anchor="center")
            newlabel.grid(row="6", column="1", columnspan="2")
            idlabel1 = Label(frame, text="ID: ")
            idlabel1.grid(row="7", column="1")
            idlabel2 = Label(frame, text=conn[4])
            idlabel2.grid(row="7", column="2")
            password1 = Label(frame, text="PASSWORD: ")
            password1.grid(row="8", column="1")
            password2 = Label(frame, text=conn[3])
            password2.grid(row="8", column="2")
            back_button = Button(frame, text="Back to Login", command=backto)
            back_button.grid(row="9", column="1", columnspan="2")

        except Exception:
            messagebox.showwarning("Error", "Invalid Input Format")   

def Successful_login(reg):

    logframe.place_forget()

    loginframe = Frame(root)
    loginframe.place(x="0", y="0", width="500", height="650")

    def issue():
        loginframe.place_forget()
        global issueframe
        issueframe = Frame(root)
        issueframe.place(x="0", y="0", width="500", height="650")
        registr = Label(issueframe, text="Registration Number : ")
        registr.place(x="110", y="45")
        clicked = StringVar()
        clicked.set(reg)
        click = StringVar()
        click.set("Choose a Book")
        e_registr = Button(issueframe, textvariable=clicked, state="disabled")
        e_registr.place(x="250", y="35", width="250", height="40")
        chooselabel = Label(issueframe, text="Name of the Book : ")
        chooselabel.place(x="120", y="135")
        dropdown = OptionMenu(issueframe, click, *options)
        dropdown.place(x="250", y="125", width="250", height="45")
        choosedate = Label(issueframe, text="Date of Issue : ")
        choosedate.place(x="150", y="225")

        def switch_date():
            submitdate.place_forget()
            getdate.config(text=cal.get_date())
            cal.place_forget()
            logsub.place(x="320", y="300", width="175", height="50")
            back_button_issue.place(x="120", y="300", width="175", height="50")

        def grab_date():
            logsub.place_forget()
            back_button_issue.place_forget()
            cal.place(x="250", y="265")
            global submitdate
            submitdate = Button(issueframe, text="Confirm", command=switch_date, width="12")
            submitdate['font']=myFont1
            submitdate.place(x="335", y="460")

        global cal
        cal = Calendar(issueframe, selectmode="day", day=1, month=9, year=2021)
        global getdate
        getdate = Button(issueframe, text="Choose date", width="34", height="2", command=grab_date)
        getdate.place(x="250", y="215")

        def issue_book(reg, date, book_name):
            mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="college")
            c = mydb.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS ISSUED_BOOKS ( REG INT, BOOK VARCHAR(255), DATE VARCHAR(255) )""")
            c.execute("""SELECT * FROM ISSUED_BOOKS WHERE REG = %s""", (reg,))
            value = c.fetchall()

            if len(value) < 3:
               c.execute("""INSERT INTO ISSUED_BOOKS(REG, BOOK, DATE) VALUES(%s, %s, %s)""", (reg, book_name, date))
               c.execute("""SELECT * FROM ISSUED_BOOKS WHERE REG = %s""", (reg,))
               conn = c.fetchall()
               print(conn)
               messagebox.showinfo("Success", "Book named  \"" + book_name +  "\"  Issued.")
               issueframe.place_forget()
               loginframe.place(x="0", y="0", width="500", height="650")  

            else:
                messagebox.showerror("Error", "Can't issue more than 3 book at a time.")
                issueframe.place_forget()
                loginframe.place(x="0", y="0", width="500", height="650")    
                

            mydb.commit()
            mydb.close()

        def backtohomeiss():
            issueframe.place_forget()
            loginframe.place(x="0", y="0", width="500", height="650")

        back_button_issue = Button(issueframe, text="Back", command=backtohomeiss)
        back_button_issue.place(x="120", y="300", width="175", height="50")
        back_button_issue['font']=myFont1

        global logsub
        logsub = Button(issueframe, text="Submit", command=lambda: issue_book(reg, cal.get_date(), click.get()))
        logsub.place(x="320", y="300", width="175", height="50")
        logsub['font']=myFont1

    
    def return_function(reg):

        logframe.place_forget()
        loginframe.place_forget()

        mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="college")
        c = mydb.cursor()
        c.execute("""SELECT * FROM ISSUED_BOOKS WHERE REG = %s""", (reg,))
        value = c.fetchall()
        book_list = ["Select a Book"]
        for i in value:
           book_list.append(i[1])
        print(book_list)   
        mydb.commit()
        mydb.close()

        returnframe = Frame(root)
        returnframe.place(x="0", y="0", width="500", height="650")

        registr_ret = Label(returnframe, text="Registration Number : ")
        registr_ret.place(x="110", y="40")
        clicked_ret = StringVar()
        clicked_ret.set(reg)
        click_ret = StringVar()
        click_ret.set("Select a Book")
        e_registr_ret = Button(returnframe, textvariable=clicked_ret, state="disabled")
        e_registr_ret.place(x="250", y="30", width="250", height="40")
        chooselabel_ret = Label(returnframe, text="Name of the Book : ")
        chooselabel_ret.place(x="120", y="130")
        dropdown_ret = OptionMenu(returnframe, click_ret, *book_list)
        dropdown_ret.place(x="250", y="120", width="250", height="45")
        
        choosedate_ret = Label(returnframe, text="Date of Return : ")
        choosedate_ret.place(x="120", y="240")

        def switch_date_ret():
            submitdate_ret.place_forget()
            getdate_ret.config(text=cal_ret.get_date())
            cal_ret.place_forget()
            retsub.place(x="320", y="300", width="175", height="50")
            back_button_return.place(x="120", y="300", width="175", height="50")

        def grab_date_ret():
            retsub.place_forget()
            back_button_return.place_forget()
            cal_ret.place(x="250", y="275")
            global submitdate_ret
            submitdate_ret = Button(returnframe, text="Confirm", command=switch_date_ret, width="12")
            submitdate_ret.place(x="335", y="465")

        def return_book(reg, date, book_name):
            mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="college")
            c = mydb.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS RETURNED_BOOKS ( REG INT, BOOK VARCHAR(255), DATE VARCHAR(255) )""")
            c.execute("""INSERT INTO RETURNED_BOOKS(REG, BOOK, DATE) VALUES(%s, %s, %s)""", (reg, book_name, date))
            c.execute("""DELETE FROM ISSUED_BOOKS WHERE REG = %s""", (reg,))
            messagebox.showinfo("Success", "Book named  \"" + book_name +  "\"  Returned.")
            c.execute("""SELECT * FROM ISSUED_BOOKS WHERE REG = %s AND BOOK = %s""", (reg, book_name,))
            books_iss = c.fetchall()
            print(books_iss)   
            mydb.commit()
            mydb.close()  
            returnframe.place_forget()
            loginframe.place(x="0", y="0", width="500", height="650")  


        global cal_ret
        cal_ret = Calendar(returnframe, selectmode="day", day=1, month=9, year=2021)
        global getdate_ret
        getdate_ret = Button(returnframe, text="Choose date", width="34", height="2", command=grab_date_ret)
        getdate_ret.place(x="250", y="230")

        global retsub
        retsub = Button(returnframe, text="Return", command=lambda: return_book(reg, cal_ret.get_date(), click_ret.get()))
        retsub.place(x="320", y="340", width="175", height="50")
        retsub['font']=myFont1

        def backtohomeret():
            returnframe.place_forget()
            loginframe.place(x="0", y="0", width="500", height="650")

        back_button_return = Button(returnframe, text="Back", command=backtohomeret)
        back_button_return.place(x="120", y="340", width="175", height="50")
        back_button_return['font']= myFont1

    def logout():

        loginframe.place_forget()
        logframe.place(x="0", y="0", height="650", width="550")

    def request_book(reg):

        loginframe.place_forget()
        requestframe = Frame(root)
        requestframe.place(x="0", y="0", width="500", height="650")

        registr_req = Label(requestframe, text="Registration Number : ")
        registr_req.place(x="110", y="40")
        clicked_req = StringVar()
        clicked_req.set(reg)
        click_req = StringVar()
        click_req.set("Select a Book")
        e_registr_req = Button(requestframe, textvariable=clicked_req, state="disabled")
        e_registr_req.place(x="250", y="30", width="250", height="40")
        chooselabel_req = Label(requestframe, text="Name of the Book : ")
        chooselabel_req.place(x="125", y="130")
        name_req = Entry(requestframe)
        name_req.place(x="250", y="120", width="250", height="45")
        
        choosedate_req = Label(requestframe, text="Date of Request : ")
        choosedate_req.place(x="145", y="240")

        def switch_date_req():
            submitdate_req.place_forget()
            getdate_req.config(text=cal_req.get_date())
            cal_req.place_forget()
            reqsub.place(x="320", y="340", width="175", height="50")
            back_button_request.place(x="120", y="340", width="175", height="50")

        def grab_date_req():
            reqsub.place_forget()
            back_button_request.place_forget()
            cal_req.place(x="250", y="275")
            global submitdate_req
            submitdate_req= Button(requestframe, text="Confirm", command=switch_date_req, width="12")
            submitdate_req.place(x="335", y="465")

        def request(reg, date, book_name):
            mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="college")
            c = mydb.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS REQUESTED_BOOKS ( REG INT, BOOK VARCHAR(255), DATE VARCHAR(255) )""")
            c.execute("""INSERT INTO REQUESTED_BOOKS(REG, BOOK, DATE) VALUES(%s, %s, %s)""", (reg, book_name, date))
            messagebox.showinfo("Success", "Request for Book named  \"" + book_name +  "\"  Registered.")
            c.execute("""SELECT * FROM REQUESTED_BOOKS WHERE REG = %s AND BOOK = %s""", (reg, book_name,))
            books_iss = c.fetchall()
            print(books_iss)   
            mydb.commit()
            mydb.close()  
            requestframe.place_forget()
            loginframe.place(x="0", y="0", width="500", height="650")

        global cal_req
        cal_req = Calendar(requestframe, selectmode="day", day=1, month=9, year=2021)
        global getdate_req
        getdate_req = Button(requestframe, text="Choose date", width="34", height="2", command=grab_date_req)
        getdate_req.place(x="250", y="230")

        global reqsub
        reqsub = Button(requestframe, text="Request", command=lambda: request(reg, cal_req.get_date(), name_req.get()))
        reqsub.place(x="320", y="340", width="175", height="50")
        reqsub['font']=myFont1

        def backtohomereq():
            requestframe.place_forget()
            loginframe.place(x="0", y="0", width="500", height="650")

        back_button_request = Button(requestframe, text="Back", command=backtohomereq)
        back_button_request.place(x="120", y="340", width="175", height="50")
        back_button_request['font']=myFont1

    

    global issue_button
    global return_button
    issue_button = Button(loginframe, text="Issue Books", command=issue)
    issue_button.place(x="205", y="60", width="250", height="45")
    issue_button['font']=myFont1
    return_button = Button(loginframe, text="Return Books", command=lambda: return_function(reg))
    return_button.place(x="205", y="160", width="250", height="45")
    return_button['font']=myFont1
    request_button = Button(loginframe, text="Request A Book", command=lambda: request_book(reg))
    request_button.place(x="205", y="260", width="250", height="45")
    request_button['font']=myFont1
    logout_button = Button(loginframe, text="Log out", command=logout)
    logout_button.place(x="205", y="370", width="250", height="45")
    logout_button['font']=myFont1


def log():

    try:
        mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="college")
        print("database connected")
        c = mydb.cursor()
        c.execute("SELECT * FROM DATA WHERE REG = %s AND PASSWORD = %s", (e_reg.get(), e_pass.get()))
        row = c.fetchone()
        print(row)
        if row == None:
            messagebox.showwarning("Error", "Incorrect User or Password")
        else:
            Successful_login(e_reg.get())
            e_reg.delete(0, END)
            e_pass.delete(0, END)

    except Exception:
        messagebox.showwarning("Error", "Invalid User")

def update(name, dob, phone, password, reg):
     
     try:
         mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="college")
         c = mydb.cursor()
         print(name, dob, phone, password, reg)
         c.execute("""UPDATE DATA SET NAME=%s, DOB=%s, PHONE=%s, PASSWORD=%s WHERE REG = %s""", 
                     (name, dob, phone, password, reg) )
         c.execute("SELECT * FROM DATA WHERE REG = %s AND DOB = %s", (reg, dob))
         conn = c.fetchall()
         print(conn)
         messagebox.showinfo("Sucess", "Details reset Sucessfull.")
         mydb.commit()
         mydb.close()
         resetframe.place_forget()
         button1.place(x = "225", y="125", width="200", height="60")
         button2.place(x = "225", y="250", width="200", height="60")
        
     except Exception:
         messagebox.showwarning("Error", Exception)

def reset(reg):

    global reset_e_name
    global reset_e_dob
    global reset_e_phone
    global reset_e_password

    global registration_number
    registration_number = IntVar()
    registration_number = reg
    
    mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="college")
    c = mydb.cursor()
    c.execute("SELECT * FROM DATA WHERE REG = %s AND DOB = %s", (e_for_reg.get(), e_for_dob.get()))
    result = c.fetchone()
    print(result)
    mydb.commit()
    mydb.close()

    if result:   
        forgetframe.place_forget()
        global resetframe
        resetframe = Frame(root)
        resetframe.place(x="0", y="0", width="500", height="650")

        global reset_e_name
        global reset_e_dob
        global reset_e_phone
        global reset_e_password

        reset_name = Label(resetframe, text="Your Name  : ")
        reset_name.place(x="130", y="50", width="200", height="60")
        reset_e_name = Entry(resetframe)
        reset_e_name.place(x="300", y="55", width="225", height="50")
        reset_dob = Label(resetframe, text="Your Date Of Birth  : ")
        reset_dob.place(x="110", y="130", width="200", height="60")
        reset_e_dob = Entry(resetframe)
        reset_e_dob.place(x="300", y="135", width="225", height="50")
        reset_Phone = Label(resetframe, text="Your Phone Number  : ")
        reset_Phone.place(x="105", y="210", width="200", height="60")
        reset_e_phone = Entry(resetframe)
        reset_e_phone.place(x="300", y="215", width="225", height="50")
        reset_password = Label(resetframe, text="Your Password  : ")
        reset_password.place(x="120", y="295", width="200", height="60")
        reset_e_password = Entry(resetframe)
        reset_e_password.place(x="300", y="300", width="225", height="50")
        up_butt = Button(resetframe, text="Update", command=lambda: update(reset_e_name.get(), reset_e_dob.get(), 
                                               reset_e_phone.get(), reset_e_password.get(), registration_number))
        up_butt.place(x="325", y="390", width="150", height="60")

        def backfromupdate():
            resetframe.place_forget()
            forgetframe.place(x="0", y="0", width="500", height="650")

        back_button_update = Button(resetframe, text="Back", command=backfromupdate)
        back_button_update.place(x="155", y="390", width="150", height="60")

    if result == NONE:
        messagebox.showerror("Error", "Invalid User")

    reset_e_name.insert(0, result[0])
    reset_e_dob.insert(0, result[1])
    reset_e_phone.insert(0, result[2])
    reset_e_password.insert(0, result[3])

    e_for_reg.delete(0, END)
    e_for_dob.delete(0, END)


def forgot():
    logframe.place_forget()
    global forgetframe
    forgetframe = Frame(root)
    forgetframe.place(x="0", y="0", width="500", height="650")
    global e_for_reg
    global e_for_dob
    for_reg = Label(forgetframe, text="Enter your registration number: ")
    for_reg.place(x="110", y="80", width="200", height="60")
    e_for_reg = Entry(forgetframe)
    e_for_reg.place(x="310", y="80", width="225", height="60")
    for_dob = Label(forgetframe, text="Enter your Date of Birth: ")
    for_dob.place(x="130", y="210", width="200", height="60")
    e_for_dob = Entry(forgetframe)
    e_for_dob.place(x="310", y="210", width="225", height="60")
    forget_button = Button(forgetframe, text="Reset Password", command=lambda: reset(e_for_reg.get()))
    forget_button.place(x="330", y="335", width="165", height="60")

    def backfromreset():
        forgetframe.place_forget()
        logframe.place(x="0", y="0", height="650", width="550")

    back_button_reset = Button(forgetframe, text="Back", command=backfromreset)
    back_button_reset.place(x="140", y="335", width="165", height="60")


def login():
    button1.place_forget()
    button2.place_forget()
    global logframe
    logframe = Frame(root)
    logframe.place(x="0", y="0", height="650", width="550")
    global e_reg 
    global e_pass
    reg = Label(logframe, text="Enter your registration number: ")
    reg.place(x="90", y="50", width="200", height="60")
    e_reg = Entry(logframe)
    e_reg.place(x="290", y="55", width="225", height="50")
    passw = Label(logframe, text="Enter your Password: ")
    passw.place(x="120", y="140", width="200", height="70")
    e_pass = Entry(logframe)
    e_pass.place(x="290", y="145", width="225", height="50")
    for_button = Button(logframe, text="Forgot Password", command=forgot)
    for_button.place(x="120", y="250", width="175", height="70")
    dest_button = Button(logframe, text="Submit", command=log)
    dest_button.place(x="330", y="250", width="175", height="70")

    def backtofront():
        logframe.place_forget()
        button1.place(x="225", y="125", width="200", height="60")
        button2.place(x="225", y="250", width="200", height="60")

    back_button = Button(logframe, text="Back", command=backtofront)
    back_button.place(x="220", y="365", width="175", height="60")
    
def signup():
    button1.place_forget()
    button2.place_forget()
    global frame
    frame = Frame(root)
    frame.place(x="0", y="0", width="500", height="650")
    global e_name
    global e_dob
    global e_phone 
    global e_password
    global e_confirm
    global dest_butt
    name = Label(frame, text="Enter Your Name  : ")
    name.place(x="135", y="35", width="200", height="50")
    e_name = Entry(frame)
    e_name.place(x="320", y="35", width="225", height="50")
    dob = Label(frame, text="Enter Your Date Of Birth  : ")
    dob.place(x="115", y="105", width="200", height="50")
    e_dob = Entry(frame)
    e_dob.place(x="320", y="105", width="225", height="50")
    Phone = Label(frame, text="Enter Your Phone Number  : ")
    Phone.place(x="110", y="175", width="200", height="50")
    e_phone = Entry(frame)
    e_phone.place(x="320", y="175", width="225", height="50")
    password = Label(frame, text="Enter Your Password  : ")
    password.place(x="125", y="245", width="200", height="50")
    e_password = Entry(frame)
    e_password.place(x="320", y="245", width="225", height="50")
    confirm = Label(frame, text="Confirm Password  : ")
    confirm.place(x="130", y="320", width="200", height="50")
    e_confirm = Entry(frame)
    e_confirm.place(x="320", y="320", width="225", height="50")
    dest_butt = Button(frame, text="Submit", command=submit)
    dest_butt['font']=myFont1
    dest_butt.place(x="320", y="402", width="165", height="55")

    def backfromsign():
        frame.place_forget()
        button1.place(x="225", y="125", width="200", height="60")
        button2.place(x="225", y="250", width="200", height="60")

    back_button_sign = Button(frame, text="Back", command=backfromsign)
    back_button_sign.place(x="130", y="402", width="165", height="55")
    back_button_sign['font']=myFont1
    
global button1
global button2
myFont = font.Font(family='Helvetica', size=20, weight='bold')
#mylabel=Label(root,text='LIBRARY MANAGEMENT SYSTEM')
#mylabel['font']= myFont
#mylabel.place(x='90',y='40')
myFont1 = font.Font(family='Helvetica', size=10, weight='bold')
button1 = Button(root, text="LOG IN", padx=53, pady=10, command=login,bg="#e09e50")
button1['font']=myFont
button2 = Button(root, text="SIGN UP", padx=50, pady=10,  command=signup,bg="#e09e50")
button2['font']=myFont
button1.place(x = "225", y="150", width="200", height="60")
button2.place(x = "225", y="250", width="200", height="60")

root.geometry('650x500')
root.mainloop()