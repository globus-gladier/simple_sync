#!/usr/bin/env python

# Define flow
flow_definition = {
  "Comment": "Move files to guest collection, set access permissions and publish metadata in search",
  "StartAt": "MoveFiles",
  "States": {
    "MoveFiles": {
      "Comment": "Transfer from Globus Tutorial Endpoint 1 to a guest collection on Eagle",
      # https://globus-automate-client.readthedocs.io/en/latest/globus_action_providers.html#globus-transfer-transfer-data
      "Type": "Action",
      "ActionUrl": "https://actions.automate.globus.org/transfer/transfer",
      "Parameters": {
        "source_endpoint_id.$": "$.input.src.id", 
        "destination_endpoint_id.$": "$.input.dest.id",
        "transfer_items": [
              {
                "source_path.$": "$.input.src.path",
                "destination_path.$": "$.input.dest.path",
                "recursive.$": "$.input.recur"
              }
        ],
      },
      "ResultPath": "$.MoveFiles",
      "WaitTime": 60,
      "Next": "SetPermission"
    }, 
    "SetPermission": {
      "Comment": "Grant read permission on the data to the Tutorial users group",
      "Type": "Action",
      # https://globus-automate-client.readthedocs.io/en/latest/globus_action_providers.html#globus-transfer-set-manage-permissions
      "ActionUrl": "https://actions.automate.globus.org/transfer/set_permission",
      "ExceptionOnActionFailure": False,
      "Parameters": {
        "endpoint_id.$": "$.input.dest.id",
        "path.$": "$.input.dest.path",
        "permissions": "r",  # read-only access
        "principal.$": "$.input.principal_identifier",  # 'group'
        "principal_type.$": "$.input.principal_type",
        "operation": "CREATE",
      },
      "ResultPath": "$.SetPermission",
      "Next": "SearchIngest"
    },
    "SearchIngest": {
      "Comment": "Ingest a Globus Search document",
      "Type": "Action",
      "ActionUrl": "https://actions.globus.org/search/ingest",
      "Parameters": {
        "search_index.$": "$.input.search_ingest_doc.search_index",  
        "subject.$": "$.input.search_ingest_doc.search_subject",  
        "visible_to.$": "$.input.search_ingest_doc.search_visible_to",  
        "content.$": "$.input.search_ingest_doc.search_content_metadata",  
      },
      "ResultPath": "$.PublishMetadata",
      "End": True
    },
  }
}

input_schema = {
    "additionalProperties": False,
    "required": [
        "input"
    ],
    "properties": {
        "input": {
            "type": "object",
            "required": [
                "src", "dest", "recur", "principal_identifier", "principal_type", "search_ingest_doc", 
            ],
            "properties": {
                "src": {
                    "type": "object",
                    "format": "globus-collection",
                    "title": "Find source collection ID and path",
                    "required": [
                        "id",
                        "path"
                    ],
                    "properties": {
                        "id": {
                            "type": "string",
                            "format": "uuid",
                        },
                        "path": {
                            "type": "string",
                            "default": "/share/godata/"
                        }
                    },
                    "additionalProperties": False
                },
                "dest": {
                    "type": "object",
                    "format": "globus-collection",
                    "title": "Find destination endpoint ID and path",
                    "required": [
                        "id",
                        "path"
                    ],
                    "properties": {
                        "id": {
                            "type": "string",
                            "format": "uuid",
                        },
                        "path": {
                            "type": "string",
                        }
                    },
                    "description": "The path to transfer and share the source files (Make sure the path ends with a slash!)",
                    "additionalProperties": False
                },
                "recur": {
                    "type": "boolean",
                    "title": "Recursive transfer",
                    "description": "Whether or not to transfer a directory recursively, must be true when transferring a directory.",
                    "default": True
                },              
                "principal_identifier": {
                    "type": "string",
                    "title": "Principal identifier - UUID of user identity or group",
                    "format": "uuid",
                    "description": "The identity id or group id to share with the destination."
                },
                "principal_type": {
                    "type": "string",
                    "title": "Type of principal to share with - user or group",
                    "enum": ["identity", "group"],
                    "default": "group",
                    "description": "Whether this is being shared with a 'user' or a 'group'"
                },
                "search_ingest_doc": {
                    "type": "object",
                    "required": [
                        "search_index",
                        "search_subject",
                        "search_visible_to",
                        "search_content_metadata",
                    ],
                    "properties": {
                        "search_index": {
                            "type": "string",
                            "title": "The Globus Search Index to use",
                            "description": "The desired index to hold this metadata"
                        },
                        "search_subject": {
                            "type": "string",
                            "title": "Globus Search Subject",
                            "description": "The identifier for this search metadata"
                        },
                        "search_visible_to": {
                            "type": "array",
                            "title": "Visible To",
                            "default": ["public"],
                            "description": "For whom should this content be accessible"
                        },
                        "search_content_metadata": {
                            "type": "object",
                            "title": "Search Metadata Content",
                            "description": "Any unstructured metadata you would like to ingest into Globus Search",
                            "additionalProperties": True
                        },
                    }
                }
            },
            "additionalProperties": False
        }
    }
}

def deploy_flow():
    from globus_automate_client import create_flows_client
    fc = create_flows_client()
    # Deploy the flow
    flow_title = f"Simple Sync Flow"
    flow = fc.deploy_flow(
    flow_definition, 
    title=flow_title,
    input_schema=input_schema
    )
    flow_id = flow['id']
    flow_scope = flow['globus_auth_scope']
    print(flow_id)
    return flow_id


if __name__ == '__main__':
    deploy_flow()