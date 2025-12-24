[app]
# Basic app information
title = Smart Rover Control
package.name = smartrover
package.domain = org.collegeproject

# Source code settings
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,md
source.exclude_dirs = tests, bin, .git, __pycache__

# App version
version = 1.0

# Main Python file
source.main = main.py

# Python requirements
requirements = python3,kivy==2.1.0,pyjnius,plyer

# App icon (optional - add icon.png to your project folder)
#icon.filename = %(source.dir)s/icon.png

# Presplash (loading screen)
#presplash.filename = %(source.dir)s/presplash.png

# Orientation
orientation = portrait

[buildozer]
# Build settings
log_level = 2
warn_on_root = 1

[android]
# Android specific settings
android.permissions = BLUETOOTH,BLUETOOTH_ADMIN,ACCESS_COARSE_LOCATION,ACCESS_FINE_LOCATION,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Android API settings (optimized for stability)
android.api = 28
android.minapi = 21
android.ndk = 21b
android.sdk = 28
android.accept_sdk_license = True

# App theme
android.theme = "@android:style/Theme.NoTitleBar"

# Add Java classes for Bluetooth
android.add_java_dir = java

# Gradle dependencies for Bluetooth
android.gradle_dependencies = 

# Architecture
android.archs = arm64-v8a, armeabi-v7a

# Release settings (for signed APK)
[android.release]
# Keystore settings (create your own keystore)
#android.release.keystore = %(source.dir)s/keystore.jks
#android.release.keyalias = smartrover
#android.release.keystore_passwd = your_password
#android.release.keyalias_passwd = your_password