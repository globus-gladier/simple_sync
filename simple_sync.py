#!/usr/bin/env python

import os
import argparse
import glob

#### This could go into a different file and be invoked without the file watcher
from globus_automate_client import create_flows_client
fc = create_flows_client()

def run_sync_flow(event_file):
    
    # Using a flow that was deployed using the "Automation Using Globus Flows" notebook
    flow_id = 'f18e35c2-594d-4fa4-a820-9b22e26f1f62'
    flow_scope = 'https://auth.globus.org/scopes/78dae322-ac8f-4fee-b008-f471ce66dbb5/flow_a54ae3a9_acda_4c40_9434_305d3680ba49_user'
    
     # Source is the endpoint where this trigger code is running
     # This id is my laptop
    source_id = '6d3275c0-e5d3-11ec-9bd1-2d2219dcc1fa'
    # to get the directory where the .done file is stored, 
    # and add a ending / to satisfy Transfer requirements
    # for moving a directory
    event_folder = os.path.dirname(event_file)
    source_path = os.path.join(event_folder, "") 
   
    # to get a resonable label, using the file that triggered the run
    event_file_name = os.path.basename(event_file)
    
    search_index = '563c3d98-6fa8-4ef5-83e2-0f378efe0a5f'

    # PEARC demo endpoint
    destination_id = '6d3275c0-e5d3-11ec-9bd1-2d2219dcc1fa'
    remote_path = '~/Project1/'
    # to be able to set permission on the specific folder being moved
    # the name of the source folder needs to be worked out to use in 
    # destination path
    event_folder_name = os.path.basename(event_folder)
    # Add a slash to meet Transfer requirements for directory transfer
    destination_path = os.path.join(remote_path, event_folder_name, "")

    # group id to share with
    group_id = '50b6a29c-63ac-11e4-8062-22000ab68755'

    #Gather some information for the transfer 
    file_names = glob.glob(source_path+'*')
    n_files = len(file_names)
    

    # Base input for the flow
    base_input = {
        "input" : {
            # local endpoint where the event listner is running
            "src": {
              "id": source_id,
              "path": source_path,
            },
            "dest": {
                "id": destination_id,
                "path": destination_path,
             },
        
            "recur": True,
            # Grant access to the Tutorial Users group
            "principal_identifier": group_id,
            "principal_type": "group",

            #information to ingest
            "search_ingest_doc": {
            "search_index": search_index,
            "search_subject": event_folder_name,
            "search_visible_to": ["public"],
            "search_content_metadata": {
                "title": event_folder_name,
                "Username":"raf",
                "fname": file_names,
                "n_files":n_files
            }
        }
    }
    }

    run_result = fc.run_flow(flow_id = flow_id, flow_scope = None, flow_input= base_input, label=event_file_name, tags=['PEARC_Test'])
    print('Moving and sharing: ' + event_folder_name)
    print('https://app.globus.org/runs/'+run_result['run_id'])

    print('Example portal for search index: ' + search_index)
    print('https://acdc.alcf.anl.gov/globus-tutorial/' + search_index)
    print('')
    

# Arg Parsing
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--localdir', type=str, default=os.path.abspath('.'))
    parser.add_argument('--include', nargs='*', type=str, default='')
    return parser.parse_args()


if __name__ == '__main__':

    from folder_watch import FileTrigger

    args = parse_args()
    local_dir = os.path.expanduser(args.localdir)
    

    ##Creates and starts the watcher
    exp = FileTrigger(local_dir, include_filters=args.include, ClientLogic=run_sync_flow)
    exp.run()
