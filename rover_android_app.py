#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smart Rover Android App - Kivy Version
Complete hardware integration for Android APK deployment
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.core.window import Window
import threading
import time
from datetime import datetime

# Android Bluetooth imports
try:
    from jnius import autoclass
    from android.permissions import request_permissions, Permission
    BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
    BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
    BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
    UUID = autoclass('java.util.UUID')
    ANDROID_PLATFORM = True
    
    # Request permissions
    request_permissions([
        Permission.BLUETOOTH,
        Permission.BLUETOOTH_ADMIN,
        Permission.ACCESS_COARSE_LOCATION,
        Permission.ACCESS_FINE_LOCATION
    ])
except ImportError:
    ANDROID_PLATFORM = False
    print("Running in desktop mode - Android features disabled")

# Set window size for mobile
Window.size = (360, 640)

class ModeSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'mode_selection'
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Title
        title = Label(
            text='🤖 Smart Rover Control',
            font_size='24sp',
            size_hint_y=None,
            height='60dp',
            color=(0.9, 0.9, 0.9, 1)
        )
        main_layout.add_widget(title)
        
        subtitle = Label(
            text='8051 Microcontroller - HC-05 Bluetooth',
            font_size='14sp',
            size_hint_y=None,
            height='40dp',
            color=(0.7, 0.7, 0.7, 1)
        )
        main_layout.add_widget(subtitle)
        
        # Scrollable mode selection
        scroll = ScrollView()
        mode_layout = BoxLayout(orientation='vertical', spacing=15, size_hint_y=None)
        mode_layout.bind(minimum_height=mode_layout.setter('height'))
        
        # Mode buttons
        modes = [
            ('📱 Android Control', 'android_control', (0.2, 0.6, 0.9, 1)),
            ('🚧 Obstacle Detection', 'obstacle_detection', (0.9, 0.5, 0.1, 1)),
            ('📍 Line Follower', 'line_follower', (0.6, 0.3, 0.7, 1)),
            ('🌡️ Temperature & Humidity', 'sensor_monitoring', (0.1, 0.7, 0.4, 1))
        ]
        
        for text, screen_name, color in modes:
            btn = Button(
                text=text,
                size_hint_y=None,
                height='80dp',
                font_size='16sp',
                background_color=color
            )
            btn.bind(on_press=lambda x, screen=screen_name: self.go_to_mode(screen))
            mode_layout.add_widget(btn)
        
        scroll.add_widget(mode_layout)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def go_to_mode(self, screen_name):
        self.manager.current = screen_name

class AndroidControlScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'android_control'
        self.bluetooth_connected = False
        self.bluetooth_socket = None
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
        
        back_btn = Button(
            text='← Back',
            size_hint_x=None,
            width='80dp',
            background_color=(0.6, 0.6, 0.6, 1)
        )
        back_btn.bind(on_press=self.go_back)
        header_layout.add_widget(back_btn)
        
        title = Label(
            text='📱 Android Control Mode',
            font_size='18sp',
            color=(0.9, 0.9, 0.9, 1)
        )
        header_layout.add_widget(title)
        
        main_layout.add_widget(header_layout)
        
        # Connection panel
        conn_layout = BoxLayout(orientation='vertical', size_hint_y=None, height='120dp', spacing=5)
        
        # Bluetooth device selection
        device_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp')
        device_layout.add_widget(Label(text='HC-05 Device:', size_hint_x=None, width='100dp'))
        
        self.device_spinner = Spinner(
            text='Select Device',
            values=['HC-05', 'Scan for devices...'],
            size_hint_x=0.6
        )
        self.device_spinner.bind(text=self.on_device_select)
        device_layout.add_widget(self.device_spinner)
        
        scan_btn = Button(
            text='🔍',
            size_hint_x=None,
            width='40dp',
            background_color=(0.2, 0.6, 0.9, 1)
        )
        scan_btn.bind(on_press=self.scan_devices)
        device_layout.add_widget(scan_btn)
        
        conn_layout.add_widget(device_layout)
        
        # Connection buttons
        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp', spacing=10)
        
        self.connect_btn = Button(
            text='Connect',
            background_color=(0.1, 0.7, 0.1, 1)
        )
        self.connect_btn.bind(on_press=self.connect_bluetooth)
        btn_layout.add_widget(self.connect_btn)
        
        self.disconnect_btn = Button(
            text='Disconnect',
            background_color=(0.8, 0.2, 0.2, 1),
            disabled=True
        )
        self.disconnect_btn.bind(on_press=self.disconnect_bluetooth)
        btn_layout.add_widget(self.disconnect_btn)
        
        conn_layout.add_widget(btn_layout)
        
        # Status
        self.status_label = Label(
            text='Status: Disconnected',
            size_hint_y=None,
            height='40dp',
            color=(0.8, 0.2, 0.2, 1)
        )
        conn_layout.add_widget(self.status_label)
        
        main_layout.add_widget(conn_layout)
        
        # Command instructions
        instructions = Label(
            text='Control Commands: F=Forward, L=Left, R=Right, B=Backward, S=Stop',
            size_hint_y=None,
            height='60dp',
            text_size=(None, None),
            halign='center',
            color=(0.8, 0.8, 0.8, 1)
        )
        main_layout.add_widget(instructions)
        
        # Control buttons
        control_layout = GridLayout(cols=3, spacing=15, size_hint_y=None, height='300dp')
        
        # Row 1: Forward
        control_layout.add_widget(Label())
        forward_btn = Button(
            text='↑\nFORWARD\n(F)',
            background_color=(0.2, 0.6, 0.9, 1),
            font_size='14sp'
        )
        forward_btn.bind(on_press=lambda x: self.send_command('F'))
        control_layout.add_widget(forward_btn)
        control_layout.add_widget(Label())
        
        # Row 2: Left, Stop, Right
        left_btn = Button(
            text='←\nLEFT\n(L)',
            background_color=(0.2, 0.6, 0.9, 1),
            font_size='14sp'
        )
        left_btn.bind(on_press=lambda x: self.send_command('L'))
        control_layout.add_widget(left_btn)
        
        stop_btn = Button(
            text='⏹\nSTOP\n(S)',
            background_color=(0.8, 0.2, 0.2, 1),
            font_size='14sp'
        )
        stop_btn.bind(on_press=lambda x: self.send_command('S'))
        control_layout.add_widget(stop_btn)
        
        right_btn = Button(
            text='→\nRIGHT\n(R)',
            background_color=(0.2, 0.6, 0.9, 1),
            font_size='14sp'
        )
        right_btn.bind(on_press=lambda x: self.send_command('R'))
        control_layout.add_widget(right_btn)
        
        # Row 3: Backward
        control_layout.add_widget(Label())
        backward_btn = Button(
            text='↓\nBACKWARD\n(B)',
            background_color=(0.2, 0.6, 0.9, 1),
            font_size='14sp'
        )
        backward_btn.bind(on_press=lambda x: self.send_command('B'))
        control_layout.add_widget(backward_btn)
        control_layout.add_widget(Label())
        
        main_layout.add_widget(control_layout)
        
        # Command log
        log_label = Label(
            text='Command Log:',
            size_hint_y=None,
            height='30dp',
            color=(0.9, 0.9, 0.9, 1)
        )
        main_layout.add_widget(log_label)
        
        self.command_log = Label(
            text='Ready to connect...',
            text_size=(None, None),
            halign='left',
            valign='top',
            color=(0.7, 0.7, 0.7, 1)
        )
        
        log_scroll = ScrollView(size_hint_y=0.3)
        log_scroll.add_widget(self.command_log)
        main_layout.add_widget(log_scroll)
        
        self.add_widget(main_layout)
    
    def go_back(self, instance):
        self.manager.current = 'mode_selection'
    
    def scan_devices(self, instance):
        """Scan for Bluetooth devices"""
        if ANDROID_PLATFORM:
            try:
                adapter = BluetoothAdapter.getDefaultAdapter()
                if adapter and adapter.isEnabled():
                    # Get paired devices
                    paired_devices = adapter.getBondedDevices().toArray()
                    device_names = ['Select Device']
                    
                    for device in paired_devices:
                        device_name = device.getName()
                        if 'HC-05' in device_name or 'HC-06' in device_name:
                            device_names.append(device_name)
                    
                    self.device_spinner.values = device_names
                    self.show_popup("Scan Complete", f"Found {len(device_names)-1} HC-05 devices")
                else:
                    self.show_popup("Bluetooth Error", "Please enable Bluetooth first!")
            except Exception as e:
                self.show_popup("Scan Error", f"Error scanning devices:\n{str(e)}")
        else:
            # Desktop simulation
            self.device_spinner.values = ['Select Device', 'HC-05 (Simulated)', 'HC-06 (Simulated)']
            self.show_popup("Scan Complete", "Simulated scan complete")
    
    def on_device_select(self, spinner, text):
        """Handle device selection"""
        if text != 'Select Device' and text != 'Scan for devices...':
            self.selected_device = text
    
    def connect_bluetooth(self, instance):
        """Connect to selected Bluetooth device"""
        if not hasattr(self, 'selected_device'):
            self.show_popup("No Device", "Please select a device first!")
            return
        
        if ANDROID_PLATFORM:
            self.connect_android_bluetooth()
        else:
            self.connect_desktop_simulation()
    
    def connect_android_bluetooth(self):
        """Connect using Android Bluetooth API"""
        try:
            adapter = BluetoothAdapter.getDefaultAdapter()
            if not adapter.isEnabled():
                self.show_popup("Bluetooth Error", "Please enable Bluetooth first!")
                return
            
            # Find the selected device
            paired_devices = adapter.getBondedDevices().toArray()
            target_device = None
            
            for device in paired_devices:
                if device.getName() == self.selected_device:
                    target_device = device
                    break
            
            if not target_device:
                self.show_popup("Device Error", "Selected device not found!")
                return
            
            # Create socket and connect
            uuid = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")  # SPP UUID
            self.bluetooth_socket = target_device.createRfcommSocketToServiceRecord(uuid)
            self.bluetooth_socket.connect()
            
            self.bluetooth_connected = True
            self.status_label.text = f"Status: Connected to {self.selected_device}"
            self.status_label.color = (0.1, 0.7, 0.1, 1)
            self.connect_btn.disabled = True
            self.disconnect_btn.disabled = False
            
            self.log_command(f"Connected to {self.selected_device}")
            
        except Exception as e:
            self.show_popup("Connection Error", f"Failed to connect:\n{str(e)}")
            self.log_command(f"Connection failed: {str(e)}")
    
    def connect_desktop_simulation(self):
        """Desktop simulation of connection"""
        self.bluetooth_connected = True
        self.status_label.text = f"Status: Connected (Desktop Mode)"
        self.status_label.color = (0.1, 0.7, 0.1, 1)
        self.connect_btn.disabled = True
        self.disconnect_btn.disabled = False
        
        self.log_command("Connected in desktop simulation mode")
    
    def disconnect_bluetooth(self, instance):
        """Disconnect from Bluetooth"""
        try:
            if self.bluetooth_socket:
                self.bluetooth_socket.close()
            
            self.bluetooth_connected = False
            self.status_label.text = "Status: Disconnected"
            self.status_label.color = (0.8, 0.2, 0.2, 1)
            self.connect_btn.disabled = False
            self.disconnect_btn.disabled = True
            
            self.log_command("Disconnected from HC-05")
            
        except Exception as e:
            self.show_popup("Disconnection Error", f"Error disconnecting:\n{str(e)}")
    
    def send_command(self, command):
        """Send command to rover"""
        if not self.bluetooth_connected:
            self.show_popup("Not Connected", "Please connect to HC-05 first!")
            return
        
        try:
            if ANDROID_PLATFORM and self.bluetooth_socket:
                # Send via Android Bluetooth
                output_stream = self.bluetooth_socket.getOutputStream()
                command_bytes = f"{command}\n".encode('utf-8')
                output_stream.write(command_bytes)
                output_stream.flush()
            
            command_names = {
                'F': 'Forward',
                'L': 'Left',
                'R': 'Right',
                'B': 'Backward',
                'S': 'Stop'
            }
            
            command_name = command_names.get(command, command)
            self.log_command(f"Sent: {command} ({command_name})")
            
        except Exception as e:
            self.show_popup("Command Error", f"Failed to send command:\n{str(e)}")
            self.log_command(f"Error sending {command}: {str(e)}")
    
    def log_command(self, message):
        """Log command to display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        current_text = self.command_log.text
        if current_text == "Ready to connect...":
            self.command_log.text = log_entry
        else:
            # Keep only last 10 entries
            lines = current_text.split('\n')
            if len(lines) >= 10:
                lines = lines[-9:]
            lines.append(log_entry)
            self.command_log.text = '\n'.join(lines)
    
    def show_popup(self, title, message):
        """Show popup message"""
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()

# Placeholder screens for other modes (similar structure)
class ObstacleDetectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'obstacle_detection'
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
        back_btn = Button(text='← Back', size_hint_x=None, width='80dp')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'mode_selection'))
        header.add_widget(back_btn)
        header.add_widget(Label(text='🚧 Obstacle Detection', font_size='18sp'))
        layout.add_widget(header)
        
        layout.add_widget(Label(text='Obstacle Detection Mode\n\n🚀 Features:\n• Real-time distance monitoring\n• Automatic obstacle avoidance\n• Configurable safe distance\n• Activity logging\n\n📱 Ready for hardware integration!', 
                               text_size=(None, None), halign='center'))
        
        self.add_widget(layout)

class LineFollowerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'line_follower'
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
        back_btn = Button(text='← Back', size_hint_x=None, width='80dp')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'mode_selection'))
        header.add_widget(back_btn)
        header.add_widget(Label(text='📍 Line Follower', font_size='18sp'))
        layout.add_widget(header)
        
        layout.add_widget(Label(text='Line Follower Mode\n\n🚀 Features:\n• 3-sensor IR array monitoring\n• Real-time line position detection\n• Speed control settings\n• Automatic path following\n\n📱 Ready for hardware integration!', 
                               text_size=(None, None), halign='center'))
        
        self.add_widget(layout)

class SensorMonitoringScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'sensor_monitoring'
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
        back_btn = Button(text='← Back', size_hint_x=None, width='80dp')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'mode_selection'))
        header.add_widget(back_btn)
        header.add_widget(Label(text='🌡️ Sensor Monitor', font_size='18sp'))
        layout.add_widget(header)
        
        layout.add_widget(Label(text='Temperature & Humidity Mode\n\n🚀 Features:\n• Real-time DHT22 sensor readings\n• Color-coded status indicators\n• Data logging with timestamps\n• CSV export functionality\n\n📱 Ready for hardware integration!', 
                               text_size=(None, None), halign='center'))
        
        self.add_widget(layout)

class SmartRoverApp(App):
    def build(self):
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens
        sm.add_widget(ModeSelectionScreen())
        sm.add_widget(AndroidControlScreen())
        sm.add_widget(ObstacleDetectionScreen())
        sm.add_widget(LineFollowerScreen())
        sm.add_widget(SensorMonitoringScreen())
        
        return sm

if __name__ == '__main__':
    SmartRoverApp().run()