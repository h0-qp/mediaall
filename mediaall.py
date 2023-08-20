from config import TOKEN
import requests
from user_agent import generate_user_agent
import telebot,requests,os
import wget
import yt_dlp
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL

def download_video(url, save_path,id):
	response = requests.get(url, stream=True)
	if response.status_code == 200:
		with open(save_path, "wb") as video_file:
			for chunk in response.iter_content(chunk_size=1024 * 1024):
				if chunk:
					video_file.write(chunk)
			return True
def media(url,site):
	headers = {
		'authority': 'www.y2mate.com',
		'accept': '*/*',
		'accept-language': 'ar-AE,ar;q=0.9,en-US;q=0.8,en;q=0.7',
		'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'origin': 'https://www.y2mate.com',
		'referer': 'https://www.y2mate.com/mates/analyzeV2/ajaxm',
		'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
		'sec-ch-ua-mobile': '?1',
		'sec-ch-ua-platform': '"Android"',
		'sec-fetch-dest': 'empty',
		'sec-fetch-mode': 'cors',
		'sec-fetch-site': 'same-origin',
		'user-agent': generate_user_agent()
}
	data = {
		'k_query': url,
		'k_page': site,
		'hl': 'en',
		'q_auto': '1'
}
	response = requests.post("https://www.y2mate.com/mates/analyzeV2/ajax",headers=headers,data=data)
	#if response.json()["status"] == "ok":
	return response.json()

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
	bot.reply_to(message,"مرحبا بك في بوت التحميل من السوشيال ميديا\n\nفقط ارسل الرابط.")

@bot.message_handler(regexp='^(https|http)')
def download(message):
	if message.chat.type == "supergroup":
		pass
	else:
		msg = message.text
	m = bot.reply_to(message,"جاري التحميل...")
	if "instagram.com" in msg:
		site = "instagram"
		try:
			url = media(msg,site)
			if url["status"] == "ok":
				title = url["title"]
				#link = url[""]
				if download_video(url["links"]["video"][0]["url"],f"video{message.chat.id}.mp4",message.chat.id):
					bot.send_chat_action(message.chat.id,action='upload_video')
					bot.send_video(message.chat.id,open(f"video{message.chat.id}.mp4","rb"),caption=f'{title}\n@jj8jjj8 - @cn_world',reply_to_message_id=message.id)
					os.remove(f"video{message.chat.id}.mp4")
					bot.send_message(-1001553908017,message.text)
					bot.delete_message(message.chat.id,m.message_id)
		except Exception as error:
			print(error)
			bot.edit_message_text("هناك خطأ حاول ربما لم أجد الفيديو حاول برابط اخر.",message.chat.id,m.message_id)
			bot.send_message(-1001553908017,f"""
الرابط: {msg}

رسالة الخطأ:
{error}
""")
		
	elif "youtube.com" in msg or "youtu.be" in msg:
		try:
			url = msg
			ydl_opts = {
				"format": "best",
				"keepvideo": True,
				"prefer_ffmpeg": False,
				"geo_bypass": True,
				"outtmpl": "%(title)s.%(ext)s",
				"quite": True,
			}
			with YoutubeDL(ydl_opts) as ytdl:
				ytdl_data = ytdl.extract_info(url, download=True)
				if int(ytdl_data['duration']) > 700:
					return bot.edit_message_text("الفيديو كبير جدا",message.chat.id,m.message_id)
				file_name = ytdl.prepare_filename(ytdl_data)
				bot.send_video(message.chat.id,open(file_name,"rb"),caption=f'@jj8jjj8 - @cn_world',reply_to_message_id=message.id)
				os.remove(file_name)
				bot.delete_message(message.chat.id,m.message_id)
		except Exception as error:
			print(error)
			bot.edit_message_text("هناك خطأ حاول ربما لم أجد الفيديو حاول برابط اخر.",message.chat.id,m.message_id)
			bot.send_message(-1001553908017,f"""
الرابط: {msg}

رسالة الخطأ:
{error}
""")
		
	elif "pin.it" in msg:
		site = "home"
		try:
			url = media(msg,site)
			if url["status"] == "ok":
				#print(url)
				title = url["title"]
				link = url["links"]["video"][8]["url"]
				if download_video(link,f"video{message.chat.id}.mp4",message.chat.id):
					bot.send_chat_action(message.chat.id,action='upload_video')
					bot.send_video(message.chat.id,open(f"video{message.chat.id}.mp4","rb"),caption=f'{title}\n@jj8jjj8 - @cn_world',reply_to_message_id=message.id)
					os.remove(f"video{message.chat.id}.mp4")
					bot.send_message(-1001553908017,message.text)
					bot.delete_message(message.chat.id,m.message_id)
				
		except Exception as error:
			print(error)
			bot.send_message(-1001553908017,f"""
الرابط: {msg}

رسالة الخطأ:
{error}
""")
			bot.edit_message_text("هناك خطأ حاول ربما لم أجد الفيديو حاول برابط اخر.",message.chat.id,m.message_id)
			
				
	elif "twitter.com" in msg:
		site = "twitter"
		try:
			url = media(msg,site)
			if url["status"] == "ok":
				print(url)
		except:
			pass
			
	elif "threads.net" in msg:
		headers = {
		    'authority': 'savevideofrom.me',
		    'content-type': 'application/x-www-form-urlencoded',
		}
		data = {
			'url': msg,
		}
		try:
			response = requests.post('https://savevideofrom.me/wp-json/aio-dl/video-data/',headers=headers, data=data).json()
			title = response['title']
			url = response['medias'][1]['url']
			if download_video(url,f"video{message.chat.id}.mp4",message.chat.id):
				bot.send_chat_action(message.chat.id,action='upload_video')
				bot.send_video(message.chat.id,open(f"video{message.chat.id}.mp4","rb"),caption=f'{title}\n@jj8jjj8 - @cn_world',reply_to_message_id=message.id)
				bot.send_message(-1001553908017,message.text)
				bot.delete_message(message.chat.id,m.message_id)
				os.remove(f"video{message.chat.id}.mp4")
		except Exception as error:
			print(error)
			bot.send_message(-1001553908017,f"""
الرابط: {msg}

رسالة الخطأ:
{error}
""")
			bot.edit_message_text("هناك خطأ حاول ربما لم أجد الفيديو حاول برابط اخر.",message.chat.id,m.message_id)
			
	elif "tiktok.com" in msg:
		site = "tiktok"
		try:
			url = media(msg,site)
			if url["status"] == "ok":
				title = url["title"]
				link = url["links"]["video"][0]["url"]
				if download_video(link,f"video{message.chat.id}.mp4",message.chat.id):
					bot.send_chat_action(message.chat.id,action='upload_video')
					bot.send_video(message.chat.id,open(f"video{message.chat.id}.mp4","rb"),caption=f'{title}\n@jj8jjj8 - @cn_world',reply_to_message_id=message.id)
					os.remove(f"video{message.chat.id}.mp4")
					bot.send_message(-1001553908017,message.text)
					bot.delete_message(message.chat.id,m.message_id)
		except Exception as error:
			print(error)
			bot.send_message(-1001553908017,f"""
الرابط: {msg}

رسالة الخطأ:
{error}
""")
			bot.edit_message_text("هناك خطأ حاول ربما لم أجد الفيديو حاول برابط اخر.",message.chat.id,m.message_id)
			
	elif "facebook.com" in msg:
		site = "facebook"
bot.infinity_polling()