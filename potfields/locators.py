import os


def main_dir_location():
    return os.getcwd()

def parent_dir_location():
    a = main_dir_location()
    a = a[:a.rfind("\\")]
    return a

def ffmpeg_file_location():
    return parent_dir_location() + "\\bin\\ffmpeg.exe"