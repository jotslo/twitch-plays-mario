# twitch-plays-mario
The script used in a month-long Twitch stream where chat were in full control of Super Mario Bros.

Twitch Plays Mario was an interactive game hosted on Twitch where the chat was in full control of Super Mario Bros. It took just under a month for the game to be fully completed.

It was inspired by [Twitch Plays Pokemon](https://www.twitch.tv/twitchplayspokemon), a hugely successful stream in 2014 where millions of people tried to beat Pokemon Red entirely through Twitch chat.

The script works by taking input from Twitch chat, interpreting it as controller input, and mimicking pressing the associated keys. The emulator used then takes the mimicked key-presses as game input and updates the game accordingly, effectively allowing Twitch to take full control of Super Mario Bros. within a sandboxed environment.

OBS and a Windows server (with a GPU) is then used to stream the emulator and attached windows to Twitch, allowing people to take full control of the game in real-time.

This script can very easily be adapted to work with other controller/keyboard-based games, simply by modifying the configuration variables at the top of the script, and the `input_map` dictionary that contains the map for each inputted command.

## Dependencies
- [twitch-python](https://pypi.org/project/twitch-python/)
- [pydirectinput](https://pypi.org/project/PyDirectInput/)
