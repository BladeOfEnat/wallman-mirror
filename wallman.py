from os import system, chdir, getenv
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import logging

# Setup logging
chdir(str(getenv("HOME")) + "/.local/share/wallman")
logger = logging.getLogger(__name__)
logging.basicConfig(filename="wallman.log", encoding="utf-8", level=logging.DEBUG)

# Initialize the global chosen_wallpaper_set variable
global chosen_wallpaper_set
chosen_wallpaper_set = False

def choose_wallpaper_set():
    # Random library for choosing wallpaper set
    from random import choice as choose_from
    wallpaper_sets = ["nature", "anime"]
    selected_set = choose_from(wallpaper_sets)
    return selected_set

def set_wallpaper_once():
    # Set the respective Wallpaper for each hour of the day
    # Deepnight Wallpaper
    if datetime.now().hour in range(0, 5):
        system("feh --bg-scale --no-fehbg /home/emma/Bilder/Hintergründe/wideAuroraNight.jpg")
    # Morning Wallpaper
    elif datetime.now().hour in range(6, 9):
        system("feh --bg-scale --no-fehbg /home/emmma/Bilder/Hintergründe/widePeninsulasMorning.jpg")
    # Dayhour Wallpaper
    elif datetime.now().hour in range(10, 17):
        system("feh --bg-scale --no-fehbg /home/emma/Bilder/Hintergründe/wideMountainDay.jpg")
    # Evening Wallpaper
    elif datetime.now().hour in range(18, 21):
        system("feh --bg-scale --no-fehbg /home/emma/Bilder/Hintergründe/wideLakeEvening.jpg")
    # Early Night Wallpaper
    else:
        system("feh --bg-scale --no-fehbg /home/emma/Bilder/Hintergründe/wideMountainEveningNight.jpg")

def set_anime_wallpaper_once():
    # Set the respective Wallpaper for each hour of the day
    # Deepnight Wallpaper
    if datetime.now().hour in range(0, 5):
        system("feh --bg-scale --no-fehbg '/home/emma/Bilder/Hintergründe/Anime Wallpaper/wideSniperNight.jpg'")
    # Morning Wallpaper
    elif datetime.now().hour in range(6, 9):
        system("feh --bg-scale --no-fehbg '/home/emma/Bilder/Hintergründe/Anime Wallpaper/wideDepressionMorning.jpg'")
    # Daytime Wallpaper
    elif datetime.now().hour in range(10, 17):
        system("feh --bg-scale --no-fehbg '/home/emma/Bilder/Hintergründe/Anime Wallpaper/WideStreetDay.jpg'")
    # Evening Wallpaper
    elif datetime.now().hour in range(18, 21):
        system("feh --bg-scale --no-fehbg '/home/emma/Bilder/Hintergründe/Anime Wallpaper/WideDualityEvening.jpg'")
    # Early Night Wallpaper
    else:
        system("feh --bg-scale --no-fehbg '/home/emma/Bilder/Hintergründe/Anime Wallpaper/wideNameNight.png'")

def set_chosen_wallpaper():
    global chosen_wallpaper_set
    if chosen_wallpaper_set == False:
        chosen_wallpaper_set = choose_wallpaper_set()
        logger.info(f"chose wallpaper set: {chosen_wallpaper_set}.")
    if chosen_wallpaper_set == "nature":
        set_wallpaper_once()
        logger.info(f"Set {chosen_wallpaper_set} wallpaper.")
    elif chosen_wallpaper_set == "anime":
        logger.info(f"Set {chosen_wallpaper_set} wallpaper.")
        set_anime_wallpaper_once()
    else:
        system("feh --bg-scale --no-fehbg /home/emma/Bilder/Hintergründe/wideFallbackScreen.jpg")
        logger.warning("Something went wrong and the fallback wallpaper has been set.")

def schedule_wallpapers():
    scheduler = BlockingScheduler()
    scheduler.add_job(set_chosen_wallpaper, trigger=CronTrigger(hour="1,6,10,18,22"))
    scheduler.start()
    logger.info("The scheduler has been started.")

def main():
    set_chosen_wallpaper()
    schedule_wallpapers()

if __name__ == "__main__":
    main()
