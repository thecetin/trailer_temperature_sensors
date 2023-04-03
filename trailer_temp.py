import gi
import datetime
import time
import threading
import sys
import subprocess as sp
import os.path
from filelock import FileLock, Timeout
import os

gi.require_version('Gtk','3.0')

from gi.repository import Gtk as gtk, GObject
from gi.repository import GLib

class Main(gtk.Window):

    def __init__(self):

        #To run same time trailer_temp_create.py file
        self.extProc = sp.Popen(['python','trailer_temp_create.py']) # runs trailer_temp_create.py 

        #Read Chauffeur, Truck and Gateway IDs from gateway.txt file
        
        self.data_id =[]
        try:
            with open("gateway.txt", 'r') as data_id:
                for tline in data_id:
                    self.data_id.append(tline.split())
            data_id.close()
        
        except IOError:
            print("When rading file, File is already locked by another process")
            

        
        self.chauffeur_id ="" #"C120"
        self.truck_id = "" #"TI120"
        self.gateaway_id = "" #"GW1200"
    
        gladeFile = "trailer_container_temp.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(gladeFile)
        self.builder.connect_signals(self)
        
        self.login_window = self.builder.get_object("login_window")
        self.login_window.connect("delete-event",gtk.main_quit)
        
        self.main_window = self.builder.get_object("main_window") 
        self.main_window.connect("delete-event",gtk.main_quit)
        
        self.login_window.show()
        
    #This function is for check id           
    def check_id(self,widget):

        #Login screen all Entry ID names
        self.entry_chauffeur = self.builder.get_object("chauffeur_id")
        self.entry_truck = self.builder.get_object("truck_id")
        self.entry_getaway = self.builder.get_object("gateaway_id")
        self.error_label = self.builder.get_object("error_label")
            
        self.text_chauffeur = self.entry_chauffeur.get_text().strip()
        self.text_truck = self.entry_truck.get_text().strip()
        self.text_getaway = self.entry_getaway.get_text().strip()
        
        #Read gateway.txt file and put it every line in a list
        door = False
        for i in range(0,len(self.data_id)):
            self.chauffeur_id = self.data_id[i][0]
            self.truck_id = self.data_id[i][1]
            self.gateaway_id = self.data_id[i][2]

            #Check if login screen entries in a gateway.txt file, make door variable True
            if (str(self.text_chauffeur) == str(self.chauffeur_id) and str(self.text_truck) == str(self.truck_id) and str(self.text_getaway) == str(self.gateaway_id)):
                door = True
                break
            else:
                door = False
        
        #Check if door variable true, then show trailer screen
        if(door):   
            self.login_window.hide()
            self.main_window.show()
            #self.update_time()
            self.update_temperatures()

            self.entry_chauffeur.set_text("")
            self.entry_truck.set_text("")
            self.entry_getaway.set_text("")
            self.error_label.set_text("")
            
            # ---------------MAIN WINDOW--------------
            #To run same time trailer_temp_create.py file
            #self.extProc = sp.Popen(['python','trailer_temp_create.py']) # runs trailer_temp_create.py

            #Show Chauffeur, Truck and Gateway IDs on main window
            cf_label = self.builder.get_object("label_chauffeur")
            truck_label = self.builder.get_object("label_truck")
            gateway_label = self.builder.get_object("label_gateway")
            
            cf_label.set_text(self.chauffeur_id)
            truck_label.set_text(self.truck_id)
            gateway_label.set_text(self.gateaway_id)
               
        else:
            self.error_label.set_text("Wrong Input!")
            print("wrong input")
    
    #Function of Update date-time every 1 second, this function is thread!
    def update_time(self):
        #self.uptime = threading.Timer(1.0, self.update_time)
        #self.uptime.start()

        x = datetime.datetime.now()
        self.time_label = self.builder.get_object("time_label")
        self.date_label = self.builder.get_object("label_date")
        self.date_ = x.strftime("%m/%d/%Y")
        self.time_ = x.strftime("%H:%M:%S")
        self.date_label.set_text(str(self.date_))
        self.time_label.set_text(str(self.time_))
        return True

    def startclocktimer(self):
		#  this takes 2 args: (how often to update in millisec, the method to run)
        GLib.timeout_add_seconds(1, self.update_time)
        #GObject.timeout_add(1000, self.update_time)
                
    
    #Update all temperature values every 6 seconds, this function is thread!
    def update_temperatures(self):
        #self.uptemp = threading.Timer(5.0, self.update_temperatures) #----Every 6 seconds temperatures will updated-----
        #self.uptemp.start()
        
     
        #Read temperatures and and their ID's from temperature.txt file
        path_to_file = 'temperature.txt'          
        self.temp_data =[]
        
        try:
            file = open(path_to_file,mode='r')
            
            for tline in file:
                self.temp_data.append(tline.split())
    
        except Exception as prblm:
            print(prblm," something happend when reading file, ")   
        finally:
            file.close()

            # Temperature screen labels
        self.t_label_1 = self.builder.get_object("t_label_01")
        self.loc_label_1 = self.builder.get_object("loc_label_01")
        self.id_label_1 = self.builder.get_object("id_label_01")

        self.t_label_2 = self.builder.get_object("t_label_02")
        self.loc_label_2 = self.builder.get_object("loc_label_02")
        self.id_label_2 = self.builder.get_object("id_label_02")

        self.t_label_3 = self.builder.get_object("t_label_03")
        self.loc_label_3 = self.builder.get_object("loc_label_03")
        self.id_label_3 = self.builder.get_object("id_label_03")

        self.t_label_4 = self.builder.get_object("t_label_04")
        self.id_label_4 = self.builder.get_object("id_label_04")

        self.t_label_5 = self.builder.get_object("t_label_05")
        self.id_label_5 = self.builder.get_object("id_label_05")

        self.t_label_6 = self.builder.get_object("t_label_06")
        self.id_label_6 = self.builder.get_object("id_label_06")

        self.t_label_7 = self.builder.get_object("t_label_07")
        self.id_label_7 = self.builder.get_object("id_label_07")

        self.t_label_8 = self.builder.get_object("t_label_08")
        self.id_label_8 = self.builder.get_object("id_label_08")

        self.t_label_9 = self.builder.get_object("t_label_09")
        self.id_label_9 = self.builder.get_object("id_label_09")

        self.t_label_10 = self.builder.get_object("t_label_10")
        self.id_label_10 = self.builder.get_object("id_label_10")

        self.t_label_11 = self.builder.get_object("t_label_11")
        self.id_label_11 = self.builder.get_object("id_label_11")

        self.t_label_12 = self.builder.get_object("t_label_12")
        self.id_label_12 = self.builder.get_object("id_label_12")

        self.t_label_13 = self.builder.get_object("t_label_13")
        self.id_label_13 = self.builder.get_object("id_label_13")

        self.t_label_14 = self.builder.get_object("t_label_14")
        self.id_label_14 = self.builder.get_object("id_label_14")

        self.t_label_15 = self.builder.get_object("t_label_15")
        self.id_label_15 = self.builder.get_object("id_label_15")

        self.t_label_16 = self.builder.get_object("t_label_16")
        self.id_label_16 = self.builder.get_object("id_label_16")

        self.t_label_17 = self.builder.get_object("t_label_17")
        self.id_label_17 = self.builder.get_object("id_label_17")

        self.t_label_18 = self.builder.get_object("t_label_18")
        self.id_label_18 = self.builder.get_object("id_label_18")

        self.t_label_19 = self.builder.get_object("t_label_19")
        self.id_label_19 = self.builder.get_object("id_label_19")

        self.t_label_20 = self.builder.get_object("t_label_20")
        self.id_label_20 = self.builder.get_object("id_label_20")

        self.t_label_21 = self.builder.get_object("t_label_21")
        self.id_label_21 = self.builder.get_object("id_label_21")

        self.t_label_22 = self.builder.get_object("t_label_22")
        self.id_label_22 = self.builder.get_object("id_label_22")
            
        #Show temperatures 
        try:
            for i in range(0,22):
                tmpt =str(self.temp_data[i][1] + " " + self.temp_data[i][2])
                ex1 = (f'self.t_label_{i+1}.set_text("{tmpt}")')
                ex2 = (f'self.id_label_{i+1}.set_text(self.temp_data[{i}][0])')
                exec (ex1)
                exec (ex2)
                
        except:
            print(self.time_ + " temperature list could not read!")
            print(self.temp_data) 
        return True
    
    def starttempupdatetimer(self):
		#  this takes 2 args: (how often to update in millisec, the method to run)
        GLib.timeout_add_seconds(5, self.update_temperatures)        

    #Disconnect button - close all window and kill the threads
    def disconnect_app(self,widget):
        sp.Popen.terminate(self.extProc) # closes the process trailer_temp_create.py
        #self.uptime.cancel()
        #self.uptemp.cancel()
        

        self.login_window.show()
        self.main_window.hide()
    
    #Exit from app on login menu    
    def exit_app(self,widget):
        sp.Popen.terminate(self.extProc) # closes the process trailer_temp_create.py
        self.login_window.close()
        self.main_window.close()
    
       
if __name__ == '__main__':
    main = Main()
    main.startclocktimer()
    main.starttempupdatetimer()
    gtk.main()
