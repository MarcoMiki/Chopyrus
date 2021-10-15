import requests
import pandas
import urllib.parse

class Chorus:
    def __init__(self, key, url):
        '''Authenticates to a Chorus site. Requires a Chorus URL and an API key'''
        self.url = url
        self.login_response = requests.post(url=url + "/rest/v1/auth/loginWithKey", json={"apiKey": key})
        self.sessionID = self.login_response.json()["sessionId"]
        self.chorus_headers = {"X-Chorus-Session": self.sessionID}

    # LOG OUT
    def log_out(self):
        """logs out from current session"""
        requests.post(url=self.url + "/rest/v1/auth/logout", headers=self.chorus_headers)

    #  SEARCH

    def make_general_global_search(self, query):
        """Make a search from a query. This uses the general global search. Returns a list of file ids"""
        query = urllib.parse.quote_plus(query)
        response = requests.get(url=self.url + f"/rest/v1/search?query={query}", headers=self.chorus_headers)
        return response.json()["response"]

    # GET USER DATA AND EXPORT IT

    def get_user_ids(self):
        """returns the IDs of all site users"""
        response = requests.get(url=self.url + "/rest/v1/site/users", headers=self.chorus_headers)
        return response.json()["response"]

    def get_user_details(self, user_id):
        """given a user id, returns details for that user"""
        response = requests.get(url=self.url + f"/rest/v1/users/{user_id}", headers=self.chorus_headers)
        return response.json()["response"]

    def get_multiple_user_details(self):
        """given a list of ids, returns details for them"""
        ids_list = self.get_user_ids()
        body = {
            "userIds": ids_list
        }
        response = requests.post(url=self.url + "/rest/v1/users/multi", json=body, headers=self.chorus_headers)
        return response.json()

    def export_user_data(self, path):
        """given a path to export to, downloads a .csv file with details for all site's users"""
        data = self.get_multiple_user_details()
        df = pandas.DataFrame(data)
        df.to_csv(path, index=False, encoding="utf-8")

    # CREATE USERS

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
        requests.post(url=self.url + "/rest/v1/site/users", json=new_user, headers=self.chorus_headers)

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
        requests.post(url=self.url + f"/rest/v1/spaces/{space_id}/users", json=new_user, headers=self.chorus_headers)

    def create_multiple_space_users(self, path):
        """given the path to a .csv spreadsheet, it creates multiple users in a specific space from the details within
        it. The spreadsheet needs to contain the following headers: name, username, email, description, space_id,
        home_shortcut"""
        user_data = pandas.read_csv(path)
        users = pandas.DataFrame.to_dict(user_data, orient="records")
        for entry in users:
            name = entry["Name"]
            username = entry["username"]
            email = entry["email"]
            description = entry["description"]
            home_shortcut = entry["home_shortcut"]
            space_id = entry["space_id"]
            self.create_space_user(space_id=space_id, name=name, email=email, username=username,
                                   description=description, home_shortcut=home_shortcut)

    def create_multiple_site_users(self, path):
        """given the path to a .csv spreadsheet, it creates multiple users from the details within it. The spreadsheet
        needs to contain the following headers: name, username, email, description, home_shortcut"""
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

    # DELETE USERS

    def delete_user(self, user_id):
        """given a user id, it deletes that user"""
        requests.delete(url=self.url + f"/rest/v1/users/{user_id}", headers=self.chorus_headers)

    def delete_multiple_users(self, path):
        """given a path to a .csv file containing multiple user ids, it deletes those users. The column header name for
        the id values needs to be id"""
        data = pandas.read_csv(path)
        ids_df = pandas.DataFrame(data)
        ids_list = ids_df["id"].tolist()
        for entry in ids_list:
            self.delete_user(entry)

    # MODIFY USER DETAILS

    def patch_user(self, user_id, value_type, value):
        """given a user id, value type and a new value it modifies that value for that user. Value types available are
        name, email or description"""
        patch = {
            value_type: value
        }
        requests.patch(url=self.url + f"/rest/v1/users/{user_id}", json=patch, headers=self.chorus_headers)

    def patch_multiple_users(self, path, value_type):
        """given a value type and a .csv file containing user ids and new values, it modifies those values for those
        users. Value types available are name, email or description. the new values have to be in a column whose
        header is the name of the value type"""
        data = pandas.read_csv(path)
        df = pandas.DataFrame(data)
        ids_list = df["id"].tolist()
        for entry in ids_list:
            value = df.at[ids_list.index(entry), value_type]
            self.patch_user(entry, value_type=value_type, value=value)

    # GET FILES DETAILS
    def get_multiple_file_ids(self, container_id):
        """given a container id it returns a list of all the ids for the files in it"""
        response = requests.get(url=self.url + f"/rest/v1/folders/{container_id}/files", headers=self.chorus_headers)
        folder_files_details = response.json()["response"]
        ids = [file["id"] for file in folder_files_details]
        return ids

    def get_file_details(self, file_id):
        """given a file id it returns its details"""
        response = requests.get(url=self.url + f"/rest/v1/files/{file_id}", headers=self.chorus_headers)
        return response.json()

    def get_file_name(self, file_id):
        """given a file id it returns the file name for that file"""
        data = self.get_file_details(file_id)
        return data["filename"]

    def get_multiple_file_details(self, container_id):
        """given a container id it returns details for all the files within, in a list"""
        files = self.get_multiple_file_ids(container_id)
        details_list = [self.get_file_details(file) for file in files]
        return details_list

    def get_item_details(self, item_id):
        """given an item id it returns its details, works on containers as well as files. It takes the GUID for folders
        but won't work with the file id available in the GUI. You will need the ID received from other api calls for
        files."""
        response = requests.get(url=self.url + f"/rest/v1/content/{item_id}", headers=self.chorus_headers)
        return response.json()["details"]

    # GET FILE DIRECT URLS

    def get_file_temp_url(self, file_id, **kwargs):
        """"given a file it creates a temporary Direct Url and returns it. It needs a file_id argument as well as any
        of these other optional arguments: blur, crop.width, crop.height, crop.x, crop.y, download, dpi, filename, fit,
        format, height, width, page, quality, rotate"""
        params = {
            f"settings.{attribute}": kwargs[attribute] for attribute in kwargs
        }
        response = requests.get(url=self.url + f"/rest/v1/files/{file_id}/temporaryDirectUrl",
                                headers=self.chorus_headers, params=params)
        return response.json()["response"]

    def get_file_url(self, file_id, **kwargs):
        """"given a file id it creates a  Direct Url and returns it.  It needs a file_id argument as well as any
        of these other optional arguments: blur, crop.width, crop.height, crop.x, crop.y, download, dpi, filename, fit,
        format, height, width, page, quality, rotate. Only works with the GUID file id"""
        params = {
            f"settings.{attribute}": kwargs[attribute] for attribute in kwargs
        }
        response = requests.get(url=self.url + f"/rest/v1/files/{file_id}/directUrl", headers=self.chorus_headers,
                                params=params)
        return response.json()["response"]

    def get_multiple_files_temp_urls(self, container_id):
        """given a container id it returns a dictionary of temporary direct URLs for these files and their file names"""
        files = self.get_multiple_file_ids(container_id)
        file_urls = {self.get_file_name(file): self.get_file_temp_url(file) for file in files}
        return file_urls

    def get_multiple_files_urls(self, container_id):
        """given a container id it returns a dictionary of temporary direct URLs for these files and their file names"""
        files = self.get_multiple_file_ids(container_id)
        file_urls = {self.get_file_name(file): self.get_file_url(file) for file in files}
        return file_urls

    def export_multiple_files_temp_urls(self, container_id, path):
        """given a container id and a path it downloads a spreadsheet with file names and temporary direct urls for
        these files"""
        file_urls = self.get_multiple_files_temp_urls(container_id)
        df = pandas.DataFrame(list(file_urls.items()), columns = ['id', 'link'], index=None)
        df.to_csv(path, index=False, encoding="utf-8")

    def export_multiple_files_urls(self, container_id, path):
        """given a container id and a path it downloads a spreadsheet with file names and direct urls for these files"""
        file_urls = self.get_multiple_files_urls(container_id)
        df = pandas.DataFrame(list(file_urls.items()), columns = ['id', 'link'], index=None)
        df.to_csv(path, index=False, encoding="utf-8")

    # GET AND MODIFY METADATA

    def get_all_file_metadata(self, file_id):
        """given a file id, it returns metadata for all fields, including the ones that are empty"""
        response = requests.get(url=self.url + f"/rest/v1/files/{file_id}/metadata",
                                headers=self.chorus_headers)
        return response.json()

    def get_item_metadata_fields(self, item_id):
        """given a file or container id it returns its metadata fields. It takes the GUID for folders but won't work
        with the file id available in the GUI. You will need the ID received from other api calls for files."""
        response = requests.get(url=self.url + f"/rest/v1/content/{item_id}/metadataFields",
                                headers=self.chorus_headers)
        return response.json()["response"]

    def get_item_metadata_value(self, item_id, field):
        """given a file or container's id and metadata field, it returns the value for that field.It takes the GUID for
        folders but won't work with the file id available in the GUI. You will need the ID received from other api calls
        for files."""
        response = requests.get(url=self.url + f"/rest/v1/content/{item_id}/metadata/{field}",
                                headers=self.chorus_headers)
        return response.json()["text"]["values"]

    def get_item_metadata(self, file_id):
        """given a file id it returns all metadata values for fields that are not empty. It takes the GUID for folders
        but won't work with the file id available in the GUI. You will need the ID received from other api calls for
        files."""
        fields = self.get_item_metadata_fields(file_id)
        metadata = {field: self.get_item_metadata_value(file_id, field) for field in fields
                    if len(self.get_item_metadata_value(file_id, field)) != 0}
        return metadata

    def update_metadata_on_item(self, item_id, field, value):
        """updates metadata value for a field on a file or container. Replaces the value on single-value fields, appends
         it on multi-value fields. It takes the GUID for folders but won't work with the file id available in the GUI.
         You will need the ID received from other api calls for files. Use a list even if you are adding a single
         value"""
        payload = {
                "text": {
                    "values": value
                     }
                }

        response = requests.patch(url=self.url + f"/rest/v1/content/{item_id}/metadata/{field}", json=payload,
                                  headers=self.chorus_headers)
        return response.json()

    def replace_metadata_on_item(self, item_id, field, value):
        """replace metadata value for a field on a file or container. It takes the GUID for folders but won't work with
        the file id available in the GUI. You will need the ID received from other api calls for files. To clear all
        values for a file and field use this method with an empty value. Use a list even if you are adding a single
         value"""
        payload = {
            "text": {
                "values": value
            }
        }
        response = requests.put(url=self.url + f"/rest/v1/content/{item_id}/metadata/{field}", json=payload,
                                headers=self.chorus_headers)
        return response.json()

    def delete_metadata_on_item(self, item_id, field, values):
        """delete metadata value for a field on a file or container. It takes the GUID for folders but won't work with
        the file id available in the GUI. You will need the ID received from other api calls for files. This only works
        with text type values"""
        payload = ""
        for value in values:
            value = urllib.parse.quote_plus(value)
            payload = payload + f"details.text.values={value}&"
        response = requests.delete(url=self.url + f"/rest/v1/content/{item_id}/metadata/{field}?{payload}",
                                   headers=self.chorus_headers)
        print(response.json())

    def get_site_vocabulary(self, field):
        """given a field, it returns the site vocabulary for that field"""
        response = requests.get(url=self.url + f"/rest/v1/site/metadata/{field}/vocab", headers=self.chorus_headers)
        return response.json()["values"]

    def  get_space_vocabulary(self, field, space_id):
        """given a field and a space id, it returns that space's vocabulary for that field"""
        response = requests.get(url=self.url + f"/rest/v1/spaces/{space_id}/metadata/{field}/vocab",
                                headers=self.chorus_headers)
        return response.json()["values"]

    def update_site_vocabulary(self, field, value):
        """add a list of new values to the site vocabulary for a given field. Use a list even if you are only sending a
        single value"""
        payload = {
            "mode": "REPLACE",
            "tagName": field,
            "values": value
        }
        response = requests.patch(url=self.url + f"/rest/v1/site/metadata/{field}/vocab", json=payload,
                                  headers=self.chorus_headers)
        print(response)

    def replace_site_vocabulary(self, field, value):
        """replace the site vocabulary for a given field with the given value or values. Use a list even if you are
        only sending a single value"""
        payload = {
                "mode": "REPLACE",
                "tagName": field,
                "values": value
            }
        response = requests.put(url=self.url + f"/rest/v1/site/metadata/{field}/vocab", json=payload,
                                headers=self.chorus_headers)
        print(response)

    def update_space_vocabulary(self, field, space_id, value):
        """add a list of new values to the space vocabulary for a given field and space. Use a list even if you are
        only sending a single value"""
        payload = {
                "mode": "REPLACE",
                "tagName": field,
                "values": value
            }
        response = requests.patch(url=self.url + f"/rest/v1/spaces/{space_id}/metadata/{field}/vocab", json=payload,
                                  headers=self.chorus_headers)
        print(response)

    def replace_space_vocabulary(self, field, space_id, value):
        """replace the space vocabulary for a given field and space with a given list of values. Use a list even if you
        are only sending a single value"""
        payload = {
            "mode": "REPLACE",
            "tagName": field,
            "values": value
        }
        response = requests.put(url=self.url + f"/rest/v1/spaces/{space_id}/metadata/{field}/vocab", json=payload,
                                  headers=self.chorus_headers)
        print(response)

    def export_site_vocabulary(self, path, field):
        """given a field and a path, export a .csv file with the site vocabulary for that field"""
        data = self.get_site_vocabulary(field=field)
        df = pandas.DataFrame({field:data})
        df.to_csv(path, index=False, encoding="utf-8")

    def export_space_vocabulary(self, path, field, space_id):
        """given a metadata field key name, a space id and path, it exports that space's vocabulary for that field"""
        data = self.get_space_vocabulary(field=field, space_id=space_id)
        df = pandas.DataFrame({field: data})
        df.to_csv(path, index=False, encoding="utf-8")

    def update_site_vocabulary_from_csv(self, path, field):
        """given a metadata field key name and a path, it adds to the site's vocabulary for that field using the rows in
         the spreadsheet. The header of the column with the values needs to be the key name of the metadata field"""
        data = pandas.read_csv(path)
        df = pandas.DataFrame(data)
        values = df[field].tolist()
        self.update_site_vocabulary(field=field, value=values)

    def replace_site_vocabulary_from_csv(self, path, field):
        """given a metadata field key name and path, it replaces the site's vocabulary for that field using the rows
         in the spreadsheet. The header of the column with the values needs to be the key name of the metadata field"""
        data = pandas.read_csv(path)
        df = pandas.DataFrame(data)
        values = df[field].tolist()
        self.replace_site_vocabulary(field=field, value=values)

    def update_space_vocabulary_from_csv(self, path, field, space_id):
        """given a metadata field key name, a space id and a path, it adds to that space's vocabulary for that field
        using the rows in the spreadsheet. The header of the column with the values needs to be the key name of the
        metadata field"""
        data = pandas.read_csv(path)
        df = pandas.DataFrame(data)
        values = df[field].tolist()
        self.update_space_vocabulary(field=field, value=values, space_id=space_id)

    def replace_space_vocabulary_from_csv(self, path, field, space_id):
        """given a metadata field key name, a space id and a path, it replaces that space's vocabulary for that field
        using the rows in the spreadsheet. The header of the column with the values needs to be the key name of the
        metadata field"""
        data = pandas.read_csv(path)
        df = pandas.DataFrame(data)
        values = df[field].tolist()
        self.replace_space_vocabulary(field=field, value=values, space_id=space_id)

