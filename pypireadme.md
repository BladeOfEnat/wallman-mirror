
# Table of Contents

1.  [Overwiev](#orga779aae)
    1.  [What is this?](#orgf7b412d)
    2.  [What can it do?](#org935ec0e)
2.  [Installation](#org022a1fd)
    1.  [Depedencies](#org90be55c)
        1.  [Always Required](#orgadb7aa8)
        2.  [Optional](#org407e4c9)
        3.  [Build dependencies](#orgab711aa)
    2.  [Installing with package Manager](#org2a19ad0)
        1.  [Gentoo](#org6686b86)
        2.  [Arch Linux](#org4eb492d)
        3.  [Others](#orga6b4e6a)
    3.  [Installing with pip](#org1b5b1b3)
    4.  [Installing manually](#org050e242)
3.  [Configuration](#orgf368a5c)
    1.  [TOML Dictionaries](#org05ab08e)
        1.  [general](#orgfa7800e)
        2.  [changing<sub>times</sub>](#org2778aa9)
        3.  [The other dictionaries](#orgf21f2d8)
4.  [TODOs](#org8cbebae)
    1.  [Structuring](#orgb43553d)
    2.  [Technical Details](#org0a633fb)
    3.  [Features](#org1c5725d)



<a id="orga779aae"></a>

# Overwiev


<a id="orgf7b412d"></a>

## What is this?

This is my project wallman. Wallman is a simple python program used for setting Dynamic Wallpapers on minimalist X11 Window Managers and Wayland compositors. The name is a reference to TomSka: <https://www.youtube.com/watch?v=k4Q3qD93rgI&t=131s>
This version is an early Alpha. As of now, it supports the most important features for my usecase, those being randomly selected wallpaper sets and wallpaper sets that change by the time of day. The program is not modular yet and I would expect a lot of bugs related to the configuration file. Just how it is, I&rsquo;m working on it.
As such, please make absolutely sure you follow the instructions on how to write the config file very closely. I will implement better config handling with more meaningful error output in the future. For now, follow everything really closely and read the logs if needed. If you do that, it *should* work.


<a id="org935ec0e"></a>

## What can it do?

Wallman currently has three main features:

-   Reading configuration details from a TOML file
-   Choosing from a set of Wallpapers and then setting the rest of the wallpapers accordingly
-   Settings Wallpapers at a specific time of the day
-   Be controlled via a systray


<a id="org022a1fd"></a>

# Installation


<a id="org90be55c"></a>

## Depedencies


<a id="orgadb7aa8"></a>

### Always Required

-   Python 3.11 or newer (Required because of tomllib)
-   APScheduler (Install python-apscheduler or APScheduler, depending on the package manager)
-   feh (Used for setting the wallpapers, hard dependency)


<a id="org407e4c9"></a>

### Optional

-   libnotify (for desktop notification support)
-   pillow (For systray support)
-   pystray (For systray support)


<a id="orgab711aa"></a>

### Build dependencies

-   setuptools
-   build


<a id="org2a19ad0"></a>

## Installing with package Manager


<a id="org6686b86"></a>

### Gentoo

This program, as of now, can be installed very easily on gentoo. Just follow these instructions:

    git clone https://git.entheuer.de/emma/Wallman.git
    doas eselect repository create wallman
    doas cp -rf Wallman/distfiles/Gentoo/wallman /var/db/repos/
    doas emerge -av wallman

A proper portage overlay will be created soon, so that updates can be handled automatically.


<a id="org4eb492d"></a>

### Arch Linux

Support for Arch Linux will be added soon.


<a id="orga6b4e6a"></a>

### Others

I will potentially write a version for nixpkgs and will also bundle wallman as a flatpak.


<a id="org1b5b1b3"></a>

## Installing with pip

Wallman is available on PyPI. Simply run:

    pip install wallman


<a id="org050e242"></a>

## Installing manually

-   Install libnotify and feh from your package manager

    pip install APScheduler pystray pillow
    git clone https://git.entheuer.de/emma/Wallman.git
    cd Wallman/
    sudo mkdir -p /var/log/wallman
    sudo chmod 733 /var/log/wallman
    mkdir -p ~/.config/wallman
    cp sample_config.toml ~/.config/wallman/wallman.toml
    doas mkdir -p /etc/wallman/
    cp -R icons/ /etc/wallman/
    doas cp src/wallman.py /usr/bin/wallman
    doas cp src/wallman_lib.py /usr/bin/wallman_lib.py
    doas cp src/wallman_systray.py /usr/bin/wallman_systray.py
    doas chmod +x /usr/bin/wallman

-   Edit the sample config
-   Profit


<a id="orgf368a5c"></a>

# Configuration

This is a short guide on how to correctly configure wallman. Look in the sample config for additional context.


<a id="org05ab08e"></a>

## TOML Dictionaries

First of all, the config file is structured via different TOML dictionaries. There are two TOML dictionaries: general and changing<sub>times</sub> that must be present in every config. Aside from that, further dictionaries are needed depending on how wallman is configured. You need to create a dictionary with the name of each wallpaper set defined in the used<sub>sets</sub> list (more on that later). You should probably just configure wallman by editing the sample config as it is by far the easiest way to do it.


<a id="orgfa7800e"></a>

### general

In general, you need to always define 3 variables and you can optionally add three more:

-   enable<sub>wallpaper</sub><sub>sets</sub>: bool
    A simple switch that states if you want to use different sets of wallpapers or not.
-   used<sub>sets</sub>: list
    A list that includes the names of the wallpaper sets you want to use. If you want to use only one, the list should have one entry.
-   wallpapers<sub>per</sub><sub>set</sub>: int
    The amount of wallpapers that you use in each set. It should be an integer.
-   Optional: notify: bool
    This defaults to &ldquo;false&rdquo;. Enable to set send a desktop notification when the wallpaper is changed. The program will still work correctly, even if this option is not defined at all.
-   Optional: fallback<sub>wallpaper</sub>: bool
    Wallpaper to be set if an error is found in the config or the wallpaper intended to be set cannot be found. Defaults to None. If none is set and the config has been written incorrectly, a ConfigError is raised and the program is exited. If an error in the config occurs but the fallback wallpaper has been defined, it will be set and wallman will exit with Code 1. If The config is written correctly but the wallpaper intended to be set can&rsquo;t be found, wallman will set the fallback wallpaper and continue to try setting future wallpapers.
-   Optional: loglevel: string
    Loglevel to be used by wallman. Defaults to INFO. Choices MUST be DEBUG, INFO, WARNING, ERROR or CRITICAL. Using any capitalization is valid, all caps is reccomended. Wallman will crash if a value is specified that is not one of the specified ones.
-   Optional: systray: bool
    This defaults to &ldquo;true&rdquo;. This enables support for a systray that has the features to re-set your wallpaper (Mostly useful if feh shits itself or if you want to set the correct wallpaper for a specific time of day after your device was suspended) without rerolling the wallpaper set used, a button to reroll and then re-set the wallpaper, as well as a Quit button. Disable this to save a very tiny amount of memory.


<a id="org2778aa9"></a>

### changing<sub>times</sub>

The changing<sub>times</sub> dictionary is used to specify the times of the day when your wallpaper is switched. The names of the keys do not matter here, the values must always be strings in the &ldquo;XX:YY:ZZ&rdquo; 24 hour time system. use 00:00:00 for midnight. Note that XX should be in the range of 00-23 and YY and ZZ should be in the range of 00-59.


<a id="orgf21f2d8"></a>

### The other dictionaries

The other dictionaries must always have the names of the wallpaper sets from used<sub>sets</sub>. If you have one wallpaper set, you need one additional dictionary, if you have two you need two etc. The standard config uses nature and anime, these names can be whatever you please as long as they are the same as the ones specified in used<sub>sets</sub>.
The keys in the dictionary once again do not matter, the names of the keys in each dictionary must be strings and be absolute paths. They should not include spaces unless prefaced by a backslash.


<a id="org8cbebae"></a>

# TODOs


<a id="orgb43553d"></a>

## Structuring

-   Write unittests
-   Add documentation for developers


<a id="org0a633fb"></a>

## Technical Details

-   Improve Modularity (Partially done)
-   Make the enabled flag in wallpaper<sub>sets</sub> actually useful by making the used<sub>sets</sub> field optional
-   Drop the feh dependecy and set wallpapers using pywlroots or python-xlib


<a id="org1c5725d"></a>

## Features

-   Add support for wallpapers that dynamically change with the time of day (Morning, noon, evening, night or light levels) rather than to times set in the config
-   Add support for wallpapers that change by the weather
-   Add support for live wallpapers

