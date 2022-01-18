import tkinter as tk
from tkinter import ttk
from time import strftime
from time import sleep
import json
#import RPi.GPIO as GPIO


class Controller(tk.Tk):                                                          
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
 
        self.wm_title("Pillendreher")
        self.wm_geometry('800x480') #self.wm_attributes('-fullscreen', True)

        container = tk.Frame(self, height=480, width=800, bg='black')
        container.place(x=0, y=0)

        self.start = Main_window(container, self)
        self.settings_c0 = Settings_window(container, self, container_0)
        self.settings_c1 = Settings_window(container, self, container_1)
        self.settings_c2 = Settings_window(container, self, container_2)
        self.settings_c3 = Settings_window(container, self, container_3)
          
        self.create_frames()
        self.show_frame(0)

    def create_frames(self):
        self.frames = {}
        
        frame_names = [self.start, self.settings_c0, self.settings_c1, self.settings_c2, self.settings_c3]

        for i in range (0, 5):
            frame_names[i].configure(bg='black')
            frame_names[i].place(x=10, y=10, height=460, width=780)
            self.frames[i] = frame_names[i]
        #print(self.frames)
       
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Main_window(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        open_setup_button = tk.Button(self, text="E", bg='black', fg='white', command=lambda: self.controller.show_frame(1))
        open_setup_button.place(x=0, y=0)
      
        self.sub_frame_2()
        self.sub_frame_1()
        
    def sub_frame_1(self):
        self.frame_1 = tk.Frame(self)
        self.frame_1.place(x=115, y=140, height=180, width=550)

        self.lbl = tk.Label(self.frame_1, font = ('calibri', 150), background = 'black', foreground = 'white')
        self.lbl.place(x=0, y=0, height=180, width=550)
        self.clock()

    def sub_frame_2(self):
        self.frame_2 = tk.Frame(self)
        self.frame_2.place(x=115, y=140, height=180, width=550)

        self.dispense_button = tk.Button(self.frame_2, text="AUSGABE", font=("Helvetica", 60), background = 'red', foreground = 'white',  command=lambda:[self.frame_1.tkraise()]) #hardware_control.dispense(self.dispense.list),
        self.dispense_button.place(x=0, y=0, height=180, width=550)

    def clock(self):
        self.check_dispense()

        string = strftime('%H:%M')
        self.lbl.config(text = string)
        self.lbl.after(1000, self.clock)

    def check_dispense(self):
        self.all_days = [container_0.days, container_1.days, container_2.days, container_3.days]
        self.all_times = [container_0.times, container_1.times, container_2.times, container_3.times]
        self.all_times_status = [container_0.times_status, container_1.times_status, container_2.times_status, container_3.times_status]
        self.all_amounts = [container_0.amount, container_1.amount, container_2.amount, container_3.amount]
        self.dispense_list = [0,0,0,0]
        
        currenttime = strftime('%H:%M:%S')
        week = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        currentday_no=week.index(strftime('%a'))

        #print('(',self.number,')', self.days, self.times)

        for j in range(0, 4):
            if self.all_days[j][currentday_no] == True:
                for i in range(0, 4):
                    if self.all_times[j][i] == currenttime and self.all_times_status[j][i] == True:
                        self.dispense_list[j] = self.all_amounts[j][i]
                        self.frame_2.tkraise()
                        print("Tablette ausgeworfen")
                    else:
                        pass
                    
                                 
class Settings_window(tk.Frame):
    def __init__(self, parent, controller, container_name):
        tk.Frame.__init__(self, parent)

        self.controller = controller 

        self.container_name = container_name
        self.storage_filename = 'settings_container_' + str(container_name.number)

        self.load_settings()
                      
        self.widgets()  

        self.update_days_button_color()
        self.time_selection(0)

    def widgets(self):
        # Buttons Navigation
        b1_button = tk.Button(self, text="Box 1", font=("Helvetica", 15), command=lambda:self.controller.show_frame(1))
        b1_button.place(x=5, y=5, height=50, width=185)
        
        b2_button = tk.Button(self, text="Box 2", font = ("Helvetica", 15), command=lambda: self.controller.show_frame(2))
        b2_button.place(x=200, y=5, height=50, width=185)

        b3_button = tk.Button(self, text="Box 3", font = ("Helvetica", 15), command=lambda: self.controller.show_frame(3))
        b3_button.place(x=395, y=5, height=50, width=185)
        
        b4_button = tk.Button(self, text="Box 4", font = ("Helvetica", 15), command=lambda: self.controller.show_frame(4))
        b4_button.place(x=590, y=5, height=50, width=185)
        
        self.activate_button = tk.Button(self, text="Aktivieren", font = ("Helvetica", 15), command=lambda: self.time_activate( hour_sb.get(), min_sb.get()))
        self.activate_button.place(x=5, y=410, height=50, width=385)

        exit_button = tk.Button(self, text="Verlassen", font = ("Helvetica", 15), command=lambda: [self.controller.show_frame(0), self.safe_settings()])
        exit_button.place(x=400, y=410, height=50, width=385)

        buttons = [b1_button, b2_button, b3_button, b4_button]

        buttons[self.container_name.number].config(font=("Helvetica", 22, "bold"))

        #Time Picker
        self.hour_string=tk.StringVar(self)
        
        hour_label = tk.Label(self, text='Stunden', font = ("Helvetica", 20))
        hour_label.place(x=5, y=85, height=40, width=300)
        hour_sb = tk.Spinbox(self, from_=00, format="%02.0f", to=23,wrap=True,textvariable=self.hour_string, state="readonly", font=('Helvetica', 100), justify=tk.CENTER)
        hour_sb.place(x=5, y=125, height=190, width=300)

        self.minutes_string=tk.StringVar(self)

        min_label = tk.Label(self, text='Minuten', font = ("Helvetica", 20))
        min_label.place(x=315, y=85, height=40, width=300)
        min_sb = tk.Spinbox(self, from_=00, format="%02.0f", to=59,wrap=True, textvariable=self.minutes_string, font=('Helvetica', 100), width=2, justify=tk.CENTER)
        min_sb.place(x=315, y=125, height=190, width=300)

        self.time_1_button = tk.Button(self, text='Zeitpunkt 1', bg='white', font = ("Helvetica", 15), command=lambda: self.time_selection(0))
        self.time_1_button.place(x=630,y=85, height=50, width=145)
        
        self.time_2_button = tk.Button(self, text='Zeitpunkt 2', bg='white', font = ("Helvetica", 15), command=lambda: self.time_selection(1))
        self.time_2_button.place(x=630,y=145, height=50, width=145)
        
        self.time_3_button = tk.Button(self, text='Zeitpunkt 3', bg='white', font = ("Helvetica", 15), command=lambda: self.time_selection(2))
        self.time_3_button.place(x=630,y=205, height=50, width=145)
        
        self.time_4_button = tk.Button(self, text='Zeitpunkt 4', bg='white', font = ("Helvetica", 15), command=lambda: self.time_selection(3))
        self.time_4_button.place(x=630,y=265, height=50, width=145)

        #Day Picker
        self.montag_button = tk.Button(self, text='Mo', font = ("Helvetica", 15), command=lambda: [self.container_name.set_dispense_days(0), self.update_days_button_color()])
        self.montag_button.place(x=5,y=330, height=60, width=105)
        
        self.dienstag_button = tk.Button(self, text='Di', font = ("Helvetica", 15), command=lambda:[self.container_name.set_dispense_days(1), self.update_days_button_color()])
        self.dienstag_button.place(x=120,y=330, height=60, width=100)
        
        self.mittwoch_button = tk.Button(self, text='Mi', font = ("Helvetica", 15), command=lambda:[self.container_name.set_dispense_days(2),self.update_days_button_color()])
        self.mittwoch_button.place(x=230,y=330, height=60, width=100)
        
        self.donnerstag_button = tk.Button(self, text='Do', font = ("Helvetica", 15), command=lambda:[self.container_name.set_dispense_days(3),self.update_days_button_color()])
        self.donnerstag_button.place(x=340,y=330, height=60, width=100)
        
        self.freitag_button = tk.Button(self, text='Fr', font = ("Helvetica", 15), command=lambda:[self.container_name.set_dispense_days(4),self.update_days_button_color()])
        self.freitag_button.place(x=450,y=330, height=60, width=100)
        
        self.samstag_button = tk.Button(self, text='Sa', font = ("Helvetica", 15), command=lambda:[self.container_name.set_dispense_days(5),self.update_days_button_color()])
        self.samstag_button.place(x=560,y=330, height=60, width=100)
        
        self.sonntag_button = tk.Button(self, text='So', font = ("Helvetica", 15), command=lambda:[self.container_name.set_dispense_days(6),self.update_days_button_color()])
        self.sonntag_button.place(x=670,y=330, height=60, width=105)

    def time_activate(self, hours, minutes):
        timestamp = hours+':'+minutes+':00'
            
        if self.container_name.times_status[self.selected_time] == False:
            self.container_name.set_dispense_times(self.selected_time, timestamp, True)
             
            self.activate_button.config(text='Deaktivieren')
            self.times_buttons[self.selected_time].config(bg='#00ff00', activebackground='green')
                    
        else:
            self.container_name.set_dispense_times(self.selected_time, timestamp, False)
            self.activate_button.config(text='Aktivieren')
            self.times_buttons[self.selected_time].config(bg='white', activebackground='white')
    
    def update_days_button_color(self):
        days_buttons = [self.montag_button, self.dienstag_button, self.mittwoch_button, self.donnerstag_button, self.freitag_button, self.samstag_button, self.sonntag_button]

        for i in range(0,7):        
            if self.container_name.days[i] == True:
                days_buttons[i].config(bg='#00ff00', activebackground='green')
            else:
                days_buttons[i].config(bg='white', activebackground='white')

    def time_selection(self, time_no):
        self.selected_time = time_no

        self.times_buttons = [self.time_1_button, self.time_2_button, self.time_3_button, self.time_4_button]
            
        #Hintergundfarbe -> Zeitpunkt aktiv-inaktiv
        for i in range(0, 4):
            if self.container_name.times_status[i] == True:
                self.times_buttons[i].config(bg='#00ff00', activebackground='green')
            else:
                self.times_buttons[i].config(bg='white', activebackground='white')

        #Auslesen ob der angewählte Zeitpunkt aktiv oder inaktiv ist
        if self.container_name.times_status[time_no] == True:
            self.activate_button.config(text='Deaktivieren')
        else:
            self.activate_button.config(text='Aktivieren')

        #Ausgewählter Zeitpunkt 1-4 Fett
        for i in self.times_buttons:
            i.config(font=("Helvetica", 15))      
        self.times_buttons[time_no].config(font=("Helvetica", 18, "bold"))

        #Auslesen des unter der Zeitpunkt abgespeicherten Uhrzeit
        time = self.container_name.times[time_no].split(':')
        self.hour_string.set(time[0])
        self.minutes_string.set(time[1])

    def load_settings(self):
        
        with open(self.storage_filename, "r") as file:
            data = json.load(file)
            file.close

        #print(data)
    
        self.container_name.days = data['days']
        self.container_name.times = data['times']
        self.container_name.times_status = data['times_status']
        self.container_name.amount = data['amount']

    def safe_settings(self):
        data = {"days": self.container_name.days, "times": self.container_name.times, "times_status": self.container_name.times_status, "amount": self.container_name.amount}
    
        with open(self.storage_filename, "w") as file:
            json.dump(data, file)
            file.close

    def reset_settings(self):
        self.days_default = [False, False, False, False, False, False, False]
        self.times_default = ['07:00:00','13:00:00','18:00:00','22:00:00']
        self.times_status_default = [False, False, False, False]
        self.amount_default = [1,1,1,1]

        data = {"days": self.days_default, "times": self.times_default, "times_status": self.times_status_default, "amount": self.amount_default}
    
        with open(self.storage_filename, "w") as file:
            json.dump(data, file)
            file.close


class Pillcontainer(object):
    def __init__(self, number):
        self.days = [0,0,0,0,0,0,0]
        self.times = [0,0,0,0]
        self.times_status = [0,0,0,0] 
        self.amount = [0,0,0,0]

        self.number = number       

    def set_dispense_days(self, day_no):
        if self.days[day_no] == False:
            self.days[day_no] = True
        else:
            self.days[day_no] = False

        print('(',self.number,')',self.days)

    def set_dispense_times(self, time_no, time, time_status):
        self.times[time_no] = time
        self.times_status[time_no] = time_status
        print('(',self.number,')',self.times, self.times_status)

    def set_amount(self, time_no, amount):
        self.amount[time_no] = amount


class Hardware(object):
    def __init__(self):

        stepper1_PIN = 17
        stepper2_PIN = 18
        stepper3_PIN = 27
        stepper4_PIN = 22
        self.direction_PIN = 23

        self.stepper_PINS = [stepper1_PIN, stepper2_PIN, stepper3_PIN, stepper4_PIN]

        sensor1_PIN = 19
        sensor2_PIN = 16
        sensor3_PIN = 26
        sensor4_PIN = 20 
        self.sensor_PINS = [sensor1_PIN, sensor2_PIN, sensor3_PIN, sensor4_PIN] 

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.direction_PIN, GPIO.OUT)
        GPIO.output(self.direction_PIN, False)

        self.pwm = ['s1', 's2', 's3', 's4']

        for i in range(0, 3):
            GPIO.setup(self.stepper_PINS[i], GPIO.OUT)
            GPIO.setup(self.sensor_PINS[i], GPIO.IN)
            self.pwm[i] = GPIO.PWM(self.stepper_PINS[i], 50)
            
    def dispense(self, dispense_list):

        for i in range(len(dispense_list)):
            if dispense_list[i] == 0:
                pass
            else:       
                self.pwm[i].start(2) 
                for j in range(0, dispense_list[i]):    
                    while GPIO.input(self.sensor_PINS[i]) == 0:
                        self.pwm[i].ChangeDutyCycle(5)        
                self.pwm[i].stop

    def LED_Bar(self, mode):
        a = mode
        #Neopixel control

    def Sounds(self, status):
        a = status

        
if __name__ == "__main__":
    container_0 = Pillcontainer(0)
    container_1 = Pillcontainer(1)
    container_2 = Pillcontainer(2)
    container_3 = Pillcontainer(3)

    #hardware_control = Hardware()

    GUI = Controller()
    GUI.mainloop()

    

    
