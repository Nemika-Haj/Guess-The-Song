# **Guess The Song**
> A Discord Game Bot where you must guess the name of the song playing! Doing so will give you exp. You can level up and become the ***Master guesser***!

## Configuring
To run the bot, you should create a `config.yml` file first. Create one inside the `bot/data` file. Make sure it is enabled exactly like it should (`config.yml`). Then, replace the following content with the required information and paste into the file.
```yaml
managers:
- 219567539049594880
- 163164447848923136
- any-id-you-wish
prefix: bot-prefix
token: bot-token
version: 1.0.0
mongo-uri: mongo-connect-uri
dashURL: dashboard-url 
# http://127.0.0.1:5000/ should be used if you're running an instance of the bot on your personal computer and the dashboard is not public. In case you have set it up in a webserver, use that URL instead.
```

## Additional Information
This bot was created in **[Discord.py](https://github.com/Rapptz/discord.py)** by **[LostNuke](https://github.com/LostNuke)** and **[Nemika](https://github.com/Nemika-Haj/)** for the **BytesToBits Discord Bot Jam**! You are free to use the bot while abiding the MIT License terms!