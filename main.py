# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import pyrogram, os, asyncio

try:
    app_id = int(os.environ.get("app_id", "20389440"))
except Exception as app_id:
    print(f"⚠️ App ID Invalid {app_id}")
try:
    api_hash = os.environ.get("api_hash", "a1a06a18eb9153e9dbd447cfd5da2457")
except Exception as api_id:
    print(f"⚠️ Api Hash Invalid {api_hash}")
try:
    bot_token = os.environ.get("bot_token", "6564513574:AAH3Y97iqQjSlV5vKKZdGDUohlhpA-LeSbw")
except Exception as bot_token:
    print(f"⚠️ Bot Token Invalid {bot_token}")
try:
    dynamic_caption = "`{file_name}`"
except Exception as dynamic_caption:
    print(f"⚠️ Dynamic Caption Invalid {dynamic_caption}")

user_captions = {}

AutoCaptionBotV1 = pyrogram.Client(
    name="AutoCaptionBotV1", api_id=app_id, api_hash=api_hash, bot_token=bot_token)

start_message = """
<b>👋Hello {}</b>
<b>I am an AutoCaption bot</b>
<b>All you have to do is add me to your channel and I will show you my power</b>
<b>@XAYOONARA</b>"""

about_message = """
<b>• Developer : <a href=https://t.me/VJ_Botz>XAYONARA</a></b>
<b>• Language : Python3</b>
<b>• Library : Pyrogram v{version}</b>"""

@AutoCaptionBotV1.on_message(pyrogram.filters.private & pyrogram.filters.command(["start"]))
def start_command(bot, update):
    update.reply(start_message.format(update.from_user.mention), parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)

@AutoCaptionBotV1.on_callback_query(pyrogram.filters.regex("start"))
def strat_callback(bot, update):
    update.message.edit(start_message.format(update.from_user.mention), parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)

@AutoCaptionBotV1.on_callback_query(pyrogram.filters.regex("about"))
def about_callback(bot, update):
    bot = bot.get_me()
    update.message.edit(about_message.format(version=pyrogram.__version__, username=bot.mention), parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)

@AutoCaptionBotV1.on_message(pyrogram.filters.private & pyrogram.filters.command(["setcaption"]))
def set_caption_command(bot, update):
    user_id = update.from_user.id if update.from_user else None
    if user_id is not None:
        # Extract the caption from the command
        command_parts = update.text.split(" ", 1)
        if len(command_parts) > 1:
            user_captions[user_id] = command_parts[1]
            update.reply(f"Caption set to: {user_captions[user_id]}")
        else:
            update.reply("Please provide a caption.")
    else:
        update.reply("Unable to identify user.")

@AutoCaptionBotV1.on_message(pyrogram.filters.channel)
def edit_caption(bot, update: pyrogram.types.Message):
    motech, _ = get_file_details(update)
    if update.from_user and update.from_user.id in user_captions:
        try:
            user_caption = user_captions[update.from_user.id]
            caption_text = user_caption.format(file_name=motech.file_name)
            bot.edit_message_caption(
                chat_id=update.chat.id,
                message_id=update.message_id,
                caption=caption_text
            )
        except pyrogram.errors.FloodWait as FloodWait:
            asyncio.sleep(FloodWait.value)
            user_caption = user_captions[update.from_user.id]
            caption_text = user_caption.format(file_name=motech.file_name)
            bot.edit_message_caption(
                chat_id=update.chat.id,
                message_id=update.message_id,
                caption=caption_text
            )
        except pyrogram.errors.MessageNotModified:
            pass

def get_file_details(update: pyrogram.types.Message):
    if update.media:
        for message_type in (
            "photo",
            "animation",
            "audio",
            "document",
            "video",
            "video_note",
            "voice",
            "sticker"
        ):
            obj = getattr(update, message_type)
            if obj:
                return obj, obj.file_id

print("Telegram AutoCaption V1 Bot Start")
print("Bot Created By https://t.me/xayoonara")

AutoCaptionBotV1.run()
