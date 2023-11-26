# Cake
Discord Bot

# Setup
1. Clone the repository:
    ```
    git clone https://github.com/StudentPP1/Cake.git
    ```

2. Create the [discord bot](https://discord.com/developers/applications)

3. Under `Privileged Gateway Intents` enable **MESSAGE CONTENT INTENT**

4. Click 'Reset Token' and place it in an environment variable named 'BOT_TOKEN'

5. Go to the OAuth2 tab, copy your "Client ID", and fill in [YOUR_ID](https://discord.com/oauth2/authorize?client_id=YOUR_ID&scope=bot&permissions=8) and add bot to the server
   
6. Copy bot's id in discord and place it in an environment variable named 'BOT_ID'
   
7. Install the required packages:
    ```
    pip install -r requirements.txt
    ```

8. run:
    ```
    python main.py
    ```

# Features
Bot capabilities:
+ `?nick` to change the nickname of guild members
+ `?t` translator
+ `?g` google query
+ `?joke` a joke from [S.T.A.L.K.E.R.](https://en.wikipedia.org/wiki/S.T.A.L.K.E.R.)
+ `?mute` mute guild member
+ `?un_mute` unmute guild member
+ `?clear` clearing chat
+ `?hello` bot greeting 
+ `?exchange` exchange rate (to UAN)
+ `?create_role` create role
+ `?get_role` issue role
+ `?send` message to a guild member
+ `?timer` timer
+ `?play` play music from YouTube
+ `?del_role` deleting a role
+ `?spam` spamming 
to a guild member or by mentioning him or her in the guild chat room
+ `?find` video download from YouTube
+ `?surprise` surprise
+ `?create-img` Generate an image using the Tupper formula
