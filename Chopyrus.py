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
        """returns the IDs of all site users"""
        response = requests.get(url=self.url + "/rest/v1/site/users", headers=self.headers)
        return response.json()["response"]

    def get_user_details(self, user_id):
        """given a user id, returns details for that user"""
        response = requests.get(url=self.url + f"/rest/v1/users/{user_id}", headers=self.headers)
        return response.json()

    def get_multiple_user_details(self):
        """given a list of ids, returns details for them"""
        ids_list = self.get_user_ids()
        body = {
            "userIds": ids_list
        }
        response = requests.post(url=self.url + "/rest/v1/users/multi", json=body, headers=self.headers)
        return response.json()

    def export_user_data(self, path):
        """given a path to export to, downloads a .csv file with details for all site's users"""
        user_details = self.get_multiple_user_details()
        data = user_details["response"]
        df = pandas.DataFrame(data)
        df.to_csv(path, index=False, encoding="utf-8")

    # FUNCTIONS TO CREATE USERS

    def create_site_user(self, name, email, username, description, home_shortcut):
        """given name, email, username, description and True/False on whether the home shortcut should be displayed,
        it creates a user"""
        new_user = {
            "description": description,
            "email": email,
            "hideHomeSpaceShortcut": home_shortcut,
            "name": name,
            "username": username
        }
        requests.post(url=self.url + "/rest/v1/site/users", json=new_user, headers=self.headers)

    def create_space_user(self, space_id, name, email, username, description, home_shortcut):
        """given name, email, username, space ID, description and True/False on whether the home shortcut should be
        displayed, it creates a user in a specific space"""
        new_user = {
            "description": description,
            "email": email,
            "hideHomeSpaceShortcut": home_shortcut,
            "name": name,
            "username": username
        }
        requests.post(url=self.url + f"/rest/v1/spaces/{space_id}/users", json=new_user, headers=self.headers)

    def create_multiple_space_users(self, path):
        """given the path to a .csv spreadsheet, it creates multiple users in a specific space from the details within
        it. The spreadsheet needs to contain the following headers: name, username, email, description, space_id,
        home_shortcut (boolean value)"""
        user_data = pandas.read_csv(path)
        users = pandas.DataFrame.to_dict(user_data, orient="records")
        for entry in users:
            name = entry["Name"]
            username = entry["username"]
            email = entry["email"]
            description = entry["description"]
            home_shortcut= entry["home_shortcut"]
            space_id = entry["space_id"]
            self.create_space_user(space_id=space_id, name=name, email=email, username=username,
                                   description=description, home_shortcut=home_shortcut)

    def create_multiple_site_users(self, path):
        """given the path to a .csv spreadsheet, it creates multiple users from the details within it. The spreadsheet
        needs to contain the following headers: name, username, email, description, home_shortcut (boolean value)"""
        user_data = pandas.read_csv(path)
        users = pandas.DataFrame.to_dict(user_data, orient="records")
        for entry in users:
            name = entry["Name"]
            username = entry["username"]
            email = entry["email"]
            description = entry["description"]
            home_shortcut = entry["home_shortcut"]
            self.create_site_user(name=name, email=email, username=username, description=description,
                                  home_shortcut=home_shortcut)

    # FUNCTIONS TO DELETE USERS

    def delete_user(self, user_id):
        """given a user id, it deletes that user"""
        requests.delete(url=self.url + f"/rest/v1/users/{user_id}", headers=self.headers)

    def delete_multiple_users(self, path):
        """given a path to a .csv file containing multiple user ids, it deletes those users. The column header name for
        the id values needs to be id"""
        data = pandas.read_csv(path)
        ids_df = pandas.DataFrame(data)
        ids_list = ids_df["id"].tolist()
        for entry in ids_list:
            self.delete_user(entry)

    # FUNCTIONS TO MODIFY USERS

    def patch_user(self, user_id, value_type, value):
        """given a user id, value type and a new value it modifies that value for that user. Value types available are
        name, email or description"""
        patch = {
            value_type: value
        }
        requests.patch(url=self.url + f"/rest/v1/users/{user_id}", json=patch, headers=self.headers)

    def patch_multiple_users(self, path, value_type):
        """given a value type and a .csv file containing user ids and new values, it modifies those values for those
        users. Value types available are name, email or description"""
        data = pandas.read_csv(path)
        df = pandas.DataFrame(data)
        ids_list = df["id"].tolist()
        for entry in ids_list:
            value = df.at[ids_list.index(entry), value_type]
            self.patch_user(entry, value_type=value_type, value=value)
