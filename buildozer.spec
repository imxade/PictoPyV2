[app]
title = PictoPy
package.name = pictopy
package.domain = org.xade
source.dir = .
# source.include_exts = py,png,jpg,kv,json,txt,html,css,js
version = 0.1

entrypoint = main.py
orientation = portrait
fullscreen = 0
icon.filename = static/asset/favicon-8.png
presplash.filename = static/asset/favicon-8.png
android.add_assets = static/,models/

# Only supported/possible requirements for Android
requirements = python3, pywebview, Flask, numpy, xxhash, onnxruntime, opencv-python-headless, certifi, blinker, bottle, click, proxy_tools
# coloredlogs, flatbuffers, humanfriendly, itsdangerous, MarkupSafe, packaging, protobuf, typing_extensions, Werkzeug #, kivy

android.permissions = INTERNET
android.enable_androidx = 1

# Add the pywebview Android JAR (replace with actual path)
# android.add_jars = pywebview-android.jar

arch = arm64-v8a
android.minapi = 21
android.ndk_api = 21
ignore_setup_py = 1
copy_libs = 1

[buildozer]
log_level = 2
warn_on_root = 0
build_dir = .buildozer
