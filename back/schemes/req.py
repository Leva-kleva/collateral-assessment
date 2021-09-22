object = {
    "type": "object",
    "properties": {
        "object": {"type": "array"}
    },
    "required": ["object"]
}

post = {'car': {
                "type": "object",
                "properties": {
                    "Engine": {"type": "array"},
                    "Mileage": {"type": "array"},
                    "Drive": {"type": "array"},
                    "Year": {"type": "array"},
                    "Box": {"type": "array"},
                    "Engine_volume": {"type": "array"},
                    "mark": {"type": "array"},
                    "Generation": {"type": "array"},
                    "Model": {"type": "array"},
                    "Torque": {"type": "array"},
                        },
                "required": ["Engine", "Mileage", "Drive", "Year",
                             "Box", "Engine_volume", "mark",
                             "Generation", "Model", "Torque",]
                },
    'flat': {
        "type": "object",
        "properties": {
            "wallsMaterial": {"type": "array"},
            "floorNumber": {"type": "array"},
            "floorsTotal": {"type": "array"},
            "totalArea": {"type": "array"},
            "kitchenArea": {"type": "array"},
            "latitude": {"type": "array"},
            "longitude": {"type": "array"},
        },
        "required": ["wallsMaterial", "floorNumber", "floorsTotal",
                     "totalArea", "kitchenArea", "latitude", "longitude"]
    }}
