from telegram.ext import Updater, CommandHandler  # type: ignore

import logging
import os
import config
import visualize
import datetime as dt
from tempfile import NamedTemporaryFile


logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)


def start(update, context):
    logging.info("Answering `start` message.")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hello there.")

def week(update, context):
    logging.info(f"Processing `week` message with args: {context.args}")
    try:
        if len(context.args) == 0:
            week_offset = 0
        elif len(context.args) == 1:
            week_offset = int(context.args[0])
        else:
            raise ValueError()
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=(f"Cannot parse arguments {args}. "
                                       f"Try `/week <w:int>` where `w` "
                                       f"is the number of weeks since "
                                       f"today. `w` defaults to 0 if "
                                       f"not given."))
        return
    day_in_week = (dt.datetime.now().date()
                   - dt.timedelta(days=week_offset*7))
    day = day_in_week - dt.timedelta(days=day_in_week.weekday())
    weekmap = visualize.Weekmap(day)
    pic = weekmap.img
    with NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        logging.info(f"Writing map to: {tmp_file.name}")
        pic.savefig(tmp_file.name, format="png", bbox_inches="tight")
        context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=tmp_file,
                filename=f"week-{weekmap.start_day.isoformat()}.png")
        os.remove(tmp_file.name)


def main():
    api_token = config.TELEGRAMTOKEN
    updater = Updater(token=api_token, use_context=True)
    updater.dispatcher.add_handler(CommandHandler(
        'start',
        start))
    updater.dispatcher.add_handler(CommandHandler(
        'week',
        week))
    updater.start_polling()

if __name__ == "__main__":
    main()
