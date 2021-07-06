# 3-AM-

*3AM is a free Discord educational and entertainment bot, that tends to deliver prime level of communication, entertainment and co-operation among people. 
*3AM provides : Chat Bot Calculator Timer and Reminder Commands Media Encoder Music Player.

Requirements:

(a) Libraries 

- discord.py
     To use built in discord functions or to create certain commands and their realtime responses

-youtube_dl
     To search and play matched music from the youtube in the discord voice channel without opening youtube or any browser itself .


-random
      Used while creating random responses to certain user interactive commands 
      for chatbot purposes .

-asyncio
      Used to support the async/await syntax used in the code .

-datetime
      Used while creating time reminders for time access and conversions .
      
(b) Framework 

   Since one of the leading commands of our bot is to play music in the voice channel , so the multimedia format has to be MP3 but as it takes music from YouTube where only MP4      format is supported , first we’ve to convert the YouTube MP4 music video into a MP3 song .
   For that we’ve made use of FFMPEG which is a multimedia framework used to decode, encode , transcode, play anything on any given format.

