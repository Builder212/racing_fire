import cx_Freeze, sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "Racing Fire",           # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]main.exe",# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
),]

msi_data = {"Shortcut": shortcut_table}
bdist_msi_options = {'data': msi_data}

executables = [cx_Freeze.Executable("main.py", base=base)]

cx_Freeze.setup(
    name="Racing Fire",
    version="1.0.1",
    options={"build_exe": {"packages":["pygame", "time", "random", "pickle", "sys"],
                           "include_files":["music/", "data/", "textures/"],
                           "include_msvcr": True,
    },
    "bdist_msi": bdist_msi_options
    },
    executables = executables
)
