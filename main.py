import os
from Chopyrus import Chorus

key = os.getenv("API_KEY")
url = os.getenv("URL")
path_to_desktop = "~/desktop/csv.csv"

chorus = Chorus(key=key, url=url)

# test methods here

print(chorus.get_file_temp_url(file_id="66285384287"))