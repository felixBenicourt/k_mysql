
# element_config.py

ELEMENT_TYPES = {
    "project": {
        "required_keys": ["name"],
        "keys_to_ignore": ["id"],
        "query_method": "get_all_project",
    },
    "sequence": {
        "required_keys": ["projectId", "name"],
        "keys_to_ignore": ["id"],
        "query_method": "get_all_sequence",
    },
    "asset": {
        "required_keys": [
            "projectId", 
            "name", 
            "type", 
            "task", 
            "variation", 
            "version", 
            "status"
        ],
        "keys_to_ignore": ["id"],
        "query_method": "get_all_asset",
    },
    "shot": {
        "required_keys": [
            "projectId", 
            "name", 
            "type", 
            "task", 
            "variation", 
            "sequenceId", 
            "version", 
            "cutIn", 
            "cutOut"
        ],
        "keys_to_ignore": ["id", "cutIn", "cutOut"],
        "query_method": "get_all_shot",
    },
}
