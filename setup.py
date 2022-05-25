import sys

from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": [], "excludes": []}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="gui",
      version="8.1",
      description="application!",
      options={"build_exe": build_exe_options},
      base_name="win32gui",
      executables=[Executable("gui.py", base=base, targetName='gui.exe', icon="icons8_search_client.ico")])
