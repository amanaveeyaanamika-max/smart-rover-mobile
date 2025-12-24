#!/bin/bash
# Quick fix for the libtinfo5 package issue

echo "🔧 Quick fix for package issues..."

# Update package lists
sudo apt update -y

# Install alternative ncurses library
echo "🔄 Installing ncurses alternatives..."
sudo apt install -y libncurses6 libtinfo6 || echo "Continuing without libtinfo..."

# Install essential build tools only
echo "🔄 Installing core build dependencies..."
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
    cmake \
    libffi-dev \
    libssl-dev

echo "✅ Core dependencies installed"

# Set up Java
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
echo "export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64" >> ~/.bashrc

# Install Python tools
echo "🔄 Installing Python build tools..."
pip3 install --upgrade pip
pip3 install setuptools==58.0.0 wheel cython==0.29.33
pip3 install buildozer==1.4.0

echo "🎉 Quick fix completed! Now try: buildozer android debug"