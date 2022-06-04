# Credits Goes To Mukund...!
# So DEAR PRO PPL DON"T EDIT THIS 


import os
import glob
import json
import logging
import random
import asyncio
import youtube_dl
from pytube import YouTube
from youtube_search import YoutubeSearch
from pytgcalls import PyTgCalls, idle
from pytgcalls import StreamType
from pytgcalls.types import Update
from pytgcalls.types import AudioPiped, AudioVideoPiped
from pytgcalls.types.stream import StreamAudioEnded, StreamVideoEnded
from pytgcalls.types import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo
)
from pyrogram import Client, filters
from pyrogram.raw.base import Update
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from Plugins.queues import QUEUE, add_to_queue, get_queue, clear_queue, pop_an_item
from Plugins.admin_check import *

bot = Client(
    "Music Stream Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

client = Client(os.environ["SESSION_NAME"], int(os.environ["API_ID"]), os.environ["API_HASH"])

app = PyTgCalls(client)

OWNER_ID = int(os.environ["OWNER_ID"])

BOT_USERNAME = os.environ["BOT_USERNAME"]

LIVE_CHATS = []

START_TEXT = """
ʜᴏɪ 

[»] ɪ ᴄᴀɴ ᴘʟᴀʏ ᴍᴜsᴄɪ ɪɴ ʙᴏᴛʜ ᴀᴜᴅɪᴏ ᴀɴᴅ ᴠɪᴅᴇᴏ ғᴏʀᴍ ᴏɴ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.

[»] ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ ᴀɴᴅ ᴇɴᴊᴏʏ.

[»] ʏᴏᴜ ᴄᴀɴ ᴍᴀᴋᴇ ʏᴏᴜʀ ᴏᴡɴ ʙᴏᴛ ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟʟᴏᴡ.

[»] ғᴏʀ ᴀɴʏ ᴋɪɴᴅ ᴏғ sᴜᴘᴘᴏʀᴛ ᴊᴏɪɴ ᴏᴜʀ sᴜᴘᴘᴏʀᴛ.

[»] ғᴏʀ ᴀɴʏ ғᴜᴛʜᴇʀ ᴜᴘᴅᴀᴛᴇ ᴏʀ ғᴏʀ ᴍᴏʀᴇ ʙᴏᴛs ᴊᴏɪɴ ᴏᴜʀ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ.
"""

START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
        ],
        [
            InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help_back"),
            InlineKeyboardButton("ʀᴇᴘᴏ", callback_data="repo")
        ],
        [
            InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/ALIEN_X_SUPPORT"),
            InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ", url="https://t.me/ALIEN_X_SUPPORT")
        ],
        [
            InlineKeyboardButton("ɢɪᴠᴇ ᴍᴇ ʜᴇᴀʀᴛ", url="https://t.me/ABOUT_MUKUND/15")
        ]
    ]
)

START_LUL = [
    [ 
        InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
    ],
    [ 
        InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help_back"),
        InlineKeyboardButton("ʀᴇᴘᴏ", callback_data="repo"),
    ],
    [ 
        InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/ALIEN_X_SUPPORT"),
        InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ", url="https://t.me/ALIEN_X_SUPPORT"),
    ],
    [ 
        InlineKeyboardButton("ɢɪᴠᴇ ᴍᴇ ʜᴇᴀʀᴛ", url="https://t.me/ABOUT_MUKUND/15"),
    ],    
]

BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", url="https://t.me/ALIEN_X_SUPPORT"),
            InlineKeyboardButton(text="ᴜᴘᴅᴀᴛᴇ", url="https://t.me/ALIEN_X_UPDATE")
        ]
    ]
)


BUTTONS = InlineKeyboardMarkup(
    [ 
        [ 
            InlineKeyboardButton(text="▷", callback_data="pause"),
            InlineKeyboardButton(text="II", callback_data="resume"),
            InlineKeyboardButton(text="‣‣I", callback_data="skip"),
            InlineKeyboardButton(text="▢", callback_data="stop")
        ],
        [ 
            InlineKeyboardButton(text="🔇", callback_data="mute"),
            InlineKeyboardButton(text="🔊", callback_data="unmute")
        ],
        [ 
            InlineKeyboardButton(text="• ᴄʟᴏsᴇ •", callback_data="ok")
        ]
    ]
)

MUKUND_MUSIC = [
    [ 
        InlineKeyboardButton(text="ᴜsᴇʀs", callback_data="basic_"),
        InlineKeyboardButton(text="ᴏᴡɴᴇʀ", callback_data="owner"),
    ],
    [ 
        InlineKeyboardButton(text="ᴀᴅᴍɪɴs", callback_data="admin_cmd"),
        InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="mukund"),
    ],
]

A_BUTTONS = [
    [
        InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="ok"),
        InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="help_back"),
    ],
]
REPO_BUTTONS = [
    [
        InlineKeyboardButton(text="sᴏᴜʀᴄᴇ", url="https://github.com/Legend-Mukund/Song"),
    ],
    [ 
        InlineKeyboardButton(text="ꜱᴜᴘᴘᴏʀᴛ", url="https://t.me/ALIEN_X_SUPPORT"),
        InlineKeyboardButton(text="ᴜᴘᴅᴀᴛᴇꜱ", url="https://t.me/ALIEN_X_UPDATE"),
        InlineKeyboardButton(text="Dᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/LEGEND_MUKUND"),
    ],
    [
        InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="mukund"),
    ],
]

REPO_MSG = """
ʜᴏɪ 

[»] ʜᴇʀᴇ ᴍᴜᴋᴜɴᴅ ᴍᴜsɪᴄ ɪ ᴄᴀɴ ᴘʟᴀʏ ᴍᴜsɪᴄ ɪɴ ʏᴏᴜʀ ᴄʜᴀᴛ.

[»] ʙᴏᴛʜ ᴀᴜᴅɪᴏ + ᴠɪᴅᴇᴏ sᴜᴘᴘᴏʀᴛ.

[»] ɪ ᴄᴀɴ ᴘʟᴀʏ ʏᴏᴜᴛᴜʙᴇ ᴠɪᴅᴇᴏs ᴛᴏᴏ sᴏ ʏᴏᴜ ᴄᴀɴ sᴇᴇ ᴍᴏᴠɪᴇs ᴛᴏᴏ.

[»] ʜᴇʀᴇ ɪs ᴛʜᴇ ʀᴇᴘᴏ ғᴏʀ ᴛʜᴇ ᴍᴜᴋᴜɴᴅ ᴍᴜsɪᴄ.

"""

HELP_TEXT = """
ʜᴏɪ 

[»] ʜᴇʀᴇ ɪs ᴛʜᴇ ʜᴇʟᴘ ᴍᴇɴᴜ ғᴏʀ ᴛʜᴇ ᴍᴜᴋᴜɴᴅ ᴍᴜsɪᴄ.

[»] ʀᴇᴀᴅ ɪᴛ ᴄᴀʀᴇ ғᴜʟʟʏ ɪᴛ ɪs ᴅɪᴠɪᴅᴇᴅ ɪɴᴛᴏ ᴛʜʀᴇᴇ sᴇᴄᴛɪᴏɴs .

[»] ᴀɴᴅ ғᴏʀ ᴀɴʏ ᴋɪɴᴅ ᴏғ ʜᴇʟᴘ ᴊᴏɪɴ @ALIEN_X_SUPPORT !!!

"""

OWNER_HELP = """
ʜᴏɪ 

[»] ʜᴇʀᴇ ɪs ᴛʜᴇ ᴏᴡɴᴇʀ ʜᴇʟᴘ ᴍᴇɴᴜ ғᴏʀ ᴛʜᴇ ᴍᴜᴋᴜɴᴅ ᴍᴜsɪᴄ.

[»] /restart : ᴛᴏ ʀᴇsᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ 

[»] sᴏᴏɴ ɪ ᴡɪʟʟ ᴀᴅᴅ ᴍᴏʀᴇ.

[»] ᴀɴᴅ ғᴏʀ ᴀɴʏ ᴋɪɴᴅ ᴏғ ʜᴇʟᴘ ᴊᴏɪɴ @ALIEN_X_SUPPORT !!!

"""

B_HELP = """
`ᴜsᴇʀ ᴄᴏᴍᴍᴀɴᴅs !!!`

[»] /play : ᴛᴏ ᴘʟᴀʏ ᴍᴜsɪᴄ ɪɴ ᴀᴜᴅɪᴏ ғᴏʀᴍ ᴏɴ ᴠᴄ.

[»] /vplay : ᴛᴏ ᴘʟᴀʏ ᴍᴜsɪᴄ ɪɴ ᴠɪᴅᴇᴏ ғᴏʀᴍ ᴏɴ ᴠᴄ.

[»] /playlist | /queue : ᴛᴏ sᴇᴇ ᴛʜᴇ ǫᴜᴇᴜᴇ ᴏʀ ᴘʟᴀʏʟɪsᴛ ᴛʜᴀᴛ ɪs ɢᴏɪɴɢ ᴛᴏ ʙᴇ ᴘʟᴀʏᴇᴅ.

[»] /join : ᴛᴏ ᴄᴀʟʟ ᴛʜᴇ ᴜsᴇʀ ʙᴏᴛ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛ

"""

A_HELP = """
`ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs !!!`

[»] /pause : ᴛᴏ ᴘᴀᴜsᴇ ᴛʜᴇ ᴜsᴇʀʙᴏᴛ ᴏɴ ᴠᴄ.

[»] /resume : ᴛᴏ ʀᴇsᴜᴍᴇ ᴛʜᴇ ᴜsᴇʀʙᴏᴛ ᴏɴ ᴠᴄ.

[»] /end : ᴛᴏ ᴇɴᴅ sᴛʀᴇᴀᴍɪɴɢ.

[»] /skip : ᴛᴏ sᴋɪᴘ ᴛʜᴇ ᴍᴜsɪᴄ ᴏɴ ᴠᴄ.

[»] /mute : ᴛᴏ ᴍᴜᴛᴇ ᴛʜᴇ ᴜsᴇʀʙᴏᴛ ᴏɴ ᴠᴄ.

[»] /unmute : ᴛᴏ ᴜɴᴍᴜᴛᴇ ᴛʜᴇ ᴜsᴇʀʙᴏᴛ ᴏɴ ᴠᴄ 

"""

@bot.on_callback_query()
def home(Client, CallbackQuery):
    if CallbackQuery.data == "mukund":
        CallbackQuery.edit_message_text(
            START_TEXT,
            reply_markup = InlineKeyboardMarkup(START_LUL)
        )
    elif CallbackQuery.data == "repo":
        CallbackQuery.edit_message_text(
            REPO_MSG,
            reply_markup = InlineKeyboardMarkup(REPO_BUTTONS)
        )
    elif CallbackQuery.data == "admin_cmd":
        CallbackQuery.edit_message_text(
            A_HELP,
            reply_markup = InlineKeyboardMarkup(A_BUTTONS)
        )
    elif CallbackQuery.data == "basic_":
        CallbackQuery.edit_message_text(
            B_HELP,
            reply_markup = InlineKeyboardMarkup(A_BUTTONS)
        )
    elif CallbackQuery.data == "owner":
        CallbackQuery.edit_message_text(
            OWNER_HELP,
            reply_markup = InlineKeyboardMarkup(A_BUTTONS)
        )    
    elif CallbackQuery.data == "help_back":
        CallbackQuery.edit_message_text(
            HELP_TEXT,
            reply_markup = InlineKeyboardMarkup(MUKUND_MUSIC)
        )
    elif CallbackQuery.data == "ok":
        CallbackQuery.message.delete()        

async def skip_current_song(chat_id):
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await app.leave_group_call(chat_id)
            clear_queue(chat_id)
            return 1
        else:
            title = chat_queue[1][0]
            duration = chat_queue[1][1]
            link = chat_queue[1][2]
            playlink = chat_queue[1][3]
            type = chat_queue[1][4]
            Q = chat_queue[1][5]
            thumb = chat_queue[1][6]
            if type == "Audio":
                await app.change_stream(
                    chat_id,
                    AudioPiped(
                        playlink,
                    ),
                )
            elif type == "Video":
                if Q == "high":
                    hm = HighQualityVideo()
                elif Q == "mid":
                    hm = MediumQualityVideo()
                elif Q == "low":
                    hm = LowQualityVideo()
                else:
                    hm = MediumQualityVideo()
                await app.change_stream(
                    chat_id, AudioVideoPiped(playlink, HighQualityAudio(), hm)
                )
            pop_an_item(chat_id)
            await bot.send_photo(chat_id, photo = thumb,
                                 caption = f"[»] <b>ɴᴏᴡ ᴘʟᴀʏɪɴɢ:</b> [{title}]({link})\n\n[»] ғᴏʀᴍᴀᴛ: `{type}` \n\n[»] <b>ᴅᴜʀᴀᴛɪᴏɴ:</b> {duration}",
                                 reply_markup = BUTTONS)
            return [title, link, type, duration, thumb]
    else:
        return 0


async def skip_item(chat_id, lol):
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        try:
            x = int(lol)
            title = chat_queue[x][0]
            chat_queue.pop(x)
            return title
        except Exception as e:
            print(e)
            return 0
    else:
        return 0


@app.on_stream_end()
async def on_end_handler(_, update: Update):
    if isinstance(update, StreamAudioEnded):
        chat_id = update.chat_id
        await skip_current_song(chat_id)


@app.on_closed_voice_chat()
async def close_handler(client: PyTgCalls, chat_id: int):
    if chat_id in QUEUE:
        clear_queue(chat_id)
        

async def yt_video(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()
    

async def yt_audio(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "bestaudio",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()

# THIS IS CALLBACK FOR FUNCTIONS 🌚

@bot.on_callback_query()
async def callbacks(_, cq: CallbackQuery):
    user_id = cq.from_user.id
    try:
        user = await cq.message.chat.get_member(user_id)
        admin_strings = ("creator", "administrator")
        if user.status not in admin_strings:
            is_admin = False
        else:
            is_admin = True
    except ValueError:
        is_admin = True        
    if not is_admin:
        return await cq.answer("[»] ʏᴏᴜ ᴀʀᴇɴ'ᴛ ᴀɴ ᴀᴅᴍɪɴ.")   
    chat_id = cq.message.chat.id
    data = cq.data
    if data == "close":
        return await cq.message.delete()
    if not chat_id in QUEUE:
        return await cq.answer("[»] ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")

    if data == "pause":
        try:
            await app.pause_stream(chat_id)
            await cq.answer("[»] ᴘᴀᴜsᴇᴅ sᴛʀᴇᴀᴍɪɴɢ.")
        except:
            await cq.answer("[»] ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")
      
    elif data == "resume":
        try:
            await app.resume_stream(chat_id)
            await cq.answer("[»] Resumed streaming.")
        except:
            await cq.answer("[»] ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")   

    elif data == "stop":
        await app.leave_group_call(chat_id)
        clear_queue(chat_id)
        await cq.answer("[»] sᴛᴏᴘᴘᴇᴅ sᴛʀᴇᴀᴍɪɴɢ.")  

    elif data == "mute":
        try:
            await app.mute_stream(chat_id)
            await cq.answer("[»] ᴍᴜᴛᴇᴅ sᴛʀᴇᴀᴍɪɴɢ.")
        except:
            await cq.answer("[»] ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")
            
    elif data == "unmute":
        try:
            await app.unmute_stream(chat_id)
            await cq.answer("[»] ᴜɴᴍᴜᴛᴇᴅ sᴛʀᴇᴀᴍɪɴɢ.")
        except:
            await cq.answer("[»] ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")
            
    elif data == "skip":
        op = await skip_current_song(chat_id)
        if op == 0:
            await cq.answer("[»] ɴᴏᴛʜɪɴɢ ɪɴ ᴛʜᴇ ǫᴜᴇᴜᴇ ᴛᴏ sᴋɪᴘ.")
        elif op == 1:
            await cq.answer("[»] ᴇᴍᴘᴛʏ ǫᴜᴇᴜᴇ, sᴛᴏᴘᴘᴇᴅ sᴛʀᴇᴀᴍɪɴɢ.")
        else:
            await cq.answer("[»] sᴋɪᴘᴘᴇᴅ.")

@bot.on_message(filters.command("help") & filters.private)
async def help_private(_, message):
    msg = HELP_TEXT.format(message.from_user.mention)
    await message.reply_text(text = msg,
                             reply_markup = MUKUND_MUSIC)            

@bot.on_message(filters.command("help") & filters.group)
async def help(_, message):
    msg = HELP_TEXT.format(message.from_user.mention)
    await message.reply_text(text = msg,
                             reply_markup = MUKUND_MUSIC)  

@bot.on_message(filters.command("start") & filters.private)
async def start_private(_, message):
    msg = START_TEXT.format(message.from_user.mention)
    await message.reply_text(text = msg,
                             reply_markup = START_BUTTONS)

@bot.on_message(filters.command("start") & filters.group)
async def start(_, message):
    msg = START_TEXT.format(message.from_user.mention)
    await message.reply_text(text = msg,
                             reply_markup = START_BUTTONS)
    

@bot.on_message(filters.command(["play", "vplay"]) & filters.group)
async def video_play(_, message):
    await message.delete()
    user_id = message.from_user.id
    state = message.command[0].lower()
    try:
        query = message.text.split(None, 1)[1]
    except:
        return await message.reply_text(f"<b>ᴜsᴀɢᴇ:</b> <code>/{state} [query]</code>")
    chat_id = message.chat.id
    if chat_id in LIVE_CHATS:
        return await message.reply_text("❗️ᴘʟᴇᴀsᴇ sᴇɴᴅ <code>/stop</code> ᴛᴏ ᴇɴᴅ ᴄᴜʀʀᴇɴᴛ ʟɪᴠᴇ sᴛʀᴇᴀᴍɪɴɢ ʙᴇғᴏʀᴇ ᴘʟᴀʏ sᴏɴɢs ᴏʀ ᴠɪᴅᴇᴏs.")
    
    m = await message.reply_text("🔄 ᴘʀᴏᴄᴇssɪɴɢ...")
    if state == "play":
        damn = AudioPiped
        ded = yt_audio
        doom = "Audio"
    elif state == "vplay":
        damn = AudioVideoPiped
        ded = yt_video
        doom = "Video"
    if "low" in query:
        Q = "low"
    elif "mid" in query:
        Q = "mid"
    elif "high" in query:
        Q = "high"
    else:
        Q = "0"
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        thumb = results[0]["thumbnails"][0]
        duration = results[0]["duration"]
        yt = YouTube(link)
        cap = f"[»] <b>ɴᴏᴡ ᴘʟᴀʏɪɴɢ:</b> [{yt.title}]({link})\n\n[»] ғᴏʀᴍᴀᴛ: `{doom}` \n\n[»] <b>ᴅᴜʀᴀᴛɪᴏɴ:</b> {duration}"
        try:
            ydl_opts = {"format": "bestvideo[height<=720]+bestaudio/best[height<=720]"}
            ydl = youtube_dl.YoutubeDL(ydl_opts)
            info_dict = ydl.extract_info(link, download=False)
            p = json.dumps(info_dict)
            a = json.loads(p)
            playlink = a['formats'][1]['manifest_url']
        except:
            ice, playlink = await ded(link)
            if ice == "0":
                return await m.edit("❗️ʏᴛᴅʟ ᴇʀʀᴏʀ !!!")               
    except Exception as e:
        return await m.edit(str(e))
    
    try:
        if chat_id in QUEUE:
            position = add_to_queue(chat_id, yt.title, duration, link, playlink, doom, Q, thumb)
            caps = f"#️⃣ [{yt.title}]({link}) <b>ǫᴜᴇᴜᴇᴅ ᴀᴛ ᴘᴏsɪᴛɪᴏɴ {position}</b> \n\n⏳ <b>ᴅᴜʀᴀᴛɪᴏɴ:</b> {duration}"
            await message.reply_photo(thumb, caption=caps)
            await m.delete()
        else:            
            await app.join_group_call(
                chat_id,
                damn(playlink),
                stream_type=StreamType().pulse_stream
            )
            add_to_queue(chat_id, yt.title, duration, link, playlink, doom, Q, thumb)
            await message.reply_photo(thumb, caption=cap, reply_markup=BUTTON)
            await m.delete()
    except Exception as e:
        return await m.edit(str(e))
    
@bot.on_message(filters.command(["join", "join@{BOT_USERNAME}"]) & filters.group)
async def join_chat(c: Client, m: Message):
    chat_id = m.chat.id
    try:
        invitelink = await c.export_chat_invite_link(chat_id)
        if invitelink.startswith("https://t.me/+"):
            invitelink = invitelink.replace(
                "https://t.me/+", "https://t.me/joinchat/"
            )
            await client.join_chat(invitelink)
            return await client.send_message(chat_id, "✅ Assistant joined chat")
    except UserAlreadyParticipant:
        return await client.send_message(chat_id, "✅ Assistant already in chat")    
    
@bot.on_message(filters.command(["saudio", "svideo"]) & filters.group)
@is_admin
async def stream_func(_, message):
    await message.delete()
    state = message.command[0].lower()
    try:
        link = message.text.split(None, 1)[1]
    except:
        return await message.reply_text(f"<b>ᴜsᴀɢᴇ:</b> <code>/{state} [link]</code>")
    chat_id = message.chat.id
    
    if state == "saudio":
        damn = AudioPiped
        emj = "🎵"
    elif state == "svideo":
        damn = AudioVideoPiped
        emj = "🎬"
    m = await message.reply_text("🔄 ᴘʀᴏᴄᴇssɪɴɢ...")
    try:
        if chat_id in QUEUE:
            return await m.edit("❗️ᴘʟᴇᴀsᴇ sᴇɴᴅ <code>/stop</code> ᴛᴏ ᴇɴᴅ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ʙᴇғᴏʀᴇ ʟɪᴠᴇ sᴛʀᴇᴀᴍɪɴɢ.")
        elif chat_id in LIVE_CHATS:
            await app.change_stream(
                chat_id,
                damn(link)
            )
            await m.edit(f"{emj} sᴛᴀʀᴛᴇᴅ sᴛʀᴇᴀᴍɪɴɢ: [Link]({link})", disable_web_page_preview=True)
        else:    
            await app.join_group_call(
                chat_id,
                damn(link),
                stream_type=StreamType().pulse_stream)
            await m.edit(f"{emj} sᴛᴀʀᴛᴇᴅ sᴛʀᴇᴀᴍɪɴɢ: [Link]({link})", disable_web_page_preview=True)
            LIVE_CHATS.append(chat_id)
    except Exception as e:
        return await m.edit(str(e))


@bot.on_message(filters.command("skip") & filters.group)
@is_admin
async def skip(_, message):
    await message.delete()
    chat_id = message.chat.id
    if len(message.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await message.reply_text("❗️ɴᴏᴛʜɪɴɢ ɪɴ ᴛʜᴇ ǫᴜᴇᴜᴇ ᴛᴏ sᴋɪᴘ.")
        elif op == 1:
            await message.reply_text("❗️ᴇᴍᴘᴛʏ ǫᴜᴇᴜᴇ, sᴛᴏᴘᴘᴇᴅ sᴛʀᴇᴀᴍɪɴɢ.")
    else:
        skip = message.text.split(None, 1)[1]
        out = "🗑 <ʙ>ʀᴇᴍᴏᴠᴇᴅ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ sᴏɴɢs ғʀᴏᴍ ᴛʜᴇ ǫᴜᴇᴜᴇ:</b> \n"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        out = out + "\n" + f"<b>#️⃣ {x}</b> - {hm}"
            await message.reply_text(out)
            
ALIVE_TEXT = """
[»] ʏᴏ ʏᴏ ᴍᴜᴋᴜɴᴅ ᴍᴜsɪᴄ ʜᴇʀᴇ.

[»] ᴜsᴇʀʙᴏᴛ : `ᴀʟɪᴠᴇ`

[»] ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ : `1.4.16`

"""
@bot.on_message(filters.command("alive"))
async def alive(_, message):
    user_id = message.from_user.id
    if user_id != OWNER_ID:
        return
    await message.reply_photo(random.choice(PHOTO), caption=ALIVE_TEXT, reply_markup = BUTTON)

                    
@bot.on_message(filters.command(["playlist", "queue"]) & filters.group)
@is_admin
async def playlist(_, message):
    chat_id = message.chat.id
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await message.delete()
            await message.reply_text(
                f"▶️ <b>ɴᴏᴡ ᴘʟᴀʏɪɴɢ:</b> [{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][4]}`",
                disable_web_page_preview=True,
            )
        else:
            out = f"<b>📃 Player queue:</b> \n\n▶️ <b>ɴᴏᴡ ᴘʟᴀʏɪɴɢ:</b> [{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][4]}` \n"
            l = len(chat_queue)
            for x in range(1, l):
                title = chat_queue[x][0]
                link = chat_queue[x][2]
                type = chat_queue[x][4]
                out = out + "\n" + f"<b>#️⃣ {x}</b> - [{title}]({link}) | `{type}` \n"
            await message.reply_text(out, disable_web_page_preview=True)
    else:
        await message.reply_text("❗ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")
    

@bot.on_message(filters.command("stop") & filters.group)
@is_admin
async def end(_, message):
    await message.delete()
    chat_id = message.chat.id
    if chat_id in LIVE_CHATS:
        await app.leave_group_call(chat_id)
        LIVE_CHATS.remove(chat_id)
        return await message.reply_text("▢ sᴛᴏᴘᴘᴇᴅ sᴛʀᴇᴀᴍɪɴɢ.")
        
    if chat_id in QUEUE:
        await app.leave_group_call(chat_id)
        clear_queue(chat_id)
        await message.reply_text("▢ sᴛᴏᴘᴘᴇᴅ sᴛʀᴇᴀᴍɪɴɢ.")
    else:
        await message.reply_text("❗ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")
        

@bot.on_message(filters.command("pause") & filters.group)
@is_admin
async def pause(_, message):
    await message.delete()
    chat_id = message.chat.id
    if chat_id in QUEUE:
        try:
            await app.pause_stream(chat_id)
            await message.reply_text("II ᴘᴀᴜsᴇᴅ sᴛʀᴇᴀᴍɪɴɢ.")
        except:
            await message.reply_text("❗ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")
    else:
        await message.reply_text("❗ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")
        
        
@bot.on_message(filters.command("resume") & filters.group)
@is_admin
async def resume(_, message):
    await message.delete()
    chat_id = message.chat.id
    if chat_id in QUEUE:
        try:
            await app.resume_stream(chat_id)
            await message.reply_text("▷ ʀᴇsᴜᴍᴇᴅ sᴛʀᴇᴀᴍɪɴɢ.")
        except:
            await message.reply_text("❗ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")
    else:
        await message.reply_text("❗ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")
        
        
@bot.on_message(filters.command("mute") & filters.group)
@is_admin
async def mute(_, message):
    await message.delete()
    chat_id = message.chat.id
    if chat_id in QUEUE:
        try:
            await app.mute_stream(chat_id)
            await message.reply_text("🔇 ᴍᴜᴛᴇᴅ sᴛʀᴇᴀᴍɪɴɢ.")
        except:
            await message.reply_text("❗ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")
    else:
        await message.reply_text("❗ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")
        
        
@bot.on_message(filters.command("unmute") & filters.group)
@is_admin
async def unmute(_, message):
    await message.delete()
    chat_id = message.chat.id
    if chat_id in QUEUE:
        try:
            await app.unmute_stream(chat_id)
            await message.reply_text("🔊 ᴜɴᴍᴜᴛᴇᴅ sᴛʀᴇᴀᴍɪɴɢ.")
        except:
            await message.reply_text("❗ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")
    else:
        await message.reply_text("❗ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")

PHOTO = [
    "https://telegra.ph/file/8d5ae37f8b4b2b1b64763.jpg",
    "https://telegra.ph/file/2d4d106a4b4ecacb99374.jpg",
    "https://telegra.ph/file/e635ced7273b64341adea.jpg",
    "https://telegra.ph/file/e42dfbac4be6ddbf1d99f.jpg",
    "https://telegra.ph/file/db0a91985e4e963b6ef31.jpg",
    "https://telegra.ph/file/9434e8ead90db9a5404e2.jpg",
]


@bot.on_message(filters.command("broadcast"))
async def broadcast(_, message: Message):
    sent=0
    failed=0
    if message.from_user.id not in OWNER_ID:
        return
    else:
        mukund = await message.reply("`sᴛᴀʀᴛᴇᴅ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ᴡᴀɪᴛ👩‍💻`")
        if not message.reply_to_message:
            await mukund.edit("**__ɢɪᴍᴍɪ ᴀɴʏ ᴍᴇssᴀɢᴇ ᴛᴏ ɢᴄᴀsᴛ...__**")
            return
        devu = message.reply_to_message.text
        async for dialog in client.iter_dialogs():
            try:
                await client.send_message(dialog.chat.id, devu)
                sent = sent+1
                await mukund.edit(f"`ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ` \n\n**sᴜᴄᴄᴇssғᴜʟʟ ɪɴ:** `{sent}` ᴄʜᴀᴛs \n**ᴜɴsᴜᴄᴄᴇssғᴜʟʟ ɪɴ:** {failed} ᴄʜᴀᴛs🗑️")
                await asyncio.sleep(3)
            except:
                failed=failed+1
        await message.reply_photo(random.choice(PHOTO), caption=f"`sᴜᴄᴄᴇsғᴜʟʟʏ ᴅᴏɴᴇ🧚‍♀️` \n\nsᴜᴄᴄᴇssғᴜʟʟ**:** `{sent}` ᴄʜᴀᴛs \n**ғᴀɪʟᴇᴅ :** {failed} ᴄʜᴀᴛs")

        
@bot.on_message(filters.command("restart"))
async def restart(_, message):
    user_id = message.from_user.id
    if user_id != OWNER_ID:
        return
    await message.reply_text("🛠 <i>ʀᴇsᴛᴀʀᴛɪɴɢ ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ...</i>")
    os.system(f"kill -9 {os.getpid()} && python3 app.py")
            

app.start()
bot.run()
idle()
