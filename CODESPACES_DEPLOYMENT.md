# GitHub Codespaces APK Build Guide

This is the **FINAL ATTEMPT** to build the Smart Rover Android APK using GitHub Codespaces. If this fails, we'll abandon the mobile app approach and stick with the desktop version.

## 🚀 Quick Start (5 minutes setup)

### Step 1: Create GitHub Repository
1. Go to [GitHub.com](https://github.com) and create a new repository
2. Name it: `smart-rover-mobile`
3. Make it public (required for free Codespaces)
4. Initialize with README

### Step 2: Upload Project Files
Upload these files to your GitHub repository:

**Essential Files:**
- `main.py` - Main app entry point
- `rover_android_app.py` - Complete Android app code
- `buildozer.spec` - APK build configuration
- `setup.sh` - Environment setup script
- `.github/workflows/build.yml` - GitHub Actions workflow

**Documentation:**
- `README.md` - Project documentation
- `CODESPACES_DEPLOYMENT.md` - This guide

### Step 3: Launch GitHub Codespaces
1. Go to your repository on GitHub
2. Click the green "Code" button
3. Select "Codespaces" tab
4. Click "Create codespace on main"
5. Wait 2-3 minutes for environment setup

### Step 4: Build APK
Run these commands in the Codespaces terminal:

```bash
# Make setup script executable
chmod +x setup.sh

# Run setup (takes 5-10 minutes)
./setup.sh

# Build APK (takes 15-30 minutes)
buildozer android debug
```

### Step 5: Download APK
If successful, your APK will be in the `bin/` directory:
```bash
ls -la bin/
```

Download it using the Codespaces file explorer or:
```bash
# Copy to workspace root for easy download
cp bin/*.apk ./smart-rover.apk
```

## 📱 APK Installation

1. **Download APK** to your Android device
2. **Enable Unknown Sources** in Android settings
3. **Install APK** by tapping the downloaded file
4. **Grant Permissions** when prompted:
   - Bluetooth
   - Location (required for Bluetooth scanning)
5. **Pair HC-05** in Android Bluetooth settings first
6. **Launch App** and test all modes

## 🔧 Troubleshooting

### Build Fails with Java Errors
```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
source ~/.bashrc
buildozer android clean
buildozer android debug
```

### Kivy Installation Issues
```bash
pip3 uninstall kivy
pip3 install kivy==2.0.0
buildozer android debug
```

### NDK/SDK Download Issues
```bash
buildozer android clean
rm -rf ~/.buildozer
buildozer android debug
```

### Out of Space Error
```bash
# Clean up space
sudo apt autoremove -y
sudo apt autoclean
df -h  # Check available space
```

## 📋 Expected Build Output

**Successful build will show:**
```
# BUILD SUCCESSFUL in 15m 30s
# APK created: bin/smartrover-1.0-debug.apk
```

**APK Size:** ~15-25 MB
**Build Time:** 15-30 minutes

## 🎯 Success Criteria

✅ **APK builds without errors**
✅ **APK installs on Android device**  
✅ **App launches and shows 4 modes**
✅ **Bluetooth connection works with HC-05**
✅ **Control commands (F,L,R,B,S) send properly**

## ❌ Failure Scenarios

If any of these occur, we abandon mobile app:

❌ **Build fails after 3 attempts**
❌ **APK won't install on Android**
❌ **Bluetooth doesn't work**
❌ **App crashes on launch**

## 🔄 Alternative: Desktop Version

If Codespaces fails, use the working desktop version:
- `rover_simple_mobile.py` - Fully functional desktop GUI
- Works with real HC-05 hardware
- All 4 modes implemented
- Professional mobile-like interface

## 📞 Final Notes

This is our **last attempt** at mobile APK. The desktop version is already working perfectly with real hardware integration. If this fails, we have a solid backup solution.

**Good luck! 🍀**