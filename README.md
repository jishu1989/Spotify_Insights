# Spotify Insights  

## Objective

The goal of this project is to write a script that fetch tracks from any Spotify playlist, as well as the metadata and the audio features for these tracks. As a test case, we will fetch the tracks and their associated metadata from the following playlist: https://open.spotify.com/playlist/2km2nHDVADmnQMhQRaTOEL?si=fMi8UPf6QLqvhsTn_2mdwA . Since we use spotipy python library for the case, we use python as a programming language to call the API and design the pipeline.

## Libraries and functions

**Spotipy**: lightweight Python library for the Spotify Web API. Spotipy you get full access to all of the music data provided by the Spotify platform.  
**load_dotenv**: is a helper function from the python-dotenv package.It loads environment variables from a ```.env``` file into your Python program so you don’t hard-code secrets like API keys.  
**SpotifyOAuth**: allows your script to log in to Spotify, get an access token, refresh it, and make API calls without you doing the low-level OAuth work.  
**os**:  
**csv**:

## Steps:

1. create a git repo.
2. create a virtual environment. where you download the packages.
3. create an account in spotify using google account or facebook or other personal email.
4. sign into spotify developers dashboard: https://developer.spotify.com/dashboard
5. create an app ->  
   <img width="912" height="691" alt="image" src="https://github.com/user-attachments/assets/15f9d657-044f-456d-b539-6783b5b743eb" />
   <img width="917" height="762" alt="image" src="https://github.com/user-attachments/assets/d205317a-8a2b-4e03-8952-7c03d321df4f" />  
6. create an ```.env``` file to store the client id,secrets and redirect uri and call them -> while function call without hard-coding them.
7. 

   


