def run_sync_flow(event_file):
    
    # Using a flow that was deployed using the "Automation Using Globus Flows" notebook
    flow_id = '5e1d78d8-1fa5-497c-94d8-be96489b666d'#raf
    flow_id = 'a54ae3a9-acda-4c40-9434-305d3680ba49'#rachana
    flow_scope = 'https://auth.globus.org/scopes/a54ae3a9-acda-4c40-9434-305d3680ba49/flow_a54ae3a9_acda_4c40_9434_305d3680ba49_user'
    
     # Source is the endpoint where this trigger code is running
     # This id is my laptop
     #raf 'cde22510-5de7-11ec-9b5c-f9dfb1abb183'
    source_id = 'e7d4f216-9a9a-11ea-8ece-02c81b96a709'
    # to get the directory where the .done file is stored, 
    # and add a ending / to satisfy Transfer requirements
    # for moving a directory
    event_folder = os.path.dirname(event_file)
    source_path = os.path.join(event_folder, "") 
   
    # to get a resonable label, using the file that triggered the run
    event_file_name = os.path.basename(event_file)
    

    # PEARC demo endpoint
    #'cde22510-5de7-11ec-9b5c-f9dfb1abb183' raf
    destination_id = 'b7641b2a-f74a-11ec-835d-cd84b862b754'
    remote_path = '/Project1/'
    # to be able to set permission on the specific folder being moved
    # the name of the source folder needs to be worked out to use in 
    # destination path
    event_folder_name = os.path.basename(event_folder)
    # Add a slash to meet Transfer requirements for directory transfer
    destination_path = os.path.join(remote_path, event_folder_name, "")

    # group id to share with
    group_id = '50b6a29c-63ac-11e4-8062-22000ab68755'

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
        }
    }
    
    run_result = fc.run_flow(flow_id = flow_id, flow_scope = flow_scope, flow_input= base_input, label=event_file_name, tags=['PEARC_Test'])
    print('Moving and sharing: ' + event_folder_name)
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
