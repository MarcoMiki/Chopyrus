import os
from Chopyrus import Chorus

key = os.getenv("API_KEY")
url = os.getenv("URL")
path_to_desktop = "~/desktop/csv.csv"

chorus = Chorus(key=key, url=url)

# print(chorus.get_multiple_file_ids('56af1aaa-396e-4aa8-9d71-f5cde39b1751'))
print(chorus.get_file_metadata(file_id='5ae23222-3306-4da7-8779-d98b73e39924'))