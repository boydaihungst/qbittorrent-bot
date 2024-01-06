import logging
import json

from telegram import ParseMode
from telegram.ext import CallbackContext

from .qbtinstance import qb
from utils import u
from config import config
import time

logger = logging.getLogger("jobs")
lastest_checked_time = time.time()


@u.failwithmessage_job
def notify_completed(context: CallbackContext):
    logger.info('executing completed job...')
    completed = qb.torrents(filter='completed', get_torrent_generic_properties=False)
    current_time = time.time()
    try:
        with open("lastest_checked_time.txt", "r") as f:
            lastest_checked_time = float(f.readline())
            f.close()
    except FileNotFoundError:
        f = open("lastest_checked_time.txt", 'w+')
        f.write(str(lastest_checked_time))
        f.close()
    for torrent in completed:
        if ( lastest_checked_time > torrent.completion_on ):
            continue

        logger.info('new completed torrent: %s (%s)', torrent.hash, torrent.name)

        if not config.notifications.completed_torrents:
            logger.info("notifications chat not set in the config file")
            continue

        if config.notifications.no_notification_tag:
            tag_lower = config.notifications.no_notification_tag.lower()
            if tag_lower in torrent.tags_list(lower=True):
                logger.info('the torrent has been tagged "%s": no notification will be sent', tag_lower)
                continue

        text = f'<code>{torrent.name_escaped}</code> completed ({torrent.size_pretty}, <a href="{torrent.public_url}">Download</a>'
        logger.debug("sending message")
        context.bot.send_message(
            chat_id=config.notifications.completed_torrents,
            text=text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            disable_notification=True
        )
    f = open("lastest_checked_time.txt", 'w+')
    f.write(str(current_time))
    f.close()
    logger.info('...completed job executed')
