# Author: Darwin Castillo
# Description: These CURL requests interact with the Spotify API to perform CRUD operations on playlists.

curl --location 'https://accounts.spotify.com/api/token' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-d 'grant_type=client_credentials' \
-d 'client_id=dca777963e774827bf490fba7d722ae5' \
-d 'client_secret=c9c0d72718a5479a8e5289ed22d19a99'


# Read (GET) - Get information about a specific artist on Spotify
curl --location 'https://api.spotify.com/v1/artists/4Z8W4fKeB5YxbusRsdQVPb' \
-H 'Authorization: Bearer BQAX3vDkHHXVMpVVbyotgRVfeqDnUP1mo4rF6OzM72ySjS2wu7eB8f46on50tl9DbPevYHLEnre5rZ7Qqike9lV8pvx5L36Sml-r74vsT2SubfzBhtg'


# Create (POST) - Create a new playlist on Spotify
curl -X POST "https://api.spotify.com/v1/me/playlists" \
  -H "Authorization: Bearer BQBdTwiVqsntyFcwVDljh_keCaOl72ZhZ3-zAWZfqY1SyNh0PrR3bDtj0gV552NxAXUCMy_rZQ33SRlZtUpM-PzoGu2DKnulXBfEPz9Oe4H1Nb_DO74" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Playlist",
    "description": "An optional description"
  }'

# Read (GET) - Get information about a specific playlist on Spotify
curl -X GET "https://api.spotify.com/v1/playlists/{playlist_id}" \
  -H "Authorization: Bearer your_access_token"

# Update (PUT or PATCH) - Update the name of a playlist on Spotify
curl -X PUT "https://api.spotify.com/v1/playlists/{playlist_id}" \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Playlist Name"
  }'

# Delete (DELETE) - Delete a playlist on Spotify
curl -X DELETE "https://api.spotify.com/v1/playlists/{playlist_id}" \
  -H "Authorization: Bearer your_access_token"