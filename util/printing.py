import json

# Pretty print json data to command line
def pretty_print(json_data):
    json_object = json.loads(str(json_data))

    json_formatted_str = json.dumps(json_object, indent=2)

    print(json_formatted_str)