# Spotify Insights  

## Objective

The goal of this project is to write a script that fetch tracks from any Spotify playlist, as well as the metadata and the audio features for these tracks. As a test case, we will fetch the tracks and their associated metadata from the following playlist: https://open.spotify.com/playlist/2km2nHDVADmnQMhQRaTOEL?si=fMi8UPf6QLqvhsTn_2mdwA . Since we use spotipy python library for the case, we use python as a programming language to call the API and design the pipeline.

## Libraries and functions

**Spotipy**: lightweight Python library for the Spotify Web API. Spotipy you get full access to all of the music data provided by the Spotify platform.  
**load_dotenv**: is a helper function from the python-dotenv package.It loads environment variables from a ```.env``` file into your Python program so you don’t hard-code secrets like API keys.  
**SpotifyOAuth**: allows your script to log in to Spotify, get an access token, refresh it, and make API calls without you doing the low-level OAuth work.  
**os**:  os is used to read environment variables and run os level commands. here we used it to get secrets safely.  
**csv**: to save ```.csv``` files, write data to -> ```.csv``` file.  
**Path**: a python library to work with file paths.

## Steps

1. create a git repo.
2. create a virtual environment. where you download the packages.
3. create an account in spotify using google account or facebook or other personal email.
4. sign into spotify developers dashboard: https://developer.spotify.com/dashboard .
5. create an app ->  
  <img width="912" height="691" alt="image" src="https://github.com/user-attachments/assets/15f9d657-044f-456d-b539-6783b5b743eb" />
  <img width="917" height="762" alt="image" src="https://github.com/user-attachments/assets/4eddaaca-d1da-43cb-bb35-57a9e34b534d" />

6. create an ```.env``` file to store the client id,secrets and redirect uri and call them -> while function call without hard-coding them.    
7. create a ```.gitignore``` file so as to skip some files like ```.env``` and the downloaded text,so that the secrets aren't exposed and the dataset doesn't make it heavy on repo.    
8. create a src folder to keep the source code : playlist_downloader.py and a data folder as a destination where the dataset will be downloaded. Folder structure:
   
```
 Spotify_Insights/
├── .env
├── src/
│   └── playlist_downloader.py
└── data/
├── requirements.txt
└── .github/
    └── workflows/
        └── spotify.yml

```  
9. automate the process using github actions.
## Code Walk through  

**Function Calls:**

The main function calls the function ```fetch_playlist_to_csv()```, which calls the function ```extract_playlist_id()```. The ```extract_playlist_id()``` function extracts the playlist_id from the url.
Good to mention, we are passing a playlist url link from the main function which was considered as a testcase before hand. ```split()``` function breaks the url into smaller substrings.

```
playlist_id=playlist_url.split("playlist/")[1].split("?")[0]

print(playlist_id)

2km2nHDVADmnQMhQRaTOEL
```

```.split("playlist/")[1]``` : breaks the url into a list of two elements, and selects the later element  -> ```['https://open.spotify.com/', '2km2nHDVADmnQMhQRaTOEL?si=fMi8UPf6QLqvhsTn_2mdwA']```. 
```.split("?")[0]``` function selects everything before question mark with the above logic.  

**Data Path Location:**  

Path location where the .csv data file will be dropped.

```
    base_dir = Path(__file__).resolve().parent.parent
    print(base_dir) ---> C:\Users\Soumya Das\Documents\git_projects\Spotify_Insights
    
    data_dir = base_dir / "data"

    print(data_dir) ----> C:\Users\Soumya Das\Documents\git_projects\Spotify_Insights\data
    
    data_dir.mkdir(exist_ok=True) --->  if the directory doesn't exists

    #the function fetch_playlist_to_csv(playlist_url, "spotify_playlist_data.csv") feeds the output_csv value:  

    output_path = data_dir / output_csv -----> C:\Users\Soumya Das\Documents\git_projects\Spotify_Insights\data\spotify_playlist_data.csv
```

**Authenticating Spotify API:**  

**Fetching Playlist tracks:**  

**Writing to .csv file:**



## Data Description  



## GH Actions

   


