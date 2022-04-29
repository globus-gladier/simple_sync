#!/usr/bin/env python

import os
import argparse

from folder_watch import FileTrigger

# Arg Parsing
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('localdir', type=str, default='.')
    return parser.parse_args()


def run_sync_flow(event_file):
    print(event_file)
    return
    flow_id = 'a95b8166-c4af-47ed-abae-ec3f430497b4'

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

if __name__ == '__main__':

    from globus_automate_client import create_flows_client
    fc = create_flows_client()

    args = parse_args()
    local_dir = os.path.expanduser(args.localdir)

    ##Creates and starts the watcher
    exp = FileTrigger(local_dir, ClientLogic=run_sync_flow)
    exp.run()





