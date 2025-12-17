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
      └── spotify_playlist_data.csv
├── requirements.txt
└── .github/
    └── workflows/
        └── spotify.yml

```  
9. automate the process using github actions.
## Script Walk through  

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

This entire part is like logging the program into spotify and request playlist, tracks and audio features.
```
sp = spotipy.Spotify(  #creates a spotify client and store it in a variable called sp
        auth_manager=SpotifyClientCredentials(  #use the client credentials method to authenticate.
            client_id=CLIENT_ID,                #who are you?
            client_secret=CLIENT_SECRET         #who its really you?
        )
    )
```
Major takeaways:  
- Spotipy requests an access token from Spotify
- Spotify checks your credentials
- Spotify says: “Okay, you’re allowed”

**Fetching Playlist tracks:**  

```
# ---- Fetch playlist tracks ----
results = sp.playlist_items(playlist_id, additional_types=["track"]) ------> first batch of items from the playlist,
returns 100 tracks, info about pagination and since additional types = track,
we only get SONGS not podcasts or episodes. 

#print(results)

tracks = results["items"] -----> list of tracks and stores them.

#print(tracks)

while results["next"]:  ----> checks whether there is a next page..
    results = sp.next(results) ----> next page of the tracks
    print(results)
    tracks.extend(results["items"]) ----> takes the new tracks from the next page and adds them to the existing list
    print(tracks)

```

**Writing to .csv file:**


```
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "track_name",
                "artists",
                "album",
                "release_date",
                "duration_ms",
                "popularity",
                "track_id"
            ] ----> one single row to the file : the header : write rows where each row is a dictionary
        )
        writer.writeheader() ----> this writes the header row

```
to print the data from dictionary to a structured dataset, which can be later into `.csv` file : 

```
import sys
import csv

writer = csv.DictWriter(
    sys.stdout,
    fieldnames=[
        "track_name",
        "artists",
        "album",
        "release_date",
        "duration_ms",
        "popularity",
        "track_id"
    ]
)

writer.writeheader()

for item in track:
    track = item["track"]
    if not track:
        continue

    writer.writerow({
        "track_name": track["name"],
        "artists": ", ".join(a["name"] for a in track["artists"]),
        "album": track["album"]["name"],
        "release_date": track["album"]["release_date"],
        "duration_ms": track["duration_ms"],
        "popularity": track["popularity"],
        "track_id": track["id"]
    })
```
the output prints the following dataset:

```
track_name,artists,album,release_date,duration_ms,popularity,track_id
Arms Of Heaven,"Talla 2XLC, Sunbeam",Arms Of Heaven,2024-08-09,238285,21,4n86PTgHwwOIrwKkWLSQqf
Trifecta,"Cosmic Gate, Arnej",Trifecta,2024-08-09,234471,39,1v8ey9429Z5ulObgHhYcqF
Half Light,"Ben Gold, Bo Bruce",Half Light,2024-08-09,229622,41,4SFnsEwWLkBS44EJdNOkj9
High Wire,"Roman Messer, ThoBa, Veronica Bravo",High Wire,2024-08-09,187934,16,4bZEQhttzKR5Bpt5KOcC2c
The Love You Give (ASOT 1185) - AK Statement Remix,"Alex Kunnari, Christina Novelli",ASOT 1185 - A State of Trance Episode 1185 [Including Live at Tomorrowland 2024 (Highlights)],2024-08-08,236510,4,2Sdj0ahVSmepLXKOBmwUVP
Slow Motion,"Rene Ablaze, AFTERUS",Slow Motion,2024-08-09,206534,20,2WWhH1fFOwqeZafWatxXZi
Thunderbolt,"RAM, Richard Durand, Digital Culture",Thunderbolt,2024-08-16,216857,20,71nTd2HsRPfulwXkFlRWuM
Daylight,"DJ Dean, Danny Fervent",Daylight,2024-08-02,225230,0,4KLteihFI7YJZCzLJnXmNo
Count On Me (ASOT 1186),"Aly & Fila, Philippe El Sisi, Omar Sherif, Jaren","ASOT 1186 - A State of Trance Episode 1186 [Including A State of Trance, Ibiza 2024 (Mix 3: Who's Afraid of 138?!)]",2024-08-15,273920,13,34vvMTbti2O0fR9mX6Ct9A
Say Something,"Ciaran McAuley, Christina Novelli",Say Something,2024-08-16,190964,31,0ryaHEkXnKDLNdnRDrvtUk
Thinking of You,Solarstone,Thinking of You,2024-08-07,202714,14,4fGYcqTM8aBhtXU7yIxtcO
Photographs,Kyau & Albert,Photographs,2024-08-06,161483,12,7wny4eDKuCN4Ynn6BvAOAW
Leonie - Torsten Stenzel Remix,"Dj T.H., Torsten Stenzel",Leonie (Torsten Stenzel Remix),2024-08-09,179000,12,3FPHJAFHl0weYNrRnqJA41
Zorn,Niconé,"Triation, Vol. IX",2024-08-09,403278,14,1S5GUzPQZeL1yvRhya36j9
Echoes,"Einmusik, Jordan Arts",Echoes,2024-08-16,295283,22,064zQysCLTlbcdrngwbI6i
Alive,"Driftmoon, Sarah Howells",Alive,2024-08-16,227363,11,3jnkgleUmAKwIR9k4m9G8R
Don't Stop,Robert Babicz,Kelch 14,2024-08-09,296689,2,4hXapk3xMtF1xub69xTBAv
Future Memories,"Estiva, Lake Avalon",Future Memories,2024-08-09,203902,32,5bD2vf35NLtUphipbcxdFL
The Realm of Imagination,"Push, Rebel Boy",The Realm of Imagination,2024-08-09,270666,16,7BxDrmXVB5XQf0pgNNIM1D
Happening - Dirty Doering Remix Edit,"Pretty Pink, Dirty Doering",Happening (Dirty Doering Remix Edit),2024-08-16,264239,20,23ND4N8q53VYT0smVmlavS
Nightflight,YORK,Nightflight,2024-08-16,198857,0,4UUSilN9d6AFhmy26ff6KC
Esperanza,"Mauro Picotto, Frankyeffe",Esperanza,2024-08-09,222857,17,6nLdrOmfkhOvn2BxRBF6lz
Adventure Awaits,"Roger Shah, Yelow",Adventure Awaits,2024-08-16,217391,31,0T79ekqISgzmMHr52H46Wz
Manray (GDJB Weekly Drive 33),"Markus Schulz, Dakota",Global DJ Broadcast Weekly Drive 33,2024-08-15,227343,4,19wvvVPtC7PRYJtwUY7r26
My Head,"RAVEKINGS, Diabllo",My Head,2024-08-09,159807,37,7j22od1gIbsynOKNf8kJP9
Love Seeking - Âme Remix Edit,"Mind Against, Âme",Love Seeking - Âme Remix,2024-08-09,249466,19,5cMC0L8fGfM8PwCjKQd14V
Sunlight,"Eximinds, Eldream",Sunlight,2024-08-09,290639,3,4yvG4pwLLyyvkBchS7RaYN
Devotion - Cold Blue Remix,"John O'Callaghan, Alex Holmes, Cold Blue",Devotion (Cold Blue Remix),2024-08-16,252857,13,64UMLSAaJnMCw0M74nrWev
Final Fight,Cosmic Boys,Final Fight,2024-08-09,174705,25,6VgTjGZqEKbcO2hL1XecvU
Escape,"Van Der Karsten, Airwalk3r",Escape,2024-08-16,166956,36,4S2hhb5EKBmlBU7cFigCJS
Bells of Kakariko,Oliver Koletzki,Bells of Kakariko,2024-08-16,409112,20,70wp7eGnmV4mCTg1f6u9n6
Guide Me Home,Laura van Dam,Guide Me Home,2024-07-26,210714,25,78VAm5dA0hs5sl77KOEMv8
Subjekt,"Allen Watts, AWaken",Subjekt,2024-08-16,188449,14,1pFarz73OQPxi4sP9fpbBy
```


## Data Description  



## GH Actions

   


