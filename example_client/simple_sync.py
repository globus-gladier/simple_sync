#!/local/data/idsbc/idstaff/gladier/miniconda3/envs/gladier/bin/python

import time, argparse, os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileTrigger:
    def __init__(self, folder_path):
        self.observer = Observer()
        self.folder_path = folder_path

    def run(self):
        print("Simple FileTrigger Started")
        if not os.path.isdir(self.folder_path):
            print("  Monitor dir does not exist.")
            print("  Dir " + self.folder_path + " was created")
            os.mkdir(self.folder_path)

        os.chdir(self.folder_path)
        print("Monitoring: " + self.folder_path)
        print('')

        event_handler = Handler()
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
    @staticmethod
    def on_any_event(event):
        print(event)
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            #ClientLogic(event.src_path)
            return None
        elif event.event_type == 'modified':
            ClientLogic(event.src_path)
            return None


def ClientLogic(event_file):
    
    pass

# Arg Parsing
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('localdir', type=str, default='.')
    return parser.parse_args()

if __name__ == '__main__':

    args = parse_args()
    local_dir = args.localdir

    # Base input for the flow
    base_input = {
        "input": {
            #Processing variables
            "base_local_dir": local_dir,
            # globus local endpoint
            "globus_local_ep": depl_input['input']['beamline_globus_ep'],
    	    "globus_local_mount" : depl_input['input']['ssx_eagle_mount'],
            # globus endpoint and mount point for remote resource
            "globus_dest_ep": depl_input['input']['theta_globus_ep'], 
    	    "globus_dest_mount" : depl_input['input']['ssx_eagle_mount'],
        }
    }

    ##Creates and starts the watcher
    exp = KanzusTriggers(local_dir)
    exp.run()



