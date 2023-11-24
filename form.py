import tkinter #creates entry form
from tkinter import ttk #creates drop down menu
import pickle #transfers model
import pandas as pd #handles data
import tensorflow as tf 
import numpy as np #changes dimensionality of array
from tensorflow.keras.models import Model

window = tkinter.Tk()#create window for entry form
window.title("Data Entry Form")
frame = tkinter.Frame(window) #create frame to present text
frame.pack() #organize text

def enter_data():
    vdss = float(voltage_entry.get()) #access variable from form, and convert to float
    print(vdss) #print to ensure variable is the correct dtype
    idss = float(drain_current_entry.get())
    print(idss)
    rds = float(on_res_entry.get())
    print(rds)
    vgs = float(gate_s_entry.get())
    print(vgs)
    ion = ion_combobox.get()
    print(ion)
    fail = fail_mode_combobox.get()
    print(fail)
    ciss = float(ciss_entry.get())
    print(ciss)
    coss = float(coss_entry.get())
    print(coss)
    crss = float(crss_entry.get())
    print(crss)
    

    #categorical data becomes numerical
    if fail == "SEGR":
        fail = 1 
    elif fail == "SEB":
        fail = 0
    elif fail == "SEL":
        fail = 2
    else:
        fail = 3
    if ion == "Ag":
        ion = 0
    elif ion =="Ar":
        ion = 1
    elif ion == "Kr":
        ion = 2
    else:
        ion = 3
    
    print(fail)#print to ensure variable is correct dtype
    print(ion)
    
    data = [vdss, ciss, coss, crss, ion, fail, idss, vgs, rds]#make array of input features
    data = np.array(data).reshape(1, -1)#convert array to 2D
    
    print(data)
    loaded_model = pickle.load(open('finalized_model.sav', 'rb'))#load model using pickle
    y_data = loaded_model.predict(data)
    print("Prediction: ", y_data)#print prediction
    

basic_info_frame = tkinter.LabelFrame(frame, text="MOSFET BASIC INFORMATION") #allocate section of frame to contain essential MOSFET characteristics
basic_info_frame.grid(row=0, column=0, padx=20, pady=20) #section is in the first row
rad_info_frame = tkinter.LabelFrame(frame, text="RAD TEST INFORMATION") #allocate section of frame to radiation testing information
rad_info_frame.grid(row=1, column=0, sticky="news", padx=20, pady=20)#section is in the second row; sticky='news' enables the section to cover the full frame
gate_cap_frame = tkinter.LabelFrame(frame, text='GATE CAPACITANCE')#allocate section of frame to information on gate capacitance
gate_cap_frame.grid(row=2, column=0, sticky="news", padx=20, pady=20)#section is in the third row

voltage_label = tkinter.Label(basic_info_frame, text="VDSS")#create label for maximum voltage(vdss) data point
voltage_label.grid(row=0, column=0) #organize label
drain_current_label = tkinter.Label(basic_info_frame, text="IDSS")#create label for drain leakage current(idss)
drain_current_label.grid(row=0, column=1)
on_res_label = tkinter.Label(basic_info_frame, text="RDS(ON)")#label for on resistance (RDS(On))
on_res_label.grid(row=0, column=2)
gate_s_label = tkinter.Label(basic_info_frame, text="VGS")#label for gate-source voltage(vgs)
gate_s_label.grid(row=0, column=3)

voltage_entry=tkinter.Entry(basic_info_frame)#create entry box for user response
drain_current_entry = tkinter.Entry(basic_info_frame)
on_res_entry = tkinter.Entry(basic_info_frame)
gate_s_entry=tkinter.Entry(basic_info_frame)

voltage_entry.grid(row=1,column=0)
drain_current_entry.grid(row=1, column=1)
on_res_entry.grid(row=1, column=2)
gate_s_entry.grid(row=1, column=3)

ion_label = tkinter.Label(rad_info_frame, text="ION TYPE")#label for type of ion used in hypothetical rad testing
ion_combobox = ttk.Combobox(rad_info_frame, values=["Ar", "Kr", "Ag", "Ta"])#comboboxes allow for drop-down menus
ion_label.grid(row=1, column=0)
ion_combobox.grid(row=2, column=0)

fail_mode_label = tkinter.Label(rad_info_frame, text="FAILURE MODE")#failure mode in assessment
fail_mode_combobox = ttk.Combobox(rad_info_frame, values=["SEGR", 'SET', 'SEL', 'SEB'])
fail_mode_label.grid(row=1, column=1)
fail_mode_combobox.grid(row=2, column=1)

ciss_label = tkinter.Label(gate_cap_frame, text='CISS')#input capacitance
ciss_label.grid(row=2, column=0)
coss_label = tkinter.Label(gate_cap_frame, text="COSS")#output capacitance
coss_label.grid(row=2, column=1)
crss_label = tkinter.Label(gate_cap_frame, text="CRSS")#reverse current
crss_label.grid(row=2, column=2)

ciss_entry = tkinter.Entry(gate_cap_frame)
ciss_entry.grid(row=3, column=0)
coss_entry = tkinter.Entry(gate_cap_frame)
coss_entry.grid(row=3, column=1)
crss_entry = tkinter.Entry(gate_cap_frame)
crss_entry.grid(row=3, column=2)


for widget in basic_info_frame.winfo_children():#organize labels, entry boxes, and comboboxes in an aesthetically pleasing way
    widget.grid_configure(padx=10, pady=5)
for widget in rad_info_frame.winfo_children():
    widget.grid_configure(padx=60, pady=10)
for widget in gate_cap_frame.winfo_children():
    widget.grid_configure(padx=30, pady=10)
    
button = tkinter.Button(frame, text="ENTER DATA", command=enter_data)#button to submit data; function enter_data() is used to feed input features into model
button.grid(row=3, columns=1, sticky="News", padx=20, pady=10)

window.mainloop()#program will run unless window is closed

