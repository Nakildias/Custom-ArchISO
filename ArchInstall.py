import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
import os
import re
import time
import getpass
import json
import requests # Import the requests library for HTTP requests

# Lastest Change Sudoer Fix and Version Check
# Performance Optimization: Faster Mirrors and Single mkinitcpio ~35% Faster then original.

# --- Configuration & Theme ---
SCRIPT_VERSION = "1.2"
MIN_BOOT_SIZE_MB = 512
LATEST_VERSION_URL = "https://raw.githubusercontent.com/Nakildias/Custom-ArchISO/main/latest_version"

# Dracula Theme Colors
DRACULA_BG = "#282a36"
DRACULA_FG = "#f8f8f2"
DRACULA_CURRENT_LINE = "#44475a"
DRACULA_COMMENT = "#6272a4"
DRACULA_CYAN = "#8be9fd"
DRACULA_GREEN = "#50fa7b"
DRACULA_ORANGE = "#ffb86c"
DRACULA_PINK = "#ff79c6"
DRACULA_PURPLE = "#bd93f9"
DRACULA_RED = "#ff5555"
DRACULA_YELLOW = "#f1fa8c"
DRACULA_BRIGHT_GREEN = "#50fa7b"
DRACULA_HIGHLIGHT = "#6272a4"
DRACULA_SELECTION_BG = "#44475a"

# Pre-defined package profiles
PACKAGE_PROFILES = {
    # A minimal server profile with just a few extra utilities beyond the base install.
    "Server (No GUI)": {
        "btop":      "Modern and feature-rich resource monitor",
        "cronie":    "Daemon for running scheduled tasks (e.g., cron jobs)",
        "fastfetch": "A fast and highly customizable tool for fetching and displaying system information with an ASCII logo.",
        "ntfs-3g":   "Driver for full read/write access to Windows NTFS filesystems",
        "openssh":   "Secure Shell server for remote login and management",
        "sudo":      "Allows permitted users to execute commands as the superuser",
        "ufw":       "Uncomplicated Firewall, a user-friendly firewall manager"
    },

    # A full-featured KDE Plasma desktop.
    "KDE Plasma": {
        "alsa-utils":       "Advanced Linux Sound Architecture utilities",
        "ark":              "KDE's native archiving and compression tool",
        "bluedevil":        "KDE's integration for managing Bluetooth devices",
        "btop":             "Modern and feature-rich resource monitor",
        "cups":             "The standard printing system for Linux",
        "discover":         "KDE's software center and application store",
        "dolphin":          "KDE's powerful and default file manager",
        "elisa":            "A simple and beautiful music player by KDE",
        "fastfetch":        "A fast and highly customizable tool for fetching and displaying system information with an ASCII logo.",
        "ffmpegthumbs":     "Generates video file thumbnails for file managers like Dolphin",
        "firefox":          "Popular open-source web browser",
        "flatpak":          "System for sandboxed desktop applications",
        "gimp":             "GNU Image Manipulation Program, a powerful photo editor",
        "gwenview":         "KDE's default image and video viewer",
        "kate":             "KDE's advanced and feature-rich text editor",
        "kcalc":            "KDE's scientific calculator",
        "kdeconnect":       "Integrates your phone and computer",
        "konsole":          "KDE's default terminal emulator",
        "kscreen":          "KDE's display management utility",
        "kwalletmanager":   "KDE's password management tool",
        "libreoffice-fresh":"A powerful and free office suite",
        "noto-fonts":       "Google's universal font family for excellent compatibility",
        "okular":           "KDE's universal document viewer (PDF, etc.)",
        "openssh":          "Secure Shell client/server for remote access",
        "p7zip":            "Command-line tool for 7z and other archive formats",
        "partitionmanager": "KDE's utility for managing disk partitions",
        "pipewire-alsa":    "PipeWire compatibility layer for ALSA applications",
        "pipewire-pulse":   "PipeWire compatibility layer for PulseAudio applications",
        "plasma-browser-integration": "Adds browser media controls to the Plasma desktop",
        "plasma-desktop":   "The core KDE Plasma desktop environment",
        "plasma-nm":        "KDE's network manager applet for the system tray",
        "plasma-pa":        "KDE's audio volume applet for the system tray",
        "plasma-systemmonitor": "Modern system resource monitor for KDE",
        "print-manager":    "A tool for managing print jobs",
        "sddm":             "Simple Desktop Display Manager, a modern login screen for Qt desktops",
        "sddm-kcm":         "KDE Configuration Module for SDDM",
        "spectacle":        "KDE's powerful screenshot utility",
        "timeshift":        "System restore utility that takes filesystem snapshots",
        "vlc":              "A highly versatile multimedia player"
    },

    # The modern GNOME desktop environment.
    "GNOME": {
        "alsa-utils":       "Advanced Linux Sound Architecture utilities",
        "btop":             "Modern and feature-rich resource monitor",
        "cups":             "The standard printing system for Linux",
        "eog":              "Eye of GNOME, the default image viewer",
        "fastfetch":        "A fast and highly customizable tool for fetching and displaying system information with an ASCII logo.",
        "file-roller":      "GNOME's archive manager for zip, tar, etc.",
        "firefox":          "Popular open-source web browser",
        "flatpak":          "System for sandboxed desktop applications",
        "gdm":              "GNOME Display Manager, the default login screen",
        "gimp":             "GNU Image Manipulation Program, a powerful photo editor",
        "gnome":            "The GNOME desktop metapackage",
        "gnome-bluetooth-3.0": "Bluetooth integration for the GNOME desktop",
        "gnome-control-center": "The main settings panel for GNOME",
        "gnome-disk-utility": "A tool for managing disk drives and media",
        "gnome-software":   "GNOME's software center",
        "gnome-system-monitor": "A utility to monitor system processes and resources",
        "gnome-terminal":   "The default terminal emulator for GNOME",
        "gnome-text-editor":"GNOME's new, simple default text editor",
        "gnome-tweaks":     "A tool for advanced GNOME configuration options",
        "gufw":             "Graphical User interface for the Uncomplicated Firewall",
        "libreoffice-fresh":"A powerful and free office suite",
        "nautilus":         "GNOME's default file manager",
        "noto-fonts":       "Google's universal font family for excellent compatibility",
        "openssh":          "Secure Shell client/server for remote access",
        "pipewire-alsa":    "PipeWire compatibility layer for ALSA applications",
        "pipewire-pulse":   "PipeWire compatibility layer for PulseAudio applications",
        "system-config-printer": "A graphical utility for printer configuration",
        "timeshift":        "System restore utility that takes filesystem snapshots",
        "totem":            "GNOME's official video (and music) player"
    },

    # The lightweight and classic XFCE desktop.
    "XFCE": {
        "alsa-utils":       "Advanced Linux Sound Architecture utilities",
        "blueman":          "A full-featured GTK-based Bluetooth manager",
        "btop":             "Modern and feature-rich resource monitor",
        "catfish":          "A handy file searching tool for XFCE",
        "cups":             "The standard printing system for Linux",
        "fastfetch":        "A fast and highly customizable tool for fetching and displaying system information with an ASCII logo.",
        "file-roller":      "A GTK-based archive manager",
        "firefox":          "Popular open-source web browser",
        "flatpak":          "System for sandboxed desktop applications",
        "gimp":             "GNU Image Manipulation Program, a powerful photo editor",
        "gnome-disk-utility": "A solid GTK-based disk management tool",
        "gufw":             "Graphical User interface for the Uncomplicated Firewall",
        "gvfs":             "Virtual filesystem for accessing network resources",
        "gvfs-smb":         "GVFS backend for Windows/Samba network shares",
        "libreoffice-fresh":"A powerful and free office suite",
        "lightdm":          "Lightweight and cross-desktop display manager",
        "lightdm-gtk-greeter": "GTK-based login screen theme for LightDM",
        "mousepad":         "XFCE's simple and fast default text editor",
        "network-manager-applet": "System tray applet for managing network connections",
        "noto-fonts":       "Google's universal font family for excellent compatibility",
        "openssh":          "Secure Shell client/server for remote access",
        "pavucontrol":      "PulseAudio Volume Control, a detailed audio mixer",
        "pipewire-alsa":    "PipeWire compatibility layer for ALSA applications",
        "pipewire-pulse":   "PipeWire compatibility layer for PulseAudio applications",
        "ristretto":        "XFCE's default image viewer",
        "system-config-printer": "A graphical utility for printer configuration",
        "thunar":           "XFCE's default file manager",
        "timeshift":        "System restore utility that takes filesystem snapshots",
        "vlc":              "A highly versatile multimedia player",
        "xfce4":            "The core XFCE desktop metapackage",
        "xfce4-goodies":    "A collection of useful plugins and utilities for XFCE",
        "xfce4-terminal":   "XFCE's default terminal emulator"
    },
    
    # The traditional and modern Cinnamon desktop.
    "Cinnamon": {
        "alsa-utils":       "Advanced Linux Sound Architecture utilities",
        "blueman":          "A full-featured GTK-based Bluetooth manager",
        "btop":             "Modern and feature-rich resource monitor",
        "cinnamon":         "The Cinnamon desktop environment",
        "cups":             "The standard printing system for Linux",
        "fastfetch":        "A fast and highly customizable tool for fetching and displaying system information with an ASCII logo.",
        "file-roller":      "A GTK-based archive manager for Cinnamon",
        "firefox":          "Popular open-source web browser",
        "flatpak":          "System for sandboxed desktop applications",
        "gimp":             "GNU Image Manipulation Program, a powerful photo editor",
        "gnome-disk-utility": "A solid GTK-based disk management tool",
        "gnome-terminal":   "A powerful and feature-rich terminal emulator",
        "gufw":             "Graphical User interface for the Uncomplicated Firewall",
        "libreoffice-fresh":"A powerful and free office suite",
        "lightdm":          "Lightweight and cross-desktop display manager",
        "lightdm-gtk-greeter": "GTK-based login screen theme for LightDM",
        "nemo":             "The default file manager for the Cinnamon desktop",
        "network-manager-applet": "System tray applet for managing network connections",
        "noto-fonts":       "Google's universal font family for excellent compatibility",
        "openssh":          "Secure Shell client/server for remote access",
        "pavucontrol":      "PulseAudio Volume Control, a detailed audio mixer",
        "pipewire-alsa":    "PipeWire compatibility layer for ALSA applications",
        "pipewire-pulse":   "PipeWire compatibility layer for PulseAudio applications",
        "system-config-printer": "A graphical utility for printer configuration",
        "timeshift":        "System restore utility (developed by Linux Mint team)",
        "vlc":              "A highly versatile multimedia player",
        "xed":              "The default, simple text editor from Linux Mint",
        "xreader":          "The default document (PDF) viewer from Linux Mint",
        "xviewer":          "The default image viewer from Linux Mint"
    },

    # The classic and lightweight MATE desktop.
    "MATE": {
        "alsa-utils":       "Advanced Linux Sound Architecture utilities",
        "atril":            "The default document (PDF) viewer for MATE",
        "blueman":          "A full-featured GTK-based Bluetooth manager",
        "btop":             "Modern and feature-rich resource monitor",
        "caja":             "The default file manager for the MATE desktop",
        "cups":             "The standard printing system for Linux",
        "engrampa":         "The default archive manager for MATE",
        "eom":              "Eye of MATE, the default image viewer",
        "fastfetch":        "A fast and highly customizable tool for fetching and displaying system information with an ASCII logo.",
        "firefox":          "Popular open-source web browser",
        "flatpak":          "System for sandboxed desktop applications",
        "gimp":             "GNU Image Manipulation Program, a powerful photo editor",
        "gnome-disk-utility": "A solid GTK-based disk management tool",
        "gufw":             "Graphical User interface for the Uncomplicated Firewall",
        "libreoffice-fresh":"A powerful and free office suite",
        "lightdm":          "Lightweight and cross-desktop display manager",
        "lightdm-gtk-greeter": "GTK-based login screen theme for LightDM",
        "mate-desktop":     "The core MATE desktop environment",
        "mate-terminal":    "The default terminal emulator for MATE",
        "mate-tweak":       "A utility for advanced customization of the MATE desktop",
        "network-manager-applet": "System tray applet for managing network connections",
        "noto-fonts":       "Google's universal font family for excellent compatibility",
        "openssh":          "Secure Shell client/server for remote access",
        "pavucontrol":      "PulseAudio Volume Control, a detailed audio mixer",
        "pipewire-alsa":    "PipeWire compatibility layer for ALSA applications",
        "pipewire-pulse":   "PipeWire compatibility layer for PulseAudio applications",
        "pluma":            "The default text editor for MATE",
        "system-config-printer": "A graphical utility for printer configuration",
        "timeshift":        "System restore utility that takes filesystem snapshots",
        "vlc":              "A highly versatile multimedia player"
    },

    # The modern and elegant Budgie desktop.
    "Budgie": {
        "alsa-utils":       "Advanced Linux Sound Architecture utilities",
        "blueman":          "A full-featured GTK-based Bluetooth manager",
        "btop":             "Modern and feature-rich resource monitor",
        "budgie-desktop":   "The Budgie desktop environment",
        "cups":             "The standard printing system for Linux",
        "fastfetch":        "A fast and highly customizable tool for fetching and displaying system information with an ASCII logo.",
        "file-roller":      "A standard GTK archive manager",
        "firefox":          "Popular open-source web browser",
        "flatpak":          "System for sandboxed desktop applications",
        "gimp":             "GNU Image Manipulation Program, a powerful photo editor",
        "gnome-disk-utility": "A solid GTK-based disk management tool",
        "gnome-text-editor":"A modern, simple text editor from the GNOME project",
        "gufw":             "Graphical User interface for the Uncomplicated Firewall",
        "libreoffice-fresh":"A powerful and free office suite",
        "lightdm":          "Lightweight and cross-desktop display manager",
        "lightdm-gtk-greeter": "GTK-based login screen theme for LightDM",
        "nemo":             "The powerful Nemo file manager (popular choice for Budgie)",
        "network-manager-applet": "System tray applet for managing network connections",
        "noto-fonts":       "Google's universal font family for excellent compatibility",
        "openssh":          "Secure Shell client/server for remote access",
        "pavucontrol":      "PulseAudio Volume Control, a detailed audio mixer",
        "pipewire-alsa":    "PipeWire compatibility layer for ALSA applications",
        "pipewire-pulse":   "PipeWire compatibility layer for PulseAudio applications",
        "system-config-printer": "A graphical utility for printer configuration",
        "timeshift":        "System restore utility that takes filesystem snapshots",
        "vlc":              "A highly versatile multimedia player"
    },

    # The fast and lightweight LXQt desktop.
    "LXQt": {
        "alsa-utils":       "Advanced Linux Sound Architecture utilities",
        "ark":              "A powerful Qt-based archive manager from the KDE project",
        "blueman":          "A full-featured GTK-based Bluetooth manager (functional choice for LXQt)",
        "btop":             "Modern and feature-rich resource monitor",
        "cups":             "The standard printing system for Linux",
        "fastfetch":        "A fast and highly customizable tool for fetching and displaying system information with an ASCII logo.",
        "featherpad":       "A lightweight and feature-rich Qt-based text editor",
        "firefox":          "Popular open-source web browser",
        "flatpak":          "System for sandboxed desktop applications",
        "gimp":             "GNU Image Manipulation Program, a powerful photo editor",
        "gufw":             "Graphical User interface for the Uncomplicated Firewall",
        "libreoffice-fresh":"A powerful and free office suite",
        "lximage-qt":       "The default image viewer for LXQt",
        "lxqt":             "The LXQt desktop environment metapackage",
        "network-manager-applet": "System tray applet for managing network connections",
        "noto-fonts":       "Google's universal font family for excellent compatibility",
        "openssh":          "Secure Shell client/server for remote access",
        "pavucontrol":      "PulseAudio Volume Control, a detailed audio mixer",
        "pcmanfm-qt":       "The default file manager for LXQt",
        "pipewire-alsa":    "PipeWire compatibility layer for ALSA applications",
        "pipewire-pulse":   "PipeWire compatibility layer for PulseAudio applications",
        "qterminal":        "A lightweight Qt-based terminal emulator",
        "sddm":             "Simple Desktop Display Manager, a modern login screen for Qt desktops",
        "system-config-printer": "A graphical utility for printer configuration",
        "vlc":              "A highly versatile multimedia player"
    },
    
    # A minimal tiling setup for advanced users with Sway (Wayland).
    "Sway (Tiling WM)": {
        "alsa-utils":       "Advanced Linux Sound Architecture utilities",
        "btop":             "Modern and feature-rich resource monitor",
        "fastfetch":        "A fast and highly customizable tool for fetching and displaying system information with an ASCII logo.",
        "firefox":          "Popular open-source web browser",
        "foot":             "A fast, lightweight, and Wayland-native terminal emulator",
        "gimp":             "GNU Image Manipulation Program, a powerful photo editor",
        "grim":             "A command-line tool for taking screenshots on Wayland",
        "ly":               "A TUI (text-based) display manager / login screen",
        "mako":             "A lightweight notification daemon for Wayland",
        "network-manager-applet": "System tray applet for managing network connections (for waybar)",
        "noto-fonts":       "Google's universal font family for excellent compatibility",
        "openssh":          "Secure Shell client/server for remote access",
        "pamixer":          "A command-line pulse audio mixer",
        "pavucontrol":      "PulseAudio Volume Control, a detailed audio mixer",
        "pipewire-alsa":    "PipeWire compatibility layer for ALSA applications",
        "pipewire-pulse":   "PipeWire compatibility layer for PulseAudio applications",
        "qt5-wayland":      "Provides Wayland support for Qt5 applications",
        "qt6-wayland":      "Provides Wayland support for Qt6 applications",
        "slurp":            "A command-line tool for selecting a region on Wayland (used with grim)",
        "sway":             "A tiling Wayland compositor, i3-compatible",
        "swaybg":           "A utility to display a background image on Sway",
        "swaylock":         "A screen locker for Sway",
        "thunar":           "A lightweight GTK file manager",
        "vlc":              "A highly versatile multimedia player",
        "waybar":           "A highly customizable Wayland bar for Sway and other compositors",
        "wl-clipboard":     "Command-line copy/paste utilities for Wayland",
        "wofi":             "A fast and lightweight application launcher for Wayland"
    },

    # A minimal tiling setup for advanced users with i3 (X11).
    "i3 (Tiling WM)": {
        "alacritty":        "A fast, cross-platform, OpenGL terminal emulator",
        "alsa-utils":       "Advanced Linux Sound Architecture utilities",
        "btop":             "Modern and feature-rich resource monitor",
        "dunst":            "A lightweight and customizable notification daemon for X11",
        "fastfetch":        "A fast and highly customizable tool for fetching and displaying system information with an ASCII logo.",
        "feh":              "A fast, lightweight image viewer, often used to set wallpapers",
        "firefox":          "Popular open-source web browser",
        "gimp":             "GNU Image Manipulation Program, a powerful photo editor",
        "i3-gaps":          "A popular fork of the i3 window manager with gaps between windows",
        "i3lock":           "A simple screen locker for the i3 window manager",
        "libreoffice-fresh":"A powerful and free office suite",
        "lightdm":          "Lightweight and cross-desktop display manager",
        "lightdm-gtk-greeter": "GTK-based login screen theme for LightDM",
        "maim":             "A utility to take screenshots of your desktop",
        "network-manager-applet": "System tray applet for managing network connections",
        "noto-fonts":       "Google's universal font family for excellent compatibility",
        "openssh":          "Secure Shell client/server for remote access",
        "pamixer":          "A command-line pulse audio mixer",
        "pavucontrol":      "PulseAudio Volume Control, a detailed audio mixer",
        "picom":            "A lightweight compositor for X11 (for transparency and effects)",
        "pipewire-alsa":    "PipeWire compatibility layer for ALSA applications",
        "pipewire-pulse":   "PipeWire compatibility layer for PulseAudio applications",
        "polybar":          "A fast and easy-to-use tool for creating status bars",
        "rofi":             "A versatile window switcher, application launcher and dmenu replacement",
        "thunar":           "A lightweight GTK file manager",
        "vlc":              "A highly versatile multimedia player"
    },
    
    # A power-user KDE Plasma profile with development and creative tools.
    "KDE Plasma (Nakildias Profile)": {
        "alsa-utils":       "Advanced Linux Sound Architecture utilities",
        "ark":              "KDE's native archiving tool",
        "bluedevil":        "KDE's Bluetooth integration stack",
        "btop":             "Modern and feature-rich resource monitor",
        "calindori":        "KDE's calendar application",
        "code":             "Visual Studio Code, a popular source-code editor",
        "cups":             "The standard printing system for Linux",
        "deluge-gtk":       "A popular, lightweight BitTorrent client",
        "discover":         "KDE's software center",
        "dnsmasq":          "Lightweight DNS forwarder and DHCP server (for virt-manager)",
        "dolphin":          "KDE's powerful and default file manager",
        "fastfetch":        "A fast and highly customizable tool for fetching and displaying system information with an ASCII logo.",
        "ffmpegthumbs":     "Generates video file thumbnails for file managers like Dolphin",
        "firefox":          "Popular open-source web browser",
        "flatpak":          "System for sandboxed desktop applications",
        "git-lfs":          "Git extension for versioning large files",
        "gimp":             "GNU Image Manipulation Program, an advanced image editor",
        "gwenview":         "KDE's default image and video viewer",
        "isoimagewriter":   "KDE's tool for writing bootable ISOs to USB drives",
        "kate":             "KDE's advanced text editor",
        "kcalc":            "KDE's scientific calculator",
        "kdeconnect":       "Integrates your phone and computer",
        "kdenlive":         "KDE's powerful non-linear video editor",
        "kfind":            "KDE's dedicated file search utility",
        "kmail":            "KDE's email client",
        "konsole":          "KDE's default terminal emulator",
        "krdc":             "KDE's remote desktop client (RDP/VNC)",
        "krdp":             "Remote desktop server support for KDE",
        "kscreen":          "KDE's display management utility",
        "kwalletmanager":   "KDE's password management tool",
        "nmap":             "Powerful network scanning and security auditing tool",
        "ntfs-3g":          "Driver for read/write access to Windows NTFS filesystems",
        "obs-studio":       "Software for video recording and live streaming",
        "openssh":          "Secure Shell client/server for remote access",
        "p7zip":            "Command-line tool for 7z and other archive formats",
        "partitionmanager": "KDE's utility for managing disk partitions",
        "pipewire-alsa":    "PipeWire compatibility layer for ALSA applications",
        "pipewire-pulse":   "PipeWire compatibility layer for PulseAudio applications",
        "plasma-browser-integration": "Adds browser media controls to the Plasma desktop",
        "plasma-desktop":   "The core KDE Plasma desktop environment",
        "plasma-nm":        "KDE's network manager applet",
        "plasma-pa":        "KDE's audio volume applet",
        "plasma-systemmonitor": "Modern system resource monitor for KDE",
        "podman":           "A daemonless container engine for OCI containers",
        "print-manager":    "A tool for managing print jobs",
        "qemu-desktop":     "A machine emulator and virtualizer (desktop parts)",
        "sddm":             "Simple Desktop Display Manager, a modern login screen",
        "sddm-kcm":         "KDE Configuration Module for SDDM",
        "spectacle":        "KDE's powerful screenshot utility",
        "spotify-launcher": "A simple launcher for the Spotify client",
        "syncthing":        "A decentralized file synchronization program",
        "system-config-printer": "A graphical utility for printer configuration",
        "thefuck":          "Corrects typos in your previous console command",
        "timeshift":        "A system restore utility that takes filesystem snapshots",
        "traceroute":       "A utility to trace the network path to a host",
        "virt-manager":     "A graphical interface for managing virtual machines",
        "vlc":              "A highly versatile multimedia player"
    }
}
# --- Helper Functions ---
def run_command(command, shell=True, check=True, capture_output=True, text=True):
    """
    Runs a shell command and handles its output and errors.
    """
    try:
        if capture_output:
            result = subprocess.run(command, shell=shell, check=check, capture_output=True, text=text, encoding='utf-8', errors='replace')
            return result.stdout.strip()
        else:
            subprocess.run(command, shell=shell, check=check, text=text)
            return True
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Command Error", f"Command failed: {e.cmd}\nOutput: {e.stdout}\nError: {e.stderr}")
        raise
    except FileNotFoundError:
        messagebox.showerror("Command Not Found", f"Command not found: {command.split()[0]}. Make sure it's in your PATH.")
        raise
    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")
        raise

class ArchInstallGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"ArchInstall by Nakildias")
        self.geometry("710x625")
        self.resizable(False, False)
        self.config(bg=DRACULA_BG)

        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.style.configure(".", background=DRACULA_BG, foreground=DRACULA_FG, font=("Fira Code", 10))
        self.style.configure("TFrame", background=DRACULA_BG)
        self.style.configure("TLabel", background=DRACULA_BG, foreground=DRACULA_FG)
        self.style.configure("TButton", background=DRACULA_CURRENT_LINE, foreground=DRACULA_GREEN, borderwidth=1, relief="flat", bordercolor=DRACULA_COMMENT)
        self.style.map("TButton",
                       background=[("active", DRACULA_HIGHLIGHT), ("disabled", DRACULA_COMMENT)],
                       foreground=[("active", DRACULA_BRIGHT_GREEN), ("disabled", DRACULA_FG)])
        
        self.style.configure("TEntry", fieldbackground=DRACULA_CURRENT_LINE, foreground=DRACULA_FG, insertcolor=DRACULA_PURPLE, bordercolor=DRACULA_COMMENT)
        self.style.configure("TCombobox", fieldbackground=DRACULA_CURRENT_LINE, foreground=DRACULA_FG, bordercolor=DRACULA_COMMENT, selectbackground=DRACULA_PURPLE, selectforeground=DRACULA_FG)
        self.style.map("TCombobox",
                       fieldbackground=[("readonly", DRACULA_CURRENT_LINE)],
                       selectbackground=[("readonly", DRACULA_PURPLE)],
                       selectforeground=[("readonly", DRACULA_FG)])

        self.style.configure("TCheckbutton", background=DRACULA_BG, foreground=DRACULA_FG, indicatorcolor=DRACULA_PURPLE)
        self.style.map("TCheckbutton",
                       background=[("active", DRACULA_BG)],
                       foreground=[("active", DRACULA_FG)])

        self.style.configure("TProgressbar", background=DRACULA_PURPLE, troughcolor=DRACULA_CURRENT_LINE, bordercolor=DRACULA_COMMENT)
        self.style.configure("Horizontal.TProgressbar", thickness=15)

        self.style.configure("Title.TLabel", font=("Fira Code", 24, "bold"), foreground=DRACULA_CYAN)
        self.style.configure("Subtitle.TLabel", font=("Fira Code", 12), foreground=DRACULA_COMMENT)
        self.style.configure("Highlight.TLabel", font=("Fira Code", 12, "bold"), foreground=DRACULA_PURPLE)
        self.style.configure("Warning.TLabel", foreground=DRACULA_RED, font=("Fira Code", 10, "bold"))
        self.style.configure("Success.TLabel", foreground=DRACULA_GREEN, font=("Fira Code", 10, "bold"))
        self.style.configure("Info.TLabel", foreground=DRACULA_CYAN, font=("Fira Code", 10, "bold"))

        self.install_vars = {
            "target_disk": tk.StringVar(value=""),
            "boot_mode": tk.StringVar(value=""),
            "boot_size": tk.StringVar(value="512M"),
            "swap_size": tk.StringVar(value=""),
            "hostname": tk.StringVar(value="archlinux"),
            "username": tk.StringVar(value="archuser"),
            "user_password": "",
            "root_password": "",
            "selected_kernel": tk.StringVar(value="linux"),
            "selected_de_name": tk.StringVar(value="Server (No GUI)"),
            "package_list": tk.StringVar(value=""),
            "install_steam": tk.BooleanVar(value=False),
            "install_discord": tk.BooleanVar(value=False),
            "enable_multilib": tk.BooleanVar(value=False),
            "enable_root_account": tk.BooleanVar(value=False),
            "log_to_file": tk.BooleanVar(value=False),
            "install_oh_my_zsh": tk.BooleanVar(value=True),
            "partition_prefix": tk.StringVar(value=""),
            "root_partition": tk.StringVar(value=""),
            "boot_partition": tk.StringVar(value=""),
            "swap_partition": tk.StringVar(value=""),
            "bios_boot_partition": tk.StringVar(value=""),
            "region": tk.StringVar(value="America"),
            "city": tk.StringVar(value="Toronto"),
            "keyboard_layout": tk.StringVar(value="us"),
            "internet_status": tk.StringVar(value=""),
            # New variable to hold the final, confirmed disk name
            "final_target_disk": tk.StringVar(value=""),
            "use_reflector": tk.BooleanVar(value=True),
            "zsh_theme": tk.StringVar(value="agnoster"),
        }

        self.current_frame = None
        self.frames = {}
        self.create_frames()
        self.show_frame(WelcomeFrame)
        # Start update check in a separate thread to avoid blocking the GUI
        threading.Thread(target=self.check_for_updates).start()

    def check_for_updates(self):
        """
        Checks for the latest version from GitHub and shows a warning if outdated.
        """
        try:
            response = requests.get(LATEST_VERSION_URL, timeout=5)
            response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
            latest_version = response.text.strip()

            # Compare versions. Assuming semantic versioning (e.g., 1.0 < 1.1)
            # You might need a more robust version comparison for complex schemes.
            def parse_version(version_str):
                return tuple(map(int, version_str.split('.')))

            current_v = parse_version(SCRIPT_VERSION)
            latest_v = parse_version(latest_version)

            if latest_v > current_v:
                messagebox.showwarning(
                    "Outdated Version",
                    f"Your ArchInstall script (v{SCRIPT_VERSION}) is outdated.\n"
                    f"The latest version available is v{latest_version}.\n"
                    "It is recommended to download the newest version for the best experience.\n\n"
                    "Visit: https://github.com/Nakildias/Custom-ArchISO"
                )
        except requests.exceptions.ConnectionError:
            # More specific error for no internet connection
            print("Could not check for updates: No internet connection.")
        except requests.exceptions.Timeout:
            print("Could not check for updates: Connection timed out.")
        except requests.exceptions.RequestException as e:
            # Catch other request-related errors (e.g., HTTP errors)
            print(f"Could not check for updates: {e}")
        except ValueError:
            # Handle cases where version string might not be a valid number
            print(f"Could not parse version string from URL: '{latest_version}' or local: '{SCRIPT_VERSION}'")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred during update check: {e}")

    def create_frames(self):
        for F in (WelcomeFrame, DiskSelectionFrame, PartitioningFrame,
                  LocaleConfigFrame, UserConfigFrame, PackageSelectionFrame,
                  InstallationProgressFrame, SummaryFrame):
            frame = F(self, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, cont):
        frame = self.frames[cont]
        self.current_frame = frame
        frame.tkraise()
        if hasattr(frame, 'on_show'):
            frame.on_show()

    def get_var(self, name):
        return self.install_vars[name].get()

    def set_var(self, name, value):
        if isinstance(self.install_vars[name], tk.StringVar):
            self.install_vars[name].set(value)
        elif isinstance(self.install_vars[name], tk.BooleanVar):
            self.install_vars[name].set(bool(value))
        else:
            self.install_vars[name] = value

    def next_step(self):
        current_frame = self.current_frame
        
        if hasattr(current_frame, 'validate_and_next'):
            if not current_frame.validate_and_next():
                return

        if current_frame == self.frames[WelcomeFrame]:
            self.show_frame(DiskSelectionFrame)
        elif current_frame == self.frames[DiskSelectionFrame]:
            self.show_frame(PartitioningFrame)
        elif current_frame == self.frames[PartitioningFrame]:
            self.show_frame(LocaleConfigFrame)
        elif current_frame == self.frames[LocaleConfigFrame]:
            self.show_frame(UserConfigFrame)
        elif current_frame == self.frames[UserConfigFrame]:
            self.show_frame(PackageSelectionFrame)
        elif current_frame == self.frames[PackageSelectionFrame]:
            self.show_frame(InstallationProgressFrame)
            threading.Thread(target=self.current_frame.start_installation).start()
        elif current_frame == self.frames[InstallationProgressFrame]:
            self.show_frame(SummaryFrame)

    def prev_step(self):
        if self.current_frame == self.frames[DiskSelectionFrame]:
            self.show_frame(WelcomeFrame)
        elif self.current_frame == self.frames[PartitioningFrame]:
            self.show_frame(DiskSelectionFrame)
        elif self.current_frame == self.frames[LocaleConfigFrame]:
            self.show_frame(PartitioningFrame)
        elif self.current_frame == self.frames[UserConfigFrame]:
            self.show_frame(LocaleConfigFrame)
        elif self.current_frame == self.frames[PackageSelectionFrame]:
            self.show_frame(UserConfigFrame)
        elif self.current_frame == self.frames[InstallationProgressFrame]:
            self.show_frame(PackageSelectionFrame)

    def exit_installer(self):
        if messagebox.askyesno("Exit Installer", "Are you sure you want to exit?"):
            self.destroy()

# --- Base Frame Class ---
class BaseFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="TFrame")

        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.nav_frame = ttk.Frame(self, style="TFrame")
        self.nav_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        self.nav_frame.grid_columnconfigure(0, weight=1)
        self.nav_frame.grid_columnconfigure(1, weight=1)
        self.nav_frame.grid_columnconfigure(2, weight=1)
        self.nav_frame.grid_columnconfigure(3, weight=1)
        self.nav_frame.grid_columnconfigure(4, weight=1)

        self.back_button = ttk.Button(self.nav_frame, text="< Back", command=self.controller.prev_step)
        self.back_button.grid(row=0, column=0, sticky="w", padx=5)

        self.next_button = ttk.Button(self.nav_frame, text="Next >", command=self.controller.next_step)
        self.next_button.grid(row=0, column=4, sticky="e", padx=5)

        self.exit_button = ttk.Button(self.nav_frame, text="Exit", command=self.controller.exit_installer)
        self.exit_button.grid(row=0, column=3, sticky="e", padx=5)

    def on_show(self):
        pass

# --- Step 1: Welcome Frame ---
class WelcomeFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        main_frame = ttk.Frame(self, padding="50", style="TFrame")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(main_frame, text="Welcome to ArchInstall", style="Title.TLabel").grid(row=0, column=0, pady=0)
        ttk.Label(main_frame, text=f"Version: {SCRIPT_VERSION}", style="Subtitle.TLabel").grid(row=1, column=0, pady=0)
        ttk.Label(main_frame, text="").grid(row=2, column=0, pady=50)
        ttk.Label(main_frame, text="This application should only be used with the dedicated custom archiso.", wraplength=500, justify="center").grid(row=3, column=0, pady=10)
        ttk.Label(main_frame, text="If you find this installer useful please leave a star on github.").grid(row=4, column=0, pady=10)
        ttk.Label(main_frame, text="⚠ THIS TOOL WILL ERASE DATA ON THE SELECTED DISK ⚠", style="Warning.TLabel", wraplength=600).grid(row=5, column=0, pady=20)

        status_frame = ttk.Frame(main_frame, style="TFrame", padding=10, relief="solid", borderwidth=1)
        status_frame.grid(row=6, column=0, pady=20, sticky="ew")
        status_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(status_frame, text="Environment Status", style="Highlight.TLabel").grid(row=0, column=0, pady=(0, 10))

        ttk.Label(status_frame, text="Boot Mode:").grid(row=1, column=0, sticky="w", padx=10)
        ttk.Label(status_frame, textvariable=self.controller.install_vars["boot_mode"], style="Info.TLabel").grid(row=1, column=0, sticky="e", padx=10)

        status_frame.grid_columnconfigure(1, weight=0) 

        # Internet status labels
        ttk.Label(status_frame, text="Internet Connection:").grid(row=2, column=0, sticky="w", padx=10)
        self.internet_status_label = ttk.Label(status_frame, textvariable=self.controller.install_vars["internet_status"])
        self.internet_status_label.grid(row=2, column=0, sticky="e", padx=10)

        # Try Again button
        self.retry_button = ttk.Button(status_frame, text="Try Again", command=self.check_internet_connection)
        self.retry_button.grid(row=2, column=1, padx=5, sticky="w")
        self.retry_button.grid_remove() # Hide it until it's needed

        self.back_button.grid_remove()
        self.exit_button.grid(row=0, column=3, sticky="e", padx=5)
        self.next_button.grid(row=0, column=4, sticky="e", padx=5)

    def on_show(self):
        """Called every time the frame is shown."""
        # Set boot mode
        boot_mode = "UEFI" if os.path.isdir("/sys/firmware/efi/efivars") else "BIOS"
        self.controller.set_var("boot_mode", boot_mode)

        # Perform the internet check
        self.check_internet_connection()
    def check_internet_connection(self):
        """Checks internet by pinging multiple sites and updates the GUI."""
        # Update UI to show that a check is in progress
        self.controller.set_var("internet_status", "Checking...")
        self.internet_status_label.config(style="Info.TLabel")
        self.next_button.config(state="disabled") # Disable "Next" during the check
        self.retry_button.grid_remove()
        self.update_idletasks() # Force the UI to refresh immediately

        # Run the actual check in a separate thread to keep the GUI responsive
        threading.Thread(target=self._perform_check).start()

    def _perform_check(self):
        """The actual network checking logic to be run in a thread."""
        hosts_to_check = [
            "https://google.com",
            "https://archlinux.org",
            "https://wiki.archlinux.org",
            "https://wikipedia.org",
            "https://github.com"
        ]
        success_count = 0
        
        for host in hosts_to_check:
            try:
                # Use a shorter timeout for each individual request
                requests.get(host, timeout=3)
                success_count += 1
            except requests.RequestException:
                # If a single host fails, just continue to the next one
                print(f"Connection to {host} failed.")
                pass

        # --- Update GUI based on the results ---
        # Check if at least 50% of the hosts were reachable
        if success_count >= len(hosts_to_check) / 2:
            self.controller.set_var("internet_status", "Available")
            self.internet_status_label.config(style="Success.TLabel")
            self.next_button.config(state="normal")
            self.retry_button.grid_remove()
        else:
            self.controller.set_var("internet_status", "Unavailable")
            self.internet_status_label.config(style="Warning.TLabel")
            self.next_button.config(state="disabled")
            self.retry_button.grid()

# --- Step 2: Disk Selection Frame ---
class DiskSelectionFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.main_frame = ttk.Frame(self, padding="20", style="TFrame")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(self.main_frame, text="Select Installation Disk", style="Title.TLabel").grid(row=0, column=0, pady=10)
        ttk.Label(self.main_frame, text="Choose the disk you want yo install Arch Linux on, all data on the selected disk will be wiped.", wraplength=600, justify="center").grid(row=1, column=0, pady=5)

        self.disk_listbox = tk.Listbox(self.main_frame, height=10, width=60, font=("Fira Code", 10),
                                        bg=DRACULA_CURRENT_LINE, fg=DRACULA_FG,
                                        selectbackground=DRACULA_PURPLE, selectforeground=DRACULA_FG,
                                        borderwidth=1, relief="solid")
        self.disk_listbox.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")
        self.disk_listbox.bind("<<ListboxSelect>>", self.on_disk_select)

        self.refresh_button = ttk.Button(self.main_frame, text="Refresh Disks", command=self.populate_disks)
        self.refresh_button.grid(row=3, column=0, pady=5)

        ttk.Label(self.main_frame, text="Selected Disk:").grid(row=4, column=0, pady=(10,0))
        ttk.Label(self.main_frame, textvariable=self.controller.install_vars["target_disk"], style="Highlight.TLabel").grid(row=5, column=0)

        self.next_button.config(state="disabled")

    def on_show(self):
        self.populate_disks()
        
        selected_disk_name = self.controller.get_var("target_disk")
        if selected_disk_name:
            self.next_button.config(state="normal")
            for idx, item in enumerate(self.available_disks):
                if item["name"] == selected_disk_name:
                    self.disk_listbox.selection_set(idx)
                    self.disk_listbox.activate(idx)
                    break
        else:
            self.next_button.config(state="disabled")

    def populate_disks(self):
        self.disk_listbox.delete(0, tk.END)
        try:
            disks_output = run_command("lsblk -dnpo name,type,size,model")
            self.available_disks = []
            for line in disks_output.splitlines():
                parts = line.split()
                if len(parts) >= 3 and parts[1] == "disk":
                    name = parts[0]
                    size = parts[2]
                    model = " ".join(parts[3:]) if len(parts) > 3 else "N/A"
                    self.available_disks.append({"name": name, "size": size, "model": model})
                    self.disk_listbox.insert(tk.END, f"{name} ({size}) - {model}")
            if not self.available_disks:
                messagebox.showwarning("No Disks Found", "No disks found. Ensure drives are properly connected.")
                self.next_button.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Disk Detection Error", f"Failed to detect disks: {e}")
            self.next_button.config(state="disabled")

    def on_disk_select(self, event):
        selected_index = self.disk_listbox.curselection()
        if selected_index:
            disk_info = self.available_disks[selected_index[0]]
            disk_name = disk_info["name"]
            
            self.disk_listbox.config(state="disabled")
            
            if messagebox.askyesno("Confirm Disk Selection",
                                   f"WARNING: All data on {disk_name} will be ERASED!\nAre you absolutely sure you want to proceed?"):
                self.controller.set_var("target_disk", disk_name)
                self.next_button.config(state="normal")
            else:
                self.disk_listbox.selection_clear(0, tk.END)
                self.controller.set_var("target_disk", "")
                self.next_button.config(state="disabled")
            
            self.disk_listbox.config(state="normal")
        else:
            self.controller.set_var("target_disk", "")
            self.next_button.config(state="disabled")

    def validate_and_next(self):
        if self.controller.get_var("target_disk"):
            return True
        else:
            messagebox.showerror("Validation Error", "Please select a disk to continue.")
            return False

# --- Step 3: Partitioning Frame ---
class PartitioningFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        main_frame = ttk.Frame(self, padding="20", style="TFrame")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(main_frame, text="Partitioning Configuration", style="Title.TLabel").grid(row=0, column=0, pady=10)
        ttk.Label(main_frame, text="Define the sizes for your boot and swap partitions.", wraplength=500, justify="center").grid(row=1, column=0, pady=5)

        form_frame = ttk.Frame(main_frame)
        form_frame.grid(row=2, column=0, pady=20)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(form_frame, text="Boot Partition Size:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.boot_size_entry = ttk.Entry(form_frame, textvariable=self.controller.install_vars["boot_size"], width=30)
        self.boot_size_entry.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(form_frame, text=f"e.g., {MIN_BOOT_SIZE_MB}M 1G", style="Subtitle.TLabel").grid(row=3, column=0, sticky="w", padx=10)

        ttk.Label(form_frame, text="Swap Partition Size:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.swap_size_entry = ttk.Entry(form_frame, textvariable=self.controller.install_vars["swap_size"], width=30)
        self.swap_size_entry.grid(row=5, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(form_frame, text=f"e.g., 4G, 8G", style="Subtitle.TLabel").grid(row=6, column=0, sticky="w", padx=10)

        info_frame = ttk.Frame(main_frame, style="TFrame", padding=10, relief="solid", borderwidth=1)
        info_frame.grid(row=7, column=0, pady=20, sticky="ew")
        info_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(info_frame, text="Partitioning Information", style="Highlight.TLabel").grid(row=0, column=0, pady=(0, 10))
        ttk.Label(info_frame, textvariable=self.controller.install_vars["boot_mode"]).grid(row=1, column=0, pady=(0, 5))
        ttk.Label(info_frame, text="GPT partitioning scheme will be used for all installations.").grid(row=2, column=0, pady=(0, 5))
        ttk.Label(info_frame, text="For Legacy BIOS, a BIOS Boot Partition will be created.").grid(row=3, column=0)

    def validate_and_next(self):
        boot_size = self.controller.get_var("boot_size").strip().upper()
        swap_size = self.controller.get_var("swap_size").strip().upper()

        if not re.fullmatch(r"^\d+[MG]$", boot_size):
            messagebox.showerror("Invalid Input", "Boot size must be a number followed by M or G (e.g., 550M, 1G).")
            return False
        
        boot_size_num = int(re.match(r"(\d+)", boot_size).group(1))
        boot_size_unit = re.search(r"([MG])$", boot_size).group(1)
        boot_size_mb = boot_size_num * 1024 if boot_size_unit == "G" else boot_size_num

        if boot_size_mb < MIN_BOOT_SIZE_MB:
            messagebox.showerror("Invalid Input", f"Boot size must be at least {MIN_BOOT_SIZE_MB}M.")
            return False

        if swap_size and not re.fullmatch(r"^\d+[MG]$", swap_size):
            messagebox.showerror("Invalid Input", "Swap size must be a number followed by M or G (e.g., 4G, 512M) or left blank.")
            return False
        
        # The final disk is now confirmed in the next step. We only set the partition prefix here.
        # This also removes the incorrect/unnecessary partition number assignments.
        target_disk = self.controller.get_var("target_disk")
        if not target_disk:
            messagebox.showerror("Disk Error", "Target disk not set. Please go back to Disk Selection.")
            return False

        if "nvme" in target_disk or "mmcblk" in target_disk:
            partition_prefix = f"{target_disk}p"
        else:
            partition_prefix = target_disk
        self.controller.set_var("partition_prefix", partition_prefix)

        return True

# --- Step 3.5: Locale Configuration Frame ---
class LocaleConfigFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        main_frame = ttk.Frame(self, padding="20", style="TFrame")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(main_frame, text="Locale Configuration", style="Title.TLabel").grid(row=0, column=0, pady=10)
        ttk.Label(main_frame, text="Set your region, timezone, and keyboard layout for the new system.", wraplength=500, justify="center").grid(row=1, column=0, pady=5)
        
        form_frame = ttk.Frame(main_frame)
        form_frame.grid(row=2, column=0, pady=20)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(form_frame, text="Time Zone Region:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.region_combobox = ttk.Combobox(form_frame, textvariable=self.controller.install_vars["region"], state="readonly")
        self.region_combobox.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        self.region_combobox.bind("<<ComboboxSelected>>", self.update_cities)
        
        ttk.Label(form_frame, text="Time Zone City:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.city_combobox = ttk.Combobox(form_frame, textvariable=self.controller.install_vars["city"], state="readonly")
        self.city_combobox.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        ttk.Label(form_frame, text="Keyboard Layout:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.keyboard_combobox = ttk.Combobox(form_frame, textvariable=self.controller.install_vars["keyboard_layout"], state="readonly")
        self.keyboard_combobox.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        
    def on_show(self):
        self.populate_locales()

    def populate_locales(self):
        try:
            regions_output = run_command("ls /usr/share/zoneinfo")
            regions = sorted([r for r in regions_output.splitlines() if r[0].isupper()])
            self.region_combobox["values"] = regions
            if self.controller.get_var("region") not in regions:
                    self.controller.set_var("region", "America" if "America" in regions else regions[0])
            self.update_cities()
        except Exception:
            messagebox.showwarning("Locale Error", "Could not load time zone regions. Defaulting to America/Toronto.")
            self.region_combobox["values"] = ["America"]
            self.city_combobox["values"] = ["Toronto"]

        try:
            keyboard_layouts_output = run_command("localectl list-x11-keymap-layouts")
            layouts = sorted(keyboard_layouts_output.splitlines())
            self.keyboard_combobox["values"] = layouts
            if self.controller.get_var("keyboard_layout") not in layouts:
                self.controller.set_var("keyboard_layout", "us" if "us" in layouts else layouts[0])
        except Exception:
            messagebox.showwarning("Keyboard Layout Error", "Could not load keyboard layouts. Defaulting to 'us'.")
            self.keyboard_combobox["values"] = ["us"]
            self.controller.set_var("keyboard_layout", "us")

    def update_cities(self, event=None):
        selected_region = self.controller.get_var("region")
        try:
            cities_output = run_command(f"ls /usr/share/zoneinfo/{selected_region}")
            cities = sorted(cities_output.splitlines())
            self.city_combobox["values"] = cities
            if self.controller.get_var("city") not in cities:
                self.controller.set_var("city", "Toronto" if "Toronto" in cities else cities[0])
        except Exception:
            messagebox.showwarning("Timezone Error", f"Could not load cities for region '{selected_region}'.")
            self.city_combobox["values"] = [""]
            self.controller.set_var("city", "")
    
    def validate_and_next(self):
        return True

# --- Step 4: User and Hostname Configuration Frame ---
class UserConfigFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        main_frame = ttk.Frame(self, padding="20", style="TFrame")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(main_frame, text="System and User Configuration", style="Title.TLabel").grid(row=0, column=0, pady=10)

        form_frame = ttk.Frame(main_frame)
        form_frame.grid(row=1, column=0, pady=20)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(form_frame, text="Hostname:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.hostname_entry = ttk.Entry(form_frame, textvariable=self.controller.install_vars["hostname"], width=40)
        self.hostname_entry.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        ttk.Label(form_frame, text="Primary Username:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.username_entry = ttk.Entry(form_frame, textvariable=self.controller.install_vars["username"], width=40)
        self.username_entry.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        ttk.Label(form_frame, text="User Password:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.user_pass_entry = ttk.Entry(form_frame, show="*", width=40)
        self.user_pass_entry.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        ttk.Label(form_frame, text="Confirm User Password:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.user_pass_confirm_entry = ttk.Entry(form_frame, show="*", width=40)
        self.user_pass_confirm_entry.grid(row=3, column=1, sticky="w", padx=10, pady=5)
        
        self.enable_root_check = ttk.Checkbutton(form_frame, text="Enable the root user?",
                                                 variable=self.controller.install_vars["enable_root_account"],
                                                 command=self.toggle_root_entries)
        self.enable_root_check.grid(row=4, column=0, sticky="w", columnspan=2, pady=(15, 5), padx=10)

        ttk.Label(form_frame, text="Root Password:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.root_pass_entry = ttk.Entry(form_frame, show="*", width=40)
        self.root_pass_entry.grid(row=5, column=1, sticky="w", padx=10, pady=5)

        ttk.Label(form_frame, text="Confirm Root Password:").grid(row=6, column=0, sticky="w", padx=10, pady=5)
        self.root_pass_confirm_entry = ttk.Entry(form_frame, show="*", width=40)
        self.root_pass_confirm_entry.grid(row=6, column=1, sticky="w", padx=10, pady=5)
        
        self.toggle_root_entries()

    def toggle_root_entries(self):
        state = "normal" if self.controller.get_var("enable_root_account") else "disabled"
        self.root_pass_entry.config(state=state)
        self.root_pass_confirm_entry.config(state=state)

    def validate_and_next(self):
        hostname = self.controller.get_var("hostname").strip()
        username = self.controller.get_var("username").strip()
        user_pass = self.user_pass_entry.get()
        user_pass_confirm = self.user_pass_confirm_entry.get()

        if not hostname or " " in hostname or "'" in hostname or "\"" in hostname:
            messagebox.showerror("Invalid Input", "Hostname cannot be empty and should not contain spaces or quotes.")
            return False

        if not username or " " in username or "'" in username or "\"" in username:
            messagebox.showerror("Invalid Input", "Username cannot be empty and should not contain spaces or quotes.")
            return False

        if not user_pass:
            messagebox.showerror("Invalid Input", "User password cannot be empty.")
            return False
        if user_pass != user_pass_confirm:
            messagebox.showerror("Invalid Input", "User passwords do not match.")
            return False

        if self.controller.get_var("enable_root_account"):
            root_pass = self.root_pass_entry.get()
            root_pass_confirm = self.root_pass_confirm_entry.get()
            if not root_pass:
                messagebox.showerror("Invalid Input", "Root password cannot be empty.")
                return False
            if root_pass != root_pass_confirm:
                messagebox.showerror("Invalid Input", "Root passwords do not match.")
                return False
            self.controller.set_var("root_password", root_pass)
        else:
            self.controller.set_var("root_password", "")

        self.controller.set_var("user_password", user_pass)
        return True

# --- Step 5: Package Selection Frame ---
class PackageSelectionFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.package_profiles = PACKAGE_PROFILES.copy()

        main_frame = ttk.Frame(self, padding="20", style="TFrame")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(main_frame, text="Package Selection", style="Title.TLabel").grid(row=0, column=0, pady=10)

        form_frame = ttk.Frame(main_frame)
        form_frame.grid(row=1, column=0, pady=20)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(form_frame, text="Select Kernel:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        kernels = ["linux", "linux-lts", "linux-zen"]
        self.kernel_combobox = ttk.Combobox(form_frame, textvariable=self.controller.install_vars["selected_kernel"], values=kernels, state="readonly", width=25)
        self.kernel_combobox.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        self.kernel_combobox.set("linux")

        ttk.Label(form_frame, text="Select Desktop Environment/Server:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        desktops = list(self.package_profiles.keys())
        self.de_combobox = ttk.Combobox(form_frame, textvariable=self.controller.install_vars["selected_de_name"], values=desktops, state="readonly", width=25)
        self.de_combobox.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        self.de_combobox.set("Server (No GUI)")
        
        self.customize_button = ttk.Button(form_frame, text="Customize", command=self.open_customize_window)
        self.customize_button.grid(row=1, column=2, sticky="w", padx=10)
        
        self.options_frame = ttk.Frame(main_frame)
        self.options_frame.grid(row=2, column=0, pady=20)
        self.options_frame.grid_columnconfigure(0, weight=1)
        self.options_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(self.options_frame, text="Optional Packages:", style="Highlight.TLabel").grid(row=0, column=0, sticky="w", columnspan=2, pady=(10,0))
        
        self.steam_check = ttk.Checkbutton(self.options_frame, text="Install Steam (enables multilib)", variable=self.controller.install_vars["install_steam"])
        self.steam_check.grid(row=1, column=0, sticky="w", padx=10)

        self.discord_check = ttk.Checkbutton(self.options_frame, text="Install Discord", variable=self.controller.install_vars["install_discord"])
        self.discord_check.grid(row=1, column=1, sticky="w", padx=10)

        self.multilib_check = ttk.Checkbutton(self.options_frame, text="Enable Multilib Repository (even if Steam not selected)", variable=self.controller.install_vars["enable_multilib"])
        self.multilib_check.grid(row=2, column=0, sticky="w", padx=10)
        
        # Update the Oh My Zsh checkbox to have a command
        self.oh_my_zsh_check = ttk.Checkbutton(self.options_frame, text="Install Oh My Zsh",
                                               variable=self.controller.install_vars["install_oh_my_zsh"],
                                               command=self.toggle_zsh_theme_selector)
        self.oh_my_zsh_check.grid(row=2, column=1, sticky="w", padx=10)

        # --- Create a new frame for the Zsh options ---
        self.zsh_options_frame = ttk.Frame(self.options_frame)
        self.zsh_options_frame.grid(row=3, column=0, columnspan=3, sticky='w', padx=20) # This frame will be shown/hidden

        # Add theme selector dropdown
        ttk.Label(self.zsh_options_frame, text="Zsh Theme:").grid(row=0, column=0, sticky="w", pady=2)
        zsh_themes = [
            "agnoster", "robbyrussell", "amuse", "avit", "bira", "bureau",
            "candy", "cloud", "crcandy", "cypher", "dallas", "fino-time", "fishy",
            "fox", "gallois", "half-life", "jnrowe", "jonathan", "lambda",
            "minimal", "murilasso", "norm", "obraun", "pygmalion", "refined",
            "sorin", "steeef", "sunrise", "ys"
        ]
        self.zsh_theme_combobox = ttk.Combobox(self.zsh_options_frame,
                                               textvariable=self.controller.install_vars["zsh_theme"],
                                               values=zsh_themes, state="readonly", width=25)
        self.zsh_theme_combobox.grid(row=0, column=1, sticky="w", padx=5)

        # --- Add label and button for theme previews ---
        def print_themes_link():
            link = "https://github.com/ohmyzsh/ohmyzsh/wiki/themes"
            print("\n" + "="*40)
            print("Oh My Zsh Themes Preview Link:")
            print(link)
            print("="*40 + "\n")
            messagebox.showinfo("Link Printed", f"The themes link has been printed to the terminal for easy access:\n\n{link}")

        ttk.Label(self.zsh_options_frame, text="To see theme previews:", style="Subtitle.TLabel").grid(row=1, column=0, sticky="w", pady=(5,0))
        self.themes_link_button = ttk.Button(self.zsh_options_frame, text="Print Link to Terminal", command=print_themes_link)
        self.themes_link_button.grid(row=1, column=1, sticky="w", padx=5, pady=(5,0))

        # Call the toggle function once to set the initial state
        self.toggle_zsh_theme_selector()
        
        ttk.Label(self.options_frame, text="Installation Options:", style="Highlight.TLabel").grid(row=3, column=0, sticky="w", columnspan=2, pady=(90,0))
        self.log_file_check = ttk.Checkbutton(self.options_frame, text="Save installation log to ./logs_archinstall.txt",
                                              variable=self.controller.install_vars["log_to_file"])
        self.log_file_check.grid(row=4, column=0, sticky="w", columnspan=2, padx=10)

        self.reflector_check = ttk.Checkbutton(self.options_frame, text="Use Reflector to find fastest mirrors (Recommended)",
                                               variable=self.controller.install_vars["use_reflector"])
        self.reflector_check.grid(row=5, column=0, sticky="w", columnspan=2, padx=10)


    def validate_and_next(self):
        selected_profile = self.controller.get_var("selected_de_name")
        self.controller.set_var("package_list", " ".join(self.package_profiles[selected_profile]))

        # At the final step before installation, confirm the target disk and lock it in.
        # This prevents the state from being lost if the user navigates back and forth.
        target_disk = self.controller.get_var("target_disk")
        if not target_disk:
            messagebox.showerror("Disk Not Selected", "No installation disk is selected. Please go back and choose a disk.")
            return False
            
        self.controller.set_var("final_target_disk", target_disk)
        return True
        
    def toggle_zsh_theme_selector(self):
        """Shows or hides the Zsh theme dropdown based on the checkbox state."""
        if self.controller.get_var("install_oh_my_zsh"):
            self.zsh_options_frame.grid()
        else:
            self.zsh_options_frame.grid_remove()
            
    def open_customize_window(self):
        profile_name = self.controller.get_var("selected_de_name")
        package_list_str = " ".join(self.package_profiles[profile_name])

        custom_window = tk.Toplevel(self)
        custom_window.title(f"Customize {profile_name}")
        custom_window.geometry("500x400")
        custom_window.config(bg=DRACULA_BG)
        custom_window.grab_set()

        frame = ttk.Frame(custom_window, padding=10)
        frame.pack(expand=True, fill="both")
        
        ttk.Label(frame, text=f"Edit packages for '{profile_name}':", style="Highlight.TLabel").pack(pady=10)
        
        text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=15, bg=DRACULA_CURRENT_LINE, fg=DRACULA_FG, insertbackground=DRACULA_PURPLE, selectbackground=DRACULA_PURPLE)
        text_widget.pack(expand=True, fill="both", padx=5, pady=5)
        text_widget.insert(tk.END, package_list_str)

        def save_packages():
            new_list = text_widget.get("1.0", tk.END).strip().split()
            self.package_profiles[profile_name] = new_list
            custom_window.destroy()

        def close_window():
            custom_window.destroy()

        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(button_frame, text="Save", command=save_packages).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Cancel", command=close_window).pack(side="right", padx=5)

# --- Step 6: Installation Progress Frame ---
class InstallationProgressFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        main_frame = ttk.Frame(self, padding="20", style="TFrame")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(main_frame, text="Installation Progress", style="Title.TLabel").grid(row=0, column=0, pady=10)

        self.progress_label = ttk.Label(main_frame, text="Initializing installation...", font=("Fira Code", 12), foreground=DRACULA_CYAN)
        self.progress_label.grid(row=1, column=0, pady=10)

        self.progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=600, mode="determinate", style="Horizontal.TProgressbar")
        self.progress_bar.grid(row=2, column=0, pady=10)

        self.log_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=90, height=20, font=("Fira Code", 9),
                                                 bg=DRACULA_CURRENT_LINE, fg=DRACULA_FG,
                                                 insertbackground=DRACULA_PURPLE, selectbackground=DRACULA_PURPLE, selectforeground=DRACULA_FG)
        self.log_text.grid(row=3, column=0, pady=10, sticky="nsew")
        self.log_text.tag_config("info", foreground=DRACULA_CYAN)
        self.log_text.tag_config("success", foreground=DRACULA_GREEN)
        self.log_text.tag_config("warn", foreground=DRACULA_ORANGE)
        self.log_text.tag_config("error", foreground=DRACULA_RED)
        
        self.log_file = None
        self.log_file_path = "./logs_archinstall.txt"

        self.next_button.config(state="disabled")
        self.back_button.config(state="disabled")

    def open_log_file(self):
        if self.controller.get_var("log_to_file"):
            try:
                self.log_file = open(self.log_file_path, "w")
                self.update_progress(f"[INFO] Logging to {self.log_file_path}", tag="info")
            except Exception as e:
                self.update_progress(f"[WARNING] Could not open log file: {e}", tag="warn")
                self.log_file = None

    def close_log_file(self):
        if self.log_file:
            self.log_file.close()

    def update_progress(self, message, progress=None, tag="info"):
        self.log_text.insert(tk.END, message + "\n", tag)
        self.log_text.see(tk.END)
        self.progress_label.config(text=message)
        if self.log_file:
            self.log_file.write(message + "\n")
            self.log_file.flush()
        if progress is not None:
            self.progress_bar["value"] = progress
        self.update_idletasks()

    def log_variables(self):
        self.update_progress("[INFO] --- Installation Variables Snapshot ---", tag="info")
        for key, value in self.controller.install_vars.items():
            if isinstance(value, (tk.StringVar, tk.BooleanVar)):
                self.update_progress(f"  - {key}: {value.get()}", tag="info")
            elif isinstance(value, str) and ("password" in key or "token" in key):
                self.update_progress(f"  - {key}: [REDACTED]", tag="info")
            else:
                self.update_progress(f"  - {key}: {value}", tag="info")
        self.update_progress("--- End of Snapshot ---", tag="info")

    def run_install_command(self, command, description, expected_status=0):
        self.update_progress(f"[INFO] {description}...", tag="info")
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
            
            for line in process.stdout:
                self.log_text.insert(tk.END, "  " + line, "info")
                self.log_text.see(tk.END)
                if self.log_file:
                    self.log_file.write("  " + line)
                    self.log_file.flush()
                self.update_idletasks()

            process.wait()
            
            if process.returncode == expected_status:
                self.update_progress(f"[SUCCESS] {description} completed.", tag="success")
                return True
            else:
                self.update_progress(f"[ERROR] {description} failed with exit code {process.returncode}.", tag="error")
                messagebox.showerror("Installation Error", f"{description} failed. Check log for details.")
                self.log_variables()
                raise subprocess.CalledProcessError(process.returncode, command, output=self.log_text.get("1.0", tk.END))
        except Exception as e:
            self.update_progress(f"[CRITICAL ERROR] Failed during {description}: {e}", tag="error")
            messagebox.showerror("Installation Aborted", f"Installation aborted due to error during {description}.")
            self.log_variables()
            self.close_log_file()
            self.controller.exit_installer()
            return False

    def start_installation(self):
        self.open_log_file()
        self.update_progress("Starting Arch Linux installation...", 0)
        self.log_variables()

        try:
            # Use the new, reliably set variable here
            target_disk = self.controller.get_var("final_target_disk")
            if not target_disk:
                self.update_progress("[ERROR] No target disk was selected. Aborting installation.", tag="error")
                messagebox.showerror("Disk Selection Error", "No target disk was selected. Please restart and choose a disk.")
                self.close_log_file()
                self.controller.exit_installer()
                return

            boot_mode = self.controller.get_var("boot_mode")
            boot_size_input = self.controller.get_var("boot_size")
            swap_size_input = self.controller.get_var("swap_size")
            hostname = self.controller.get_var("hostname")
            username = self.controller.get_var("username")
            user_password = self.controller.install_vars["user_password"]
            root_password = self.controller.install_vars["root_password"]
            enable_root = self.controller.get_var("enable_root_account")
            install_oh_my_zsh = self.controller.get_var("install_oh_my_zsh")
            selected_kernel = self.controller.get_var("selected_kernel")
            selected_de_name = self.controller.get_var("selected_de_name")
            package_list_str = self.controller.get_var("package_list")
            install_steam = self.controller.get_var("install_steam")
            install_discord = self.controller.get_var("install_discord")
            enable_multilib = self.controller.get_var("enable_multilib")
            partition_prefix = self.controller.get_var("partition_prefix")
            region = self.controller.get_var("region")
            city = self.controller.get_var("city")
            keyboard_layout = self.controller.get_var("keyboard_layout")
            use_reflector = self.controller.get_var("use_reflector")
            zsh_theme = self.controller.get_var("zsh_theme")

            de_pkgs = package_list_str.split()
            optional_pkgs = []
            if install_steam: optional_pkgs.append("steam")
            if install_discord: optional_pkgs.append("discord")
            base_pkgs = {
                "base":             "A metapackage with the bare minimum for a functional system.",
                selected_kernel:    "The Linux kernel, the core of the operating system.",
                "linux-firmware":   "Firmware files required by many hardware drivers.",
                "base-devel":       "Essential tools for building/compiling software (e.g., gcc, make).",
                "grub":             "The GRand Unified Bootloader, for loading the operating system.",
                "gptfdisk":         "Tools for managing GUID Partition Table (GPT) disks.",
                "networkmanager":   "A service that automatically manages network connections.",
                "nano":             "A simple, user-friendly command-line text editor.",
                "vim":              "A highly configurable and powerful command-line text editor.",
                "git":              "A distributed version control system for tracking code.",
                "wget":             "A non-interactive network downloader for fetching files.",
                "curl":             "A versatile command-line tool for transferring data with URLs.",
                "reflector":        "A script to retrieve and sort the fastest repository mirrors.",
                "zsh":              "The Z shell, a powerful and popular alternative to Bash."
            }
            if boot_mode == "UEFI":
                base_pkgs["efibootmgr"] = "Boot manager for UEFI systems."

            cpu_vendor = run_command("grep -m 1 'vendor_id' /proc/cpuinfo | awk '{print $3}'")
            microcode_package = ""
            if "GenuineIntel" in cpu_vendor:
                microcode_package = "intel-ucode"
            elif "AuthenticAMD" in cpu_vendor:
                microcode_package = "amd-ucode"
            
            if microcode_package:
                base_pkgs[microcode_package] = "Processor microcode for CPU stability and security."

            # If Oh My Zsh is being installed, add the required fonts for themes like agnoster.
            if install_oh_my_zsh:
                base_pkgs["powerline-fonts"] = "Fonts for powerline-like shells and themes (e.g., agnoster)."
            
            base_pkgs_list = list(base_pkgs.keys())
            all_pkgs = base_pkgs_list + de_pkgs + optional_pkgs

            
            # OPTIMIZATION 1: Faster Mirror Setup
            self.update_progress("Configuring Pacman mirrors...", 5)
            # Always back up the original mirrorlist, just in case
            if not self.run_install_command("cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.backup", "Backing up original mirrorlist"): return

            if use_reflector:
                self.update_progress("Using Reflector to find fastest mirrors...", tag="info")
                if not self.run_install_command("reflector --verbose --protocol https --country 'Canada' --latest 20 --sort rate --save /etc/pacman.d/mirrorlist", "Configuring mirrors with Reflector"): return
            else:
                self.update_progress("Skipping Reflector. Using existing mirrorlist.", tag="warn")
            
            # PACMAN.CONF LIVE ENVIRONMENT OVERWRITE
            self.update_progress("Overwriting live environment pacman.conf to enable repositories...", tag="info")
            live_pacman_conf_content = """
[options]
HoldPkg         = pacman glibc
Architecture = auto
Color
ParallelDownloads = 5
CheckSpace
[core]
Include = /etc/pacman.d/mirrorlist
[extra]
Include = /etc/pacman.d/mirrorlist
"""
            if install_steam or enable_multilib:
                live_pacman_conf_content += """
[multilib]
Include = /etc/pacman.d/mirrorlist
"""
            
            try:
                with open("/etc/pacman.conf", "w") as f:
                    f.write(live_pacman_conf_content)
                self.update_progress("Successfully wrote updated pacman.conf for live environment.", tag="success")
            except Exception as e:
                self.update_progress(f"[ERROR] Failed to write pacman.conf for live environment: {e}", tag="error")
                messagebox.showerror("Configuration Error", "Failed to write pacman.conf for live environment. Aborting.")
                self.close_log_file()
                self.controller.exit_installer()
                return

            # Synchronize package databases
            if not self.run_install_command("pacman -Syy --noconfirm", "Synchronizing package databases"): return
            if not self.run_install_command("pacman -Sy archlinux-keyring --noconfirm", "Updating archlinux-keyring"): return
            
            # 2. Partition and Format
            self.update_progress("Partitioning and formatting disk...", 15)
            self.update_progress(f"Ensuring all partitions on {target_disk} are unmounted...", tag="info")
            if not self.run_install_command(f"umount -R {target_disk} || true", "Unmounting existing partitions"): return

            # Partitioning commands... (using the corrected sequential logic)
            if not self.run_install_command(f"wipefs --all --force {target_disk} >/dev/null 2>&1 || true && sgdisk --zap-all {target_disk}", f"Wiping disk {target_disk}"): return
            if not self.run_install_command(f"sgdisk -og {target_disk}", f"Initializing GPT on {target_disk}"): return

            part_num = 1
            if boot_mode == "BIOS":
                if not self.run_install_command(f"sgdisk -n {part_num}:0:+1M -t {part_num}:EF02 -c {part_num}:\"BIOSBootPartition\" {target_disk}", f"Creating BIOS Boot partition"): return
                self.controller.set_var("bios_boot_partition", f"{partition_prefix}{part_num}")
                part_num += 1

            boot_part_num = part_num
            boot_type = "EF00" if boot_mode == "UEFI" else "8300"
            boot_name = "EFISystem" if boot_mode == "UEFI" else "LinuxBoot"
            if not self.run_install_command(f"sgdisk -n {boot_part_num}:0:+{boot_size_input} -t {boot_part_num}:{boot_type} -c {boot_part_num}:\"{boot_name}\" {target_disk}", f"Creating boot partition"): return
            self.controller.set_var("boot_partition", f"{partition_prefix}{boot_part_num}")
            part_num += 1

            if swap_size_input:
                swap_part_num = part_num
                if not self.run_install_command(f"sgdisk -n {swap_part_num}:0:+{swap_size_input} -t {swap_part_num}:8200 -c {swap_part_num}:\"LinuxSwap\" {target_disk}", f"Creating swap partition"): return
                self.controller.set_var("swap_partition", f"{partition_prefix}{swap_part_num}")
                part_num += 1

            root_part_num = part_num
            if not self.run_install_command(f"sgdisk -n {root_part_num}:0:0 -t {root_part_num}:8300 -c {root_part_num}:\"LinuxRoot\" {target_disk}", f"Creating root partition"): return
            self.controller.set_var("root_partition", f"{partition_prefix}{root_part_num}")

            if not self.run_install_command(f"sync && sleep 1 && partprobe {target_disk}", "Rereading partition table"): return
            time.sleep(2)

            root_partition_path = self.controller.get_var("root_partition")
            boot_partition_path = self.controller.get_var("boot_partition")
            swap_partition_path = self.controller.get_var("swap_partition")

            if not self.run_install_command(f"mkfs.ext4 -F {root_partition_path}", f"Formatting root {root_partition_path}"): return
            if boot_mode == "UEFI":
                if not self.run_install_command(f"mkfs.fat -F32 {boot_partition_path}", f"Formatting boot {boot_partition_path} as FAT32"): return
            else:
                if not self.run_install_command(f"mkfs.ext4 -F {boot_partition_path}", f"Formatting boot {boot_partition_path} as ext4"): return

            if swap_size_input:
                if not self.run_install_command(f"mkswap {swap_partition_path}", f"Formatting swap {swap_partition_path}"): return
            self.update_progress("Disk partitioning and formatting complete.", 25, tag="success")

            # 3. Mount Filesystems
            self.update_progress("Mounting filesystems...", 30)
            if not self.run_install_command(f"mount {root_partition_path} /mnt", "Mounting root"): return
            if not self.run_install_command(f"mount --mkdir {boot_partition_path} /mnt/boot", "Mounting boot"): return
            if swap_size_input:
                if not self.run_install_command(f"swapon {swap_partition_path}", "Activating swap"): return
            self.update_progress("Filesystems mounted.", 35, tag="success")

            # 4. Install Base System
            self.update_progress("Installing base system and packages (pacstrap)... This will take a while.", 40)
            pacstrap_cmd = ["pacstrap", "-K", "/mnt"] + all_pkgs
            if not self.run_install_command(" ".join(pacstrap_cmd), "Installing base system via pacstrap"): return
            self.update_progress("Base system installed.", 60, tag="success")

            # 5. Configure Installed System (chroot)
            self.update_progress("Configuring installed system in chroot...", 70)
            
            # --- START OF THE CORRECTLY INDENTED BLOCK ---
            if not self.run_install_command("genfstab -U /mnt >> /mnt/etc/fstab", "Generating fstab"): return

            # This section correctly writes the pacman.conf for the NEW system inside /mnt
            self.update_progress("Configuring pacman.conf in chroot...", tag="info")
            pacman_conf_content = """
[options]
HoldPkg         = pacman glibc
Architecture = auto
Color
ParallelDownloads = 5
CheckSpace
[core]
Include = /etc/pacman.d/mirrorlist
[extra]
Include = /etc/pacman.d/mirrorlist
"""
            if install_steam or enable_multilib:
                pacman_conf_content += """
[multilib]
Include = /etc/pacman.d/mirrorlist
"""
            pacman_conf_path = "/mnt/etc/pacman.conf"
            with open(pacman_conf_path, "w") as f:
                f.write(pacman_conf_content)

            # Ensure the mirrorlist is copied to the new system's chroot
            if not self.run_install_command("cp /etc/pacman.d/mirrorlist /mnt/etc/pacman.d/mirrorlist", "Copying mirrorlist to chroot"): return

            # STEP 1: Define the initial part of the chroot script
            chroot_script_content = rf"""#!/bin/bash
set -e
set -o pipefail

info() {{ echo "[CHROOT INFO] $1"; }}
error() {{ echo "[CHROOT ERROR] $1"; exit 1; }}

info "Setting timezone to {region}/{city}..."
ln -sf "/usr/share/zoneinfo/{region}/{city}" /etc/localtime
hwclock --systohc

info "Configuring Locale (en_US.UTF-8)..."
echo "en_US.UTF-8 UTF-8" > /etc/locale.gen
locale-gen
echo "LANG=en_US.UTF-8" > /etc/locale.conf
echo "KEYMAP={keyboard_layout}" > /etc/vconsole.conf

info "Setting hostname to '{hostname}'..."
echo "{hostname}" > /etc/hostname
cat <<EOF_HOSTS > /etc/hosts
127.0.0.1           localhost
::1                 localhost
127.0.1.1           {hostname}.localdomain {hostname}
EOF_HOSTS

enable_root={str(enable_root).lower()}
if [ "$enable_root" = "true" ]; then
  info "Setting root password..."
  echo "root:{root_password}" | chpasswd
else
  info "Root account will be locked. Use sudo."
  passwd -d root &>/dev/null && passwd -l root &>/dev/null
fi

info "Creating user '{username}' and adding to wheel group..."
useradd -m -G wheel -s /bin/zsh "{username}"
echo "{username}:{user_password}" | chpasswd

info "Configuring sudo for 'wheel' group..."
echo '%wheel ALL=(ALL:ALL) ALL' > /etc/sudoers.d/10-wheel-sudo
chmod 440 /etc/sudoers.d/10-wheel-sudo

info "Enabling NetworkManager service..."
systemctl enable NetworkManager.service
"""
            # STEP 2: Use Python logic to determine the display manager
            enable_dm = ""
            if selected_de_name in ["KDE Plasma", "KDE Plasma (Nakildias Profile)", "LXQt"]:
                enable_dm = "sddm"
            elif selected_de_name == "GNOME":
                enable_dm = "gdm"
            elif selected_de_name in ["XFCE", "Cinnamon", "MATE", "Budgie", "i3 (Tiling WM)"]:
                enable_dm = "lightdm"
            elif selected_de_name == "Sway (Tiling WM)":
                enable_dm = "ly"

            # STEP 3: Conditionally append the display manager command
            if enable_dm:
                chroot_script_content += f"""
info "Enabling Display Manager service ({enable_dm})..."
systemctl enable {enable_dm}.service
"""
            # STEP 4: Append the final part of the chroot script
            chroot_script_content += f"""
if pacman -Qs openssh &>/dev/null; then info "Enabling sshd service..."; systemctl enable sshd.service; fi
if pacman -Q cups &>/dev/null; then info "Enabling cups service..."; systemctl enable cups.service; fi
if pacman -Qs bluez &>/dev/null && pacman -Qs bluez-utils &>/dev/null; then info "Enabling bluetooth service..."; systemctl enable bluetooth.service; fi

info "Updating initial ramdisk environment (mkinitcpio)..."
mkinitcpio -P
"""
            
            with open("/mnt/configure_chroot.sh", "w") as f:
                f.write(chroot_script_content)
            os.chmod("/mnt/configure_chroot.sh", 0o755)

            if not self.run_install_command("arch-chroot /mnt /configure_chroot.sh", "Executing chroot configuration script"): return
            if not self.run_install_command("rm /mnt/configure_chroot.sh", "Removing chroot script"): return
            self.update_progress("System configured inside chroot.", 80, tag="success")

            # 6. Install Bootloader
            self.update_progress("Installing and configuring GRUB bootloader...", 85)
            if boot_mode == "UEFI":
                if not self.run_install_command("arch-chroot /mnt grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=ARCH --recheck", "Installing GRUB for UEFI"): return
            else: # BIOS
                if not self.run_install_command(f"arch-chroot /mnt grub-install --target=i386-pc --recheck {target_disk}", f"Installing GRUB for BIOS on {target_disk}"): return
            
            if not self.run_install_command("arch-chroot /mnt grub-mkconfig -o /boot/grub/grub.cfg", "Generating GRUB configuration"): return
            self.update_progress("GRUB bootloader installed.", 90, tag="success")

            # 7. Install Oh My Zsh (Optional)

            if install_oh_my_zsh:
                self.update_progress("Installing Oh My Zsh...", 92)
                ohmyzsh_script = f"""
#!/bin/bash
set -e
info() {{ echo "[CHROOT INFO] $1"; }}

install_for_user() {{
    local user="$1"
    local theme="$2"
    local user_home
    if [ "$user" = "root" ]; then user_home="/root"; else user_home="/home/$user"; fi
    
    info "Installing Oh My Zsh for '$user'..."
    # Attempt to install using curl, fall back to wget
    sudo -u "$user" env HOME="$user_home" RUNZSH=no CHSH=no sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended || \
    sudo -u "$user" env HOME="$user_home" RUNZSH=no CHSH=no sh -c "$(wget -qO- https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
    
    # Set the Zsh theme if the .zshrc file exists
    if [ -f "$user_home/.zshrc" ]; then
        sed -i "s/^ZSH_THEME=.*/ZSH_THEME=\\"$theme\\"/g" "$user_home/.zshrc"
    fi
}}

# Install for the created user
install_for_user "{username}" "{zsh_theme}"

# Install for root if enabled
if [ "{str(enable_root).lower()}" = "true" ]; then
    install_for_user "root" "robbyrussell"
fi
"""
                with open("/mnt/install_ohmyzsh.sh", "w") as f:
                    f.write(ohmyzsh_script)
                os.chmod("/mnt/install_ohmyzsh.sh", 0o755)
                if not self.run_install_command("arch-chroot /mnt /install_ohmyzsh.sh", "Installing Oh My Zsh"): return
                if not self.run_install_command("rm /mnt/install_ohmyzsh.sh", "Removing Oh My Zsh install script"): return
                self.update_progress("Oh My Zsh installation complete.", 95, tag="success")


            # 8. Final Steps and Cleanup
            self.update_progress("Performing final steps and cleanup...", 98)
            if not self.run_install_command("sync", "Syncing filesystem"): return
            if not self.run_install_command("umount -R /mnt", "Unmounting all filesystems"): return
            if swap_size_input:
                if not self.run_install_command(f"swapoff {swap_partition_path} || true", "Deactivating swap"): return
            
            self.update_progress("Installation complete!", 100, tag="success")
            messagebox.showinfo("Installation Complete", "Arch Linux has been successfully installed!")
            self.next_button.config(state="normal")
            
        except subprocess.CalledProcessError as e:
            self.update_progress(f"Installation failed. Error: {e.output}", tag="error")
            messagebox.showerror("Installation Failed", f"The installation encountered an error. Check log for details.\nError: {e.cmd} failed.")
            self.close_log_file()
            self.controller.exit_installer()
        except Exception as e:
            self.update_progress(f"An unexpected error occurred: {e}", tag="error")
            messagebox.showerror("Installation Failed", f"An unexpected error occurred: {e}")
            self.close_log_file()
            self.controller.exit_installer()
        finally:
            self.close_log_file()


# --- Step 7: Summary Frame ---
class SummaryFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        main_frame = ttk.Frame(self, padding="20", style="TFrame")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(main_frame, text="Installation Summary", style="Title.TLabel").grid(row=0, column=0, pady=10)
        ttk.Label(main_frame, text="Congratulations! Your Arch Linux installation is complete.", style="Success.TLabel").grid(row=1, column=0, pady=5)
        ttk.Label(main_frame, text="You can now reboot or shut down your system.").grid(row=2, column=0, pady=5)

        ttk.Label(main_frame, text="Remember to remove the installation medium before doing so.", style="Warning.TLabel", wraplength=600).grid(row=3, column=0, pady=20)

        ttk.Label(main_frame, text="Installation Details:", style="Highlight.TLabel").grid(row=4, column=0, sticky="w", pady=(10,0))
        details_text = tk.Text(main_frame, wrap=tk.WORD, width=60, height=10, state="disabled",
                                 bg=DRACULA_CURRENT_LINE, fg=DRACULA_FG,
                                 insertbackground=DRACULA_PURPLE, selectbackground=DRACULA_PURPLE, selectforeground=DRACULA_FG,
                                 borderwidth=1, relief="solid", font=("Fira Code", 9))
        details_text.grid(row=5, column=0, pady=5, sticky="nsew")
        self.details_text = details_text

        self.reboot_button = ttk.Button(self.nav_frame, text="Reboot Now", command=self.reboot_system)
        self.reboot_button.grid(row=0, column=1, sticky="e", padx=5)
        
        self.shutdown_button = ttk.Button(self.nav_frame, text="Shutdown", command=self.shutdown_system)
        self.shutdown_button.grid(row=0, column=2, sticky="e", padx=5)
        
        self.back_button.grid_remove()
        self.next_button.grid_remove()
        self.exit_button.grid_remove()

    def on_show(self):
        self.details_text.config(state="normal")
        self.details_text.delete("1.0", tk.END)
        self.details_text.insert(tk.END, f"Target Disk: {self.controller.get_var('final_target_disk')}\n")
        self.details_text.insert(tk.END, f"Boot Mode: {self.controller.get_var('boot_mode')}\n")
        self.details_text.insert(tk.END, f"Boot Partition Size: {self.controller.get_var('boot_size')}\n")
        self.details_text.insert(tk.END, f"Swap Partition Size: {self.controller.get_var('swap_size') or 'None'}\n")
        self.details_text.insert(tk.END, f"Hostname: {self.controller.get_var('hostname')}\n")
        self.details_text.insert(tk.END, f"Username: {self.controller.get_var('username')}\n")
        self.details_text.insert(tk.END, f"Selected Kernel: {self.controller.get_var('selected_kernel')}\n")
        self.details_text.insert(tk.END, f"Desktop Environment: {self.controller.get_var('selected_de_name')}\n")
        self.details_text.insert(tk.END, f"Packages: {self.controller.get_var('package_list')}\n")
        self.details_text.insert(tk.END, f"Install Steam: {'Yes' if self.controller.get_var('install_steam') else 'No'}\n")
        self.details_text.insert(tk.END, f"Install Discord: {'Yes' if self.controller.get_var('install_discord') else 'No'}\n")
        self.details_text.insert(tk.END, f"Enable Multilib: {'Yes' if self.controller.get_var('enable_multilib') else 'No'}\n")
        self.details_text.insert(tk.END, f"Install Oh My Zsh: {'Yes' if self.controller.get_var('install_oh_my_zsh') else 'No'}\n")
        self.details_text.insert(tk.END, f"Root Account Enabled: {'Yes' if self.controller.get_var('enable_root_account') else 'No'}\n")
        self.details_text.insert(tk.END, f"Time Zone: {self.controller.get_var('region')}/{self.controller.get_var('city')}\n")
        self.details_text.insert(tk.END, f"Keyboard Layout: {self.controller.get_var('keyboard_layout')}\n")
        self.details_text.insert(tk.END, f"Installation Log Saved: {'Yes' if self.controller.get_var('log_to_file') else 'No'}\n")
        self.details_text.config(state="disabled")

    def reboot_system(self):
        if messagebox.askyesno("Reboot System", "Are you sure you want to reboot now?"):
            try:
                run_command("reboot", check=False, capture_output=False)
            except Exception as e:
                messagebox.showerror("Reboot Error", f"Failed to initiate reboot: {e}. Please reboot manually.")
            self.controller.destroy()

    def shutdown_system(self):
        if messagebox.askyesno("Shutdown System", "Are you sure you want to shut down now?"):
            try:
                run_command("shutdown now", check=False, capture_output=False)
            except Exception as e:
                messagebox.showerror("Shutdown Error", f"Failed to initiate shutdown: {e}. Please shut down manually.")
            self.controller.destroy()

if __name__ == "__main__":
    if os.geteuid() != 0:
        messagebox.showerror("Permission Denied", "ArchInstall GUI must be run as root. Please run with 'sudo python3 your_script_name.py'.")
        exit(1)
        
    app = ArchInstallGUI()
    app.mainloop()
