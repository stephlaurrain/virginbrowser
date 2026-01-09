# -*-coding:utf-8 -*

import os
import time
import inspect
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
import utils.file_utils as file_utils
import utils.mylog as mylog
import utils.jsonprms as jsonprms
from utils.mydecorators import _error_decorator
import watchdog.observers
import watchdog.events


class Bot:
      
        #def __init__(self):                

        def trace(self,stck):                
                self.log.lg(f"{stck[0].function} ({ stck[0].filename}-{stck[0].lineno})")

        # init
        @_error_decorator()
        def init_webdriver(self, chrome_profile): 
                self.trace(inspect.stack())               
                options = uc.ChromeOptions()                      
                # options.add_argument("--disable-web-security")               
                # pi / docker               
                # options.add_argument(f"user-agent={self.jsprms.prms['user_agent']}")
                options.add_argument("--start-maximized")                                                      
                if chrome_profile is not None:                        
                        full_profile_path = os.path.join(self.root_app, "data", "profiles", chrome_profile)
                        driver = uc.Chrome(user_data_dir=full_profile_path, options=options)
                else:
                        driver = uc.Chrome(options=options)
                # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
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
                        self.log = mylog.Log(self.root_app)
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
        
        def handler(self, event):
                if event.is_directory:
                        self.driver.refresh()
                        return

        @_error_decorator()
        def autorefresh(self, path_to_check):    
                event_handler = watchdog.events.FileSystemEventHandler()
                event_handler.on_modified = self.handler

                observer = watchdog.observers.Observer()
                observer.schedule(event_handler, path=path_to_check, recursive=True)
                observer.start()
                try:
                        while True:
                                time.sleep(1)
                except KeyboardInterrupt:
                        observer.stop()
                        observer.join()

        def main(self, command="", jsonfile="", param_lst=[]):                          
                try:
                        print("params=", command, jsonfile, param_lst)
                                        
                        self.init_main(jsonfile)
                        self.trace(inspect.stack())
                        # wait_node = self.jsprms.prms['wait']
                        # self.humanize = Humanize(self.trace, self.log, wait_node['offset'], wait_node['time'], wait_node['default'])
                        
                        if (command == "browse"):
                                profile_node = self.jsprms.prms['profiles']
                                hardgreen = "\033[32m\033[1m"
                                normalgreen = "\033[32m\033[2m"
                                normalcolor = "\033[0m"
                                print(f"{hardgreen}\n\n===Profiles list===\n")                                                                    
                                for idx, prof in enumerate(profile_node):
                                        print(f"{normalgreen}{idx} - {prof['name']}")
                                choice = input("\nPlease select profile number : ")
                                for idx, prof in enumerate(profile_node):
                                        if int(choice) == idx: 
                                                print(f"Choosen {idx} - {prof['name']}")
                                                profile = prof['profile'] if prof['profile']!="" else None
                                                self.driver = self.init_webdriver(profile)
                                                print(prof['url'])                                                
                                                self.driver.get(prof['url'])             
                                                if prof['autorefresh']:                                                        
                                                        self.autorefresh(prof['pathtocheck'])

                                print(f"{normalcolor}\n")                                                                    
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


              
               
    

        
                

        

