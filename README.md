# simple-sync-service

We provide two simple folder watchers for flows.
The example flows can be found in detail at globus-jupyter-notebooks](https://github.com/globus/globus-jupyter-notebooks).

## Install 
This examples require only the `globus_automate_client` and `watchdog` packages. They can be installed by setting a new environment with:

     pip install -r requirements.txt

## Deploy flow
Two flows are provided for this examples, the first executes a `folder transfer` and `set permissions` while the second also `publishes` metadata in a globus portal. 

Both scripts can be executes to register a new flow with globus services:

    ./def_simple_sync.py
    ./def_simple_sync_publish.py

## Deploy Client

The clients (`simple_sync.py` and `simple_sync_publish.py` are executables with the following inputs:

`--local_dir` defines the folder to watch.
`--includes` defines the file types that will trigger the flow. This can receive a list separated by spaces.

```bash
./simplesync.py --local_dir $local_dir --include .txt
```

## Client logic

The trigger logic can be easily modified on `folder_watch.py`

```python
class Handler(FileSystemEventHandler):
def __init__(self, ClientLogic, include_filters):
     super(FileSystemEventHandler).__init__()
     self.logic_function = ClientLogic
     self.include_filters = include_filters
def on_any_event(self, event):
     if event.event_type == 'created':
          print("File created: "+ os.path.basename(event.src_path))
          for pattern in self.include_filters:
               if event.src_path.endswith(pattern):
                    print("File with " + pattern)
                    print("Starting Flow")
                    self.logic_function(event.src_path)
                    return None
```
In this case. The flow will be started everytime a file is created and endswith the filetype on `--includes`

It is important to notice that the logic can also be included on the client file `simple_sync.py`.

