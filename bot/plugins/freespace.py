import logging

# noinspection PyPackageRequirements
from telegram import Update, BotCommand
from telegram.ext import CommandHandler, CallbackContext

from bot.qbtinstance import qb
from bot.updater import updater
from utils import u
from utils import Permissions

logger = logging.getLogger(__name__)


@u.check_permissions(required_permission=Permissions.ADMIN)
@u.failwithmessage
def on_freespace_command(update: Update, context: CallbackContext):
    logger.info('/freespace from %s', update.message.from_user.first_name)
    # do not remove downloaded torrent file
    # qb.delete_all_permanently()
    #text = f"Cleared storage, save path: <code>{qb.save_path}</code>"
    text = f"feature disabled"

    update.message.reply_html(text)


updater.add_handler(CommandHandler(["space", "freespace"], on_freespace_command), bot_command=BotCommand("freespace", "free space from download path"))
