import gitlab # sudo apt-get install python3-gitlab
import os
import requests

i=0
files = []
return_value = [] # contain all java files which contain an element or more from pgmlist
pgmlist = ['PGNAME1', 'PGNAME2', 'PGNAME3']

gl = gitlab.Gitlab('https://xxxxxxxxxxxxxx.com', oauth_token='xxxxxxxxxxxxx')
# token created with proper rights (API, read, etc.)
# see https://xxxxxxxxxx.com/-/profile/personal_access_tokens
gl.auth()

# list all projects
projects = gl.projects.list(all=True)

for project in projects:
    print(project.name)
    if(project.empty_repo == False): # no need to check an empty / an archived project
        files = project.repository_tree(recursive=True, archived=False)
        for file in files:
            if(file["type"] == 'blob' and ('.java' in file["name"])) :
                print("  - " + file["name"])
                f = project.files.get(file_path=file['path'], ref=project.default_branch) # if ref=Main, we may encounter 404 error
                file_content = f.decode()
               
                for pgm in pgmlist:
                    if pgm in str(file_content): 
                        return_value.append({
                            "project": project.name,
                            "file": file['path'],
                            "pgm": pgm
                        })
                        print(return_value[i])
                        i+=1
    print("\n")
print('END')
