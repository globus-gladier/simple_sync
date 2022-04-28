#!/usr/bin/env python

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
            ClientLogic(event.src_path)
            return None
        elif event.event_type == 'modified':
            ClientLogic(event.src_path)
            return None

def ClientLogic(event_file):
    print(event_file)

def deploy_flow():
    import simple_sync_def
    # Deploy the flow
    flow_title = f"Simple Sync Flow"
    flow = fc.deploy_flow(
    simple_sync_def.flow_definition, 
    title=flow_title,
    input_schema=simple_sync_def.input_schema,
    )
    flow_id = flow['id']
    flow_scope = flow['globus_auth_scope']
    print(flow_id)
    return flow_id

# Arg Parsing
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('localdir', type=str, default='.')
    return parser.parse_args()

if __name__ == '__main__':

    from globus_automate_client import create_flows_client
    fc = create_flows_client()

    #flow_id = deploy_flow()
    flow_id = 'a95b8166-c4af-47ed-abae-ec3f430497b4'
    args = parse_args()
    local_dir = args.localdir

    # Base input for the flow
    base_input = {
        "input": {
            # globus local endpoint
            "example_transfer_source_endpoint_id": '',
    	    "example_transfer_source_endpoint_path" : '',
            # globus endpoint and mount point for remote resource
            "example_transfer_destination_id": '', 
    	    "example_transfer_destination_path" : '',
        }
    }

    ##Creates and starts the watcher
    exp = FileTrigger(local_dir)
    exp.run()





