import json
import requests


class CodeWarsApi:
    def __init__(self, token):
        self.token = token

    def get_kata_name_and_description(self, kata_id):
        endpoint = f"https://www.codewars.com/api/v1/code-challenges/{kata_id}"
        res = requests.get(endpoint, params={"Authorization": self.token})
        data = json.loads(res.text)
        return data["name"], data["description"]

    def get_user_total_completed(self, user_name, page_number):
        endpoint = f"https://www.codewars.com/api/v1/users/{user_name}/code-challenges/completed?page={page_number}"

        res = requests.get(endpoint, params={"Authorization": self.token})
        return json.loads(res.text)
