
# Table of Contents

1.  [Overwiev](#org70d0f50)
    1.  [What is this?](#org9dbde7a)
    2.  [What can it do?](#org61fa072)
2.  [Installation](#org5e49eb8)
    1.  [Depedencies](#org23b5a62)
        1.  [Always Required](#org25a4801)
        2.  [Optional](#orgc0e231f)
        3.  [Build dependencies](#orgff11720)
    2.  [Installing with package Manager](#org1c00890)
        1.  [Gentoo](#org2bf48d4)
        2.  [Arch Linux](#org8ee76f6)
        3.  [Others](#org9f16ddd)
    3.  [Installing with pip](#org7e3fb17)
    4.  [Installing manually](#org084fc6e)
3.  [Configuration](#orgaf8fdf8)
    1.  [TOML Dictionaries](#orgad4f0fd)
        1.  [general](#orgd418b79)
        2.  [changing<sub>times</sub>](#org69326d0)
        3.  [The other dictionaries](#org615f120)
4.  [TODOs](#org276954e)
    1.  [Structuring](#orgb4e81c3)
    2.  [Technical Details](#org9e956af)
    3.  [Features](#orgb74d954)



<a id="org70d0f50"></a>

# Overwiev


<a id="org9dbde7a"></a>

## What is this?

This is my project wallman. Wallman is a simple python program used for setting Dynamic Wallpapers on minimalist X11 Window Managers and Wayland compositors. The name is a reference to TomSka: <https://www.youtube.com/watch?v=k4Q3qD93rgI&t=131s>
This version is an early Alpha. As of now, it supports the most important features for my usecase, those being randomly selected wallpaper sets and wallpaper sets that change by the time of day. The program is not modular yet and I would expect a lot of bugs related to the configuration file. Just how it is, I&rsquo;m working on it.
As such, please make absolutely sure you follow the instructions on how to write the config file very closely. I will implement better config handling with more meaningful error output in the future. For now, follow everything really closely and read the logs if needed. If you do that, it *should* work.


<a id="org61fa072"></a>

## What can it do?

Wallman currently has three main features:

-   Reading configuration details from a TOML file
-   Choosing from a set of Wallpapers and then setting the rest of the wallpapers accordingly
-   Settings Wallpapers at a specific time of the day
-   Be controlled via a systray


<a id="org5e49eb8"></a>

# Installation


<a id="org23b5a62"></a>

## Depedencies


<a id="org25a4801"></a>

### Always Required

-   Python 3.11 or newer (Required because of tomllib)
-   APScheduler (Install python-apscheduler or APScheduler, depending on the package manager)
-   feh (Used for setting the wallpapers, hard dependency)


<a id="orgc0e231f"></a>

### Optional

-   libnotify (for desktop notification support)
-   pillow (For systray support)
-   pystray (For systray support)


<a id="orgff11720"></a>

### Build dependencies

-   setuptools
-   build


<a id="org1c00890"></a>

## Installing with package Manager


<a id="org2bf48d4"></a>

### Gentoo

This program, as of now, can be installed very easily on gentoo. Just follow these instructions:

    git clone https://git.entheuer.de/emma/Wallman.git
    doas eselect repository create wallman
    doas cp -rf Wallman/distfiles/Gentoo/wallman /var/db/repos/
    doas emerge -av wallman

A proper portage overlay will be created soon, so that updates can be handled automatically.


<a id="org8ee76f6"></a>

### Arch Linux

Support for Arch Linux will be added soon.


<a id="org9f16ddd"></a>

### Others

I will potentially write a version for nixpkgs and will also bundle wallman as a flatpak.


<a id="org7e3fb17"></a>

## Installing with pip

Wallman is available on PyPI. Simply run:

    pip install wallman


<a id="org084fc6e"></a>

## Installing manually

-   Install libnotify and feh from your package manager

    pip install APScheduler pystray pillow
    git clone https://git.entheuer.de/emma/Wallman.git
    cd Wallman/
    mkdir -p ~/.local/share/wallman
    mkdir -p ~/.config/wallman
    touch ~/.local/share/wallman/wallman.log
    cp sample_config.toml ~/.config/wallman/wallman.toml
    cp systrayIcon.jpg ~/.config/wallman/systrayIcon.jpg
    doas cp src/wallman.py /usr/bin/wallman
    doas cp src/wallman_lib.py /usr/bin/wallman_lib.py
    doas chmod +x /usr/bin/wallman

-   Edit the sample config
-   Profit


<a id="orgaf8fdf8"></a>

# Configuration

This is a short guide on how to correctly configure wallman. Look in the sample config for additional context.


<a id="orgad4f0fd"></a>

## TOML Dictionaries

First of all, the config file is structured via different TOML dictionaries. There are two TOML dictionaries: general and changing<sub>times</sub> that must be present in every config. Aside from that, further dictionaries are needed depending on how wallman is configured. You need to create a dictionary with the name of each wallpaper set defined in the used<sub>sets</sub> list (more on that later). You should probably just configure wallman by editing the sample config as it is by far the easiest way to do it.


<a id="orgd418b79"></a>

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
    Loglevel to be used by wallman. Defaults to WARNING. Choices MUST be DEBUG, INFO, WARNING, ERROR or CRITICAL. Using any capitalization is valid, all caps is reccomended. Wallman will crash if a value is specified that is not one of the specified ones.
-   Optional: systray: bool
    This defaults to &ldquo;true&rdquo;. This enables support for a systray that has the features to re-set your wallpaper (Mostly useful if feh shits itself or if you want to set the correct wallpaper for a specific time of day after your device was suspended) without rerolling the wallpaper set used, a button to reroll and then re-set the wallpaper, as well as a Quit button. Disable this to save a very tiny amount of memory.


<a id="org69326d0"></a>

### changing<sub>times</sub>

The changing<sub>times</sub> dictionary is used to specify the times of the day when your wallpaper is switched. The names of the keys do not matter here, the values must always be strings in the &ldquo;XX:YY:ZZ&rdquo; 24 hour time system. use 00:00:00 for midnight. Note that XX should be in the range of 00-23 and YY and ZZ should be in the range of 00-59.


<a id="org615f120"></a>

### The other dictionaries

The other dictionaries must always have the names of the wallpaper sets from used<sub>sets</sub>. If you have one wallpaper set, you need one additional dictionary, if you have two you need two etc. The standard config uses nature and anime, these names can be whatever you please as long as they are the same as the ones specified in used<sub>sets</sub>.
The keys in the dictionary once again do not matter, the names of the keys in each dictionary must be strings and be absolute paths. They should not include spaces unless prefaced by a backslash.


<a id="org276954e"></a>

# TODOs


<a id="orgb4e81c3"></a>

## Structuring

-   Write unittests
-   Add documentation for developers


<a id="org9e956af"></a>

## Technical Details

-   Improve Modularity (Partially done)
-   Make the enabled flag in wallpaper<sub>sets</sub> actually useful by making the used<sub>sets</sub> field optional
-   Drop the feh dependecy and set wallpapers using pywlroots or python-xlib


<a id="orgb74d954"></a>

## Features

-   Add support for wallpapers that dynamically change with the time of day (Morning, noon, evening, night or light levels) rather than to times set in the config
-   Add support for wallpapers that change by the weather
-   Add support for live wallpapers

