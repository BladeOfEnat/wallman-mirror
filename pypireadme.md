# Table of Contents

1.  [Overwiev](#org19ef638)
    1.  [What is this?](#org148aad0)
    2.  [What can it do?](#org0041bf1)
2.  [Installation](#orgc40ee8b)
    1.  [Depedencies](#org2cb62ef)
        1.  [Always Required](#org0d0b0f7)
        2.  [Optional](#orgf04ec77)
        3.  [Build dependencies](#org3951087)
    2.  [Installing with pip](#org24bde1c)
    3.  [Installing with package Manager](#org9575c55)
    4.  [Installing manually](#org2c63e0f)
3.  [Configuration](#org812c501)
    1.  [TOML Dictionaries](#org51e3333)
        1.  [general](#org79747a5)
        2.  [changing<sub>times</sub>](#orgc425813)
        3.  [The other dictionaries](#org9f47b06)
4.  [TODOs](#orgc26c243)
    1.  [Structuring](#org8dd22d4)
    2.  [Technical Details](#org6103451)
    3.  [Features](#org38d78ba)



<a id="org19ef638"></a>

# Overwiev


<a id="org148aad0"></a>

## What is this?

This is my project wallman. Wallman is a simple python program used for setting Dynamic Wallpapers on minimalist X11 Window Managers and Wayland compositors. The name is a reference to TomSka: <https://www.youtube.com/watch?v=k4Q3qD93rgI&t=131s>
This version is an early Alpha. As of now, it supports the most important features for my usecase, those being randomly selected wallpaper sets and wallpaper sets that change by the time of day. The program is not modular yet and I would expect a lot of bugs related to the configuration file. Just how it is, I&rsquo;m working on it.
As such, please make absolutely sure you follow the instructions on how to write the config file very closely. I will implement better config handling with more meaningful error output in the future. For now, follow everything really closely and read the logs if needed. If you do that, it *should* work.


<a id="org0041bf1"></a>

## What can it do?

Wallman currently has three main features:

-   Reading configuration details from a TOML file
-   Choosing from a set of Wallpapers and then setting the rest of the wallpapers accordingly
-   Settings Wallpapers at a specific time of the day


<a id="orgc40ee8b"></a>

# Installation


<a id="org2cb62ef"></a>

## Depedencies


<a id="org0d0b0f7"></a>

### Always Required

-   Python 3.11 or newer (Required because of tomllib)
-   APScheduler (Install python-apscheduler or APScheduler, depending on the package manager)
-   feh (Used for setting the wallpapers, hard dependency)


<a id="orgf04ec77"></a>

### Optional

-   libnotify (for desktop notification support)


<a id="org3951087"></a>

### Build dependencies

-   setuptools
-   build


<a id="org24bde1c"></a>

## Installing with pip

Wallman is available on PYPI. Simply run:

    pip install wallman


<a id="org9575c55"></a>

## Installing with package Manager

Versions in the AUR and an ebuild for Gentoo will be added soon. A flatpak and Nixpkgs version are on the horizon, too.


<a id="org2c63e0f"></a>

## Installing manually

-   Clone this git repo
-   Create a log file and a configuration file:

    mkdir -p ~/.local/share/wallman
    mkdir -p ~/.config/wallman
    touch ~/.local/share/wallman/wallman.log
    cp sample_config.toml ~/.config/wallman/wallman.toml

-   Edit the sample config
-   (Optional): Adjust the loglevel to your liking. This will be part of the config or a command line argument soon.
-   Profit


<a id="org812c501"></a>

# Configuration

This is a short guide on how to correctly configure wallman. Look in the sample config for additional context.


<a id="org51e3333"></a>

## TOML Dictionaries

First of all, the config file is structured via different TOML dictionaries. There are two TOML dictionaries: general and changing<sub>times</sub> that must be present in every config. Aside from that, further dictionaries are needed depending on how wallman is configured. You need to create a dictionary with the name of each wallpaper set defined in the used<sub>sets</sub> list (more on that later). You should probably just configure wallman by editing the sample config as it is by far the easiest way to do it.


<a id="org79747a5"></a>

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


<a id="orgc425813"></a>

### changing<sub>times</sub>

The changing<sub>times</sub> dictionary is used to specify the times of the day when your wallpaper is switched. The names of the keys do not matter here, the values must always be strings in the &ldquo;XX:YY:ZZ&rdquo; 24 hour time system. use 00:00:00 for midnight. Note that XX should be in the range of 00-23 and YY and ZZ should be in the range of 00-59.


<a id="org9f47b06"></a>

### The other dictionaries

The other dictionaries must always have the names of the wallpaper sets from used<sub>sets</sub>. If you have one wallpaper set, you need one additional dictionary, if you have two you need two etc. The standard config uses nature and anime, these names can be whatever you please as long as they are the same as the ones specified in used<sub>sets</sub>.
The keys in the dictionary once again do not matter, the names of the keys in each dictionary must be strings and be absolute paths. They should not include spaces unless prefaced by a backslash.


<a id="orgc26c243"></a>

# TODOs


<a id="org8dd22d4"></a>

## Structuring

-   Write unittests
-   Add documentation for developers


<a id="org6103451"></a>

## Technical Details

-   Improve Modularity
-   Make the enabled flag in wallpaper<sub>sets</sub> actually useful by making the used<sub>sets</sub> field optional
-   Add support for different loglevels in the config file or as a command line argument
-   Drop the feh dependecy and set wallpapers using pywlroots or python-xlib


<a id="org38d78ba"></a>

## Features

-   Add support for setting a fallback wallpaper if a wallpaper the user set is not found
-   Add support for wallpapers that dynamically change with the time of day (Morning, noon, evening, night or light levels) rather than to times set in the config
-   Add support for wallpapers that change by the weather
-   Add support for live wallpapers

