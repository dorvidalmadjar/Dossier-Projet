__author__ = 'Doryan'

import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
includefiles = ["Images/"]

build_exe_options = {"packages": ["os"], "excludes": [], "include_files" : includefiles}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "ProjetISN-PortraitRobot",
    version = "1",
    options = {"build_exe": build_exe_options},
    description = "Projet ISN 2015 - TS2 - Outil de Portrait Robot",
    executables = [Executable("projet.py", base=base)],
)

