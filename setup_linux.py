import cx_Freeze, sys

base = None

executables = [cx_Freeze.Executable("main.py", base=base)]

cx_Freeze.setup(
    name="Racing Fire",
    version="1.0.1",
    options={"build_exe": {"packages":["pygame", "time", "random", "pickle", "sys"],
                           "include_files":["music/", "data/", "textures/"],
    }},
    executables = executables
)
