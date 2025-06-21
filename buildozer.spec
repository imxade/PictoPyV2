[app]
title = PictoPy
package.name = pictopy
package.domain = org.xade
source.dir = .
source.include_exts = py,png,jpg,kv,json,txt,html,css,js
version = 0.1

entrypoint = main.py
orientation = portrait
fullscreen = 0
icon.filename = static/asset/favicon.png
presplash.filename = static/asset/favicon.png
android.add_assets = static/,models/

# Only supported/possible requirements for Android
requirements = mpmath, python3, kivy, pywebview, blinker, bottle, click, coloredlogs, Flask, flatbuffers, humanfriendly, itsdangerous, Jinja2, MarkupSafe, mpmath, numpy, packaging, protobuf, proxy_tools, sympy, typing_extensions, Werkzeug, xxhash

android.permissions = INTERNET
android.enable_androidx = 1

# Add the pywebview Android JAR (replace with actual path)
android.add_jars = pywebview-android.jar

arch = arm64-v8a
android.minapi = 21
android.ndk_api = 21
ignore_setup_py = 1
copy_libs = 1

[buildozer]
log_level = 2
warn_on_root = 0
build_dir = .buildozer
