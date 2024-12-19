import keyboard
import guitar
import logging

class Guitar_piano_coded():
    def __init__(self, path, keys, strings):

        # Configure logging
        logging.basicConfig(
            filename='guitar1.log',   # Log file name
            level=logging.ERROR,      # Log level (ERROR for error-level logs)
            format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
        )

        self.guitar = guitar.Guitar(path)
        self.pressed_keys = set()

        self.keys_order = keys
        self.keys_len = len(keys)

        self.strings = strings
        self.strings_len = len(strings)

        for key in keys:
            keyboard.hook_key(key, self.on_note_key)

        for key in strings:
            keyboard.hook_key(key, self.on_string_key)

    def guitar_play(self, i):
        self.guitar.play(i)
        print(f"g1 note: {i}")

    def get_note_num(self):
        # If no keys
        if(len(self.pressed_keys) == 0):
            return 0

        # If 1 key
        elif(len(self.pressed_keys) == 1):
            for i in range(self.keys_len):
                if(self.keys_order[i] in self.pressed_keys):
                    return i+1

        # If 2 keys   
        elif(len(self.pressed_keys) == 2):
            for i in range(self.keys_len):
                if(self.keys_order[i] in self.pressed_keys):
                    return i+13

        # If 2 keys
        elif(len(self.pressed_keys) == 3):
            for i in range(self.keys_len):
                if(self.keys_order[i] in self.pressed_keys):
                    return i+24


    # Hook for key presses
    def on_note_key(self, e):
        if e.event_type == keyboard.KEY_DOWN:
            self.pressed_keys.add(e.name)
        elif e.event_type == keyboard.KEY_UP:
            try:
                self.pressed_keys.remove(e.name)
            except KeyError:
                logging.error(f"KeyError: Tried to remove non-existent key {e.name}")

    # Hook for string presses
    def on_string_key(self, e):
        if e.event_type == keyboard.KEY_DOWN:
            note_num = self.get_note_num()
            self.guitar_play(note_num + self.strings.index(e.name)*34)


def main():
    path = 'clean'
    keys = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c']
    strings = ['1', '2', '3', '4', '5', '6']

    g1 = Guitar_piano_coded(path, keys, strings)
    
    # Keep the script running
    keyboard.wait('esc')

if __name__ == "__main__":
    main()