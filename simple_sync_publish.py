#!/usr/bin/env python

import os
import argparse
import glob

#### This could go into a different file and be invoked without the file watcher
from globus_automate_client import create_flows_client
fc = create_flows_client()

def run_sync_flow(event_file):
    
    # Using a flow that was deployed using the "Automation Using Globus Flows" notebook
    # To do: update to flow that needs to be run 
    flow_id = '9f330207-3db6-4f57-8c72-8253922ae754'
    # To do: update the scope for the flow
    flow_scope = 'https://auth.globus.org/scopes/9f330207-3db6-4f57-8c72-8253922ae754/flow_9f330207_3db6_4f57_8c72_8253922ae754_user'
    
    # Source is the endpoint where this trigger code is running
    # To do: update to id of the endpoint where this code is running
    source_id = 'e7d4f216-9a9a-11ea-8ece-02c81b96a709'
    
    # To do: update to destination endpoint, 
    # Must be a shared endpoint or guest collection so permission can be set
    destination_id = 'b7641b2a-f74a-11ec-835d-cd84b862b754'
    # To do: update path
    remote_path = '/Test/'

    # To do: update to set group id to share with
    # group id to share with
    group_id = '50b6a29c-63ac-11e4-8062-22000ab68755'

    # to get the directory where the .done file is stored, 
    # and add a ending / to satisfy Transfer requirements
    # for moving a directory
    event_folder = os.path.dirname(event_file)
    source_path = os.path.join(event_folder, "") 
    
    # to get a resonable label, using the file that triggered the run
    event_file_name = os.path.basename(event_file)
   
    # to get a resonable label, using the file that triggered the run
    event_file_name = os.path.basename(event_file)
    
    # to be able to set permission on the specific folder being moved
    # the name of the source folder needs to be worked out to use in 
    # destination path
    event_folder_name = os.path.basename(event_folder)
    # Add a slash to meet Transfer requirements for directory transfer
    destination_path = os.path.join(remote_path, event_folder_name, "")

    #Globus search information
    #To do: Specify the search index to publish your metadata 
    search_index = '563c3d98-6fa8-4ef5-83e2-0f378efe0a5f'

    #Gather some information for the transfer
    #To do: add specific information and add it to "search_content_metadata" in the base_in
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

            #information to ingest on globus Search
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

    run_result = fc.run_flow(flow_id = flow_id, flow_scope = flow_scope, flow_input= base_input, label=event_file_name, tags=['PEARC_Test'])
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
