import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pyautogui
import time
import os
import threading

class BasicUI:
    screen_width, screen_height = pyautogui.size()
    center_x = screen_width / 2
    center_y = screen_height / 2

    missions = {
        "死水套&机心套": "MengQian.png",
        "大公套&幽锁套": "YouMing.png",
        "莳者套&信使套": "YaoShi.png",
        "快枪手套&猎人套": "Default.png",
        "过客套&圣骑士套": "Default.png",
        "铁卫套&量子套": "Default.png",
        "拳王套&火匠套": "Default.png",
        "雷套&怪盗套": "Default.png",
        "风套&废土套": "Default.png",
        "漫游指南": "Exp.png",
        "光锥强化材料": "WeaponExp.png",
        "信用点": "Credit.png"
    }
    def mouse_center(self):
        pyautogui.moveTo(self.center_x, self.center_y)
    
    def locate_and_click(self, image_name, conf):
        image_path = os.path.join(os.path.dirname(__file__), 'Image', image_name)
        found = False
        while not found:
            try:
                pyautogui.click(pyautogui.locateOnScreen(image_path, confidence = conf))
                found = True
            except Exception as e:
                time.sleep(1)
                
    def locate_only(self, image_name, conf):
        image_path = os.path.join(os.path.dirname(__file__), 'Image', image_name)
        found = False
        while not found:
            try:
                pyautogui.moveTo(pyautogui.locateOnScreen(image_path, confidence = conf))
                found = True
            except Exception as e:
                time.sleep(1)
                
    def one_time_locate_only(self, image_name, conf):
        image_path = os.path.join(os.path.dirname(__file__), 'Image', image_name)
        try:
            pyautogui.moveTo(pyautogui.locateOnScreen(image_path, confidence=conf))
        except Exception as e:
            return
    
    def one_time_locate_bool(self, image_name, conf):
        image_path = os.path.join(os.path.dirname(__file__), 'Image', image_name)
        try:
            pyautogui.moveTo(pyautogui.locateOnScreen(image_path, confidence=conf))
            return True
        except Exception as e:
            return False
                
    def validate_int(self, value_if_allowed):
        if value_if_allowed.isdigit() or value_if_allowed == "":
            return True
        else:
            return False

    def update_quest_type_display(self):
        if self.quest_type.get() == "ErosionTunnel.png":
            self.string_label.config(text="当前副本类型：侵蚀隧洞")
        elif self.quest_type.get() == "ArtificialBlossom.png":
            self.string_label.config(text="当前副本类型：拟造花萼（金）")
        else:
            self.string_label.config(text="当前未选择副本类型")

    def update_dropdown_menu(self, options):
        self.option_menu['values'] = options
        if options:
            self.option_var.set(options[0])  # 设置默认选项为第一个

    def quit(self):
        os._exit(0)
        #self.root.destroy()
        
    def select_game_directory(self):
        self.game_address = filedialog.askopenfilename(filetypes=[("Executable Files", "*.exe")])
        if self.game_address:
            self.directory_label.config(text=f"所选位置: {self.game_address}")
        else:
            self.game_address = self.default_game_address
            self.directory_label.config(text=f"所选位置: {self.game_address}")



    def get_mission(self, mission_name):
        return self.missions.get(mission_name, "Default.png")

    def start_task_thread(self):
        if self.game_address and not self.string_label.cget("text")=="当前未选择副本类型":
            self.task_thread = threading.Thread(target=self.start_task)
            self.task_thread.start()
    
    def __init__(self, root):
        self.root = root
        self.root.title("星穹铁道日常")

        self.root.geometry("600x800")

        #Game Directory
        self.default_game_address = "C:/Program Files/HoYoPlay/launcher.exe"
        self.game_address = self.default_game_address
  
        self.select_directory_button = tk.Button(root, text="选择Hoyoplay位置", command=self.select_game_directory)
        self.select_directory_button.pack(pady=10)

        
        self.directory_label = tk.Label(root, text=f"所选位置: {self.game_address}",wraplength=500)
        self.directory_label.pack(pady=10)

        #Quest Type
        self.list_label = tk.Label(root, text="副本类型")
        self.list_label.pack(pady=10)

        #quest_type value here
        self.quest_type = tk.StringVar()

        self.quest_frame = tk.Frame(root)
        self.quest_frame.pack(pady=10)

        #ErosionTunnel
        self.button1 = tk.Button(self.quest_frame, text="侵蚀隧洞", command=lambda: (self.quest_type.set("ErosionTunnel.png"),
                                                                                     self.update_quest_type_display(),
                                                                                     self.update_dropdown_menu(list(self.missions.keys())[:9])))
        #ArtificialBlossom
        self.button1.pack(side=tk.LEFT,padx=5)
        self.button2 = tk.Button(self.quest_frame, text="拟造花萼（金）", command=lambda: (self.quest_type.set("ArtificialBlossom.png"),
                                                                                         self.update_quest_type_display(),
                                                                                         self.update_dropdown_menu(list(self.missions.keys())[9:])))
        self.button2.pack(side=tk.LEFT,padx=5)

        # Add a label to display the current quest type
        self.string_label = tk.Label(root, text="")
        self.string_label.pack(pady=10)

        self.update_quest_type_display()

        #Option menu
        self.option_label = tk.Label(root, text="选择项目")
        self.option_label.pack(pady=10)

        #option value here
        self.option_var = tk.StringVar()
        self.option_menu = ttk.Combobox(root, textvariable=self.option_var)
        self.option_menu.pack(pady=10)
        
        #Time Entry
        self.times_label = tk.Label(root, text="输入刷取次数:")
        self.times_label.pack(pady=10)
        
        self.times = tk.StringVar(value=6)
        
        vcmd = (self.root.register(self.validate_int), '%P')
        self.times_entry = tk.Entry(root, textvariable=self.times, validate='key', validatecommand=vcmd)
        self.times_entry.pack(pady=10)

        self.checkbox_var = tk.BooleanVar()
        
        # Monthly Pass checkbox
        self.checkbox = tk.Checkbutton(root, text="小月卡", variable=self.checkbox_var, command=None)
        self.checkbox.pack(pady=10)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        # Start Button
        self.start_button = tk.Button(self.button_frame, text="开始日常", command=self.start_task_thread)
        self.start_button.pack(side=tk.LEFT, padx=5)

        # Quit Button
        self.quit_button = tk.Button(self.button_frame, text="退出", command=self.quit)
        self.quit_button.pack(side=tk.LEFT, padx=5)


    
    def start_task(self):
        found = False
        os.startfile(self.game_address)
        
        #Find Star_Rail Game
        self.locate_and_click('StarRail.png',0.8)
        #Find launch game button
        self.locate_and_click('Launch.png',0.8)
        self.locate_and_click('StartGame.png',0.8)
        self.locate_and_click('EnterGame.png',0.8)

        #MonthlyPass
        if self.checkbox_var.get():
            self.locate_and_click("MonthlyPass1.png", 0.8)

            self.locate_only("MonthlyPass2.png", 0.8)

            pyautogui.click(self.center_x, self.center_y + 600)

        self.locate_only('EnterGameDetector.png',0.8)
        pyautogui.press('esc')
        self.locate_and_click('Guide.png',0.8)

        #Find Teleport button
        found = False
        while not found:
            try:
                self.one_time_locate_only("TeleportUnselected.png",0.8)
                self.locate_and_click("TeleportUnselected.png",0.8)
                found = True
            except:
                try:
                    self.one_time_locate_only("TeleportSelected.png",0.8)
                    found = True
                except:
                    time.sleep(1)
        
        #Choose what to get
        self.locate_and_click(self.quest_type.get(),0.8)

        #Choose what to get 2 and locate teleport
        self.mouse_center()
        found = False
        while not self.one_time_locate_bool(self.get_mission(self.option_menu.get()),0.9):
            pyautogui.scroll(-3)
        image_path = os.path.join(os.path.dirname(__file__), 'Image', self.get_mission(self.option_menu.get()))
        location = pyautogui.locateOnScreen(image_path, confidence = 0.9)
        teleport_image_path = os.path.join(os.path.dirname(__file__), 'Image', "Teleport.png")
        teleport_locations = list(pyautogui.locateAllOnScreen(teleport_image_path, confidence=0.7))
        min_diff = float('inf')
        best_location = None
        for loc in teleport_locations:
                center = pyautogui.center(loc)
                y_diff = abs(center.y - location[1])
                if y_diff < min_diff:
                        min_diff = y_diff
                        best_location = center    
        pyautogui.click(best_location)

        self.locate_and_click('Challenge.png',0.9)
        self.locate_and_click('StartCombat.png',0.9)
        time.sleep(1)
        found = False
        while not found:
            try:
                self.one_time_locate_only("SpeedUp.png",0.8)
                self.locate_and_click("SpeedUp.png",0.8)
                found = True
            except:
                try:
                    self.one_time_locate_only("SpedUp.png",0.8)
                    found = True
                except:
                    time.sleep(1)
        self.locate_and_click('Auto.png',0.9)
        for i in range(0,int(self.times.get())):
            self.locate_and_click('Restart.png',0.9)
            
            
        
    
if __name__ == "__main__":
    root = tk.Tk()
    app = BasicUI(root)
    root.mainloop()
