import requests,re,random,wget,yt_dlp,os,datetime,time,asyncio
from user_agent import generate_user_agent
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL
from kvsqlite.sync import Client as C
import glob

#import logging
import aiogram
from aiogram import Bot, Dispatcher, types,filters
#from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup as km, InlineKeyboardButton as btn
import time
from config import TOKEN,ID

db = C("download.sqlite")

token = TOKRN
#logging.basicConfig(level=logging.INFO)


bot = Bot(token=token)
#storage = MemoryStorage()
bot = Dispatcher(bot)#, storage=storage)

def stm(seconds):
	return '{:02}:{:02}:{:02}'.format(seconds // 3600, seconds % 3600 // 60, seconds % 60)

def download_video(url, save_path,id):
	response = requests.get(url, stream=True)
	if response.status_code == 200:
		with open(save_path, "wb") as video_file:
			for chunk in response.iter_content(chunk_size=1024 * 1024):
				if chunk:
					video_file.write(chunk)
			return True

what = {
	"adaa": "False",
	"replace_channel": "False",
	"replace_startMSG": "False"
}
mis = {
}

if not db.exists("startMSG"):
	db.set("startMSG", '''- مرحبا بك {mention}
	- في بوت تحميل من الانستكرام 
	
للتحميل ارسل الرابط فقط.''')

if not db.exists("channel"):
	id_channel = -1001199094601
	info = requests.get(f"https://api.telegram.org/bot{token}/getChat?chat_id={id_channel}").json()
	info = info["result"]
	id = info["id"]
	title = info["title"]
	username = info["username"]
	link = info["invite_link"]
	data = {
		"title": title,
		"id": id,
		"username": username,
		"link": link
	}
	db.set("channel",data)

userbot = "V2TDBOT" # يوزر البوت بدون @

if db.get("channel")["username"] == None:
	username = userbot
else:
	username = db.get("channel")["username"]

dev = ID #ايدي حسابك

in_msg = """
دخل شخص جديد للبوت الخاص بك.

اسمه: {}
ايديه: {}
معرفه: @{}

عدد اعضاء البوت الان {} عضو
"""

for i in dir(bot.bot):
	print(i)

@bot.message_handler(filters.CommandStart())
async def welcome(message):
	if db.get("members") == None:
		db.set("members", [1160471152])
	name = message.from_user.full_name
	id = message.from_user.id
	mention = "["+name+"](tg://user?id="+str(id)+")"
	
	if message.from_user.id != dev:
		members = db.get("members")
		print(members)
		if not id in members:
			members.append(id)
			db.set("members",members)
			number = 0
			for i in db.get("members"):
				number += 1
			if db.get("dkhol") == True:
				await bot.bot.send_message(dev,in_msg.format(message.from_user.first_name,message.from_user.id,message.from_user.username,number))
		else:
			pass
		await message.reply(db.get("startMSG").replace("{mention}",mention),parse_mode="Markdown")
		if db.get("forward") == True and message.from_user.id != dev:
			await message.forward(dev)
	else:
		if db.get("dkhol") in [None,False]:
			dkhol = "❌"
		else:
			dkhol = "✅"
		
		if db.get("forward") in [None,False]:
			forward = "❌"
		else:
			forward = "✅"
		
		btn1 = btn(text="الاحصائيات",callback_data="stats")
		btn2 = btn(text="اذاعة",callback_data="adaa")

		btn3 = btn(text=f"اشعار الدخول {dkhol}",callback_data="dkhol")
		btn4 = btn(text=f"توجيه الرسائل {forward}",callback_data="forward")
		
		btn5 = btn(text="قناة الاشتراك الاجباري.",callback_data="channel")
		btn6 = btn(text="رسالة start.",callback_data="startMSG")
		
		btns = km().add(btn1,btn2).add(btn3,btn4).add(btn5,btn6)
		
		await message.reply(db.get("startMSG").replace("{mention}",mention),parse_mode="Markdown")
		await message.reply("""
مرحبا بك سيدي في بوتك اختر ادناه...""",reply_markup=btns)

@bot.message_handler(filters.Regexp("^نسخ(ه|ة) احتياطي(ه|ة)$"))
async def nska(message):
	if message.from_user.id != dev:
		return
	await message.reply_document(open("download.sqlite","rb"))

@bot.message_handler(filters.Regexp("^(http|https)://(www.|)instagram.com"))
async def instagram(message):
	if db.get("forward") == True and message.from_user.id != dev:
		await message.forward(dev)
	print("instagram")
	link = message.text
	chat_id = message.chat.id
	if what["adaa"] == "True" and message.from_user.id == dev:
		done = 0
		users = db.get("members")
		for user in users:
			try:
				await bot.bot.copy_message(chat_id=user,from_chat_id=chat_id,message_id=message.message_id)
				done += 1
			except:
				continue
		await message.reply(f"تم ارسال الاذاعة الى {done} من الاعضاء")
		what["adaa"] = "False"
		return
	m = await message.reply("جاري التحميل انتظر...")
	if "/p/" in link or "/reel/" in link:
		response = requests.get(f"https://apimedia.hussienalaraqe8.repl.co/instagram?url={link}").json()
		#print(response)
		try:
			if response["title"] is None:
				title = "no caption"
			else:
				title = response["title"]
		
			medias = []
			media = []
			videos = response["links"]["video"]
			print(videos[0]["url"])
			n = 0
			
			if len(videos) == 1:
				await bot.bot.send_chat_action(chat_id, "upload_video")
				if "video" in videos[0]["q_text"]:
					download_video(videos[0]["url"],f"{chat_id}{n}.mp4",message.from_user.id)
					await message.reply_video(open(f"{chat_id}{n}.mp4","rb"),caption=f"@{username}")
					await m.delete()
					os.remove(f"{chat_id}{n}.mp4")
				else:
					download_video(videos[0]["url"],f"{chat_id}{n}.jpg",message.from_user.id)
					await message.reply_photo(open(f"{chat_id}{n}.jpg","rb"),caption=f"@{username}")
					await m.delete()
					os.remove(f"{chat_id}{n}.jpg")
				return
				
			for num in range(len(videos)):
				video = videos[num]
				if len(media) >= 10:
					await bot.bot.send_chat_action(chat_id, "upload_video")
					await message.reply_media_group(media)
					media.clear()
					continue
				if "video" in video["q_text"]:
					download_video(video["url"],f"{chat_id}{n}.mp4",message.from_user.id)
					media.append(types.InputMediaVideo(open(f"{chat_id}{n}.mp4","rb"),caption=f"@{username}"))
					n +=1
				else:
					download_video(video["url"],f"{chat_id}{n}.jpg",message.from_user.id)
					media.append(types.InputMediaPhoto(open(f"{chat_id}{n}.jpg","rb"),caption=f"@{username}"))
					n+=1
				
				time.sleep(1)
			
			if len(media) >=1:
				await bot.bot.send_chat_action(chat_id, "upload_video")
				await message.reply_media_group(media)
				media.clear()
			await m.delete()
			for i in glob.glob(f"{chat_id}*.mp4"):
				os.remove(i)
			for i in glob.glob(f"{chat_id}*.jpg"):
				os.remove(i)
		except Exception as error:
			print(error)
			await m.edit_text("حدث خطأ.")
			await bot.bot.send_message(dev,f"""
الرابط: {message.text}

رسالة الخطأ:
{error}
""")
	
	elif "/s/" in link:
		response = requests.get(f"https://apimedia.hussienalaraqe8.repl.co/highlights?url={link}").json()
		try:
			media = []
			videos = response["data"]['medias']
			n = 0
			if len(videos) == 1:
				await bot.bot.send_chat_action(chat_id, "upload_video")
				if "video" in videos[0]["q_text"]:
					download_video(videos[0]["url"],f"{chat_id}{n}.mp4",message.from_user.id)
					await message.reply_video(open(f"{chat_id}{n}.mp4","rb"))
					await m.delete()
					os.remove(f"{chat_id}{n}.mp4")
				else:
					download_video(videos[0]["url"],f"{chat_id}{n}.jpg",message.from_user.id)
					await message.reply_photo(open(f"{chat_id}{n}.jpg","rb"),caption=f"@{username}")
					await m.delete()
					os.remove(f"{chat_id}{n}.jpg")
				return
			
			for video in videos:
				#video = videos[num]
				if len(media) >= 10:
					await bot.bot.send_chat_action(chat_id, "upload_video")
					await message.reply_media_group(media)
					media.clear()
					continue
				video = video["src"]
				if ".mp4" in video:
					download_video(video,f"{chat_id}{n}.mp4",message.from_user.id)
					media.append(types.InputMediaVideo(open(f"{chat_id}{n}.mp4","rb"),caption=f"@{username}"))
					n+=1
				else:
					download_video(video,f"{chat_id}{n}.jpg",message.from_user.id)
					media.append(types.InputMediaPhoto(open(f"{chat_id}{n}.jpg","rb"),caption=f"@{username}"))
					n+=1
				time.sleep(1)
			if len(media) >=1:
				await bot.bot.send_chat_action(chat_id, "upload_video")
				await message.reply_media_group(media)
				media.clear()
			await m.delete()
			for i in glob.glob(f"{chat_id}*.mp4"):
				os.remove(i)
			for i in glob.glob(f"{chat_id}*.jpg"):
				os.remove(i)
		except Exception as error:
			print(error)
			await m.edit_text("حدث خطأ.")
			await bot.bot.send_message(dev,f"""
الرابط: {message.text}

رسالة الخطأ:
{error}
""")

	else:
		response = requests.get(f"https://apimedia.hussienalaraqe8.repl.co/story?url={link}").json()
		try:
			No = response['success']
			if No == False:
				await m.edit_text('تأكد من الرابط.')
			else:
				media = []
				n = 0
				num_media = response["data"]['medias']
				await m.edit_text(f"Done  {n}/{len(num_media)} ♻️")
				videos = response["data"]['medias']
				if len(videos) == 1:
					await bot.bot.send_chat_action(chat_id, "upload_video")
					if "video" in videos[0]["q_text"]:
						download_video(videos[0]["url"],f"{chat_id}{n}.mp4",message.from_user.id)
						await message.reply_video(open(f"{chat_id}{n}.mp4","rb"))
						await m.delete()
						os.remove(f"{chat_id}{n}.mp4")
					else:
						download_video(videos[0]["url"],f"{chat_id}{n}.jpg",message.from_user.id)
						await message.reply_photo(open(f"{chat_id}{n}.jpg","rb"),caption=f"@{username}")
						await m.delete()
						os.remove(f"{chat_id}{n}.jpg")
					return
				
				for video in response["data"]['medias']:
					if len(media) >= 10:
						await bot.bot.send_chat_action(chat_id, "upload_video")
						await message.reply_media_group(media)
						media.clear()
						continue
					video = video["src"]
					if ".mp4" in video:
						download_video(video,f"{chat_id}{n}.mp4",message.from_user.id)
						media.append(types.InputMediaVideo(open(f"{chat_id}{n}.mp4","rb"),caption=f"@{username}"))
						n += 1
					else:
						download_video(video,f"{chat_id}{n}.jpg",message.from_user.id)
						media.append(types.InputMediaPhoto(open(f"{chat_id}{n}.jpg","rb"),caption=f"@{username}"))
						n += 1
					await m.edit_text(f"Done  {n}/{len(num_media)} ♻️")
				if len(media) >=1:
					await message.reply_media_group(media)
					media.clear()
					
				await m.delete()
				for i in glob.glob(f"{chat_id}*.mp4"):
					os.remove(i)
				for i in glob.glob(f"{chat_id}*.jpg"):
					os.remove(i)
		
		except Exception as error:
			print(error)
			await m.edit_text("حدث خطأ.")
			await bot.bot.send_message(dev,f"""
الرابط: {message.text}

رسالة الخطأ:
{error}
""")

@bot.message_handler(filters.Regexp("^(http|https)://pin.it"))
async def pint(message):
	if db.get("forward") == True and message.from_user.id != dev:
		await message.forward(dev)
	print("pinterest")
	link = message.text
	chat_id = message.chat.id
	msg = await message.reply("__جاري التحميل__")
	try:
		url = requests.get(f"https://apimedia.hussienalaraqe8.repl.co/pinterest?url={link}").json()
		
		link = url["link"]
		#print(link)
		photo = url["thmub"]
			
		response= requests.get(photo)
		with open(f"{message.chat.id}.png", "wb") as file:
			file.write(response.content)
		#thumb = f"{message.chat.id}.png" 
		
		if download_video(link,f"video{message.chat.id}.mp4",message.chat.id):
			await bot.bot.send_chat_action(chat_id, "upload_video")
			await message.reply_video(
				open(f"video{message.chat.id}.mp4","rb"),
				caption=f'@{username}',
				thumb=open(f"{message.chat.id}.png","rb")
				)
			os.remove(f"video{message.chat.id}.mp4")
			os.remove(f"{message.chat.id}.png")
			await msg.delete()
	except Exception as error:
		print(error)
		await msg.edit_text("**حدث خطأ**")
		await bot.send_message(dev,f"""
الرابط: {message.text}

رسالة الخطأ:
{error}
""")

mis = {}
@bot.message_handler(filters.Regexp("^(http|https)://(vm.tiktok.com|tiktok.com)"))
async def tiktok(message):
	if db.get("forward") == True and message.from_user.id != dev:
		await message.forward(dev)
	print("tik")
	text = message.text
	msg = await message.reply("**جاري التحميل ...**",parse_mode="Markdown")
	try:
		url = requests.get(f'https://tikwm.com/api/?url={text}').json()
		music = url['data']['music']
		region = url['data']['region']
		tit = url['data']['title']
		if "images" in str(url["data"].keys()):
			vid = url["data"]["images"]
		else:
			vid = url['data']['play']
		ava = url['data']['author']['avatar']
		rand = str("".join(random.choice("qwertyuiopasdfghjklzxcvbnm")for i in range(5)))+"get_tiktok"
		mis[rand] = music
		name = url['data']['music_info']['author']
		time = url['data']['duration']
		sh = url['data']['share_count']
		com = url['data']['comment_count']
		wat = url['data']['play_count']
		await msg.delete()
		await message.reply_photo(ava,caption=f'- اسم الحساب : **{name}**\n - دوله الحساب : **{region}**\n\n- عدد مرات المشاهدة : **{wat}**\n- عدد التعليقات : **{com}**\n- عدد مرات المشاركة : **{sh}**\n- طول الفيديو : **{time}**',parse_mode="Markdown")
		if "list" in str(type(vid)):
			photos = []
			btns = km().add(btn('تحميل الصوت',callback_data=rand))
			for photo in vid:
				photos.append(types.InputMediaPhoto(photo,caption=f"{tit}"))
				if len(photos) ==10:
					await message.reply_media_group(
						message.chat.id,
						media=photos
					)
					photos.clear()
					continue
			await message.reply_media_group(message.chat.id,media=photos)
			await message.reply("هل تريد تحميل الصوت؟",reply_markup=btns)
			return
		btns = km().add(btn('تحميل الصوت',callback_data=rand))
		await message.reply_video(
			vid,
			caption=f"{tit}",
			reply_markup=btns,
		)
	except Exception as error:
		await message.reply('حصل خطأ. );')
		await bot.bot.send_message(dev,f"""Error:

الرابط: {text}

رسالة الخطأ: {str(error)}
""")

@bot.message_handler(filters.Regexp("^(http|https)://(watch?v=|youtu.be/|shorts/youtu.be/|www.youtube.com/|youtube.com/)"))
async def ytube(message):
	if db.get("forward") == True and message.from_user.id != dev:
		await message.forward(dev)
	print("youtube")
	m = await message.reply("جاري التحميل...")
	try:
		vid_id = message.text.split("watch?v=")[1]
	except:
		try:
			vid_id = message.text.split("youtu.be/")[1].split("?")[0]
		except:
			try:
				vid_id = message.text.split("shorts/")[1].split("?")[0]
			except:
				vid_id = message.text.split("youtu.be/")[1]
	try:
		print(vid_id)
		yt = YoutubeSearch(f'https://youtu.be/{vid_id}', max_results=1).to_dict()
		title = yt[0]['title']
		print(title)
		url = f'https://youtu.be/{vid_id}'
		reply_markup = km().add(btn("صوت 💿", callback_data=f'{id}AUDIO{vid_id}'),btn("فيديو 🎥", callback_data=f'{id}VIDEO{vid_id}'))
		await m.delete()
		await message.reply_photo(
			str(yt[0]["thumbnails"][0].split("?")[0]),
			caption=f"**⤶ العنوان - [{title}]({url})**",
			reply_markup=reply_markup,
			parse_mode="Markdown"
		)
	except Exception as error:
		await m.edit_text('error );')
		await bot.bot.send_message(dev,f"""Error:

الرابط: {vid_id}

رسالة الخطأ: {str(error)}
""")

@bot.message_handler(filters.Regexp("(twitter.com|x.com)"))
async def twist(message):
	if db.get("forward") == True and message.from_user.id != dev:
		await message.forward(dev)
	chat_id = message.chat.id
	m = await message.reply("**جاري التحميل...**")
	await message.delete()
	try:
		url = requests.get(f"https://apimedia.hussienalaraqe8.repl.co/twitter?url={message.text}").json()
		url = url["link"]
		number = str(random.randint(1,1000))
		download_video(url,f"{number}.mp4",message.chat.id)
		await bot.bot.send_chat_action(chat_id, "upload_video")
		vid = await m.reply_video(open(f"{number}.mp4","rb"),caption="سيتم حذف الفيديو بعد 10 ثواني لمنع الاستخدام فيما هو غير اخلاقي.")
		await m.delete()
		os.remove(f"{number}.mp4")
		await asyncio.sleep(10)
		await vid.delete()
	except Exception as error:
		await m.edit_text("حدث خطأ.")
		await bot.bot.send_message(dev,f"""
الرابط: {message.text}

الخطأ: {error}
""")

@bot.message_handler(filters.Regexp("^(http|https)://(threads.net|www.threads.net)"))
async def threadsss(message):
	if db.get("forward") == True and message.from_user.id != dev:
		await message.forward(dev)
	chat_id = message.chat.id
	m = await message.reply("**جاري التحميل...**")
	try:
		response = requests.get(f"https://apimedia.hussienalaraqe8.repl.co/threads?url={message.text}").json()
		url = response["link"]
		title = response["title"]
		number = str(random.randint(1,1000))
		download_video(url,f"{number}.mp4",message.chat.id)
		await bot.bot.send_chat_action(chat_id, "upload_video")
		await message.reply_video(open(f"{number}.mp4","rb"),caption=f"@{username}")
		os.remove(f"{number}.mp4")
	except Exception as error:
		await m.edit_text("حدث خطأ.")
		await bot.bot.send_message(dev,f"""
الرابط: {message.text}

الخطأ: {error}
""")

@bot.message_handler(filters.Regexp("^(https|http)://(snapchat.com|t.snapchat.com)"))
async def snapchatt(message):
	if db.get("forward") == True and message.from_user.id != dev:
		await message.forward(dev)
	chat_id = message.chat.id
	m = await message.reply("**جاري التحميل...**")
	try:
		response = requests.get(f"https://apimedia.hussienalaraqe8.repl.co/snapchat?url={message.text}").json()
		url = response["link"]
		title = response["title"]
		number = str(random.randint(1,1000))
		download_video(url,f"{number}.mp4",message.chat.id)
		await bot.bot.send_chat_action(chat_id, "upload_video")
		await message.reply_video(open(f"{number}.mp4","rb"),caption=f"@{username}")
		m.delete()
		os.remove(f"{number}.mp4")
	except Exception as error:
		await m.edit_text("حدث خطأ.")
		await bot.bot.send_message(dev,f"""
الرابط: {message.text}

الخطأ: {error}
""")

@bot.message_handler(filters.Regexp("^(https|http)://(spotify|open.spotify)"))
async def spotyyify(message):
	if db.get("forward") == True and message.from_user.id != dev:
		await message.forward(dev)
	msg = await message.reply("__جاري التحميل__",parse_mode="markdown")
	song = requests.get(f"https://apimedia.hussienalaraqe8.repl.co/spotify?url={message.text}").json()
	title = song["title"]
	link = song["link"]
	ydl_ops = {"format": "bestaudio[ext=m4a]"}
	try:
		with yt_dlp.YoutubeDL(ydl_ops) as ydl:
			info_dict = ydl.extract_info(link, download=False)
			if int(info_dict['duration']) > 700:
				return await message.edit_text(text="**⚠️ حد التحميل ساعة ونص فقط**",parse_mode="Html")
			file_name = ydl.prepare_filename(info_dict)
			ydl.process_info(info_dict)
			await message.reply_audio(
				audio=open(file_name,"rb"),
				caption=f"{title}",
				performer=info_dict['channel'],
				title=info_dict['title'],
				)
			await msg.delete()
			os.remove(file_name)
	except Exception as error:
		print(error)
		return await message.edit_text(text="**⚠️ صار خطأ**",parse_mode="Html")

@bot.message_handler(filters.Regexp("^(@|[a-zA-Z]|[0-9])"))
async def instagram_s(message):
	if db.get("forward") == True and message.from_user.id != dev:
		await message.forward(dev)
	print("instagram_story")
	chat_id = message.chat.id
	if not "@" in message.text:
		user = message.text
	else:
		user = message.text.split("@")[1]
	#print()
	link = "https://instagram.com/"+user
	
	m = await message.reply("جاري التحميل...")
	response = requests.get(f"https://apimedia.hussienalaraqe8.repl.co/story?url={link}").json()
	print(response)
	try:
		No = response['success']
		if No == False:
			await m.edit_text('تأكد من الرابط.')
		else:
			media = []
			num_media = response["data"]['medias']
			n = 0
			await m.edit_text(f"Done  {n}/{len(num_media)} ♻️")
			videos = response["data"]['medias']
			if len(videos) == 1:
				await bot.bot.send_chat_action(chat_id, "upload_video")
				if "video" in videos[0]["q_text"]:
					download_video(videos[0]["url"],f"{chat_id}{n}.mp4",message.from_user.id)
					await message.reply_video(open(f"{chat_id}{n}.mp4","rb"))
					await m.delete()
					os.remove(f"{chat_id}{n}.mp4")
				else:
					download_video(videos[0]["url"],f"{chat_id}{n}.jpg",message.from_user.id)
					await message.reply_photo(open(f"{chat_id}{n}.jpg","rb"),caption=f"@{username}")
					await m.delete()
					os.remove(f"{chat_id}{n}.jpg")
				return
			
			try:
				for video in response["data"]['medias']:
					if len(media) == 10:
						await bot.bot.send_chat_action(chat_id, "upload_video")
						await message.reply_media_group(media)
						media.clear()
						continue
					video = video["src"]
					if ".mp4" in video:
						download_video(video,f"{chat_id}{n}.mp4",message.from_user.id)
						media.append(types.InputMediaVideo(open(f"{chat_id}{n}.mp4","rb"),caption=f"@{username}"))
						n += 1
					else:
						download_video(video,f"{chat_id}{n}.jpg",message.from_user.id)
						media.append(types.InputMediaPhoto(open(f"{chat_id}{n}.jpg","rb"),caption=f"@{username}"))
						n += 1
					await m.edit_text(f"Done  {n}/{len(num_media)} ♻️")
				if len(media) >=1:
					await message.reply_media_group(media)
					media.clear()
					
				await m.delete()
				for i in glob.glob(f"{chat_id}*.mp4"):
					os.remove(i)
				for i in glob.glob(f"{chat_id}*.jpg"):
					os.remove(i)
			except Exception as error:
				if "The media you tried to send is invalid" in str(error):
					for media in response["data"]['medias']:
						media = media["src"]
						if ".mp4" in media:
							await bot.bot.send_video(message.chat.id,media)
						else:
							await bot.bot.send_photo(message.chat.id,media)
					await message.reply("عذرًا Sir. تم ارسالها بشكل متقطع لان الحساب يحتوي على صورة متحركة في الاستوري خاصته، وانت تدري بعمو تلكرام مايخليك تدز صورة متحركة بمجموعة صور كـAlbum واحد")
	except Exception as error:
		print(error)
		await m.edit_text("حدث خطأ.")
		await bot.bot.send_message(dev,f"""
الرابط: {message.text}

رسالة الخطأ:
{error}
""")



@bot.message_handler(filters.Regexp("^(سلام|عليكم)"))
async def echo(message):
	await message.reply(message.text)

@bot.callback_query_handler(filters.Regexp("AUDIO"))
async def get_audio_from_youtube(query):
	#id = query.data.split("AUDIO")[0]
	vid_id = query.data.split("AUDIO")[1]
	
	downloading = km().add(btn("يتم التحميل",url=f"https://t.me/{username}"))
	uploading = km().add(btn("يتم الرفع لتليجرام",url=f"https://t.me/{username}"))
	error = km().add(btn("Error ⚠️",url=f"https://t.me/{username}"))
	
	print(query.message)
	await query.message.edit_caption("**جاري التحميل ..**", reply_markup=downloading,parse_mode="Markdown")
	
	url = f'https://youtu.be/{vid_id}'
	ydl_ops = {"format": "bestaudio[ext=m4a]"}
	print(vid_id)
				
	with yt_dlp.YoutubeDL(ydl_ops) as ydl:
		info_dict = ydl.extract_info(url, download=False)
		if int(info_dict['duration']) > 5006:
			return await query.message.edit_caption("**⚠️ حد التحميل ساعة ونص فقط**",reply_markup=error)
			
		try:
			audio_file = ydl.prepare_filename(info_dict)
			ydl.process_info(info_dict)
			await query.message.edit_caption("**جاري الإرسال ..**", reply_markup=uploading,parse_mode="Markdown")
			response= requests.get(info_dict['thumbnail'])
			with open(f"{vid_id}.png", "wb") as file:
				file.write(response.content)
			thumb = f"{vid_id}.png"
			msg = await query.message.reply_audio(
				open(audio_file,"rb"),
				title=info_dict['title'],
				duration=int(info_dict['duration']),
				performer=info_dict['channel'],
				#caption=f'• البحث من -› {user.mention}',
				thumb=thumb,
				reply_markup=km().add(btn("My Src",url=f"https://t.me/{username}"))
			)
				
			await query.message.edit_caption("**تم التحميل.**",parse_mode="Markdown")
				
			os.remove(audio_file)
			os.remove(thumb)
			return
		except Exception as err:
			print(str(err))
			await query.message.edit_caption("**⚠️ صار خطأ.**",reply_markup=error,parse_mode="Markdown")
			await bot.bot.send_message(dev,f"""Error:

الرابط: {url}

رسالة الخطأ: {str(err)}
""")
			return

@bot.callback_query_handler(filters.Regexp("VIDEO"))
async def get_video_from_youtube(query):
	#id = query.data.split("VIDEO")[0]
	vid_id = query.data.split("VIDEO")[1]
	
	downloading = km().add(btn("يتم التحميل",url=f"https://t.me/{username}"))
	uploading = km().add(btn("يتم الرفع لتليجرام",url=f"https://t.me/{username}"))
	error = km().add(btn("Error ⚠️",url=f"https://t.me/{username}"))
	
	url = f'https://youtu.be/{vid_id}'
	await query.message.edit_caption("**جاري التحميل ..**", reply_markup=downloading,parse_mode="Markdown")
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
		#print(ytdl_data["title"])
		if int(ytdl_data['duration']) > 5006:
			return await query.message.edit_caption("**⚠️ حد التحميل ساعة ونص فقط**",reply_markup=error,parse_mode="Markdown")
		
		try:
			file_name = ytdl.prepare_filename(ytdl_data)
			await query.message.edit_caption("**جاري الإرسال ..**", reply_markup=uploading,parse_mode="Markdown")
			response= requests.get(ytdl_data['thumbnail'])
			with open(f"{vid_id}.png", "wb") as file:
				file.write(response.content)
			thumb = f"{vid_id}.png"
			#user = bot.get_users(int(id))	
			msg = await query.message.reply_video(
				open(file_name,"rb"),
				duration=int(ytdl_data['duration']),
				#caption=f'• البحث من  -› {user.mention}',
				thumb=thumb,
				reply_markup=km().add(btn("My Src",url=f"https://t.me/{username}"))
			)
			os.remove(file_name)
			os.remove(thumb)
			await query.message.edit_caption("**تم التحميل.**",parse_mode="Markdown")
		except Exception as err:
			print(str(err))
			await query.message.edit_caption("**⚠️ صار خطأ.**",reply_markup=error,parse_mode="Markdown")
			await bot.bot.send_message(dev,f"""Error:

الرابط: {url}

رسالة الخطأ: {str(err)}
""")
			return

@bot.callback_query_handler(filters.Regexp("get_tiktok"))
async def get_audio_tiktok(query):
	if mis[query.data]:
		audio = mis[query.data].split("get_tiktok")[0]
		print(audio)
		#query.message.delete()
		await query.message.reply_audio(audio)
		del mis[query.data]
		return

@bot.callback_query_handler()
async def tre(call):
	if db.get("dkhol") in [None,False]:
		dkhol = "❌"
	else:
		dkhol = "✅"
	
	if db.get("forward") in [None,False]:
		forward = "❌"
	else:
		forward = "✅"
		
	btn1 = btn(text="الاحصائيات",callback_data="stats")
	btn2 = btn(text="اذاعة",callback_data="adaa")

	btn3 = btn(text=f"اشعار الدخول {dkhol}",callback_data="dkhol")
	btn4 = btn(text=f"توجيه الرسائل {forward}",callback_data="forward")
		
	btn5 = btn(text="قناة الاشتراك الاجباري.",callback_data="channel")
	btn6 = btn(text="رسالة start.",callback_data="startMSG")
		
	btns = km().add(btn1,btn2).add(btn3,btn4).add(btn5,btn6)
	
	back = km().add(btn(text = "رجوع",callback_data="back"))
	
	replace_channel = km().add(btn(text="تغيير/وضع قناة اشتراك اجباري",callback_data="replace_channel"),btn(text="رجوع",callback_data="back"))
	
	replace_startMSG = km().add(btn(text="تغيير رسالة ستارت",callback_data="replace_startMSG"),btn(text = "رجوع",callback_data="back"))
	
	if call.data == "stats":
		users = 0
		for i in db.get("members"):
			users += 1
		await call.message.edit_text(f"""
قائمة الاعضاء.

عدد الاعضاء: {users}""",
			reply_markup=back
		)
	elif call.data == "adaa":
		await call.message.edit_text("تمام، دز اارسالة وراح ادزها للكل تدلل سيدي.",reply_markup=back)
		what["adaa"] = "True"
	
	elif call.data == "dkhol":
		if db.get("dkhol") == False or db.get("dkhol") == None:
			db.set("dkhol", True)
			await call.answer("تم التفعيل.")
		elif db.get("dkhol") == True:
			db.set("dkhol", False)
			await call.answer("تم التعطيل.")
			
	elif call.data == "forward":
		if db.get("forward") == False or db.get("forward") == None:
			db.set("forward", True)
			await call.answer("تم التفعيل.")
			
		elif db.get("forward") == True:
			db.set("forward", False)
			await call.answer("تم التعطيل.")
	
	elif call.data == "channel":
		channel = db.get("channel")
		if channel == None:
			channel = "لا يوجد."
		id = channel["id"]
		title = channel["title"]
		username = channel["username"]
		link = channel["link"]
		await call.message.edit_text(f"""قناة الاشتراك الاجباري:
title: [{title}]({link})
id: {id}
username: @{username}
""",reply_markup=replace_channel,parse_mode="Markdown")
	
	elif call.data == "replace_channel":
		what["replace_channel"] = "True"
		await call.message.edit_text("الان عليك رفع البوت أدمن بقناتك، وإرسال ID القناة\nمثال -1003445791104",reply_markup=back)
	
	elif call.data == "startMSG":
		startMSG = db.get("startMSG")
		await call.message.edit_text(startMSG,reply_markup=replace_startMSG)
	
	elif call.data == "replace_startMSG":
		what["replace_startMSG"] = "True"
		await call.message.edit_text("الان عليك ارسال الرسالة الجديدة يمكنك ارفاق `{mention}` ليكون منشن للعضو الذي دخل.",reply_markup=back)
	
	elif call.data == "back":
		await call.message.edit_text("مرحبا بك سيدي في بوتك اختر ادناه...",reply_markup=btns)
		what["adaa"] = "False"
		what["replace_channel"] = "False"
		what["replace_startMSG"] = "False"
	
	if db.get("dkhol") in [None,False]:
		dkhol = "❌"
	else:
		dkhol = "✅"
	
	if db.get("forward") in [None,False]:
		forward = "❌"
	else:
		forward = "✅"
		
	btn1 = btn(text="الاحصائيات",callback_data="stats")
	btn2 = btn(text="اذاعة",callback_data="adaa")

	btn3 = btn(text=f"اشعار الدخول {dkhol}",callback_data="dkhol")
	btn4 = btn(text=f"توجيه الرسائل {forward}",callback_data="forward")
		
	btn5 = btn(text="قناة الاشتراك الاجباري.",callback_data="channel")
	btn6 = btn(text="رسالة start.",callback_data="startMSG")
		
	btns = km().add(btn1,btn2).add(btn3,btn4).add(btn5,btn6)
	if call.data in ["back","dkhol","forward"]:
		await call.message.edit_text("مرحبا بك سيدي في بوتك اختر ادناه..",reply_markup=btns)
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(bot, skip_updates=True)
