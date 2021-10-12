import os
from Chopyrus import Chorus

key = os.getenv("API_KEY")
url = os.getenv("URL")
path_to_desktop = "~/desktop/csv.csv"

chorus = Chorus(key=key, url=url)

# test methods here
# print(chorus.get_multiple_files_temp_urls("be7d7677-9b55-48b1-8264-54b921f5e508"))
# print(chorus.export_multiple_files_temp_urls(container_id="be7d7677-9b55-48b1-8264-54b921f5e508", path=path_to_desktop))
print(chorus.get_item_details("dc7c7dd2-1eb9-4546-9a5d-b0b467d4f3aa"))