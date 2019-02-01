# Mx3's Publishr
A script to automate the tedious process of getting music out, currently in construction.
### Currently supported features
- Cover arts square auto-creation (by cropping)
- Renaming of audio files following a scheme
- CLI log types dynamically created, see LOG_TYPES in consts.py

/!\\ Readme imported from my personnal trello card's description

## Processing

### INPUTS
- Filename
- Artist (`SELF_NAME` by default) ¤
- Track kind (album, ep, remix or single)
- Collection name ¤
- Description ¤
  - French
  - English
- Cover art 
  - Landscape version
  - Square version (cropped landscape version if not provided)
- Video (auto-generated w/ fade in&out, using landscape cover if not provided)

¤ means explicitly added by user
nothing means implicitly fetched with predetermined paths & filenaming schemes

### FILES CREATED
- Lowres cover art versions
- Full Album zip file (if its a collection)

### DATA UPLOADED
- Database
- Social networks (using buffer)
  - Cover arts (FB/TW:Landscape/IG:Square, with button "out now" added)
- Website filesystem
  - Cover arts 
  - Full album
  - Audio file(s)
- YouTube (1 week delay ?)
  - Video
  - Cover art (used for thumbnail, landscape version)
- Newsletter

### FILES MODIFIED
- audio file (adds ID3 tags)

## Resources

### NOTES
- Upload duration of tracks (and array of durations of tracknames if track is a collection) to DB in order to levrage server resources usage

### RESOURCES
- Twitter API
- Facebook API
- Instagram API
- YouTube Data API
- mx3creations.com's musiclist database table (through API ?)

### PYTHON CONCEPTS
- File object
- HTTP Request (cURL ?)
- Image operations
- Video operations
- ID3 Tags operations
- Database operations
- CLI Progress bars ?
- Regex

### NAMING SCHEMES
- Cover arts : \<collection\> cover art (\<landscape|square\>).png
- Songs/Videos filenames : \<artist\> - \<trackname\>.\<mp3|wav\>