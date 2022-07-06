
import os
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileTrigger():
    def __init__(self, folder_path, include_filters, ClientLogic=None):
        self.observer = Observer()
        self.folder_path = folder_path
        self.include_filters = include_filters
        self.ClientLogic = ClientLogic

    def run(self):
        print("Simple FileTrigger Started")
        print('')

        if not self.ClientLogic:
            print('No fallback function defined for events.')
            print('Using system print()')
            self.ClientLogic = print

        if not os.path.isdir(self.folder_path):
            print("  Monitor dir does not exist.")
            print("  Dir " + self.folder_path + " was created")
            os.mkdir(self.folder_path)

        os.chdir(self.folder_path)
        print("Monitoring: " + self.folder_path)
        print('')

        event_handler = Handler(self.ClientLogic, self.include_filters)
        self.observer.schedule(event_handler, self.folder_path, recursive = True)
        self.observer.start()

        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Client Stopped")

        self.observer.join()

class Handler(FileSystemEventHandler):
    def __init__(self, ClientLogic, include_filters):
        super(FileSystemEventHandler).__init__()
        self.logic_function = ClientLogic
        self.include_filters = include_filters

    #This is the callback function for file events.
    #You can edit it to trigger at file creation, modification, deletion and have different behaviours for each.
    def on_any_event(self, event):
        # print(event)
        if event.is_directory and event.event_type == 'created':
            # print("directory created")
            # self.logic_function(event.src_path)
            return None
        elif event.event_type == 'created':
            print("file created")
            for pattern in self.include_filters:
                if event.src_path.endswith(pattern):
                        print("File with " + pattern)
                        self.logic_function(event.src_path)
                        return None
        # elif event.event_type == 'modified':
        #     self.logic_function(event.src_path)
        #     return None