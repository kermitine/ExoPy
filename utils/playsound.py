import winsound
from config.config import *

def play_sound(file_path, loop_enabled):
    if user_flags['sound_enabled'] is True:
        if loop_enabled:
            winsound.PlaySound(file_path, winsound.SND_ASYNC | winsound.SND_LOOP | winsound.SND_FILENAME)
        else:
            winsound.PlaySound(file_path, winsound.SND_ASYNC | winsound.SND_FILENAME)
        return 'sound played'
    else:
        return 'sound effects are disabled'