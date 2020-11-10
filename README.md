# Octabot
Octabot is a discord bot, made with discord.py, with a small handful of features.

## Features
Octabot's main feature is playing pre-installed mp3 files with additional features such as sending users a list of all installed songs, playing those songs and playing every song in a random order. 
Octabot also features a small emote game, with saving statistics, and an image classification feature.

More information about the bot's features and commands can be found at the bottom of this Readme!

## Requirements and Installation
To run this bot Python 3.6+ along with the discord.py[voice] module needs to be installed. 
Additional requirements are FFmpeg, which must be set up in the PATH on windows 10, and [this stunning image classification module](https://github.com/Cloud11665/Octagon).

There should be an 'Octagon' directory within the Octabot directory which would contain mp3 files for the bot to use but it's been emptied of mp3 files. Check this [readme](Octabot/Octagon/README.md) for more information

To run the bot a file containing a discord bot token is needed. Simply put a file called 'Token.txt', which is containing just the discord bot token, inside of the Octabot directory. Furthermore, when first ran the program will generate an 'Octalog' file, which will log information on the bot's operations. An 'Octagame' Database file will also be generated when one of the oct$game commands are first ran.

## Information
This is my first attempt at making a discord bot along with this likely being the biggest python program I've made, so expect areas in the code which could be improved.
I don't plan to use this bot for anything, it was mainly for fun, so feel free to copy any of the code or tell me about any issues with the code. *I also hope you enjoy the lovely notes I've left in the code.*

If you want context for the theme of this bot, search "Octagon YTPMV" on Youtube. Or alternatively watch [this Glorious video](https://www.youtube.com/watch?v=ddWJatRxfz8).

## Commands
All of these commands have the ```oct$``` prefix before them!
# General commands
| Command | Description |
| --- | --- |
| help | Summons an embed message displaying and explaining all of these commands. |
| ping | Pings the bot. Returns how long this took in milliseconds. |
| search | Requires an image to be attached with the message. Returns an image highlighting any octagons in the attached image. |

# Voice commands
| Command | Description |
| --- | --- |
| list | Sends a list of all the mp3 files saved within the Octagon directory. This list will be sent to the message author's direct messages. |
| join | Has Octabot join the voice channel in which the message author is connected to |
| leave | Has Octabot leave the voice channel which it's in |
| play <song> | Plays the song passed in the song argument. The song must be in the Octagon directory and for the author to be in a voice channel with Octabot |
| shuffle | Plays a random song in the Octagon directory |
| shuffleall | Plays all the songs in the Octagon directory in a random order |
| shuffleinfo | Responds with the song name currently being played with shuffleall |
| shuffleclear | Clears all the songs in the shuffle queue |
| pause | Pauses the song currently playing |
| resume | Resumes the current song if paused |
| stop | Stops the current song playing. This will also skip to the next song if using shuffleall |

# OctaGame commands
All of these commands have the ```oct$game``` prefix before them!
| Command | Description |
| --- | --- |
| help | Summons a help explaining aim of the game along with the other commands related to OctaGame |
| stats | Responds with the author's OctaGame stats within an message. These stats are how many times they've won in each of the three difficulties. |
| easy | Lets the author play OctaGame on the easy difficulty |
| normal | Lets the author play OctaGame on the normal difficulty |
| hard | Lets the author play OctaGame on the hard difficulty |
