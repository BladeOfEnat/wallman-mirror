
# Table of Contents

1.  [Overwiev](#org054ef0d)
    1.  [What is this?](#orgbf4dad3)
    2.  [What can it do?](#orgdf86200)
2.  [Installation](#orge115851)
    1.  [Depedencies](#org1c920d8)
        1.  [Always Required](#org5a03048)
        2.  [Optional](#org2bb7a20)
        3.  [Build dependencies](#orgbdbc04d)
    2.  [Installing with package Manager](#org3f3b4a9)
        1.  [Gentoo](#orgcfe6102)
        2.  [Arch Linux](#org4adff79)
        3.  [Others](#orgdcb0d42)
    3.  [Installing with pip](#org41ac4c9)
    4.  [Installing manually](#org88055b7)
3.  [Configuration](#orgc0a8c31)
    1.  [TOML Dictionaries](#orgc09a1b5)
        1.  [general](#org8297129)
        2.  [changing<sub>times</sub>](#org5f9734c)
        3.  [The other dictionaries](#org4d41b53)
4.  [TODOs](#org9f0b1f0)
    1.  [Structuring](#org036190c)
    2.  [Technical Details](#org35cda78)
    3.  [Features](#org8250c51)



<a id="org054ef0d"></a>

# Overwiev


<a id="orgbf4dad3"></a>

## What is this?

This is my project wallman. Wallman is a simple python program used for setting Dynamic Wallpapers on minimalist X11 Window Managers and Wayland compositors. The name is a reference to TomSka: <https://www.youtube.com/watch?v=k4Q3qD93rgI&t=131s>
This version is an early Alpha. As of now, it supports the most important features for my usecase, those being randomly selected wallpaper sets and wallpaper sets that change by the time of day. The program is not modular yet and I would expect a lot of bugs related to the configuration file. Just how it is, I&rsquo;m working on it.
As such, please make absolutely sure you follow the instructions on how to write the config file very closely. I will implement better config handling with more meaningful error output in the future. For now, follow everything really closely and read the logs if needed. If you do that, it *should* work.


<a id="orgdf86200"></a>

## What can it do?

Wallman currently has three main features:

-   Reading configuration details from a TOML file
-   Choosing from a set of Wallpapers and then setting the rest of the wallpapers accordingly
-   Settings Wallpapers at a specific time of the day


<a id="orge115851"></a>

# Installation


<a id="org1c920d8"></a>

## Depedencies


<a id="org5a03048"></a>

### Always Required

-   Python 3.11 or newer (Required because of tomllib)
-   APScheduler (Install python-apscheduler or APScheduler, depending on the package manager)
-   feh (Used for setting the wallpapers, hard dependency)


<a id="org2bb7a20"></a>

### Optional

-   libnotify (for desktop notification support)


<a id="orgbdbc04d"></a>

### Build dependencies

-   setuptools
-   build


<a id="org3f3b4a9"></a>

## Installing with package Manager


<a id="orgcfe6102"></a>

### Gentoo

This program, as of now, can be installed very easily on gentoo. Just follow these instructions:

    git clone https://git.entheuer.de/emma/Wallman.git
    doas eselect repository create wallman
    doas cp -rf Wallman/distfiles/Gentoo/wallman /var/db/repos/
    doas emerge -av wallman

A proper portage overlay will be created soon so that updates can be handled automatically.


<a id="org4adff79"></a>

### Arch Linux

Support for Arch Linux will be added soon.


<a id="orgdcb0d42"></a>

### Others

I will potentially write a version for nixpkgs and will also bundle wallman as a flatpak.


<a id="org41ac4c9"></a>

## Installing with pip

Wallman is available on PyPI. Simply run:

    pip install wallman


<a id="org88055b7"></a>

## Installing manually

    git clone https://git.entheuer.de/emma/Wallman.git
    cd Wallman/
    mkdir -p ~/.local/share/wallman
    mkdir -p ~/.config/wallman
    touch ~/.local/share/wallman/wallman.log
    cp sample_config.toml ~/.config/wallman/wallman.toml
    doas cp src/wallman.py /usr/bin/wallman
    doas cp src/wallman_lib.py /usr/bin/wallman_lib.py
    doas chmod +x /usr/bin/wallman

-   Edit the sample config
-   (Optional): Adjust the loglevel in Source Code to your liking.
-   Profit


<a id="orgc0a8c31"></a>

# Configuration

This is a short guide on how to correctly configure wallman. Look in the sample config for additional context.


<a id="orgc09a1b5"></a>

## TOML Dictionaries

First of all, the config file is structured via different TOML dictionaries. There are two TOML dictionaries: general and changing<sub>times</sub> that must be present in every config. Aside from that, further dictionaries are needed depending on how wallman is configured. You need to create a dictionary with the name of each wallpaper set defined in the used<sub>sets</sub> list (more on that later). You should probably just configure wallman by editing the sample config as it is by far the easiest way to do it.


<a id="org8297129"></a>

### general

In general, you need to always define 3 variables and you can optionally add two more:

-   enable<sub>wallpaper</sub><sub>sets</sub>: bool
    A simple switch that states if you want to use different sets of wallpapers or not.
-   used<sub>sets</sub>: list
    A list that includes the names of the wallpaper sets you want to use. If you want to use only one, the list should have one entry.
-   wallpapers<sub>per</sub><sub>set</sub>: int
    The amount of wallpapers that you use in each set. It should be an integer.
-   Optional: notify: bool
    This defaults to &ldquo;false&rdquo;. Enable to set send a desktop notification when the wallpaper is changed. The program will still work correctly, even if this option is not defined at all.
-   Optional: fallback<sub>wallpaper</sub>: bool
    Wallpaper to be set if an error is found in the config. Defaults to None. If none is set and the config is written incorrectly, a ConfigError is raised and the program is exited. If an error in the config occurs but the fallback wallpaper has been defined, it will be set and wallman will exit with Code 1.


<a id="org5f9734c"></a>

### changing<sub>times</sub>

The changing<sub>times</sub> dictionary is used to specify the times of the day when your wallpaper is switched. The names of the keys do not matter here, the values must always be strings in the &ldquo;XX:YY:ZZ&rdquo; 24 hour time system. use 00:00:00 for midnight. Note that XX should be in the range of 00-23 and YY and ZZ should be in the range of 00-59.


<a id="org4d41b53"></a>

### The other dictionaries

The other dictionaries must always have the names of the wallpaper sets from used<sub>sets</sub>. If you have one wallpaper set, you need one additional dictionary, if you have two you need two etc. The standard config uses nature and anime, these names can be whatever you please as long as they are the same as the ones specified in used<sub>sets</sub>.
The keys in the dictionary once again do not matter, the names of the keys in each dictionary must be strings and be absolute paths. They should not include spaces unless prefaced by a backslash.


<a id="org9f0b1f0"></a>

# TODOs


<a id="org036190c"></a>

## Structuring

-   Write unittests
-   Add documentation for developers


<a id="org35cda78"></a>

## Technical Details

-   Improve Modularity
-   Make the enabled flag in wallpaper<sub>sets</sub> actually useful by making the used<sub>sets</sub> field optional
-   Add support for different loglevels in the config file or as a command line argument
-   Drop the feh dependecy and set wallpapers using pywlroots or python-xlib


<a id="org8250c51"></a>

## Features

-   Add support for setting a fallback wallpaper if a wallpaper the user set is not found
-   Add support for wallpapers that dynamically change with the time of day (Morning, noon, evening, night or light levels) rather than to times set in the config
-   Add support for wallpapers that change by the weather
-   Add support for live wallpapers

