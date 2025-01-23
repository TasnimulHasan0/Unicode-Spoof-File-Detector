import os
import re
import time
import tkinter as tk
from tkinter import messagebox
import magic
import win32com.client
import win32serviceutil
import win32service
import win32event
import servicemanager
import win32security
import win32file

class UnicodeSpoofDetector:
    def __init__(self, download_folder=None):
        self.download_folder = download_folder or os.path.expanduser('~\\Downloads')
        self.suspicious_unicode_patterns = [
            r'[\u200B-\u200D\u2060\u2061\u2062\u2063\u2064]',
            r'[\u202A-\u202E]',
            r'[^\x00-\x7F]',
            r'[\u2028\u2029]',
            r'[\uFFF0-\uFFFF]'
        ]
        self.dangerous_extensions = [
            '.exe', '.bat', '.cmd', '.vbs', '.ps1', 
            '.msi', '.scr', '.jar', '.js'
        ]

    def contains_suspicious_unicode(self, filename):
        return any(re.search(pattern, filename) for pattern in self.suspicious_unicode_patterns)

    def detect_file_spoof(self, filepath):
        filename = os.path.basename(filepath)
        
        if self.contains_suspicious_unicode(filename):
            return True
        
        try:
            file_type = magic.from_file(filepath)
            
            for ext in self.dangerous_extensions:
                if filename.lower().endswith(ext):
                    if 'executable' in file_type.lower() and not filename.lower().endswith(ext):
                        return True
            
            return False
        except Exception:
            return False

    def show_warning_popup(self, filepath):
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning(
            "Potential Spoofed File Detected", 
            f"The file '{os.path.basename(filepath)}' is potentially dangerous.\n"
            "It uses Unicode characters to spoof file extensions."
        )

    def block_file_execution(self, filepath):
        try:
            sd = win32security.GetFileSecurity(filepath, win32security.DACL_SECURITY_INFORMATION)
            dacl = sd.GetSecurityDescriptorDacl()
            
            dacl.AddAccessDeniedAce(
                win32security.ACL_REVISION, 
                win32file.FILE_ALL_ACCESS, 
                win32security.ConvertStringSidToSid("S-1-1-0")
            )
            
            sd.SetSecurityDescriptorDacl(1, dacl, 0)
            win32security.SetFileSecurity(filepath, win32security.DACL_SECURITY_INFORMATION, sd)
            
            root = tk.Tk()
            root.withdraw()
            messagebox.showwarning(
                "File Execution Blocked", 
                f"The file '{os.path.basename(filepath)}' is blocked from executing.\n"
                "To run this file, stop the file detector."
            )
        except Exception as e:
            print(f"Error blocking file: {e}")

    def monitor_downloads(self):
        shell = win32com.client.Dispatch("Shell.Application")
        downloads_folder = shell.Namespace(self.download_folder)
        processed_files = set()

        while True:
            try:
                for item in downloads_folder.Items():
                    filepath = os.path.join(self.download_folder, item.Name)
                    
                    if filepath not in processed_files:
                        if self.detect_file_spoof(filepath):
                            self.show_warning_popup(filepath)
                            self.block_file_execution(filepath)
                        
                        processed_files.add(filepath)
            except Exception as e:
                print(f"Monitoring error: {e}")
            
            time.sleep(5)

class FileSpoofService(win32serviceutil.ServiceFramework):
    _svc_name_ = "UnicodeSpoofDetector"
    _svc_display_name_ = "Unicode Spoof File Detector"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                               servicemanager.PYS_SERVICE_STARTED,
                               (self._svc_name_, ''))
        self.main()

    def main(self):
        detector = UnicodeSpoofDetector()
        detector.monitor_downloads()

def set_service_auto_start():
    import win32service
    try:
        hscm = win32service.OpenSCManager(
            None, None, win32service.SC_MANAGER_ALL_ACCESS
        )
        
        hs = win32service.OpenService(
            hscm, 
            "UnicodeSpoofDetector", 
            win32service.SERVICE_CHANGE_CONFIG
        )
        
        win32service.ChangeServiceConfig(
            hs,
            win32service.SERVICE_NO_CHANGE,
            win32service.SERVICE_AUTO_START,
            win32service.SERVICE_NO_CHANGE,
            None, None, 0, None, None, None, None
        )
        
        print("Service set to start automatically on boot")
    except Exception as e:
        print(f"Error setting service to auto-start: {e}")

def main():
    win32serviceutil.HandleCommandLine(FileSpoofService)
    set_service_auto_start()

if __name__ == '__main__':
    main()
