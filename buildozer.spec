[app]
title = PictoPy
package.name = PictoPy
package.domain = org.xade

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,css
source.include_patterns = static/*,models/*

version = 0.1

requirements = python3,kivy,flask,click,blinker,coloredlogs,humanfriendly,itsdangerous,Jinja2,MarkupSafe,numpy,packaging,typing_extensions,Werkzeug,xxhash

icon.filename = %(source.dir)s/static/asset/favicon
presplash.filename = %(source.dir)s/static/asset/favicon

orientation = portrait
fullscreen = 0

android.archs = arm64-v8a
android.minapi = 21
android.api = 31
android.ndk_api = 21
p4a.bootstrap = sdl2

log_level = 2

[buildozer]
warn_on_root = 1
