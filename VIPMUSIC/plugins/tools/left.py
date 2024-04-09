from VIPMUSIC import app
from pyrogram import filters
from pyrogram.errors import RPCError
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from os import environ
from typing import Union, Optional
from PIL import Image, ImageDraw, ImageFont
from os import environ
import random
from pyrogram import Client, filters
from pyrogram.types import ChatJoinRequest, InlineKeyboardButton, InlineKeyboardMarkup
from PIL import Image, ImageDraw, ImageFont
import asyncio, os, time, aiohttp
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from asyncio import sleep
from pyrogram import filters, Client, enums
from pyrogram.enums import ParseMode
from pyrogram import *
from pyrogram.types import *
from logging import getLogger
from VIPMUSIC.utils.vip_ban import admin_filter
from VIPMUSIC import app
from pyrogram import filters
from pyrogram.errors import RPCError
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from os import environ
from typing import Union, Optional
from PIL import Image, ImageDraw, ImageFont
import random
import asyncio

random_photo = [
    "https://telegra.ph/file/e444b74940e480dd62a11.jpg",
    "https://telegra.ph/file/06e5de22a8a02d0be0010.jpg",
    "https://telegra.ph/file/843359e2b1553b792df2d.jpg",
    "https://telegra.ph/file/d62b1af207276d22f1211.jpg",
    "https://telegra.ph/file/1e0e6a85cea882a6980ce.jpg",
]

bg_path = "VIPMUSIC/assets/userinfo.png"
font_path = "VIPMUSIC/assets/hiroko.ttf"

get_font = lambda font_size, font_path: ImageFont.truetype(font_path, font_size)

async def get_userinfo_img(
    bg_path: str,
    font_path: str,
    user_id: Union[int, str],
    profile_path: Optional[str] = None
):
    bg = Image.open(bg_path)

    if profile_path:
        img = Image.open(profile_path)
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.pieslice([(0, 0), img.size], 0, 360, fill=255)

        circular_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        circular_img.paste(img, (0, 0), mask)
        resized = circular_img.resize((400, 400))
        bg.paste(resized, (440, 160), resized)

    img_draw = ImageDraw.Draw(bg)

    img_draw.text(
        (529, 627),
        text=str(user_id).upper(),
        font=get_font(46, font_path),
        fill=(255, 255, 255),
    )

    path = f"./userinfo_img_{user_id}.png"
    bg.save(path)
    return path

@app.on_chat_member_updated(filters.group, group=-22)
async def member_has_left(client: app, member: ChatMemberUpdated):
    if (
        not member.new_chat_member
        and member.old_chat_member.status not in {"banned", "left", "restricted"}
        and member.old_chat_member
    ):
        user = (
            member.old_chat_member.user
            if member.old_chat_member
            else member.from_user
        )
        if user.photo:
            photo = await app.download_media(user.photo.big_file_id)
            welcome_photo = await get_userinfo_img(
                bg_path=bg_path,
                font_path=font_path,
                user_id=user.id,
                profile_path=photo,
            )
        else:
            welcome_photo = random.choice(random_photo)

        caption = f"**#New_Member_Left**\n\n**๏** {user.mention} **ʜᴀs ʟᴇғᴛ ᴛʜɪs ɢʀᴏᴜᴘ**\n**๏ sᴇᴇ ʏᴏᴜ sᴏᴏɴ ᴀɢᴀɪɴ..!**"
        button_text = "๏ ᴠɪᴇᴡ ᴜsᴇʀ ๏"
        deep_link = f"tg://openmessage?user_id={user.id}"

        message = await client.send_photo(
            chat_id=member.chat.id,
            photo=welcome_photo,
            caption=caption,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(button_text, url=deep_link)]
            ])
        )
        async def delete_message():
            await asyncio.sleep(30)
            await message.delete()

        # Run the task
        asyncio.create_task(delete_message())
