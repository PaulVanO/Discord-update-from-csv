# Discord-update-from-csv

A bot request from a fellow Reddit user
This bot is designed to take any CSV (see below for formatting requirements) and add a specified role to that list of members.  Popular for server owners that have Google forms and wish to bulk add roles to those members


## Getting Started

### Setting up the Bot account
1. Login to Discord web - https://discord.com
2. Navigate to Discord Developer Portal - https://discord.com/developers/applications
3. Click *New Application*
4. Give the Appplication a name and *Create*
5. Go to Bot tab and click *Add Bot*
6. Keep the default settings for Public Bot - *checked* and Require OAuth2 Code Grant - *unchecked*
7. Under **Priveleged Gateway Intents** enable SERVER MEMBERS INTENT and MESSAGE CONTENT INTENT (required)
7. Add bot image (optional)
8. Generate a new token and copy it.  Discord no longer keeps this token available. If you lose it, you will need to generate a new one.
9. Go to OAuth2 tab > URL Generator
10. Under *Scopes* - Check Bot
11. Under *Bot Permissions* - check Manage Roles, Read Messages/View Channels, Send Messages, Read Message History
12. Copy the generated link and Go to the URL in your browser - Invite Bot to your Discord server

### Configuring the Bot
Take the copied Token from step 8 above.  Open the .env-sample file in your favorite editor and paste the copied token
Should read `TOKEN='your pasted token'`.  Save and close
Rename .env-sample to just `.env`

The bot is now ready to run


### Using the Bot

The bot is designed to check on_message events (per request) for a specific csv file being uploaded (members.csv)
This csv can be as long as necessary, however, it must be formatted accordingly:


Column 1 | Discord Name | Column 3 | Column 4| ...
--- | --- | --- | --- | ---
Some Data | Username#0000 | Some other data | More data | ...


The bot looks for the discord name in column 2.  No matter how many columns or rows your csv file is, discord names must ALWAYS
be in the 2nd column of data AND your data must have a header row, or risk your first row of values being skipped.


Simply update your members.csv to any channel the bot has access to, include the role ID for the role you wish to grant this list of members,
and press enter.   That's it!

You will either recive a message that ALL members were updated to your submitted role OR
You will be provided a list of invalid usernames that not found as members in your server.


**Notes**
- Each time a new members.csv is uploaded, the bot's cached version will be replaced
- Since the bot is not being added with Administrator permissions, though you could if you wanted, it is required that the bot's highest role is higher than the role you wish to grant your csv members.