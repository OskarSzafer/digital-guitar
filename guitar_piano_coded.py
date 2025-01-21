import keyboard
import guitar
import logging

class Guitar_wrapper():

    def __init__(self, pleyer, keys, strings, string_mode_fingerstye = False):

        self.string_mode_fingerstye = string_mode_fingerstye

        # Configure logging
        logging.basicConfig(
            filename = 'guitar1.log',   # Log file name
            level = logging.ERROR,      # Log level (ERROR for error-level logs)
            format = '%(asctime)s - %(levelname)s - %(message)s'  # Log format
        )

        self.guitar = pleyer
        self.pressed_keys = set()

        self.keys_order = keys
        self.keys_len = len(keys)

        self.strings = strings
        self.strings_len = len(strings)

        # To keep track of hooked keys and their callbacks
        self.hooked_keys = []

        for key in keys:
            keyboard.hook_key(key, self.on_note_key)
            self.hooked_keys.append(('note', key, self.on_note_key))

        for key in strings:
            keyboard.hook_key(key, self.on_string_key)
            self.hooked_keys.append(('string', key, self.on_string_key))

    def __del__(self):
        for hook_type, key, callback in self.hooked_keys:
            keyboard.unhook_key(key, callback)
        self.hooked_keys.clear()
        logging.info("All keyboard hooks have been removed and resources cleaned up.")

    def guitar_play(self, i):
        print(f"g1 note: {i}")
        self.guitar.play(i)

    def get_note_num(self, fs=False):
        # If no keys
        if(len(self.pressed_keys) == 0):
            #if(fs):
                
            return 0

        # If 1 key
        elif(len(self.pressed_keys) == 1):
            for i in range(self.keys_len):
                if(self.keys_order[i] in self.pressed_keys):
                    return i+1

        # If 2 keys   
        elif(len(self.pressed_keys) == 2)and(fs==False):
            for i in range(self.keys_len):
                if(self.keys_order[i] in self.pressed_keys):
                    return i+13

        # If 3 keys
        elif(len(self.pressed_keys) == 3)and(fs==False):
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
            if not self.string_mode_fingerstye:
                note_num = self.get_note_num(fs=False)
                if self.strings.index(e.name) < 3: 
                    # top to bottom
                    self.guitar_play(note_num)
                else:
                    # bottom to top
                    self.guitar_play(note_num + 24)
            else:
                note_num = self.get_note_num(fs=True)
                # fingerstyle, strings top to bottom
                self.guitar_play(note_num + self.strings.index(e.name))


class Input_handler():

    def __init__(self, frets, strings, mode_keys, fingerstyle_modes, chord_modes):
        self.mode_keys = mode_keys

        self.fingerstyle_modes = fingerstyle_modes
        self.chord_modes = chord_modes

        self.current_mode = 0

        print(f"PLAYER SET TO {self.chord_modes[self.current_mode]}")
        self.wrapper = Guitar_wrapper(guitar.Guitar(self.chord_modes[self.current_mode]), frets, strings)

        self.hooked_keys = []
        keyboard.hook_key(self.mode_keys[0], self.previous_mode)
        self.hooked_keys.append(('mode', self.mode_keys[0], self.previous_mode))
        keyboard.hook_key(self.mode_keys[1], self.next_mode)
        self.hooked_keys.append(('mode', self.mode_keys[1], self.next_mode))
        keyboard.hook_key(self.mode_keys[2], self.flip_string_mode)
        self.hooked_keys.append(('mode', self.mode_keys[2], self.flip_string_mode))

        
    def update_wrapper(self):
        if self.wrapper.string_mode_fingerstye:
            self.wrapper.guitar = guitar.Guitar(self.fingerstyle_modes[self.current_mode])
            print(f"PLAYER SET TO {self.fingerstyle_modes[self.current_mode]}")
        else:
            self.wrapper.guitar = guitar.Guitar(self.chord_modes[self.current_mode])
            print(f"PLAYER SET TO {self.chord_modes[self.current_mode]}")

    def previous_mode(self, e):
        if e.event_type != keyboard.KEY_DOWN:
            return

        self.current_mode = self.current_mode - 1
        if self.current_mode < 0:
            self.current_mode = len(self.fingerstyle_modes) - 1

        self.update_wrapper()

    def next_mode(self, e):
        if e.event_type != keyboard.KEY_DOWN:
            return

        self.current_mode = self.current_mode + 1
        if self.current_mode >= len(self.fingerstyle_modes):
            self.current_mode = 0

        self.update_wrapper()

    def flip_string_mode(self, e):
        if e.event_type != keyboard.KEY_DOWN:
            return

        self.wrapper.string_mode_fingerstye = not self.wrapper.string_mode_fingerstye
        self.update_wrapper()


def main():
    frets = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c']
    strings = ['1', '2', '3', '4', '5', '6']

    # previous_mode, next_mode, flip string_mode
    mode_keys = [',', '.', '0']

    fingerstyle_modes  = ['Samples', 'Clean_fs']
    chord_modes = ['Samples', 'Clean']

    input_handler = Input_handler(frets, strings, mode_keys, fingerstyle_modes, chord_modes)


    # wait for 'esc' key to exit
    keyboard.wait('esc')

    del input_handler


if __name__ == "__main__":
    main()