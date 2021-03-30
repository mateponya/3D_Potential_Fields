# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 00:22:19 2021

@author: PawelG
"""

import os


def main_dir():
    return os.getcwd()

def parent_dir():
    a = main_dir()
    a = a[:a.rfind("\\")]
    return a

def ffmpeg():
    return parent_dir() + "\\bin\\ffmpeg.exe"


if __name__ == "__main__":
    print(ffmpeg())