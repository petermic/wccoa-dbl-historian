import mysql.connector
import plotly.graph_objects as go
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo
from datetime import datetime
from datetime import timedelta

window = tk.Tk()

user='mvtx'
host='db1.sphenix.bnl.gov'
port='3306'
database='mvtx'
password = tk.StringVar()

# Main window

window.columnconfigure([0,1],weight=1,minsize=200)
window.rowconfigure([0,1,2,3],weight=1,minsize=10)

table_label = ttk.Label(text="Table: ")
DPE_label = ttk.Label(text="DPE: ")
timerange_label = ttk.Label(text="Time range: ")

table_selected = tk.StringVar()
DPE_selected = tk.StringVar()
timerange_selected = tk.StringVar()

table_dropdown = ttk.Combobox(textvariable=table_selected,width=50)
DPE_dropdown = ttk.Combobox(textvariable=DPE_selected,width=50)
timerange_dropdown = ttk.Combobox(textvariable=timerange_selected,width=50)

plot_button = ttk.Button(text="Plot",state=tk.DISABLED)

table_label.grid(row=0,column=0,padx=10,pady=10)
table_dropdown.grid(row=0,column=1,padx=10,pady=10)
DPE_label.grid(row=1,column=0,padx=10,pady=10)
DPE_dropdown.grid(row=1,column=1,padx=10,pady=10)
timerange_label.grid(row=2,column=0,padx=10,pady=10)
timerange_dropdown.grid(row=2,column=1,padx=10,pady=10)
plot_button.grid(row=3,column=0,padx=10,pady=10)

def query(querystring):
    try:
        cnx = mysql.connector.connect(user=user,host=host,port=port,database=database,password=password.get())
        crsr = cnx.cursor()
    except mysql.connector.Error as err:
        showinfo("MySQL Error",message=err)
        return [[],False]
    except e:
        print(e)
        return [[],False]
    try:
        crsr.execute(querystring)
    except mysql.connector.Error as err:
        showinfo("MySQL Error",message=err)
        return [[],False]
    except e:
        return [[],False]
    return [crsr.fetchall(),True]

def fill_table_dropdown():
    [res, success] = query("SHOW TABLES")
    if not success:
        window.destroy()
    tables = ()
    for r in res:
        tables += (r,)
    table_dropdown['values'] = tables

# Password window
def ask_password():
    password_window = tk.Toplevel(window)

    def hit_ok():
        password_window.destroy()
        fill_table_dropdown()

    password_label = ttk.Label(master=password_window,text="Please enter the password for:")
    password_label2 = ttk.Label(master=password_window,text="user "+user+", host "+host+", port "+port+", database "+database)
    password_entry = ttk.Entry(master=password_window,textvariable=password,show='*')
    password_button = ttk.Button(master=password_window,text="Ok",command=hit_ok)

    password_label.pack()
    password_label2.pack()
    password_entry.pack()
    password_button.pack()

    password_window.wm_transient(window)

def fill_DPE_dropdown(*args):
    [res, success] = query("SELECT DISTINCT DPE FROM "+table_selected.get())
    if not success:
        window.destroy()
    DPEs = ()
    for r in res:
        DPEs += (r,)
    DPE_dropdown['values'] = DPEs

def fill_timerange_dropdown(*args):
    timerange_dropdown['values'] = ('10 minutes','1 hour','1 day','3 days','1 week','1 month','all')

def enable_plot(*args):
    plot_button['state']=tk.NORMAL

def get_time_string():
    ts = timerange_selected.get()
    now = datetime.now()
    before = ""
    if ts == '10 minutes':
        before = now - timedelta(minutes=10)
    elif ts == '1 hour':
        before = now - timedelta(hours=1)
    elif ts == '1 day':
        before = now - timedelta(days=1)
    elif ts == '3 days':
        before = now - timedelta(days=3)
    elif ts == '1 week':
        before = now - timedelta(days=7)
    elif ts == '1 month':
        before = now - timedelta(months=1)
    elif ts == 'all':
        return '0000-00-00 00:00:00'
    return before.strftime("%Y-%m-%d %H:%M:%S")

def gen_plot():
    [res, success] = query("SELECT * FROM "+table_selected.get()+" WHERE DPE='"+DPE_selected.get()+"' AND STRCMP(Zeit,'"+get_time_string()+"')=1")
    if not success:
        window.destroy()
        sys.exit()
    fig = go.Figure()
    fig.add_trace(go.Scatter(name=DPE_selected.get(),x=[s[1] for s in res], y=[s[2] for s in res],mode='lines'))
    fig.show()
    window.destroy()

table_dropdown.bind('<<ComboboxSelected>>',fill_DPE_dropdown)
DPE_dropdown.bind('<<ComboboxSelected>>',fill_timerange_dropdown)
timerange_dropdown.bind('<<ComboboxSelected>>',enable_plot)

plot_button['command']=gen_plot

window.after_idle(ask_password)

window.mainloop()
