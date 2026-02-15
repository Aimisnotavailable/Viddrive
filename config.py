
import pygame
import numpy as np
import os
import math
import cv2
import config
from screeninfo import get_monitors
from pathlib import Path    

# Setup Output Directory
IMG_PATH = Path(f'{os.getcwd()}/imgs/')
VID_PATH = Path(f'{os.getcwd()}/vids/')
IMG_OUT_DIR = "imgs"
VID_OUT_DIR = "vids"

OUT_VIDEO_FILE = 'out_video.avi'
FPS = 30
CODEC = cv2.VideoWriter_fourcc(*'MJPG')

os.makedirs(IMG_OUT_DIR, exist_ok=True)
os.makedirs(VID_OUT_DIR, exist_ok=True)

# Standard colors
WHITE = np.array([255, 255, 255], dtype=np.uint8)
BLACK = np.array([0, 0, 0], dtype=np.uint8)
BLUE  = np.array([0, 0, 255], dtype=np.uint8)