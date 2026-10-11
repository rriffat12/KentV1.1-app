[app]

# ===== IDENTITAS APP =====
title = kenttV1
package.name = kenttv1
package.domain = com.kentt

# ===== SOURCE =====
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,json,txt
source.exclude_dirs = bin,.buildozer,__pycache__,.git
source.exclude_patterns = *.pyc,*.pyo

# ===== VERSION =====
version = 1.0.0

# ===== DEPENDENCIES =====
requirements = python3,kivy,pyjnius

# ===== ORIENTATION =====
orientation = portrait

# ===== WINDOW =====
fullscreen = 0

# ===== ANDROID =====
android.permissions = INTERNET,SYSTEM_ALERT_WINDOW,FOREGROUND_SERVICE

android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a

android.allow_backup = True
android.accept_sdk_license = True

# ===== LOG LEVEL =====
log_level = 2

# ===== BUILD =====
warn_on_root = 1

[buildozer]
log_level = 2
warn_on_root = 1