
# Table of Contents

1.  [Overwiev](#org2f278b8)
    1.  [What is this?](#org388817f)
    2.  [What can it do?](#org181b8b7)
2.  [Installation](#org9472446)
    1.  [Depedencies](#org5977b9f)
        1.  [Always Required](#org3f4fbec)
        2.  [Optional](#org66e727c)
        3.  [Build dependencies](#org818620a)
    2.  [Installing with package Manager](#orgb41bd96)
        1.  [Gentoo](#org135d2b8)
        2.  [Arch Linux](#org1d65d77)
        3.  [Others](#org32866d5)
    3.  [Installing with pip](#org59bd85f)
    4.  [Installing manually](#orgf93bb3e)
3.  [Configuration](#orgd8c9052)
    1.  [TOML Dictionaries](#org059100a)
        1.  [general](#orge724ab7)
        2.  [changing<sub>times</sub>](#orgac9b284)
        3.  [The other dictionaries](#org2f91798)
4.  [TODOs](#orgab8e139)
    1.  [Structuring](#orga5d5528)
    2.  [Technical Details](#org8559da1)
    3.  [Features](#org5a7f88b)



<a id="org2f278b8"></a>

# Overwiev


<a id="org388817f"></a>

## What is this?

This is my project wallman. Wallman is a simple python program used for setting Dynamic Wallpapers on minimalist X11 Window Managers and Wayland compositors. The name is a reference to TomSka: <https://www.youtube.com/watch?v=k4Q3qD93rgI&t=131s>
This version is an early Alpha. As of now, it supports the most important features for my usecase, those being randomly selected wallpaper sets and wallpaper sets that change by the time of day. The program is not modular yet and I would expect a lot of bugs related to the configuration file. Just how it is, I&rsquo;m working on it.
As such, please make absolutely sure you follow the instructions on how to write the config file very closely. I will implement better config handling with more meaningful error output in the future. For now, follow everything really closely and read the logs if needed. If you do that, it *should* work.


<a id="org181b8b7"></a>

## What can it do?

Wallman currently has three main features:

-   Reading configuration details from a TOML file
-   Choosing from a set of Wallpapers and then setting the rest of the wallpapers accordingly
-   Settings Wallpapers at a specific time of the day


<a id="org9472446"></a>

# Installation


<a id="org5977b9f"></a>

## Depedencies


<a id="org3f4fbec"></a>

### Always Required

-   Python 3.11 or newer (Required because of tomllib)
-   APScheduler (Install python-apscheduler or APScheduler, depending on the package manager)
-   feh (Used for setting the wallpapers, hard dependency)


<a id="org66e727c"></a>

### Optional

-   libnotify (for desktop notification support)


<a id="org818620a"></a>

### Build dependencies

-   setuptools
-   build


<a id="orgb41bd96"></a>

## Installing with package Manager


<a id="org135d2b8"></a>

### Gentoo

This program, as of now, can be installed very easily on gentoo. Just follow these instructions

    git clone https://git.entheuer.de/emma/Wallman.git
    doas eselect repository create wallman
    doas cp -rf Wallman/distfiles/Gentoo/wallman /var/db/repos/
    doas emerge -av wallman


<a id="org1d65d77"></a>

### Arch Linux

Support for Arch Linux will be added soon.


<a id="org32866d5"></a>

### Others

I will potentially write a version for nixpkgs and will also bundle wallman as a flatpak.


<a id="org59bd85f"></a>

## Installing with pip

Wallman is available on PyPI. Simply run:

    pip install wallman


<a id="orgf93bb3e"></a>

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


<a id="orgd8c9052"></a>

# Configuration

This is a short guide on how to correctly configure wallman. Look in the sample config for additional context.


<a id="org059100a"></a>

## TOML Dictionaries

First of all, the config file is structured via different TOML dictionaries. There are two TOML dictionaries: general and changing<sub>times</sub> that must be present in every config. Aside from that, further dictionaries are needed depending on how wallman is configured. You need to create a dictionary with the name of each wallpaper set defined in the used<sub>sets</sub> list (more on that later). You should probably just configure wallman by editing the sample config as it is by far the easiest way to do it.


<a id="orge724ab7"></a>

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


<a id="orgac9b284"></a>

### changing<sub>times</sub>

The changing<sub>times</sub> dictionary is used to specify the times of the day when your wallpaper is switched. The names of the keys do not matter here, the values must always be strings in the &ldquo;XX:YY:ZZ&rdquo; 24 hour time system. use 00:00:00 for midnight. Note that XX should be in the range of 00-23 and YY and ZZ should be in the range of 00-59.


<a id="org2f91798"></a>

### The other dictionaries

The other dictionaries must always have the names of the wallpaper sets from used<sub>sets</sub>. If you have one wallpaper set, you need one additional dictionary, if you have two you need two etc. The standard config uses nature and anime, these names can be whatever you please as long as they are the same as the ones specified in used<sub>sets</sub>.
The keys in the dictionary once again do not matter, the names of the keys in each dictionary must be strings and be absolute paths. They should not include spaces unless prefaced by a backslash.


<a id="orgab8e139"></a>

# TODOs


<a id="orga5d5528"></a>

## Structuring

-   Write unittests
-   Add documentation for developers


<a id="org8559da1"></a>

## Technical Details

-   Improve Modularity
-   Make the enabled flag in wallpaper<sub>sets</sub> actually useful by making the used<sub>sets</sub> field optional
-   Add support for different loglevels in the config file or as a command line argument
-   Drop the feh dependecy and set wallpapers using pywlroots or python-xlib


<a id="org5a7f88b"></a>

## Features

-   Add support for setting a fallback wallpaper if a wallpaper the user set is not found
-   Add support for wallpapers that dynamically change with the time of day (Morning, noon, evening, night or light levels) rather than to times set in the config
-   Add support for wallpapers that change by the weather
-   Add support for live wallpapers

