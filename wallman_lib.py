#!/usr/bin/env python3
from os import chdir, getenv, system
import logging
import tomllib
from datetime import datetime, time
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

# setup logging
chdir(str(getenv("HOME")) + "/.local/share/wallman/")
logger = logging.getLogger(__name__)
logging.basicConfig(filename="wallman.log", encoding="utf-8", level=logging.DEBUG)

# read config
        # a = list(data["changing_times"].values())
        # print(a[0])

class ConfigError(Exception):
    pass

class _ConfigLib:
    def _initialize_config(self) -> dict:
        chdir(str(getenv("HOME")) + "/.config/wallman/")
        with open("wallman.toml", "rb") as config_file:
            data = tomllib.load(config_file)
            return data
            # a = list(data["changing_times"].values())
            # print(a[0])

    def __init__(self):
        self.config_file: dict = self._initialize_config() # Full config
        # Dictionaries
        self.config_general: dict = self.config_file["general"]
        self.config_changing_times: dict = self.config_file["changing_times"]
        # Values in Dicts
        self.config_wallpaper_sets_enabled: bool = self.config_general["enable_wallpaper_sets"]
        self.config_used_sets: list = self.config_general["used_sets"]
        self.config_wallpapers_per_set: int = self.config_general["wallpapers_per_set"]
        self.config_total_changing_times: int = len(self.config_changing_times)
        try:
            self.config_notify = self.config_general["notify"]
        except KeyError:
            self.config_notify = False

class ConfigValidity(_ConfigLib):
    def __init__(self):
        super().__init__()

    def _check_wallpapers_per_set_and_changing_times(self) -> None:
        # Check if the amount of wallpapers_per_set and given changing times match
        if self.config_total_changing_times == self.config_wallpapers_per_set:
            logger.debug("The amount of changing times and wallpapers per set is set correctly")
        else:
            logger.error("The amount of changing times and the amount of wallpapers per set does not match.")
            raise ConfigError("Please provide an amount of changing_times equal to wallpapers_per_set.")

    def _check_general_validity(self) -> None:
        if len(self.config_general) < 3:
            logger.error("An insufficient amount of parameters for general has been provided, exiting...")
            raise ConfigError("general should have at least 3 elements")

    def _check_wallpaper_dicts(self)-> None:
        # This block checks if a dictionary for each wallpaper set exists
        for wallpaper_set in self.config_used_sets:
            if wallpaper_set in self.config_file:
                logger.debug(f"The dictionary {wallpaper_set} has been found in config.")
            else:
                 logger.error(f"No dictionary {wallpaper_set} has been found in the config.")
                 raise ConfigError(f"The dictionary {wallpaper_set} has not been found in the config")

    def _check_wallpaper_amount(self) -> None:
        # This block checks if if each wallpaper set dictionary provides enough wallpapers to satisfy wallpapers_per_set
        for wallpaper_set in self.config_used_sets:
            if len(self.config_file[wallpaper_set]) == self.config_wallpapers_per_set:
                logger.debug(f"Dictionary {wallpaper_set} has sufficient values.")
            else:
                logger.error(f"Dictionary {wallpaper_set} does not have sufficient entries")
                raise ConfigError(f"Dictionary {wallpaper_set} does not have the correct amount of entries")

    def validate_config(self) -> None:
        self._check_wallpapers_per_set_and_changing_times()
        self._check_general_validity()
        self._check_wallpaper_dicts()
        self._check_wallpaper_amount()
        logger.debug("The config file has been validated successfully (No Errors)")

class WallpaperLogic(_ConfigLib):
    def __init__(self):
        super().__init__()
        self.chosen_wallpaper_set = False

    # Returns a list of a split string that contains a changing time from the config file
    def _clean_times(self, desired_time) -> list:
        unclean_times = list(self.config_changing_times.values())[desired_time]
        return unclean_times.split(":")

    def _choose_wallpaper_set(self) -> None:
        from random import choice as choose_from
        self.chosen_wallpaper_set = choose_from(self.config_used_sets)
        self.wallpaper_list = list(self.config_file[self.chosen_wallpaper_set].values())
        logger.debug(f"Chose wallpaper set {self.chosen_wallpaper_set}")

    # Verify if a given time is in a given range
    def _time_in_range(self, start, end, x) -> bool:
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x < end

    def _notify_user(self):
        system("notify-send 'Wallman' 'A new Wallpaper has been set.'")
        logger.debug("Sent desktop notification.")

    def set_wallpaper_by_time(self) -> None:
        # Ensure use of a consistent wallpaper set
        if self.chosen_wallpaper_set is False:
            self._choose_wallpaper_set()
        for time_range in range(self.config_total_changing_times - 1):
            clean_time = self._clean_times(time_range)
            clean_time_two = self._clean_times(time_range + 1)
            # Check if the current time is between a given and the following changing time and if so, set that wallpaper. If not, keep trying.
            if self._time_in_range(time(int(clean_time[0]), int(clean_time[1]), int(clean_time[2])), time(int(clean_time_two[0]), int(clean_time_two[1]), int(clean_time_two[2])), datetime.now().time()):
                system(f"feh --bg-scale --no-fehbg {self.wallpaper_list[time_range]}")
                if self.config_notify:
                    self._notify_user()
                return
            else:
                continue

        system(f"feh --bg-scale --no-fehbg {self.wallpaper_list[-1]}")
        if self.config_notify:
            self._notify_user()

    def schedule_wallpapers(self):
        scheduler = BlockingScheduler()
        # Create a scheduled job for every changing time
        for changing_time in range(len(self.config_changing_times)):
            clean_time = self._clean_times(changing_time)
            scheduler.add_job(self.set_wallpaper_by_time, trigger=CronTrigger(hour=clean_time[0], minute=clean_time[1], second=clean_time[2]))
        scheduler.start()
        logger.info("The scheduler has been started.")
