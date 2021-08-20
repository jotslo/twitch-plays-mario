from tkinter import font
import pydirectinput
import tkinter
import twitch
import threading
import time

# configuration
channel_name = "jotslo"
bot_nickname = "botslo"
oauth_value = "oauth:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# max chars in each window
move_len = 19
chat_len = 25

# contents of feed windows
move_feed = []
chat_feed = []

# current clock time
time_value = ""

# command to key-press map
input_map = {
    "a": {"key": "a", "display": "A", "wait": 0.5},
    "b": {"key": "b", "display": "B", "wait": 0.5},
    "up": {"key": "u", "display": "▲", "wait": 1},
    "down": {"key": "d", "display": "▼", "wait": 1},
    "left": {"key": "l", "display": "◀", "wait": 1},
    "right": {"key": "r", "display": "▶", "wait": 1}
}

class Time(tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)


def update_move_feed(sender, key):
    # when new command inputted, bump up every line
    for i in range(len(move_feed) - 1):
        move_feed[i]["text"] = move_feed[i + 1]["text"]
    
    # get bottom value in feed
    bottom_value = move_feed[len(move_feed) - 1]
    
    # if sender name is too long, add "..." to end of name
    # to prevent overflow, and update bottom value of feed
    if len(sender) > move_len - 2:
        bottom_value["text"] = f"{sender[:move_len - 5]}... {key}"
    
    # otherwise, update bottom value of feed without modification
    else:
        bottom_value["text"] = sender + " " * (move_len - len(sender) - 1) + key


def simulate_key_press(key, wait):
    value = key["key"]

    # if wait time not defined, use wait time in input_map
    if not wait:
        wait = key["wait"]
    
    # mimic key press, wait defined time and then release key
    pydirectinput.keyDown(value)
    time.sleep(wait)
    pydirectinput.keyUp(value)


def interpret_input(message):
    msg = message.text.lower()

    # if message has too many commas, ignore message
    if msg.count(",") > 5:
        return
    
    # otherwise, get each substring between commas
    # , removing surrounding spaces
    for keys in msg.split(","):
        keys = keys.strip()

        # if set of commands has more than 5 spaces, skip to next set of commands
        if keys.count(" ") > 5:
            continue

        active_threads = []

        # get each key in the set, removing surrounding spaces
        for key in keys.split():
            key = key.strip()

            # if key is in input map, update move feed
            if key in input_map:
                update_move_feed(message.sender, input_map[key]["display"])

                # then, simulate key press in a new thread so keys can be
                # pressed simultaneously
                new_thread = threading.Thread(
                    target=simulate_key_press,
                    args=(input_map[key], None, )
                )

                # call function and add to active_threads list
                new_thread.start()
                active_threads.append(new_thread)
            
            # if key is in input map and ends with a digit, update move feed
            elif key[:-1] in input_map and key[-1].isdigit():
                update_move_feed(message.sender, input_map[key[:-1]]["display"])

                # then, simulate key press in a new thread
                # pass over associated digit (divided by 10) to represent key press length
                new_thread = threading.Thread(
                    target=simulate_key_press,
                    args=(input_map[key[:-1]], float(key[-1]) / 10, )
                )

                # call function and add to active_threads list
                new_thread.start()
                active_threads.append(new_thread)
        
        # keep waiting until all threads in the list are no longer alive
        while any(thread.is_alive() for thread in active_threads):
            time.sleep(0.1)


def on_message(message):
    # when message sent, call interpret_input function in new thread
    threading.Thread(target=interpret_input, args=(message, )).start()


def update_time():
    # every second, update the clock with the current time
    while True:
        time.sleep(1)
        time_value["text"] = time.strftime("%I:%M:%S %p")


def recent_moves():
    global time_value

    # create root window showing recent moves, with arcade font
    root = tkinter.Tk()
    root.configure(background="black")
    root.title("RecentMoves")
    font_style = font.Font(family="Press Start 2P", size=20)

    # create 16 labels, pack them into teh window and add to feed list
    for i in range(16):
        new_label = tkinter.Label(root, text=" " * 19,
            font=font_style, bg="#000", fg="#fff")
        new_label.pack()
        move_feed.append(new_label)
    
    # create another window showing current time, with smaller font size
    font_style = font.Font(family="Press Start 2P", size=16)
    time_window = tkinter.Toplevel(root)
    time_window.title("Time")
    time_window.configure(background="black")

    # create label with default time value and pack into window
    time_value = tkinter.Label(time_window, text="12:00:00 AM",
        font=font_style, bg="#000", fg="#fff")
    time_value.pack()

    # call update_time in new thread to constantly update time value
    # and then display windows to be shown in obs
    Time(time_window)
    threading.Thread(target=update_time).start()
    root.mainloop()


# call recent_moves in new thread to ensure matching thread for each window
threading.Thread(target=recent_moves).start()

# call twitch chat class with channel, bot name and authentication
bot = twitch.Chat(
    channel=f"#{channel_name}",
    nickname=bot_nickname,
    oauth=oauth_value
)

# subscribe to channel's messages, with on_message function as callback
bot.subscribe(on_message)
