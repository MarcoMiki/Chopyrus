import os
from Chopyrus import Chorus

key = os.getenv("API_KEY")
url = os.getenv("URL")
path_to_desktop = "~/desktop/csv.csv"

chorus = Chorus(key=key, url=url)

# test methods here

# print(chorus.get_multiple_file_ids("be7d7677-9b55-48b1-8264-54b921f5e508"))
# print(chorus.get_file_url("47deb116-2172-4e89-8175-5a967bcfeb7d"))
# print(chorus.get_file_name("47deb116-2172-4e89-8175-5a967bcfeb7d"))
# chorus.export_multiple_files_temp_urls(container_id="be7d7677-9b55-48b1-8264-54b921f5e508", path=path_to_desktop)