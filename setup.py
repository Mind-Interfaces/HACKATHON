from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["pygame", "OpenGL", "random", "requests", "threading", "datetime", "itertools", "moviepy", "websockets"],
    "include_files": ["loop.wav", "pong.wav", "ping.wav", "surf.wav", "drop.wav", "warp.wav", "oof.wav", "keywords.txt"],
    "excludes": []
}

setup(
    name="MUSICUBE",
    version="0.1",
    options={"build_exe": build_exe_options},
    executables=[Executable("MUSICUBE_2045.py")]
)
