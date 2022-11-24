# Wavedemon - Tool to work with your Tidal library

Couldn't get all the features I wanted with one thing
so I wrote this

---

# Goals
 - Daemonize
 - Avoid redownloads by keeping IDs in a sqlite database
 - Support adding to library via external applications
 - Check at defined intervals for changes to library and download

 ---

# Status
 - Can download all albums and playlists
 - Have db interface ready to try out
 - Working on splitting out current code to more organized structure, mostly done

---

# Todo List
 - Finish reorganizing current code
 - Add tests to verify database entries
 - Dockerize this so I can throw it around