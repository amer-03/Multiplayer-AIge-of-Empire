import json
import urllib.parse

class JsonProcessor:

    @staticmethod
    def to_string(json_obj):

        # Convert the dictionary to a JSON string
        json_str = json.dumps(json_obj)

        # URL-encode the JSON string to make it safe for query parameters
        query_string = urllib.parse.quote(json_str)

        return query_string


    @staticmethod
    def to_json(string_obj):

        # URL-decode the string
        json_str = urllib.parse.unquote(string_obj)

        # Parse the JSON string back to a dictionary
        json_obj = json.loads(json_str)

        return json_obj
