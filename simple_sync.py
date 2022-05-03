#!/usr/bin/env python

import os
import argparse

#### This could go into a different file and be invoked without the file watcher
from globus_automate_client import create_flows_client
fc = create_flows_client()

def run_sync_flow(event_file):
    flow_id = '5e1d78d8-1fa5-497c-94d8-be96489b666d' # run simple_sync_def.py for a new one


    event_file_name = os.path.basename(event_file)
    remote_path = '~/test_result'

    # Base input for the flow
    base_input = {
        # globus local endpoint
        "source_endpoint_id": 'cde22510-5de7-11ec-9b5c-f9dfb1abb183',
        "source_path" : event_file,
        # globus endpoint and mount point for remote resource
        "destination_endpoint_id": 'cde22510-5de7-11ec-9b5c-f9dfb1abb183', 
        "destination_path" : os.path.join(remote_path,event_file_name),
    }

    run_result = fc.run_flow(flow_id, None, base_input, label=event_file_name)
    print('Moving: ' + event_file)
    print('https://app.globus.org/runs/'+run_result['run_id'])

# Arg Parsing
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('localdir', type=str, default='.')
    return parser.parse_args()


if __name__ == '__main__':

    from folder_watch import FileTrigger

    args = parse_args()
    local_dir = os.path.expanduser(args.localdir)

    ##Creates and starts the watcher
    exp = FileTrigger(local_dir, ClientLogic=run_sync_flow)
    exp.run()





