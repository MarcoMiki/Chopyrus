import requests
import pandas


class Chorus:
    def __init__(self, key, url):
        '''Authenticates to a Chorus site. Requires URL and a site API key generated from the "admin - site" menu'''
        self.url = url
        self.login_response = requests.post(url=url + "/rest/v1/auth/loginWithKey", json={"apiKey": key})
        self.sessionID = self.login_response.json()["sessionId"]
        self.headers = {"X-Chorus-Session": self.sessionID}

    # FUNCTIONS TO GET USER DATA AND EXPORT IT

    def get_user_ids(self):
        """function"""
        response = requests.get(url=self.url + "/rest/v1/site/users", headers=self.headers)
        return response.json()["response"]

    def get_user_details(self, user_id):
        """function"""
        response = requests.get(url=self.url + f"/rest/v1/users/{user_id}", headers=self.headers)
        return response.json()

    def get_multiple_user_details(self):
        """function"""
        ids_list = self.get_user_ids()
        body = {
            "userIds": ids_list
        }
        response = requests.post(url=self.url + "/rest/v1/users/multi", json=body, headers=self.headers)
        return response.json()

    def export_user_data(self, path):
        """function"""
        user_details = self.get_multiple_user_details()
        data = user_details["response"]
        df = pandas.DataFrame(data)
        df.to_csv(path, index=False, encoding="utf-8")

    # FUNCTIONS TO CREATE USERS

    def create_site_user(self, name, email, username, description, home_shortcut):
        """function"""
        new_user = {
            "description": description,
            "email": email,
            "hideHomeSpaceShortcut": home_shortcut,
            "name": name,
            "username": username
        }
        requests.post(url=self.url + "/rest/v1/site/users", json=new_user, headers=self.headers)

    def create_space_user(self, space_id, name, email, username, description, home_shortcut):
        """function"""
        new_user = {
            "description": description,
            "email": email,
            "hideHomeSpaceShortcut": home_shortcut,
            "name": name,
            "username": username
        }
        requests.post(url=self.url + f"/rest/v1/spaces/{space_id}/users", json=new_user, headers=self.headers)

    def create_multiple_space_users(self, path):
        """function"""
        user_data = pandas.read_csv(path)
        users = pandas.DataFrame.to_dict(user_data, orient="records")
        for entry in users:
            name = entry["Name"]
            username = entry["username"]
            email = entry["email"]
            description = entry["description"]
            space_id = entry["space_id"]
            self.create_space_user(space_id=space_id, name=name, email=email, username=username,
                                   description=description, home_shortcut=True)

    def create_multiple_site_users(self, path):
        """function"""
        user_data = pandas.read_csv(path)
        users = pandas.DataFrame.to_dict(user_data, orient="records")
        for entry in users:
            name = entry["Name"]
            username = entry["username"]
            email = entry["email"]
            description = entry["description"]
            self.create_site_user(name=name, email=email, username=username, description=description,
                                  home_shortcut=True)

    # FUNCTIONS TO DELETE USERS

    def delete_user(self, user_id):
        """function"""
        requests.delete(url=self.url + f"/rest/v1/users/{user_id}", headers=self.headers)

    def delete_multiple_users(self, path):
        """function"""
        data = pandas.read_csv(path)
        ids_df = pandas.DataFrame(data)
        ids_list = ids_df["id"].tolist()
        for entry in ids_list:
            self.delete_user(entry)

    # FUNCTIONS TO MODIFY USERS

    def patch_user(self, user_id, value_type, value):
        """function"""
        patch = {
            value_type: value
        }
        requests.patch(url=self.url + f"/rest/v1/users/{user_id}", json=patch, headers=self.headers)

    def patch_multiple_users(self, path, value_type):
        """function"""
        data = pandas.read_csv(path)
        df = pandas.DataFrame(data)
        ids_list = df["id"].tolist()
        for entry in ids_list:
            value = df.at[ids_list.index(entry), value_type]
            self.patch_user(entry, value_type=value_type, value=value)
