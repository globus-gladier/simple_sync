flow_definition = {
        'Comment': 'Transfer a file or directory in Globus',
        'StartAt': 'ExampleTransfer',
        'States': {
            'ExampleTransfer': {
                'Comment': 'Transfer a file or directory in Globus',
                'Type': 'Action',
                'ActionUrl': 'https://actions.automate.globus.org/transfer/transfer',
                'Parameters': {
                    'source_endpoint_id.$': '$.example_transfer_source_endpoint_id',
                    'destination_endpoint_id.$': '$.example_transfer_destination_endpoint_id',
                    'transfer_items': [
                        {
                            'source_path.$': '$.example_transfer_source_path',
                            'destination_path.$': '$.example_transfer_destination_path',
                            'recursive.$': '$.example_transfer_recursive',
                        }
                    ]
                },
                'ResultPath': '$.ExampleTransfer',
                'WaitTime': 600,
                'End': True
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
                "example_transfer_source_endpoint_id", "example_transfer_source_path", "example_transfer_destination_endpoint_id", "example_transfer_destination_path",
                
                "principal", "principal_type", 
            ],
            "properties": {
                "example_transfer_source_endpoint_id": {
                    "type": "string",
                    "format": "uuid",
                },
                "example_transfer_source_path": {
                    "type": "string",
                },
                "example_transfer_destination_endpoint_id": {
                    "type": "string",
                    "format": "uuid",
                },
                "example_transfer_destination_path": {
                    "type": "string",
                },
                "principal": {
                    "type": "string",
                    "format": "uuid",
                },
                "principal_type": {
                    "type": "string",
                    "enum": ["identity", "group"]
                },
                
            },
            "additionalProperties": False
        }
    }
}
