#!/bin/bash
# GitHub Codespaces Setup Script for Smart Rover APK Build
# This script sets up the complete Android build environment

set -e  # Exit on any error

echo "🚀 Setting up Smart Rover APK Build Environment"
echo "================================================"

# Update system
echo "🔄 Updating system packages..."
sudo apt update -y
sudo apt upgrade -y
echo "✅ System updated successfully"

# Install essential dependencies
echo "🔄 Installing system dependencies..."
sudo apt install -y \
    git \
    zip \
    unzip \
    openjdk-11-jdk \
    python3-pip \
    python3-dev \
    build-essential \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    libltdl-dev \
    wget \
    curl
echo "✅ System dependencies installed"

# Set up Java environment
echo "🔄 Configuring Java environment..."
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
echo "export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64" >> ~/.bashrc
echo "✅ Java environment configured"

# Install Python build tools with specific versions
echo "🔄 Installing Python build tools..."
pip3 install --upgrade pip
pip3 install setuptools==58.0.0
pip3 install wheel
pip3 install cython==0.29.33
pip3 install buildozer==1.4.0
echo "✅ Python build tools installed"

# Install Kivy with compatible version
echo "🔄 Installing Kivy..."
pip3 install kivy==2.1.0
echo "✅ Kivy installed"

# Install additional Python dependencies
echo "🔄 Installing additional dependencies..."
pip3 install pyjnius plyer
echo "✅ Additional dependencies installed"

# Verify installations
echo "🔍 Verifying installations..."
python3 --version
java -version
buildozer version
echo "✅ All tools verified"

# Create necessary directories
echo "🔄 Creating build directories..."
mkdir -p ~/.buildozer
mkdir -p bin
echo "✅ Build directories created"

echo ""
echo "🎉 Setup completed successfully!"
echo "📋 Next steps:"
echo "   1. Run: chmod +x setup.sh && ./setup.sh"
echo "   2. Run: buildozer android debug"
echo "   3. Wait 15-30 minutes for APK build"
echo "   4. Find APK in bin/ directory"
echo ""
echo "🚀 Ready to build Smart Rover APK!"