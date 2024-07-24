import json


class Utilities:
    @staticmethod
    def pretty_print_json(json_object):
        """
        Static method to pretty print a JSON object.

        Parameters:
        json_object (dict): JSON object to be pretty printed.

        Returns:
        str: Pretty printed JSON string.
        """
        return json.dumps(json_object, indent=2, sort_keys=True)
