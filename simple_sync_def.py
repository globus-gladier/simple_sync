#!/usr/bin/env python

flow_definition = {
        'Comment': 'Transfer a file using Globus Transfer',
        'StartAt': 'SimpleTransfer',
        'States': {
            'SimpleTransfer': {
                'Comment': 'Transfer a file or directory in Globus',
                'Type': 'Action',
                'ActionUrl': 'https://actions.automate.globus.org/transfer/transfer',
                'Parameters': {
                    'source_endpoint_id.$': '$.source_endpoint_id',
                    'destination_endpoint_id.$': '$.destination_endpoint_id',
                    'transfer_items': [
                        {
                            'source_path.$': '$.source_path',
                            'destination_path.$': '$.destination_path',
                        }
                    ]
                },
                'ResultPath': '$.SimpleTransfer',
                'WaitTime': 600,
                'End': True
            },
        }
    }

input_schema = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "source_endpoint_id": {"type": "string"},
        "source_path": {"type": "string"},
        "destination_endpoint_id": {"type": "string"},
        "destination_path": {"type": "string"},
    },
    "required": [
        "source_endpoint_id",
        "source_path",
        "destination_endpoint_id",
        "destination_path",
    ],
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