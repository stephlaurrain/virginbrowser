# -*-coding:utf-8 -*

import os
from os import path
import sys
import random
from datetime import datetime
from time import sleep
import inspect
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import utils.file_utils as file_utils
import utils.mylog as mylog
import utils.jsonprms as jsonprms
import utils.img_utils as img_utils
from utils.humanize import Humanize
from utils.mydecorators import _error_decorator
from selenium.webdriver.common.action_chains import ActionChains


class Bot:
      
        #def __init__(self):                

        def trace(self,stck):                
                self.log.lg(f"{stck[0].function} ({ stck[0].filename}-{stck[0].lineno})")

        # init
        @_error_decorator()
        def init_webdriver(self, chrome_profile): 
                self.trace(inspect.stack())               
                options = webdriver.ChromeOptions()
                if (self.jsprms.prms['headless']):
                        options.add_argument("--headless")
                else:
                        if chrome_profile != None:
                                options.add_argument(f"user-data-dir=./data{os.path.sep}profiles{os.path.sep}{chrome_profile}")
                # anti bot detection
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
                # pi / docker
                if (self.jsprms.prms['box']):
                        options.add_argument("--no-sandbox")
                        options.add_argument("--disable-dev-shm-usage")
                        options.add_argument("--disable-gpu")
                        prefs = {"profile.managed_default_content_settings.images": 2}
                        options.add_experimental_option("prefs", prefs)
                # options.add_argument(f"user-agent={self.jsprms.prms['user_agent']}")
                options.add_argument("--start-maximized")
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)                
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                # resolve unreachable
                driver.set_window_size(1900, 1080)
                # driver.set_window_position(0, 0, windowHandle=) #, windowHandle='current')
                driver.maximize_window()
                 
                return driver
        
        @_error_decorator()
        def remove_logs(self):
                self.trace(inspect.stack())
                keep_log_time = self.jsprms.prms['keep_log']['time']
                keep_log_unit = self.jsprms.prms['keep_log']['unit']
                self.log.lg(f"=>clean logs older than {keep_log_time} {keep_log_unit}")                        
                file_utils.remove_old_files(f"{self.root_app}{os.path.sep}log", keep_log_time, keep_log_unit)   

        def init_main(self, jsonfile):
                try:
                        self.root_app = os.getcwd()
                        self.log = mylog.Log()
                        self.log.init(jsonfile)
                        # self.trace(inspect.stack())
                        jsonFn = f"{self.root_app}{os.path.sep}data{os.path.sep}conf{os.path.sep}{jsonfile}.json"                        
                        self.jsprms = jsonprms.Prms(jsonFn)
                        self.log.lg("=HERE WE GO=")                        
                        self.remove_logs()
                        
                except Exception as e:
                        self.log.errlg(f"Wasted ! : {e}")
                        raise

        @_error_decorator()
        def newtab(self,url):            
                self.driver.execute_script("window.open('{0}');".format(url))
                self.driver.switch_to.window(self.driver.window_handles[-1]) 
        
        @_error_decorator()
        def reset_profile(self):    
                profile_dir = f"{self.root_app}{os.path.sep}chromeprofile"
                file_utils.rmrf(profile_dir)                
                import tarfile
                arch = f"{self.root_app}{os.path.sep}data{os.path.sep}chromeprofile.tar.gz"
                file = tarfile.open(arch)
                file.extractall(f"{self.root_app}{os.path.sep}")
                file.close()

        def main(self, command="", jsonfile="", param_lst=[]):                          
                try:
                        print("params=", command, jsonfile, param_lst)
                                        
                        self.init_main(jsonfile)
                        self.trace(inspect.stack())
                        # wait_node = self.jsprms.prms['wait']
                        # self.humanize = Humanize(self.trace, self.log, wait_node['offset'], wait_node['time'], wait_node['default'])
                        
                        if (command == "browse"):
                                profile_node = self.jsprms.prms['profiles']
                                for idx, prof in enumerate(profile_node):
                                        print(f"{idx} - {prof['name']}")
                                choice = input("\nP134$3 $313(7 profile number : ")
                                for idx, prof in enumerate(profile_node):
                                        if int(choice) == idx: 
                                                print(f"Choosen {idx} - {prof['name']}")
                                                profile = prof['profile'] if prof['profile']!="" else None
                                                self.driver = self.init_webdriver(profile)
                                                print(prof['url'])
                                                self.driver.get(prof['url'])                                                
                                input("Let u browsing, waiting 4 k to end : ")
                                if hasattr(self, 'driver') and self.driver is not None:
                                        self.driver.close()
                                        self.driver.quit()

                        if (command == "resetprofile"): 
                                self.reset_profile()                                
                        

                except KeyboardInterrupt:
                        print("==Interrupted==")
                        pass
                except Exception as e:
                        print("GLOBAL MAIN EXCEPTION")
                        self.log.errlg(e)
                        # raise
                        #
                finally:
                        
                        print("The end")                        


              
               
    

        
                

        

