# Chopyrus
Chorus library for the ThirdLight Chorus API. It requires an active Chorus subscription and the API module to be used.

Not all API methods are included here, but enough to help most use cases. 

# Usage

Initialising the class requires an API key and a site URL which you can retrieve from your Chorus site. Note that the API key should be generated from the "admin" menu and will not be specific for a particular user. 

This means that all methods in this library relate to the site itself. You won't find methods to get a specific user's contexts or perform actions as that user.

Initialising the class will also log you in to the Chorus site passed as an argument for it. Note that a valid API key is also required, and depending on what API key is used and whether it was generated for the site, a space or a user you will get different results with the various methods. 

Using a specific API key basically logs you in as that entity, so you may want to use a site API key most times if possible as that would be the same as logging in as the first admin user in alphabetical order (and you would expect site admins to have access to most files and spaces). One reason why a method could return an error or less results than expected can be that you logged in with a key that is not authorised to perform the action you want to perform, i.e. you are trying to modify a site metadata vocabulary but you are not logged in with a site api key.

Note: you can find ids for folders, spaces, collections and smart collections (collectively referred as "container" here) within the Chorus GUI. When a method references the file id you can use the file reference that you can find in Chorus too. When a method references the item id you will have to use the id provided by the relevant API methods. User ids can only be obtained via API methods.


# Methods

**LOG OUT**

**log_out**

Logs out from current session.



**SEARCH**

**make_general_global_search(query)**


Makes a general global search from a query. Takes a string and returns a list of file ids.




**GET USER DATA AND EXPORT IT**

**get_user_ids**


Returns a list with the IDs of all the users for the site.


**get_user_details(user_id)**


Takes a user id and returns details for that user.


**get_multiple_user_details**


Takes a list of user ids and returns their details.

**export_user_data(path)**
Takes a download path to export to and, downloads a .csv file with details for all site's users. The path should include the name of the file, for example ".../folder/file.csv" is a valid path, but "...folder/" is not.


**CREATE USERS**

**create_site_user(name, email, username, description, home_shortcut)**

Takes a few details and creates a user with them. Needs: name, email, username, description and a boolean True/False value on whether the home shortcut should be displayed for this user. The description value can be an empty string.

**create_space_user(space_id, name, email, username, description, home_shortcut):**


Takes a few details and creates a user with them. Needs: name, email, username, space id, description and a boolean True/False value on whether the home shortcut should be displayed for this user. The description value can be an empty string. 

**create_multiple_space_users(path)**

Takes the path to a .csv spreadsheet and it creates multiple users in a specific space from the details within it. The spreadsheet needs to contain the following headers: name, username, email, description, space_id, home_shortcut. home_shortcut is a boolean True/False value on whether the home shortcut should be displayed for this user, all the other values shold be strings. The users will have the space corresponding to the space id entered set as their home space and will be automatically added to the "Members" role.

**create_multiple_site_users(path)**
Takes the path to a .csv spreadsheet and it creates multiple users from the details within it. The spreadsheet needs to contain the following headers: name, username, email, description, home_shortcut (True/False). Home_shortcut is a boolean True/False value on whether the home shortcut should be displayed for this user, all the other values shold be strings. Note that no user will be assigned a home space.


**DELETE USERS**

**delete_user(user_id)**
It deletes the user corresponding to the user id provided.

**delete_multiple_users(path)**
Takes the path to a .csv file containing multiple user ids and it deletes those users. The column header for the id values needs to be "id".


**MODIFY USERDETAILS**

**patch_user(user_id, value_type, value)**
Takes a user id, value type and a new value and modifies that value for that user. Value types available are name, email or description and should all be strings.

**patch_multiple_users(path, value_type)**

Takes a value type, a .csv file containing user ids and new values and it modifies those values for those users. Value types available are name, email or description. the column header for the values needs to be the name of the value type.


**GET FILES DETAILS**

**get_multiple_file_ids(container_id)**

Takes a container id and returns a list of all the ids for the files in it

**get_file_details(file_id)**
Takes a file id and returns its details.

**get_file_name(file_id)**
Takes a file id and returns the file name for that file.

**get_multiple_file_details(container_id)**
Takes a container id and returns details for all the files within, in a list.

**get_item_details(item_id)**
Takes an item id and returns its details, works on containers as well as files. It takes the GUID for folders but won't work with the file id available in the GUI. You will need the ID received from other api calls for files.


**GET FILE DIRECT URLS**

**get_file_temp_url(file_id, **kwargs)**
Takes a file id, creates a temporary Direct Url and returns it. It needs a file_id argument as well as any of these other optional arguments: blur, crop.width, crop.height, crop.x, crop.y, download, dpi, filename, fit, format, height, width, page, quality, rotate. See the Chorus API official documentation for explanation on what all these arguments do. Temporary Direct Urls have a short duration and are useful for applications that only need to download these files or send them somewhere else.

**get_file_url(file_id, **kwargs)**
Takes a file id, creates a permanent Direct Url and returns it. It needs a file_id argument as well as any of these other optional arguments: blur, crop.width, crop.height, crop.x, crop.y, download, dpi, filename, fit, format, height, width, page, quality, rotate. See the Chorus API official documentation for explanation on what all these arguments do. Direct Urls work until manually revoked from within Chorus or with an API call.

**get_multiple_files_temp_urls(container_id)**
Takes a container id and returns a dictionary with temporary direct URLs for these files and their file names as values and keys.Temporary Direct Urls have a short duration and are useful for applications that only need to download these files or send them somewhere else.

**get_multiple_files_urls(container_id)**
Takes a container id and returns a dictionary with direct URLs for these files and their file names as values and keys. Direct Urls work until manually revoked from within Chorus or with an API call.

**export_multiple_files_temp_urls(container_id, path)**
Takes a container id and a path and downloads a spreadsheet containing file names and temporary direct urls for these files. Temporary Direct Urls have a short duration and are useful for applications that only need to download these files or send them somewhere else.

export_multiple_files_urls(self, container_id, path):
Takes a container id and a path and downloads a spreadsheet containing file names and direct urls for these files. Direct Urls work until manually revoked from within Chorus or with an API call.


**GET AND MODIFY METADATA**

**get_all_file_metadata(file_id)**
Takes a file id and returns metadata for all fields, including the ones that are empty.

**get_item_metadata_fields(item_id)**
Takes a file or container id and returns its metadata fields. It takes the GUID for folders but won't work with the file id available in the GUI. You will need the ID received from other api calls for files.

**get_item_metadata_value(item_id, field)**
Takes a file or container's id and metadata field and returns the value for that field. It takes the GUID for folders but won't work with the file id available in the GUI. You will need the ID received from other api calls for files.

**get_item_metadata(self, file_id)**
Takes a file id and returns all metadata values for fields that are not empty. It takes the GUID for folders but won't work with the file id available in the GUI. You will need the ID received from other api calls for files.

**update_metadata_on_item(item_id, field, value)**
Takes a file or container's id and updates the metadata values for that field for it. It replaces the value on single-value fields and appends it on multi-value fields. It takes the GUID for folders but won't work with the file id available in the GUI. You will need the ID received from other api calls for files. Use a list even if you are adding a single value.

**replace_metadata_on_item(item_id, field, value)**
Takes a file or container's id and replaces the metadata values for that field for it. It takes the GUID for folders but won't work with the file id available in the GUI. You will need the ID received from other api calls for files. To clear all values for a file and field use this method with an empty value. Use a list even if you are adding a single value.

**delete_metadata_on_item(item_id, field, values)**
Takes a file or container's id and deletes onr or more metadata values for that field for it. It takes the GUID for folders but won't work with the file id available in the GUI. You will need the ID received from other api calls for files. This only works with text type values.

**get_site_vocabulary(field)**
Takes a a metadata field key name and returns the site vocabulary for that field.

**get_space_vocabulary(field, space_id)**
Takes a metadata field key name and a space id and returns that space's vocabulary for that field.

**update_site_vocabulary(field, value)**
Takes a list of values and adds them to the site vocabulary for a given field. Use a list even if you are only sending a single value.

**replace_site_vocabulary(field, value)**
Takes a list of values and replaces the site vocabulary for a given field with it. Use a list even if you are only sending a single value.

**update_space_vocabulary(field, space_id, value)**
Takes a list of values and adds them to the space vocabulary for a given field. Use a list even if you are only sending a single value.

**replace_space_vocabulary(field, space_id, value)**
Takes a list of values and replaces the site vocabulary for a given field with it. Use a list even if you are only sending a single value.

**export_site_vocabulary(path, field)**
Takes a metadata field key name and a download path and export a .csv file with the site vocabulary for that field there. The path should include the name of the file, for example ".../folder/file.csv" is a valid path, but "...folder/" is not.

**export_space_vocabulary(path, field, space_id)**
Takes a metadata field key name and a download path and export a .csv file with the space vocabulary for that field there. The path should include the name of the file, for example ".../folder/file.csv" is a valid path, but "...folder/" is not.

**update_site_vocabulary_from_csv(path, field)**
Takes a metadata field key name and a file path to a .csv file with new values to import and adds these values to the site vocabulary for that field. The path should include the name of the file, for example ".../folder/file.csv" is a valid path, but "...folder/" is not. The column header for the values needs to be the metadata field key name.

**replace_site_vocabulary_from_csv(path, field)**
Takes a metadata field key name and a file path to a .csv file with new values to import and uses these values to replace the site vocabulary for that field. The path should include the name of the file, for example ".../folder/file.csv" is a valid path, but "...folder/" is not. The column header for the values needs to be the metadata field key name.

**update_space_vocabulary_from_csv(path, field, space_id)**
Takes a metadata field key name and a file path to a .csv file with new values to import and adds these values to the space vocabulary for that field. The path should include the name of the file, for example ".../folder/file.csv" is a valid path, but "...folder/" is not. The column header for the values needs to be the metadata field key name.

**replace_space_vocabulary_from_csv(path, field, space_id)**
Takes a metadata field key name and a file path to a .csv file with new values to import and uses these values to replace the site vocabulary for that field. The path should include the name of the file, for example ".../folder/file.csv" is a valid path, but "...folder/" is not. The column header for the values needs to be the metadata field key name.
