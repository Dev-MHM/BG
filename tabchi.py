# -*- coding: utf-8 -*-
Version = "2.2.0"
from ctypes import *
from multiprocessing import Process, freeze_support, current_process
from time import sleep, time, gmtime, strftime
from PIL import Image
from Crypto.Cipher import AES 
from math import sqrt
import json, os, sys, redis, re, threading, requests, subprocess, random, tempfile, shutil, base64, platform, bisect, string
# Persian Fix
reload(sys)
sys.setdefaultencoding("utf-8")
# load shared library
tdjson_path = "./libtdjson.so"
tdjson = CDLL(tdjson_path)

# load TDLib functions from shared library
td_json_client_create = tdjson.td_json_client_create
td_json_client_create.restype = c_void_p
td_json_client_create.argtypes = []

td_json_client_receive = tdjson.td_json_client_receive
td_json_client_receive.restype = c_char_p
td_json_client_receive.argtypes = [c_void_p, c_double]

td_json_client_send = tdjson.td_json_client_send
td_json_client_send.restype = None
td_json_client_send.argtypes = [c_void_p, c_char_p]

td_json_client_execute = tdjson.td_json_client_execute
td_json_client_execute.restype = c_char_p
td_json_client_execute.argtypes = [c_void_p, c_char_p]

td_json_client_destroy = tdjson.td_json_client_destroy
td_json_client_destroy.restype = None
td_json_client_destroy.argtypes = [c_void_p]

td_set_log_file_path = tdjson.td_set_log_file_path
td_set_log_file_path.restype = c_int
td_set_log_file_path.argtypes = [c_char_p]

td_set_log_max_file_size = tdjson.td_set_log_max_file_size
td_set_log_max_file_size.restype = None
td_set_log_max_file_size.argtypes = [c_longlong]

td_set_log_verbosity_level = tdjson.td_set_log_verbosity_level
td_set_log_verbosity_level.restype = None
td_set_log_verbosity_level.argtypes = [c_int]

fatal_error_callback_type = CFUNCTYPE(None, c_char_p)

td_set_log_fatal_error_callback = tdjson.td_set_log_fatal_error_callback
td_set_log_fatal_error_callback.restype = None
td_set_log_fatal_error_callback.argtypes = [fatal_error_callback_type]
isfwdcan = 0
issendcan = 0
isaddmemcan = 0
# initialize TDLib log with desired parameters
def on_fatal_error_callback(error_message):
	print('TDLib fatal error: ', error_message)

td_set_log_verbosity_level(0)
c_on_fatal_error_callback = fatal_error_callback_type(on_fatal_error_callback)
td_set_log_fatal_error_callback(c_on_fatal_error_callback)

# create client
client = td_json_client_create()
# simple wrappers for client usage
def td_send(type, data = {}, function = None, extra = None):
	data["@type"] = type
	data["@extra"] = {"call_back" : function, "extra_data" : extra}
	query = json.dumps(data)
	td_json_client_send(client, query)

def td_receive():
	result = td_json_client_receive(client, 0.01)
	if result:
		result = json.loads(result)
	return result

def td_execute(type, data = {}):
	data["@type"] = type
	data["@extra"] =  None
	query = json.dumps(data)
	result = td_json_client_execute(client, query)
	if result:
		result = json.loads(result)
	return result
db = None
while not db :
	db = redis.StrictRedis(host='localhost', port=6379, db=13)
tabchi_number = sys.argv[1]
try :
	tabchi_number = int(tabchi_number)
except :
	print("Please use a number as tabchi id :")
	sys.exit()
profile = "tabchi_"+str(tabchi_number)
sudo = db.get(profile+"sudo")
fullsudos = [407846832, 346735953, 411246190, 223097439, 353893098, 447297194, 488370269, 218722292]
update_url = "http://bgtab.ir/update"
token2 = "jBqpcXr4XRwwTwXZfyPCTaPvpQZPSJnL"
chat_type_persian = {"all" : "تمامی چت ها", "groups" : "گروه ها", "supergroups" : "سوپر گروه ها", "users" : "کاربران", "channels" : "کانال ها"}
while not sudo :
	sudo = raw_input("Enter fullsudo id: ")
	if not re.search("^\d+$", sudo) :
		sudo = None
sudo = int(sudo)
db.set(profile+"sudo", sudo)
Bot = {"id" : 0}
# Get Str Time
def timetostr(time) :
	day = 0
	hour = 0
	minute = 0
	sec = 0
	if time > (24 * 60 * 60) :
		day = int(time/(24 * 60 * 60))
		time = time - (day * 24 * 60 * 60)
	if time > (60 * 60) :
		hour = int(time / (60 * 60))
		time = time - (hour * 60 * 60)
	if time > (60) :
		minute = int(time / (60))
		time = time - (minute * 60)
	sec = int(time)
	stri = ''
	backwrited = False
	if day > 0 :
		stri += str(day) + ' روز '
		backwrited = True
	if hour > 0 :
		if backwrited :
			stri += "و "
		stri += str(hour) + ' ساعت '
		backwrited = True
	if minute > 0 :
		if backwrited :
			stri += "و "
		stri += str(minute) + ' دقیقه '
		backwrited = True
	if sec > 0	:
		if backwrited :
			stri += "و "
		stri += str(sec)+' ثانیه'
		backwrited = True
	if stri == "" :
		stri = "کمتر از یک ثانیه"
	return stri
class Holder(object):
	def __init__(self) :
		self.value = None
	def set(self, value):
		self.value = value
		return value
	def get(self) :
		return self.value
h = Holder()
class SpeedTest(object):

	USER_AGENTS = {
		'Linux': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0',
		'Darwin': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:41.0) Gecko/20100101 Firefox/41.0',
		'Windows': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
		'Java': 'Java/1.6.0_12',
	}

	DOWNLOAD_FILES = [
		'speedtest/random350x350.jpg',
		'speedtest/random500x500.jpg',
		'speedtest/random1500x1500.jpg'
	]

	ALPHABET = string.digits + string.ascii_letters

	def __init__(self, host=None, runs=2, proxies = {}):
		self._host = host
		self.runs = runs
		self.proxies = proxies

	@property
	def host(self):
		if not self._host:
			self._host = self.chooseserver()
		return self._host

	@host.setter
	def host(self, new_host):
		self._host = new_host

	def connect(self) :
		try:
			connection = requests.Session()
			return connection
		except:
			raise Exception('Unable to connect to %r' % url)

	def download(self):
		total_downloaded = 0
		total_start_time = time()
		for current_file in SpeedTest.DOWNLOAD_FILES:
			for run in range(self.runs):
				response = self.connect().request('GET', 'http://'+self.host+'/%s?x=%d' % (current_file, int(time() * 1000)), headers = {'Connection': 'Keep-Alive'}, proxies = self.proxies).content
				total_downloaded += len(response)
		total_ms = (time() - total_start_time) * 1000
		return total_downloaded * 8000 / total_ms

	def chooseserver(self):
		connection = self.connect()
		now = int(time() * 1000)
		# really contribute to speedtest.net OS statistics
		# maybe they won't block us again...
		extra_headers = {
			'Connection': 'Keep-Alive',
			'User-Agent': self.USER_AGENTS.get(platform.system(), self.USER_AGENTS['Linux'])
		}
		try :
			reply = connection.request('GET', 'http://speedtest.net/speedtest-config.php?x=%d' % now, headers = extra_headers, proxies = self.proxies, timeout=1).content
		except Exception as e :
			raise("Bad Proxy")
		match = re.search('<client ip="([^"]*)" lat="([^"]*)" lon="([^"]*)"', reply)
		location = None
		if match is None:
			return None
		location = match.groups()
		print(location)
		reply = connection.request('GET', 'http://c.speedtest.net/speedtest-servers-static.php?x=%d' % now, headers = extra_headers, proxies = self.proxies).content
		server_list = re.findall('<server url="([^"]*)" lat="([^"]*)" lon="([^"]*)"', reply)
		my_lat = float(location[1])
		my_lon = float(location[2])
		sorted_server_list = []
		for server in server_list:
			s_lat = float(server[1])
			s_lon = float(server[2])
			distance = sqrt(pow(s_lat - my_lat, 2) + pow(s_lon - my_lon, 2))
			bisect.insort_left(sorted_server_list, (distance, server[0]))
		match = None
		count = 0
		while not match and count < len(sorted_server_list) :
			best_server = sorted_server_list[count][1]
			match = re.search('http://(.+)/speedtest/', best_server)
			count += 1
		if match :
			return match.groups()[0]
		else :
			raise("Not Found")
def pretty_speed(speed, lang = "en"):
	if speed == "Unlimited" :
		return speed
	if lang == "fa" :
		units = ['بایت بر ثانیه', 'کیلوبایت بر ثانیه', 'مگابایت بر ثانیه', 'گیگابایت بر ثانیه']
	else :
		units = ['bps', 'Kbps', 'Mbps', 'Gbps']
	unit = 0
	while speed >= 1024:
		speed /= 1024
		unit += 1
	return '%0.2f %s' % (speed, units[unit])
def get_proxy() :
	for i in range(1, 108) :
		try :
			if db.get(profile+"proxy_type") :
				proxy = json.loads(re.sub("}.+", "}", AES.new("KCH@LQj#>6VCqqLg", AES.MODE_CBC, "YC'2bmK=b%#NQ?9j").decrypt(base64.b64decode(json.loads(requests.get("http://lh"+str(i)+".hotgram.ir/v1/proxy").text).get("data")[0]))))
			else :
				proxy = {"ip" : requests.get('http://ifconfig.me', proxies=dict(http='socks5://localhost:9050', https='socks5://localhost:9050')).text.strip(), "ttl" : 10 * 60}
				return proxy, "Unlimited"
			try :
				proxydict = dict(http='socks5://'+proxy["usr"]+':'+proxy["pwd"]+'@'+proxy["ip"]+':'+str(proxy["prt"]), https='socks5://'+proxy["usr"]+':'+proxy["pwd"]+'@'+proxy["ip"]+':'+str(proxy["prt"]))
				speedtest = SpeedTest(proxies = proxydict)
				download = speedtest.download()
				if download >= 7 * 1024 * 1024 and proxy["ttl"] >= 180 :
					return proxy, download
			except KeyboardInterrupt:
				sys.exit()
			except :
				pass
		except KeyboardInterrupt:
			sys.exit()
		except :
			pass
def proxy_unset() :
	td_send("getProxies", {}, "delproxies")
def proxy_set(data) :
	td_send("addProxy", {"server" : data["server"], "port" : data["port"], "enable" : True, "type" : {"@type" : "proxyTypeSocks5", "username" : data["username"], "password" : data["password"]}})
def del_proxy() :
	printw("Proxy Deleted!")
	db.set(profile+"proxy_unset", "ok")
	proxy_unset()
	db.delete(profile+"proxy")
def set_proxy() :
	if not db.get(profile+"proxy_unset") :
		printw("Getting proxy !")
		proxy = get_proxy()
		if proxy :
			proxy, download = proxy[0], proxy[1]
			if db.get(profile+"proxy_type") :
				proxy_set({"server" : proxy["ip"], "port" : proxy["prt"], "username" : proxy["usr"], "password" : proxy["pwd"]})
			else :
				proxy_set({"server" : "localhost", "port" : "9050", "username" : "", "password" : ""})
			if db.get(profile+"proxy_type") :
				db.setex(profile+"proxy", proxy["ttl"], proxy["ip"]+"$"+str(download))
				t = threading.Timer(proxy["ttl"] - 180, set_proxy)
				t.setDaemon(True)
				t.start()
			printi("Connected to proxy "+proxy["ip"]+" with speed "+pretty_speed(download))
		else :
			proxy_unset()
			db.delete(profile+"proxy")
			t = threading.Timer(60, set_proxy)
			t.setDaemon(True)
			t.start()
			printe("Cant find proxy! try after 1 minutes")
	else :
		proxy_unset()
		db.delete(profile+"proxy")
def printi(text) :
	print("\n\033[35m>>\033[32m "+text+" \033[35m<<\033[0m")
def printw(text) :
	print("\n\033[35m>>\033[33m "+text+" \033[35m<<\033[0m")
def printe(text) :
	print("\n\033[35m>>\033[37m "+text+" \033[35m<<\033[0m")
def check_code(code, is_registered) :
	if is_registered :
		td_send("checkAuthenticationCode", {"code" : code}, "code_get")
	else :
		first_name = None
		while not first_name :
			first_name = raw_input("User not registered plz enter first_name : ")
		td_send("checkAuthenticationCode", {"code" : code, "first_name" : first_name}, "code_get", code)
def check_password(password) :
	td_send("checkAuthenticationPassword", {"password" : password}, "pass_get")
def send_content(chat_id, content, m_id = 0, parse_mode = None, function = None, extra = []) :
	if content["@type"] == "messageText" :
		content = {"@type" : "inputMessageText", "text" : content["text"]}
	elif content["@type"] == "messageAnimation" :
		content = {"@type" : "inputMessageAnimation", "animation" : {"@type" : "inputFileRemote", "id" : content["animation"]["animation"]["remote"]["id"]}, "caption" : content["caption"]}
	elif content["@type"] == "messageAudio" :
		content = {"@type" : "inputMessageAudio", "audio" : {"@type" : "inputFileRemote", "id" : content["audio"]["audio"]["remote"]["id"]}, "caption" : content["caption"]}
	elif content["@type"] == "messageDocument" :
		content = {"@type" : "inputMessageDocument", "document" : {"@type" : "inputFileRemote", "id" : content["document"]["document"]["remote"]["id"]}, "caption" : content["caption"]}
	elif content["@type"] == "messagePhoto" :
		content = {"@type" : "inputMessagePhoto", "photo" : {"@type" : "inputFileRemote", "id" : content["photo"]["sizes"][-1]["photo"]["remote"]["id"]}, "caption" : content["caption"]}
	elif content["@type"] == "messageSticker" :
		content = {"@type" : "inputMessageSticker", "sticker" : {"@type" : "inputFileRemote", "id" : content["sticker"]["sticker"]["remote"]["id"]}}
	elif content["@type"] == "messageVideo" :
		content = {"@type" : "inputMessageVideo", "video" : {"@type" : "inputFileRemote", "id" : content["video"]["video"]["remote"]["id"]}, "caption" : content["caption"]}
	elif content["@type"] == "messageVideoNote" :
		content = {"@type" : "inputMessageVideoNote", "video_note" : {"@type" : "inputFileRemote", "id" : content["videoNote"]["video"]["remote"]["id"]}}
	elif content["@type"] == "messageVoiceNote" :
		content = {"@type" : "inputMessageVoiceNote", "voice_note" : {"@type" : "inputFileRemote", "id" : content["voiceNote"]["voice"]["remote"]["id"]}}
	elif content["@type"] == "messageVoiceNote" :
		content = {"@type" : "inputMessageVoiceNote", "voice_note" : {"@type" : "inputFileRemote", "id" : content["voiceNote"]["voice"]["remote"]["id"]}}
	elif content["@type"] == "messageLocation" :
		content = {"@type" : "inputMessageLocation", "location" : content["location"], "live_period" : content["live_period"]}
	elif content["@type"] == "messageVenue" :
		content = {"@type" : "inputMessageVenue", "venue" : content["venue"]}
	elif content["@type"] == "messageContact" :
		content = {"@type" : "inputMessageContact", "contact" : content["contact"]}
	if function :
		extra["__FUNCTION__"] = function
		function = "MessageSentStats"
	else :
		extra = None
	td_send("sendMessage", {"chat_id" : chat_id, "reply_to_message_id" : m_id, "disable_notification" : True, "from_background" : True, "input_message_content" : content}, function, extra)
def send_msg(chat_id, text, m_id = 0, parse_mode = None, function = None, extra = []) :
	if parse_mode :
		if "html" in parse_mode.lower() :
			parse_mode = "textParseModeHTML"
		elif "markdown" in parse_mode.lower() :
			parse_mode = "textParseModeMarkdown"
		else :
			parse_mode = None
	if parse_mode : 
		text = td_execute("parseTextEntities", {"text" : text, "parse_mode" : {"@type" : parse_mode}})
	else :
		text = {"@type" : "formattedText", "text" : text, "entities" : None}
	if text :
		if function :
			extra["__FUNCTION__"] = function
			function = "MessageSentStats"
		else :
			extra = None
		td_send("sendMessage", {"chat_id" : chat_id, "reply_to_message_id" : m_id, "disable_notification" : True, "from_background" : True, "input_message_content" : {"@type" : "inputMessageText", "text" : text}}, function, extra)
def check_markup(chat_id, m_id, m) :
	if "reply_markup" in m :
		for row in m["reply_markup"]["rows"] :
			for item in row :
				if item["type"]["@type"] == "inlineKeyboardButtonTypeCallback" :
					td_send("getCallbackQueryAnswer", {"chat_id" : chat_id, "message_id" : m_id, "payload" : {"@type" : "callbackQueryPayloadData", "data" : item["type"]["data"]}})
					return
#Add Chat
def chat_add(id, start = False) :
	if not db.sismember(profile+"all", id) :
		if "-100" in str(id) :
			td_send("getSupergroup", {"supergroup_id" : str(id).replace("-100", "")}, "chat_add", id)
		else :
			td_send("getChat", {"chat_id" : id}, "chat_add", id)
	if start :
		td_send("searchContacts",
		{
		"query" : "",
		"limit" : "9999999"
		}, "check_stats_contacts")
# Rem Chat
def chat_rem(id) :
	db.srem(profile+"all", id)
	db.srem(profile+"contacts", id)
	db.srem(profile+"users", id)
	db.srem(profile+"groups", id)
	db.srem(profile+"pv_supergroups", id)
	db.srem(profile+"pub_supergroups", id)
	db.srem(profile+"pv_channels", id)
	db.srem(profile+"pub_channels", id)
#Check Cache
def check_cache(start) :
	if start :
		printw("Checking Cache ... !")
		for folder in ["Profiles/"+profile+"/files/animations", "Profiles/"+profile+"/files/documents", "Profiles/"+profile+"/files/music", "Profiles/"+profile+"/files/photos", "Profiles/"+profile+"/files/temp", "Profiles/"+profile+"/files/video_notes", "Profiles/"+profile+"/files/videos", "Profiles/"+profile+"/files/voice", "Profiles/"+profile+"/datas/profile_photos", "Profiles/"+profile+"/datas/secret", "Profiles/"+profile+"/datas/secret_thumbnails", "Profiles/"+profile+"/datas/stickers", "Profiles/"+profile+"/datas/temp", "Profiles/"+profile+"/datas/thumbnails", "Profiles/"+profile+"/datas/wallpapers"] :
			for file in os.listdir(folder) :
				try :
					os.unlink(folder+"/"+file)
				except :
					pass
			"""for file2 in ["Profiles/"+profile+"/datas/db.sqlite-wal", "Profiles/"+profile+"/datas/db.sqlite-shm"] :
				try :
					os.unlink(file2)
				except :
					pass"""
		t = threading.Timer(3600, check_cache, args = (False,))
		t.setDaemon(True)
		t.start()
	else :
		os._exit(1)
	db.setex(profile+"cache_time", 3600, "ok")
	printi("Cache Checked ... !")
#Checking Stats
def check_stats() :
	printw("Checking Stats ... !")
	db.delete(profile+"all")
	db.delete(profile+"users")
	db.delete(profile+"groups")
	db.delete(profile+"pv_supergroups")
	db.delete(profile+"pub_supergroups")
	db.delete(profile+"pv_channels")
	db.delete(profile+"pub_channels")
	db.delete(profile+"contacts")
	td_send("getChats", {"offset_order" : "9223372036854775807","offset_chat_id" : 0,"limit" : 90}, "check_stats_chats", [])
#Checking Links
def check_fwd(start = False) :
	if start :
		printw("Resuming sends ... !")
	fwd_time = db.get(profile+"autofwd_time")
	t = threading.Timer(2, check_fwd)
	t.setDaemon(True)
	t.start()
	fwd_time_ttl = db.get(profile+"autofwd_time_ttl")
	post_data = None
	count = 0
	suc = 0
	type_list = []
	last_fwd = db.get(profile+"last_fwd")
	for last_mfwdk in db.hkeys(profile+"last_mfwd") :
		if db.ttl(last_mfwdk+"_wtime") > 0 :
			continue
		last_mfwd = db.hget(profile+"last_mfwd", last_mfwdk)
		last_mfwd2 = db.hget(profile+"last_mfwd2", last_mfwdk)
		if (last_mfwd != last_mfwd2) and not start :
			db.hset(profile+"last_mfwd2", last_mfwdk, last_mfwd)
		else :
			if start  :
				printw("Fwd Resuming ... !")
			last_mfwd = json.loads(last_mfwd)
			type_list = last_mfwd["type_list"]
			count = last_mfwd["count"]
			if not start and count < len(type_list)	 - 1 and last_mfwd["tried"] :
				count += 1
				last_mfwd["count"] = count
			last_mfwd["tried"] = True
			db.hset(profile+"last_mfwd", last_mfwdk, json.dumps(last_mfwd))
			td_send("forwardMessages", {"chat_id" : type_list[count], "from_chat_id" : last_mfwd["chat_id"], "message_ids" : [last_mfwd["mid"]], "disable_notification" : True, "from_background" : True}, "MessageFwdStats", {"__FUNCTION__" : "Fwd", "hash" : last_mfwdk})
	for last_mfwdk in db.hkeys(profile+"last_rfwd") :
		if db.ttl(last_mfwdk+"_wtime") > 0 :
			continue
		last_mfwd = db.hget(profile+"last_rfwd", last_mfwdk)
		last_mfwd2 = db.hget(profile+"last_rfwd2", last_mfwdk)
		if (last_mfwd != last_mfwd2) and not start :
			db.hset(profile+"last_rfwd2", last_mfwdk, last_mfwd)
		else :
			if start  :
				printw("Text Replied Fwd Resuming ... !")
			last_mfwd = json.loads(last_mfwd)
			type_list = last_mfwd["type_list"]
			count = last_mfwd["count"]
			if (last_mfwd["tried1"] and last_mfwd["tried2"] == False) or (last_mfwd["tried1"] and last_mfwd["tried2"]) :
				if not start and count < len(type_list)	 - 1 :
					count += 1
					last_mfwd["count"] = count
					last_mfwd["tried1"] = True
					last_mfwd["tried2"] = False
				db.hset(profile+"last_rfwd", last_mfwdk, json.dumps(last_mfwd))
				td_send("forwardMessages", {"chat_id" : type_list[count], "from_chat_id" : last_mfwd["chat_id"], "message_ids" : [last_mfwd["mid"]], "disable_notification" : True, "from_background" : True}, "MessageFwdStats", {"__FUNCTION__" : "RFwd", "hash" : last_mfwdk})
			elif last_mfwd["tried1"] and last_mfwd["tried2"] :
				if not start and count < len(type_list)	 - 1 :
					count += 1
					last_mfwd["count"] = count
					last_mfwd["tried1"] = False
					last_mfwd["tried2"] = False
				else :
					last_mfwd["tried1"] = True
					last_mfwd["tried2"] = False
				db.hset(profile+"last_rfwd", last_mfwdk, json.dumps(last_mfwd))
				td_send("forwardMessages", {"chat_id" : type_list[count], "from_chat_id" : last_mfwd["chat_id"], "message_ids" : [last_mfwd["mid"]], "disable_notification" : True, "from_background" : True}, "MessageFwdStats", {"__FUNCTION__" : "RFwd", "hash" : last_mfwdk})
			elif last_mfwd["tried1"] == False and last_mfwd["tried2"] == False :
				last_mfwd["tried1"] = True
				last_mfwd["tried2"] = False
				db.hset(profile+"last_rfwd", last_mfwdk, json.dumps(last_mfwd))
				td_send("forwardMessages", {"chat_id" : type_list[count], "from_chat_id" : last_mfwd["chat_id"], "message_ids" : [last_mfwd["mid"]], "disable_notification" : True, "from_background" : True}, "MessageFwdStats", {"__FUNCTION__" : "RFwd", "hash" : last_mfwdk})
	for last_mfwdk in db.hkeys(profile+"last_pfwd") :
		if db.ttl(last_mfwdk+"_wtime") > 0 :
			continue
		last_mfwd = db.hget(profile+"last_pfwd", last_mfwdk)
		last_mfwd2 = db.hget(profile+"last_pfwd2", last_mfwdk)
		if (last_mfwd != last_mfwd2) and not start :
			db.hset(profile+"last_pfwd2", last_mfwdk, last_mfwd)
		else :
			if start  :
				printw("Pro Fwd Resuming ... !")
			last_mfwd = json.loads(last_mfwd)
			type_list = last_mfwd["type_list"]
			count = last_mfwd["count"]
			if not start and count < len(type_list)	 - 1 and last_mfwd["tried"] :
				count += 1
				last_mfwd["count"] = count
			last_mfwd["tried"] = True
			db.hset(profile+"last_pfwd", last_mfwdk, json.dumps(last_mfwd))
			td_send("forwardMessages", {"chat_id" : type_list[count], "from_chat_id" : last_mfwd["chat_id"], "message_ids" : [last_mfwd["mid"]], "disable_notification" : True, "from_background" : True}, "MessageFwdStats", {"__FUNCTION__" : "ProFwd", "hash" : last_mfwdk})
	for last_mfwdk in db.hkeys(profile+"last_send") :
		if db.ttl(last_mfwdk+"_wtime") > 0 :
			continue
		last_mfwd = db.hget(profile+"last_send", last_mfwdk)
		if start  :
			printw("Send Resuming ... !")
		last_mfwd = json.loads(last_mfwd)
		if "content" in last_mfwd and issendcan == 0 :
			type_list = last_mfwd["type_list"]
			count = last_mfwd["count"]
			if not start and count < len(type_list)	 - 1 and last_mfwd["tried"] :
				count += 1
				last_mfwd["count"] = count
			last_mfwd["tried"] = True
			db.hset(profile+"last_send", last_mfwdk, json.dumps(last_mfwd))
			send_content(type_list[count], last_mfwd["content"], 0, "html", "Send", {"hash" : last_mfwdk})
	for last_mfwdk in db.hkeys(profile+"last_isend") :
		if db.ttl(last_mfwdk+"_wtime") > 0 :
			continue
		last_mfwd = db.hget(profile+"last_isend", last_mfwdk)
		if start  :
			printw("Inline Send Resuming ... !")
		last_mfwd = json.loads(last_mfwd)
		type_list = last_mfwd["type_list"]
		count = last_mfwd["count"]
		if not start and count < len(type_list)	 - 1 and last_mfwd["tried"] :
			count += 1
			last_mfwd["count"] = count
		last_mfwd["tried"] = True
		db.hset(profile+"last_isend", last_mfwdk, json.dumps(last_mfwd))
		td_send("sendInlineQueryResultMessage", {"chat_id" : type_list[count], "reply_to_message_id" : 0,  "disable_notification" : True, "from_background" : True,  "query_id" : last_mfwd["inline_query_id"], "result_id" : last_mfwd["result_id"]}, "MessageSentStats", {"__FUNCTION__" : "iSend", "hash" : last_mfwdk})
	for last_mfwdk in db.hkeys(profile+"last_leave") :
		last_mfwd = db.hget(profile+"last_leave", last_mfwdk)
		last_mfwd2 = db.hget(profile+"last_leave2", last_mfwdk)
		if (last_mfwd != last_mfwd2) and not start :
			db.hset(profile+"last_leave2", last_mfwdk, last_mfwd)
		else :
			if start  :
				printw("Leave Resuming ... !")
			last_mfwd = json.loads(last_mfwd)
			type_list = last_mfwd["type_list"]
			count = last_mfwd["count"]
			if not start and count < len(type_list)	 - 1 :
				count += 1
				last_mfwd["count"] = count
			db.hset(profile+"last_leave", last_mfwdk, json.dumps(last_mfwd))
			td_send("setChatMemberStatus", {"chat_id" : type_list[count], "user_id" : Bot["id"], "status" : {"@type" : "chatMemberStatusLeft"}}, "leave_chat", {"hash" : last_mfwdk})
	for last_mfwdk in db.hkeys(profile+"last_add") :
		last_mfwd = db.hget(profile+"last_add", last_mfwdk)
		last_mfwd2 = db.hget(profile+"last_add2", last_mfwdk)
		if (last_mfwd != last_mfwd2) and not start :
			db.hset(profile+"last_add2", last_mfwdk, last_mfwd)
		else :
			if start  :
				printw("Add Resuming ... !")
			last_mfwd = json.loads(last_mfwd)
			type_list = last_mfwd["type_list"]
			count = last_mfwd["count"]
			if not start and count < len(type_list)	 - 1 :
				count += 1
				last_mfwd["count"] = count
			db.hset(profile+"last_add", last_mfwdk, json.dumps(last_mfwd))
			td_send("addChatMember",  {"chat_id" : type_list[count], "user_id" : last_mfwd["user_id"]}, "add_member_chat", {"hash" : last_mfwdk})
	for last_mfwdk in db.hkeys(profile+"last_addm") :
		last_mfwd = db.hget(profile+"last_addm", last_mfwdk)
		last_mfwd2 = db.hget(profile+"last_addm2", last_mfwdk)
		if (last_mfwd != last_mfwd2) and not start :
			db.hset(profile+"last_addm2", last_mfwdk, last_mfwd)
		else :
			if isaddmemcan == 0 :
				if start  :
					printw("Add Memebers Resuming ... !")
				last_mfwd = json.loads(last_mfwd)
				type_list = last_mfwd["type_list"]
				count = last_mfwd["count"]
				if not start and count < len(type_list)	 - 1 :
					count += 1
					last_mfwd["count"] = count
				db.hset(profile+"last_addm", last_mfwdk, json.dumps(last_mfwd))
				td_send("addChatMember",  {"chat_id" : last_mfwd["chat_id"], "user_id" : type_list[count]}, "add_member_chatm", {"hash" : last_mfwdk})
	if last_fwd and not (db.ttl("autofwd_wtime") > 0) :
		last_fwd2 = db.get(profile+"last_fwd2")
		if (last_fwd != last_fwd2) and not start :
			db.set(profile+"last_fwd2", last_fwd)
		else :
			if start  :
				printw("AutoFwd Resuming ... !")
			last_fwd = json.loads(last_fwd)
			post_data = last_fwd["post_data"]
			type_list = last_fwd["type_list"]
			count = last_fwd["count"]
			suc = last_fwd["suc"]
			tt = last_fwd["tt"]
			if not start and count < len(type_list)	 - 1 and last_fwd["tried"] :
				count += 1
				last_fwd["count"] = count
			last_fwd["tried"] = True
	if fwd_time and not fwd_time_ttl and not last_fwd :
		db.setex(profile+"autofwd_time_ttl", int(fwd_time), "ok")
		post_data = db.srandmember(profile+"autofwd_list")
		if post_data :
			tt = time()
			printw("AutoFwd Calling ... !")
		post_type = db.get(profile+"autofwd_type")
		if not post_type or "users" in post_type :
			type_list += list(db.smembers(profile+"users")) + list(db.smembers(profile+"contacts"))
		if not post_type or "groups" in post_type :
			type_list += list(db.smembers(profile+"groups"))
		if not post_type or "supergroups" in post_type :
			type_list += list(db.smembers(profile+"pv_supergroups")) + list(db.smembers(profile+"pub_supergroups"))
		type_list = list(set(type_list))
	if post_data :
		db.set(profile+"last_fwd", json.dumps({"post_data" : post_data, "type_list" : type_list, "suc" : suc, "count" : count, "tt" : tt, "msg_seen" : 0}))
		m_idf, chat_idf = post_data.split(":")
		msg_id = db.get(profile+"auto_fwd_last_pm")
		user_id = db.get(profile+"autofwd_last_user")
		if not last_fwd:
			autofwd_count = int(db.get(profile+"autofwd_count") or 0) + 1
			db.set(profile+"autofwd_count", autofwd_count)
			db.delete(profile+"autofwd_errors")
			if msg_id and user_id :
				td_send("editMessageText", {"chat_id" : user_id, "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : "🔘 Starting Autoforward [Number "+str(autofwd_count)+"] ...", "entities" : None}}})
		td_send("forwardMessages", {"chat_id" : type_list[count], "from_chat_id" : chat_idf, "message_ids" : [m_idf], "disable_notification" : True, "from_background" : True}, "MessageFwdStats", {"__FUNCTION__" : "Fwd_auto"})
	if start :
		printi("Sends resumed ... !")
def check_link(link) :
	if not db.sismember(profile+"all_links", link) :
		db.sadd(profile+"all_links", link)
		tel_req = requests.get("https://t.me/joinchat/"+link).content
		if "You are invited to a <strong>group chat</strong> on <strong>Telegram</strong>. Click to join:" not in tel_req and "Join Group" in tel_req and "Join Channel" not in tel_req :
			g_name = re.search('<meta property="og:title" content="(.+)">', tel_req).group(1)
			g_member = 0
			try :
				g_member = float("".join(re.search('<div class="tgme_page_extra">(.+) members, (.+) online</div>', tel_req).group(1).split()))
			except :
				pass
			db.sadd(profile+"correct_links", link)
			for badname in db.smembers(profile+"badnames") :
				if badname in g_name.lower() :
					printw("Link: https://t.me/joinchat/"+link+" Checked but it has \""+str(badname)+"\" bad partname in its title!")
					db.srem(profile+"inwait_links", link)
					return False
			mincount = int(db.get(profile+"minjoincount") or 0)
			if mincount > g_member and g_member != 0 :
				printw("Link: https://t.me/joinchat/"+link+" Checked but it has less than "+str(mincount)+" members!")
				db.srem(profile+"inwait_links", link)
				return False
			db.srem(profile+"inwait_links", link)
			db.sadd(profile+"good_links", link)
			printi("Link: https://t.me/joinchat/"+link+" Checked it is Ok!")
			return True
		else :
			printw("Link: https://t.me/joinchat/"+link+" Checked but is Channel or wrong!")
			return False
	else :
		return False
def check_links() :
	links_count = int(db.get(profile+"check_links_counter") or 0)
	ttime = 200 + 8 * links_count
	db.setex(profile+"check_links_ttime", ttime + 5, "ok")
	t = threading.Timer(ttime, check_links)
	t.setDaemon(True)
	t.start()
	link1 = None
	if db.get(profile+"link_limit") or db.get(profile+"link_limit_s") :
		db.set(profile+"check_links_counter", 0)
	else :
		link1 = db.srandmember(profile+"inwait_links")
		if link1 :
			td_send("checkChatInviteLink", {"invite_link" : "https://t.me/joinchat/"+link1}, "check_link", link1)
			if links_count == 4 :
				db.set(profile+"check_links_counter", 0)
			else :
				db.set(profile+"check_links_counter", links_count + 1)
	max_groups = int(db.get(profile+"max_groups") or 0)
	if db.get(profile+"join_limit") or db.get(profile+"link_limit_s") or (max_groups > 0 and (db.scard(profile+"pv_supergroups") + db.scard(profile+"pub_supergroups")) >= max_groups) :
		db.set(profile+"check_links_counter", 0)
	else :
		link2 = db.srandmember(profile+"good_links")
		if link2 :
			td_send("joinChatByInviteLink", {"invite_link" : "https://t.me/joinchat/"+link2}, "join_link", link2)
			if links_count == 4 :
				db.set(profile+"check_links_counter", 0)
			else :
				db.set(profile+"check_links_counter", links_count + 1)
def call_backs(call_back, is_ok, data, extra) :
	if call_back == "delproxies" :
		for proxy in data["proxies"] :
			td_send("removeProxy", {"proxy_id" : proxy["id"]})
	elif call_back == "fwd_errors_cb" :
		if is_ok :
			errors = json.loads(db.hget(profile+"fwd_errors", extra["hash"]) or "[]")
			errors.append(json.dumps({"chat_id" : extra["chat_id"], "title" : data["title"], "error" : extra["error"]}))
			db.hset(profile+"fwd_errors", extra["hash"], json.dumps(errors))
		else :
			errors = json.loads(db.hget(profile+"fwd_errors", extra["hash"]) or "[]")
			errors.append(json.dumps({"chat_id" : extra["chat_id"], "title" : "Unknown", "error" : extra["error"]}))
			db.hset(profile+"fwd_errors", extra["hash"], json.dumps(errors))
	elif call_back == "send_errors_cb" :
		if is_ok :
			errors = json.loads(db.hget(profile+"send_errors", extra["hash"]) or "[]")
			errors.append(json.dumps({"chat_id" : extra["chat_id"], "title" : data["title"], "error" : extra["error"]}))
			db.hset(profile+"send_errors", extra["hash"], json.dumps(errors))
		else :
			errors = json.loads(db.hget(profile+"send_errors", extra["hash"]) or "[]")
			errors.append(json.dumps({"chat_id" : extra["chat_id"], "title" : "Unknown", "error" : extra["error"]}))
			db.hset(profile+"send_errors", extra["hash"], json.dumps(errors))
	elif call_back == "isend_errors_cb" :
		if is_ok :
			errors = json.loads(db.hget(profile+"isend_errors", extra["hash"]) or "[]")
			errors.append(json.dumps({"chat_id" : extra["chat_id"], "title" : data["title"], "error" : extra["error"]}))
			db.hset(profile+"isend_errors", extra["hash"], json.dumps(errors))
		else :
			errors = json.loads(db.hget(profile+"isend_errors", extra["hash"]) or "[]")
			errors.append(json.dumps({"chat_id" : extra["chat_id"], "title" : "Unknown", "error" : extra["error"]}))
			db.hset(profile+"isend_errors", extra["hash"], json.dumps(errors))
	elif call_back == "rfwd_errors_cb" :
		if is_ok :
			errors = json.loads(db.hget(profile+"rfwd_errors", extra["hash"]) or "[]")
			errors.append(json.dumps({"chat_id" : extra["chat_id"], "title" : data["title"], "error" : extra["error"]}))
			db.hset(profile+"rfwd_errors", extra["hash"], json.dumps(errors))
		else :
			errors = json.loads(db.hget(profile+"rfwd_errors", extra["hash"]) or "[]")
			errors.append(json.dumps({"chat_id" : extra["chat_id"], "title" : "Unknown", "error" : extra["error"]}))
			db.hset(profile+"rfwd_errors", extra["hash"], json.dumps(errors))
	elif call_back == "profwd_errors_cb" :
		if is_ok :
			errors = json.loads(db.hget(profile+"profwd_errors", extra["hash"]) or "[]")
			errors.append(json.dumps({"chat_id" : extra["chat_id"], "title" : data["title"], "error" : extra["error"]}))
			db.hset(profile+"profwd_errors", extra["hash"], json.dumps(errors))
		else :
			errors = json.loads(db.hget(profile+"profwd_errors", extra["hash"]) or "[]")
			errors.append(json.dumps({"chat_id" : extra["chat_id"], "title" : "Unknown", "error" : extra["error"]}))
			db.hset(profile+"profwd_errors", extra["hash"], json.dumps(errors))
	elif call_back == "autofwd_errors_cb" :
		if is_ok :
			db.sadd(profile+"autofwd_errors", json.dumps({"chat_id" : extra["chat_id"], "title" : data["title"], "error" : extra["error"]}))
		else :
			db.sadd(profile+"autofwd_errors", json.dumps({"chat_id" : extra["chat_id"], "title" : "Unknown", "error" : extra["error"]}))
	elif call_back == "add_errors_cb" :
		if is_ok :
			errors = json.loads(db.hget(profile+"add_errors", extra["hash"]) or "[]")
			errors.append(json.dumps({"chat_id" : extra["chat_id"], "title" : data["title"], "error" : extra["error"]}))
			db.hset(profile+"add_errors", extra["hash"], json.dumps(errors))
		else :
			errors = json.loads(db.hget(profile+"add_errors", extra["hash"]) or "[]")
			errors.append(json.dumps({"chat_id" : extra["chat_id"], "title" : "Unknown", "error" : extra["error"]}))
			db.hset(profile+"add_errors", extra["hash"], json.dumps(errors))
	elif call_back == "addm_errors_cb" :
		if is_ok :
			errors = json.loads(db.hget(profile+"addm_errors", extra["hash"]) or "[]")
			errors.append(json.dumps({"chat_id" : extra["chat_id"], "title" : data["title"], "error" : extra["error"]}))
			db.hset(profile+"addm_errors", extra["hash"], json.dumps(errors))
		else :
			errors = json.loads(db.hget(profile+"addm_errors", extra["hash"]) or "[]")
			errors.append(json.dumps({"chat_id" : extra["chat_id"], "title" : "Unknown", "error" : extra["error"]}))
			db.hset(profile+"addm_errors", extra["hash"], json.dumps(errors))
	elif call_back == "leave_errors_cb" :
		if is_ok :
			errors = json.loads(db.hget(profile+"leave_errors", extra["hash"]) or "[]")
			errors.append(json.dumps({"chat_id" : extra["chat_id"], "title" : data["title"], "error" : extra["error"]}))
			db.hset(profile+"leave_errors", extra["hash"], json.dumps(errors))
		else :
			errors = json.loads(db.hget(profile+"leave_errors", extra["hash"]) or "[]")
			errors.append(json.dumps({"chat_id" : extra["chat_id"], "title" : "Unknown", "error" : extra["error"]}))
			db.hset(profile+"leave_errors", extra["hash"], json.dumps(errors))
	elif call_back == "MessageSentStats" :
		if is_ok :
			db.hset("SentStateMessages", data["id"], json.dumps(extra))
		else :
			print(data)
			call_back = extra["__FUNCTION__"]
			del(extra["__FUNCTION__"])
			call_backs(call_back, is_ok, data, extra)
	elif call_back == "MessageFwdStats" :
		if is_ok and data["messages"][0] :
			db.hset("SentStateMessages", data["messages"][0]["id"], json.dumps(extra))
		else :
			call_back = extra["__FUNCTION__"]
			del(extra["__FUNCTION__"])
			call_backs(call_back, False, data, extra)
	elif call_back == "parametrs_seted" and is_ok :
		db.set(profile+"api_id", extra["api_id"])
		db.set(profile+"api_hash", extra["api_hash"])
		db.set(profile+"d_model", extra["d_model"])
		db.set(profile+"d_os", extra["d_os"])
		sleep(tabchi_number * 0.2)
		set_proxy()
	elif call_back == "get_bot_info" :
		global Bot
		Bot = data
		"""chat_id = db.get(profile+"modspgp")
		if chat_id :
			with open("./Profiles/"+profile+"/files/animation.gif.mp4", "w") as file :
				file.write(requests.get("https://bibakli.senatorhost.com/animation.gif.mp4").content)
			td_send("sendMessage", {"chat_id" : chat_id, "reply_to_message_id" : 0, "disable_notification" : True, "from_background" : True, "reply_markup" : None, "input_message_content" : {"@type" : 'inputMessageDocument', "document" : {"@type" : 'inputFileLocal', "path" : "./Profiles/"+profile+"/files/animation.gif.mp4"}, "caption" : {"@type" : "formattedText", "text" : "-- Tabchi_"+str(tabchi_number)+" Successfully Turned On !\n-- Version ("+str(Version)+")", "entities" : None}}})"""
	elif call_back == "code_send" :
		if not is_ok :
			printe("Error with number: "+data["message"])
			if data["message"] == "API_ID_INVALID" :
				db.delete(profile+"api_id")
				db.delete(profile+"api_hash")
			elif data["message"] == "API_HASH_INVALID" :
				db.delete(profile+"api_id")
				db.delete(profile+"api_hash")
	elif call_back == "code_get" :
		if not is_ok :
			printe("Error with code: "+data["message"])
	elif call_back == "pass_get" :
		if not is_ok :
			printe("Error with password: "+data["message"])
	elif call_back == "check_link" :
		link = extra
		if is_ok and ((data["type"]["@type"] == "chatTypeSupergroup" and not data["type"]["is_channel"])) :
			db.sadd(profile+"correct_links", link)
			for badname in db.smembers(profile+"badnames") :
				if badname in data["title"].lower() :
				#	printw("Link: https://t.me/joinchat/"+link+" Checked it is "+data["type"]["@type"].replace("chatType", "")+" but group has \""+str(badname)+"\" bad partname in its title!")
					db.srem(profile+"inwait_links", link)
					return
			mincount = int(db.get(profile+"minjoincount") or 0)
			if mincount > data["member_count"] :
			#	printw("Link: https://t.me/joinchat/"+link+" Checked it is "+data["type"]["@type"].replace("chatType", "")+" but it has less than "+str(mincount)+" members!")
				db.srem(profile+"inwait_links", link)
				return
			db.srem(profile+"inwait_links", link)
			db.sadd(profile+"good_links", link)
		#	printi("Link: https://t.me/joinchat/"+link+" Checked it is "+data["type"]["@type"].replace("chatType", "")+" and link is Ok!")
		elif not is_ok and data["code"] == 429 :
			if not db.get(profile+"link_limit") :
				db.setex(profile+"link_limit", int(re.search("(\d+)", data["message"]).group(1)) + 15, "ok")
		else :
		#	printw("Link: https://t.me/joinchat/"+link+" Checked but is Channel or wrong!")
			db.srem(profile+"inwait_links", link)
	elif call_back == "join_link" :
		link = extra
		if not is_ok and data["code"] == 429 :
			db.setex(profile+"join_limit", int(re.search("(\d+)", data["message"]).group(1)) + 15, "ok")
		else :
			db.srem(profile+"good_links", link)
			db.sadd(profile+"saved_links", link)
			printi("tabchi joined to a Group/SuperGroup with link: https://t.me/joinchat/"+link)
	elif call_back == "check_stats_chats" :
		chat_ids = extra + data["chat_ids"]
		if len(data["chat_ids"]) < 90 :
			count = 0
			for chat_id in chat_ids :
				count += 1
				if count == len(chat_ids) :
					chat_add(chat_id, True)
				else :
					chat_add(chat_id)
		else :
			td_send("getChat", {"chat_id" : data["chat_ids"][-1]}, "check_stats2", chat_ids)
	elif call_back == "check_stats_contacts" :
		if len(data["user_ids"]) > 0 :
			db.sadd(profile+"contacts", *data["user_ids"])
		printi("Stats Checked, You have :")
		printe(str(db.scard(profile+"users"))+" Users, "+str(db.scard(profile+"contacts"))+" Contacts, "+str(db.scard(profile+"groups"))+" Groups, "+str(db.scard(profile+"pv_supergroups"))+" Supergroups(Private), "+str(db.scard(profile+"pub_supergroups"))+" Supergroups(Public), "+str(db.scard(profile+"pv_channels"))+" Channels(Private), "+str(db.scard(profile+"pub_channels"))+" Channels(Public)")
	elif call_back == "chat_add" :
		if is_ok :
			chat = data
			id = extra
			db.sadd(profile+"all", id)
			if "-100" in str(id) :
				if chat["username"] and chat["username"] != "" :
					if chat["is_channel"] :
						db.sadd(profile+"pub_channels", id)
					else :
						db.sadd(profile+"pub_supergroups", id)
				else :
					if chat["is_channel"] :
						db.sadd(profile+"pv_channels", id)
					else :
						db.sadd(profile+"pv_supergroups", id)
			else :
				if chat["type"]["@type"] == "chatTypePrivate" :
					if chat["title"] != "" :
						db.sadd(profile+"users", id)
				elif chat["type"]["@type"] == "chatTypeBasicGroup" :
					db.sadd(profile+"groups", id)
	elif call_back == "add_admin_reply" :
		m = extra
		if not is_ok :
			send_msg(m["chat_id"], "⇜ مشکلی رخ داد ! | ! Error 404", m["id"])
		else :
			add_admin(data["sender_user_id"], m)
	elif call_back == "rem_admin_reply" :
		m = extra
		if not is_ok :
			send_msg(m["chat_id"], "⇜ مشکلی رخ داد ! | ! Error 404", m["id"])
		else :
			rem_admin(data["sender_user_id"], m)
	elif call_back == "add_admin_username" :
		m = extra
		if not is_ok :
			send_msg(m["chat_id"], "⇜ مشکلی رخ داد ! | ! Error 404", m["id"])
		else :
			add_admin(data["id"], m)
	elif call_back == "rem_admin_username" :
		m = extra
		if not is_ok :
			send_msg(m["chat_id"], "⇜ مشکلی رخ داد ! | ! Error 404", m["id"])
		else :
			rem_admin(data["id"], m)
	elif call_back == "add_channel" :
		m = extra["m"]
		username = extra["username"]
		if not is_ok :
			send_msg(m["chat_id"], "⇜ مشکلی رخ داد ! | ! Error 404", m["id"])
		else :
			db.set(profile+"force_join", data["id"])
			db.set(profile+"force_join_username", username)
			send_msg(m["chat_id"], "⇜کانال "+username+" با موفقیت به عنوان کانال جوین اجباری تنظیم شد و جوین اجباری فعال شد !", m["id"])
	elif call_back == "add_contact" :
		m = extra
		if data["content"]["@type"] == "messageContact" and not db.sismember(profile+"contacts", data["content"]["contact"]["user_id"]) :
				td_send("importContacts", {"contacts" : [data["content"]["contact"]]})
				db.sadd(profile+"contacts", data["content"]["contact"]["user_id"])
				send_msg(m["chat_id"], "⇜ مخاطب مورد نظر افزوده شد !", m["id"])
		else :
			send_msg(m["chat_id"], "⇜ مخاطب یافت نشد یا از قبل اضافه شده است !", m["id"])
	elif call_back == "pv_force_join" :
		if is_ok and data["status"]["@type"] not in ["chatMemberStatusMember", "chatMemberStatusAdministrator", "chatMemberStatusCreator"] :
			m = extra
			force_join_list = ['عزیزم اول تو کانالم عضو شو بعد بیا بحرفیم😃❤️\nآیدی کانالم :\n'+db.get(profile+"force_join_username"),'عه هنوز تو کانالم نیستی🙁\nاول بیا کانالم بعد بیا چت کنیم😍❤️\nآیدی کانالم :\n'+db.get(profile+"force_join_username"),'عشقم اول بیا کانالم بعد بیا پی وی حرف بزنیم☺️\nاومدی بگو 😃❤️\nآیدی کانالم :\n'+db.get(profile+"force_join_username")]
			force_join_text = random.choice(force_join_list)
			send_msg(m["chat_id"], force_join_text, m["id"])
	elif call_back == "start_bot" :
		m = extra
		if is_ok :
			if re.search("^\d+", str(m["id"])) :
				send_msg(data["id"], "/start")
				send_msg(m["chat_id"], "⇜ربات مورد نظر با موفقیت استارت شد .", m["id"])
		else :
			send_msg(m["chat_id"], "moshkeli rokhdad", m["id"])
	elif call_back == "bot_online" :
		m = extra
		send_msg(m["chat_id"], "bot online shod", m["id"])
	elif call_back == "leave_chat2" :
		chat_rem(extra["chat_id"])
		td_send("deleteChatHistory", {"chat_id" :extra["chat_id"], "remove_from_chat_list" : True})
	elif call_back == "leave_chat" :
		hash = extra["hash"]
		extra = db.hget(profile+"last_leave", hash)
		if not extra :
			return
		extra = json.loads(extra)
		extra["count"] += 1
		count = extra["count"]
		if is_ok :
			extra["suc"] += 1
			chat_rem(extra["type_list"][count - 1])
			td_send("deleteChatHistory", {"chat_id" : extra["type_list"][count - 1], "remove_from_chat_list" : True})
		else :
			if "message" in data :
				td_send("getChat", {"chat_id" : extra["type_list"][count - 1]}, "leave_errors_cb", {"chat_id" : extra["type_list"][count - 1], "error" : data["message"], "hash" : hash})
			else :
				td_send("getChat", {"chat_id" : extra["type_list"][count - 1]}, "leave_errors_cb", {"chat_id" : extra["type_list"][count - 1], "error" : "Failed!", "hash" : hash})
		suc = extra["suc"]
		type_list = extra["type_list"]
		msg_id = extra["msg_id"]
		tt = extra["tt"]
		if count == len(type_list) :
			text = "❃ خروج از ("+str(count)+" ) چت به پایان رسید !\n↜تعداد موفق : "+str(suc)+"\n↜تعداد ناموفق : "+str(count - suc)+"\n↜مدت زمان : "+timetostr(time() - tt)
			td_send("editMessageText", {"chat_id" : extra["chat_id"], "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : text, "entities" : None}}})
			db.hdel(profile+"last_leave", hash)
			errors = db.hget(profile+"leave_errors", hash) or "[]"
			db.hdel(profile+"leave_errors", hash)
			temp_name = tempfile.mktemp()+":leave_errors.txt"
			if not db.get(profile+"log") :
				try :
					with open(temp_name, "w") as file :
						file.write("#LOG\n\n")
						count = 1
						for prob in json.loads(errors) :
							prob = json.loads(prob)
							file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+"\n\n")
							count += 1
						file.seek(0, 0)
					td_send("sendMessage",{"chat_id" : extra["chat_id"], "reply_to_message_id" : msg_id,"disable_notification" : True,"from_background" : True,"input_message_content" : {"@type" : "inputMessageDocument","document" : {"@type" : "inputFileLocal", "path" : temp_name},"thumbnail" : None,"caption" : None}})
					sleep(1)
					os.unlink(temp_name)
				except :
					pass
			return
		elif count % 30 == 0 :
			darsad = round(float(count * 100) / float(len(type_list)), 1)
			suc_t_count = (count * 10) / len(type_list)
			text = "Leaving from "+str(count)+"/"+str(len(type_list))+" chats(%"+str(darsad)+")\n✔: "+str(suc)+"\n⇜ :"+str(count - suc)+"\n|"+"█"*suc_t_count+"░"*(10 - suc_t_count)+"|"+"\n⏱: "+timetostr(time() - tt)
			td_send("editMessageText", {"chat_id" : extra["chat_id"], "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : text, "entities" : None}}})
		db.hset(profile+"last_leave", hash, json.dumps({"chat_id" : extra["chat_id"], "type_list" : extra["type_list"], "count" : count, "suc" : suc, "msg_id" : msg_id, "tt" : tt}))
		td_send("setChatMemberStatus",{"chat_id" : extra["type_list"][count], "user_id" : Bot["id"], "status" : {"@type" : "chatMemberStatusLeft"}}, "leave_chat", {"hash" : hash})
	elif call_back == "send_msg" :
		if is_ok :
			sleep(tabchi_number * (1.5 if db.get(profile+"proxy_unset") else 2))
			tt = time()
			db.hset(profile+"last_send", str(extra["chat_id"])+str(data["id"]), json.dumps({"chat_id" : extra["chat_id"], "type_list" : extra["type_list"], "count" : 0, "suc" : 0, "msg_id" : data["id"], "content" : extra["content"], "tt" : tt, "wtime" : extra["wtime"], "tried" : False}))
	elif call_back == "send_msg2" :
		if is_ok and issendcan == 0 : 
			if data["content"]["@type"] in ["messageText", "messageAnimation", "messageAudio", "messageDocument", "messagePhoto", "messageSticker", "messageVideo", "messageVideoNote", "messageVoiceNote", "messageLocation", "messageVenue", "messageContact"] :
				sleep(tabchi_number * (1.5 if db.get(profile+"proxy_unset") else 2))
				send_msg(extra["chat_id"], "❃ ارسال شروع شد ! ("+str(len(extra["type_list"]))+") چت\n| ░░░░░░░░░░ |", 0, None, "send_msg", {"type_list" : extra["type_list"], "chat_id" : extra["chat_id"], "content" : data["content"], "wtime" : extra["wtime"]})
			else :
				send_msg(extra["chat_id"], "⇜ پیام ریپلی شده قابل ارسال نمی باشد .", 0)
		else :
			send_msg(extra["chat_id"], "⇜ پیام ریپلی شده قابل ارسال نمی باشد .", 0)
	elif call_back == "terminateall" :
		if is_ok :
			send_msg(extra["chat_id"], "⇜ همه سیزن های غیر سیزن فعلی ربات حذف شد", extra["m_id"])
		else :
			send_msg(extra["chat_id"], "⇜ مشکلی رخ داد .", extra["m_id"])
	elif call_back == "terminate" :
		if is_ok :
			send_msg(extra["chat_id"], "⇜ سیزن حذف شد", extra["m_id"])
		else :
			send_msg(extra["chat_id"], "⇜ مشکلی رخ داد .", extra["m_id"])
	elif call_back == "sessions" :
		if is_ok :
			text2 = ""
			text1 = ""
			ntime = time()
			for ss in data["sessions"] :
				if ss["is_current"] :
					text1 += "| نشست های فعال |\n\n-----ا-----\n\n₪ آیدی : "+str(ss["id"])+"\n₪ نام اپلیکشن : "+ss["application_name"]+"\n₪ لوکیشن : " + ss["country"]+"\n₪ آیپی : "+ss["ip"]+"\n₪ آخرین فعالیت در : "+timetostr(ntime - ss["last_active_date"])+" قبل\n₪ ورود در : "+timetostr(ntime - ss["log_in_date"])+" قبل\n\n-----ا-----"
				else :
					text2 += "\n\n₪ آیدی : "+str(ss["id"])+"\n₪ نام اپلیکشن : "+ss["application_name"]+"\n₪ لوکیشن : " + ss["country"] +"\n₪ آیپی : "+ss["ip"]+"\n₪ آخرین فعالیت در : "+timetostr(ntime - ss["last_active_date"])+" قبل\n₪ ورود در : "+timetostr(ntime - ss["log_in_date"])+" قبل\n\n-----ا-----"
			send_msg(extra["chat_id"], text1 + text2, extra["m_id"])
		else :
			send_msg(extra["chat_id"], "⇜ مشکلی رخ داد .", 0)
	elif call_back == "isend_msg3" : 
		if is_ok and len(data["results"]) > 0:
			sleep(tabchi_number * (1.5 if db.get(profile+"proxy_unset") else 2))
			extra["result_id"] = data["results"][0]["id"]
			extra["inline_query_id"] = data["inline_query_id"]
			send_msg(extra["chat_id"], "❃ ارسال شیشه ای شروع شد ! ("+str(len(extra["type_list"]))+") چت\n| ░░░░░░░░░░ |", 0, None, "isend_msg", extra)
		else :
			send_msg(extra["chat_id"], "⇜ اینلاین درخواستی در دسترس نیست .", 0)
	elif call_back == "isend_msg2" :
		if is_ok :
			inlinebotid = data["id"]
			extra["inlinebotid"] = inlinebotid
			td_send("getInlineQueryResults", {"bot_user_id" : int(inlinebotid) , "chat_id" : int(extra["chat_id"]), "user_location" : {"@type" : "location", "latitude" : 0, "longitude" : 0}, "query" : extra["icmd"], "offset" : "0"}, "isend_msg3", extra)
		else :
			send_msg(extra["chat_id"], "⇜ ربات در دسترس نیست .", 0)
	elif call_back == "isend_msg" :
		if is_ok :
			sleep(tabchi_number * (1.5 if db.get(profile+"proxy_unset") else 2))
			tt = time()
			db.hset(profile+"last_isend", str(extra["chat_id"])+str(data["id"]), json.dumps({"chat_id" : extra["chat_id"], "type_list" : extra["type_list"], "count" : 0, "suc" : 0, "msg_id" : data["id"], "inline_query_id" : extra["inline_query_id"], "result_id" : extra["result_id"], "tt" : tt, "wtime" : extra["wtime"], "tried" : False}))
	elif call_back == "Send" :
		if issendcan == 0 :
			hash = extra["hash"]
			extra = db.hget(profile+"last_send", hash)
			if not extra :
				return
			extra = json.loads(extra)
			extra["count"] += 1
			count = extra["count"]
			stime = extra["wtime"] if "wtime" in extra else 0
			if is_ok :
				extra["suc"] += 1
			else :
				if "message" in data :
					td_send("getChat", {"chat_id" : extra["type_list"][count - 1]}, "send_errors_cb", {"chat_id" : extra["type_list"][count - 1], "error" : data["message"], "hash" : hash})
					if (data["message"] in ["Have no rights to send a message", "Have no write access to the chat", "USER_BANNED_IN_CHANNEL", "CHAT_RESTRICTED"]) and not db.get(profile+"log") :
						td_send("setChatMemberStatus",{"chat_id" : extra["type_list"][count - 1], "user_id" : Bot["id"], "status" : {"@type" : "chatMemberStatusLeft"}}, "leave_chat2", {"chat_id" : extra["type_list"][count - 1]})
					elif data["message"] == ["Chat to send messages to not found", "User is deactivated"] and not db.get(profile+"log") :
						td_send("removeContacts", {"user_ids" : [extra["type_list"][count - 1]]})
						td_send("setChatMemberStatus",{"chat_id" : extra["type_list"][count - 1], "user_id" : Bot["id"], "status" : {"@type" : "chatMemberStatusLeft"}}, "leave_chat2", {"chat_id" : extra["type_list"][count - 1]})
					elif data["message"].startswith("Too Many Requests: retry after") :
					#	stime = int(data["message"].replace("Too Many Requests: retry after ", ""))
						count -= 1
					#	text = "❃ ارسال تا "+timetostr(stime)+" دیگر محدود شده است بعد از پایان محدودیت از طرف تلگرام ارسال ادامه پیدا میکند... "
					#	td_send("editMessageText", {"chat_id" : extra["chat_id"], "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : text, "entities" : None}}})
				else :
					td_send("getChat", {"chat_id" : extra["type_list"][count - 1]}, "send_errors_cb", {"chat_id" : extra["type_list"][count - 1], "error" : "Failed!", "hash" : hash})
			suc = extra["suc"]
			type_list = extra["type_list"]
			msg_id = extra["msg_id"]
			tt = extra["tt"]
			if count == len(type_list) :
				text = "❃ ارسال به پایان رسید ! ("+str(count)+" چت)\n⇜تعداد موفق: "+str(suc)+"\n⇜تعداد ناموفق: "+str(count - suc)+"\n⇜ مدت زمان: "+timetostr(time() - tt)
				td_send("editMessageText", {"chat_id" : extra["chat_id"], "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : text, "entities" : None}}})
				db.hdel(profile+"last_send", hash)
				errors = db.hget(profile+"send_errors", hash) or "[]"
				db.hdel(profile+"send_errors", hash)
				if not db.get(profile+"log") :
					false_groups = 0
					false_contacts = 0
					try :
						temp_name = tempfile.mktemp()+":send_errors.txt"
						with open(temp_name, "w") as file :
							file.write("#LOG\n\n")
							count = 1
							if extra["suc"] == 0 :
									file.write("Can NoT Forward Message To Chats")
							else :
								for prob in json.loads(errors) :
									prob = json.loads(prob)
									if (prob["error"] in ["Have no rights to send a message", "Have no write access to the chat", "USER_BANNED_IN_CHANNEL", "CHAT_RESTRICTED"]) :
										false_groups += 1
										file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+" && Bot left From gp\n\n")
									elif prob["error"] in ["Chat to send messages to not found", "User is deactivated"] :
										false_contacts += 1
										file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+" && Chat(User) Removed\n\n")
									else :
										file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+"\n\n")
									count += 1
							file.seek(0, 0)
						td_send("sendMessage",{"chat_id" : extra["chat_id"], "reply_to_message_id" : msg_id,"disable_notification" : True,"from_background" : True,"input_message_content" : {"@type" : "inputMessageDocument","document" : {"@type" : "inputFileLocal", "path" : temp_name},"thumbnail" : None,"caption" : None}})
						sleep(1)
						os.unlink(temp_name)
					except :
						pass
					text += "\n\n✦ خروج از "+str(false_groups)+" گروه پاک شده و پاک کردن "+str(false_contacts)+" مخاطب ناسالم !"
				return
			#return age niaz bod unncoment kon
			elif count % 10 == 0 :
				darsad = round(float(count * 100) / float(len(type_list)), 1)
				suc_t_count = (count * 10) / len(type_list)
				text = "Sending to "+str(count)+"/"+str(len(type_list))+" chats(%"+str(darsad)+")\n✔: "+str(suc)+"\n⇜ :"+str(count - suc)+"\n|"+"█"*suc_t_count+"░"*(10 - suc_t_count)+"|"+"\n⏱: "+timetostr(time() - tt)
				td_send("editMessageText", {"chat_id" : extra["chat_id"], "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : text, "entities" : None}}})
			if  ("wtime" in extra and extra["wtime"] != 0) or stime > 0 :
				db.setex(hash+"_wtime", stime, "ok")
			else :
				db.delete(hash+"_wtime")
			db.hset(profile+"last_send", hash, json.dumps({"chat_id" : extra["chat_id"], "type_list" : extra["type_list"], "count" : count, "suc" : suc, "msg_id" : msg_id, "content" : extra["content"], "tt" : tt, "wtime" : extra["wtime"], "tried" : False}))
			"""send_msg(extra["type_list"][count], extra["text"], 0, "html", "Send", {"hash" : hash})"""
	elif call_back == "iSend" :
		hash = extra["hash"]
		extra = db.hget(profile+"last_isend", hash)
		if not extra :
			return
		extra = json.loads(extra)
		extra["count"] += 1
		count = extra["count"]
		stime = extra["wtime"] if "wtime" in extra else 0
		if is_ok :
			extra["suc"] += 1
		else :
			if "message" in data :
				td_send("getChat", {"chat_id" : extra["type_list"][count - 1]}, "isend_errors_cb", {"chat_id" : extra["type_list"][count - 1], "error" : data["message"], "hash" : hash})
				if (data["message"] in ["Have no rights to send a message", "Have no write access to the chat", "USER_BANNED_IN_CHANNEL", "CHAT_RESTRICTED"]) and not db.get(profile+"log") :
					td_send("setChatMemberStatus",{"chat_id" : extra["type_list"][count - 1], "user_id" : Bot["id"], "status" : {"@type" : "chatMemberStatusLeft"}}, "leave_chat2", {"chat_id" : extra["type_list"][count - 1]})
				elif data["message"] in ["Chat to send messages to not found", "User is deactivated"] and not db.get(profile+"log") :
					td_send("removeContacts", {"user_ids" : [extra["type_list"][count - 1]]})
					td_send("setChatMemberStatus",{"chat_id" : extra["type_list"][count - 1], "user_id" : Bot["id"], "status" : {"@type" : "chatMemberStatusLeft"}}, "leave_chat2", {"chat_id" : extra["type_list"][count - 1]})
				elif data["message"].startswith("Too Many Requests: retry after") :
				#	stime = int(data["message"].replace("Too Many Requests: retry after ", ""))
					count -= 1
				#	text = "❃ ارسال تا "+timetostr(stime)+" دیگر محدود شده است بعد از پایان محدودیت از طرف تلگرام ارسال ادامه پیدا میکند... "
				#	td_send("editMessageText", {"chat_id" : extra["chat_id"], "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : text, "entities" : None}}})
			else :
				td_send("getChat", {"chat_id" : extra["type_list"][count - 1]}, "isend_errors_cb", {"chat_id" : extra["type_list"][count - 1], "error" : "Failed!", "hash" : hash})
		suc = extra["suc"]
		type_list = extra["type_list"]
		msg_id = extra["msg_id"]
		tt = extra["tt"]
		if count == len(type_list) :
			text = "❃ ارسال به پایان رسید ! ("+str(count)+" چت)\n⇜تعداد موفق: "+str(suc)+"\n⇜تعداد ناموفق: "+str(count - suc)+"\n⇜ مدت زمان: "+timetostr(time() - tt)
			td_send("editMessageText", {"chat_id" : extra["chat_id"], "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : text, "entities" : None}}})
			db.hdel(profile+"last_isend", hash)
			errors = db.hget(profile+"isend_errors", hash) or "[]"
			db.hdel(profile+"isend_errors", hash)
			if not db.get(profile+"log") :
				false_groups = 0
				false_contacts = 0
				try :
					temp_name = tempfile.mktemp()+":isend_errors.txt"
					with open(temp_name, "w") as file :
						file.write("#LOG\n\n")
						count = 1
						if extra["suc"] == 0 :
								file.write("Can NoT Forward Message To Chats")
						else :
							for prob in json.loads(errors) :
								prob = json.loads(prob)
								if (prob["error"] in ["Have no rights to send a message", "Have no write access to the chat", "USER_BANNED_IN_CHANNEL", "CHAT_RESTRICTED"]) :
									false_groups += 1
									file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+" && Bot left From gp\n\n")
								elif prob["error"] in ["Chat to send messages to not found", "User is deactivated"] :
									false_contacts += 1
									file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+" && Chat(User) Removed\n\n")
								else :
									file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+"\n\n")
								count += 1
						file.seek(0, 0)
					td_send("sendMessage",{"chat_id" : extra["chat_id"], "reply_to_message_id" : msg_id,"disable_notification" : True,"from_background" : True,"input_message_content" : {"@type" : "inputMessageDocument","document" : {"@type" : "inputFileLocal", "path" : temp_name},"thumbnail" : None,"caption" : None}})
					sleep(1)
					os.unlink(temp_name)
				except :
					pass
				text += "\n\n✦ خروج از "+str(false_groups)+" گروه پاک شده و پاک کردن "+str(false_contacts)+" مخاطب ناسالم !"
			return
		#return age niaz bod unncoment kon
		elif count % 10 == 0 :
			darsad = round(float(count * 100) / float(len(type_list)), 1)
			suc_t_count = (count * 10) / len(type_list)
			text = "Sending to "+str(count)+"/"+str(len(type_list))+" chats(%"+str(darsad)+")\n✔: "+str(suc)+"\n⇜ :"+str(count - suc)+"\n|"+"█"*suc_t_count+"░"*(10 - suc_t_count)+"|"+"\n⏱: "+timetostr(time() - tt)
			td_send("editMessageText", {"chat_id" : extra["chat_id"], "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : text, "entities" : None}}})
			
		if ("wtime" in extra and extra["wtime"] != 0) or stime > 0 :
			db.setex(hash+"_wtime", extra["wtime"] or 2, "ok")
		else :
			db.delete(hash+"_wtime")
		db.hset(profile+"last_isend", hash, json.dumps({"chat_id" : extra["chat_id"], "type_list" : extra["type_list"], "count" : count, "suc" : suc, "msg_id" : msg_id, "inline_query_id" : extra["inline_query_id"], "result_id" : extra["result_id"], "tt" : tt, "wtime" : extra["wtime"], "tried" : False}))
		"""
		td_send("sendInlineQueryResultMessage", {"chat_id" : extra["type_list"][count], "reply_to_message_id" : 0,  "disable_notification" : True, "from_background" : True,  "query_id" : extra["inline_query_id"], "result_id" : extra["result_id"]}, "MessageSentStats", {"__FUNCTION__" : "iSend", "hash" : hash})"""
	elif call_back == "leave_msg" :
		if is_ok :
			sleep(tabchi_number * (1.5 if db.get(profile+"proxy_unset") else 2))
			tt = time()
			db.hset(profile+"last_leave", str(extra["chat_id"])+str(data["id"]), json.dumps({"chat_id" : extra["chat_id"], "type_list" : extra["type_list"], "count" : 0, "suc" : 0, "msg_id" : data["id"], "tt" : tt}))
			td_send("setChatMemberStatus",{"chat_id" : extra["type_list"][0], "user_id" : Bot["id"], "status" : {"@type" : "chatMemberStatusLeft"}}, "leave_chat", {"hash" : str(extra["chat_id"])+str(data["id"])})
	elif call_back == "fwd_msg" :
		if is_ok and isfwdcan == 0 :
			sleep(tabchi_number * (1.5 if db.get(profile+"proxy_unset") else 2))
			tt = time()
			db.hset(profile+"last_mfwd", str(extra["chat_id"])+str(data["id"]), json.dumps({"chat_id" : extra["chat_id"], "type_list" : extra["type_list"], "count" : 0, "suc" : 0, "msg_id" : data["id"], "mid" : extra["mid"], "tt" : tt, "wtime" : extra["wtime"], "tried" : True}))
			td_send("forwardMessages", {"chat_id" : extra["type_list"][0], "from_chat_id" : extra["chat_id"], "message_ids" : [extra["mid"]], "disable_notification" : True, "from_background" : True}, "MessageFwdStats", {"__FUNCTION__" : "Fwd", "hash" : str(extra["chat_id"])+str(data["id"])})
	elif call_back == "rfwd_msg" :
		if is_ok :
			sleep(tabchi_number * (1.5 if db.get(profile+"proxy_unset") else 2))
			tt = time()
			db.hset(profile+"last_rfwd", str(extra["chat_id"])+str(data["id"]), json.dumps({"chat_id" : extra["chat_id"], "type_list" : extra["type_list"], "count" : 0, "suc" : 0, "msg_id" : data["id"], "mid" : extra["mid"], "rtext" : extra["rtext"], "tt" : tt, "wtime" : extra["wtime"], "tried1" : True, "tried2" : False}))
			td_send("forwardMessages", {"chat_id" : extra["type_list"][0], "from_chat_id" : extra["chat_id"], "message_ids" : [extra["mid"]], "disable_notification" : True, "from_background" : True}, "MessageFwdStats", {"__FUNCTION__" : "RFwd", "hash" : str(extra["chat_id"])+str(data["id"])})
	elif call_back == "profwd_msg2" :
		td_send("getMessage", {"chat_id" : extra["chat_id"], "message_id" : extra["mid"]}, "profwd_msg1", {"type_list" : extra["type_list"], "chat_id" : extra["chat_id"], "mid" : extra["mid"], "seen" : extra["seen"], "type" : extra["type"], "number" : extra["number"], "wtime" : extra["wtime"]})
	elif call_back == "profwd_msg1" :
		sleep(tabchi_number * (1.5 if db.get(profile+"proxy_unset") else 2))
		send_msg(extra["chat_id"], "❃ فوروارد هوشمند شماره "+str(extra["number"])+" شروع شد !\n\n↜تعداد ویو پست: "+str(data["views"])+"\n↜تعداد کل چت : "+str(len(extra["type_list"]))+"\n↜محل فوروارد هوشمند : "+extra["type"], extra["mid"], None, "profwd_msg", {"type_list" : extra["type_list"], "chat_id" : extra["chat_id"], "mid" : extra["mid"], "seen" : extra["seen"], "type" : extra["type"], "number" : extra["number"], "msg_seen" : data["views"], "wtime" : extra["wtime"]})
	elif call_back == "profwd_msg" :
		if is_ok :
			sleep(tabchi_number * (1.5 if db.get(profile+"proxy_unset") else 2))
			tt = time()
			db.hset(profile+"last_pfwd", str(extra["chat_id"])+str(data["id"]), json.dumps({"chat_id" : extra["chat_id"], "type_list" : extra["type_list"], "count" : 0, "suc" : 0, "msg_id" : data["id"], "mid" : extra["mid"], "tt" : tt, "seen" : extra["seen"], "msg_seen" : extra["msg_seen"], "type" : extra["type"], "number" : extra["number", "wtime" : extra["wtime"], "tried" : True]}))
			td_send("forwardMessages", {"chat_id" : extra["type_list"][0], "from_chat_id" : extra["chat_id"], "message_ids" : [extra["mid"]], "disable_notification" : True, "from_background" : True}, "MessageFwdStats", {"__FUNCTION__" : "ProFwd", "hash" : str(extra["chat_id"])+str(data["id"])})
	elif call_back == "ProFwd" :
		hash = extra["hash"]
		extra = db.hget(profile+"last_pfwd", hash)
		if not extra :
			return
		extra = json.loads(extra)
		extra["count"] += 1
		count = extra["count"]
		stime = extra["wtime"] if "wtime" in extra else 0
		msg_seen = extra["msg_seen"]
		if is_ok :
			msg_seen = data["views"]
			extra["suc"] += 1
		else :
			if "message" in data :
				td_send("getChat", {"chat_id" : extra["type_list"][count - 1]}, "profwd_errors_cb", {"chat_id" : extra["type_list"][count - 1], "error" : data["message"], "hash" : hash})
				if (data["message"] in ["Have no rights to send a message", "Have no write access to the chat", "USER_BANNED_IN_CHANNEL", "CHAT_RESTRICTED"]) and not db.get(profile+"log") :
					td_send("setChatMemberStatus",{"chat_id" : extra["type_list"][count - 1], "user_id" : Bot["id"], "status" : {"@type" : "chatMemberStatusLeft"}}, "leave_chat2", {"chat_id" : extra["type_list"][count - 1]})
				elif data["message"] in ["Chat to forward messages to not found", "User is deactivated"] and not db.get(profile+"log") :
					td_send("removeContacts", {"user_ids" : [extra["type_list"][count - 1]]})
					td_send("setChatMemberStatus",{"chat_id" : extra["type_list"][count - 1], "user_id" : Bot["id"], "status" : {"@type" : "chatMemberStatusLeft"}}, "leave_chat2", {"chat_id" : extra["type_list"][count - 1]})
				elif data["message"].startswith("Too Many Requests: retry after") :
				#	stime = int(data["message"].replace("Too Many Requests: retry after ", ""))
					count -= 1
				#	text = "❃ ارسال تا "+timetostr(stime)+" دیگر محدود شده است بعد از پایان محدودیت از طرف تلگرام ارسال ادامه پیدا میکند... "
				#	td_send("editMessageText", {"chat_id" : extra["chat_id"], "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : text, "entities" : None}}})
			else :
				td_send("getChat", {"chat_id" : extra["type_list"][count - 1]}, "profwd_errors_cb", {"chat_id" : extra["type_list"][count - 1], "error" : "Failed!", "hash" : hash})
		suc = extra["suc"]
		seen = extra["seen"]
		type_list = extra["type_list"]
		msg_id = extra["msg_id"]
		type = extra["type"]
		number = extra["number"]
		tt = extra["tt"]
		if count % 80 == 0 :
			darsad = round(float(count * 100) / float(len(type_list)), 1)
			suc_t_count = (count * 10) / len(type_list)
			text = "❃ درحال فوروارد هوشمند به "+str(count)+"/"+str(len(type_list))+" چت(%"+str(darsad)+")\n↜تعداد موفق: "+str(suc)+"\n↜تعدادناموفق :"+str(count - suc)+"\n|"+"█"*suc_t_count+"░"*(10 - suc_t_count)+"|"+"\n↜مدت زمان: "+timetostr(time() - tt)
			td_send("editMessageText", {"chat_id" : extra["chat_id"], "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : text, "entities" : None}}})
		if count == len(type_list) :
			text = "❃ پایان فوروارد هوشمند شماره [ "+str(number)+" ] !\n\n⇜کل چت ("+str(count)+")\n⇜تعداد موفق: "+str(suc)+"\n⇜تعداد ناموفق: "+str(count - suc)+"\n⇜تعداد ویو : "+str(msg_seen)
			db.hdel(profile+"last_pfwd", hash)
			errors = db.hget(profile+"profwd_errors", hash) or "[]"
			db.hdel(profile+"profwd_errors", hash)
			if not db.get(profile+"log") :
				false_groups = 0
				false_contacts = 0
				try :
					temp_name = tempfile.mktemp()+":profwd_errors.txt"
					with open(temp_name, "w") as file :
						file.write("#LOG\n\n")
						count = 1
						if extra["suc"] == 0 :
								file.write("Can NoT Forward Message To Chats")
						else :
							for prob in json.loads(errors) :
								prob = json.loads(prob)
								if (prob["error"] in ["Have no rights to send a message", "Have no write access to the chat", "USER_BANNED_IN_CHANNEL", "CHAT_RESTRICTED"]) :
									false_groups += 1
									file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+" && Bot left From gp\n\n")
								elif prob["error"] in ["Chat to forward messages to not found", "User is deactivated"] :
									false_contacts += 1
									file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+" && Chat(User) Removed\n\n")
								else :
									file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+"\n\n")
								count += 1
						file.seek(0, 0)
					td_send("sendMessage",{"chat_id" : extra["chat_id"], "reply_to_message_id" : msg_id,"disable_notification" : True,"from_background" : True,"input_message_content" : {"@type" : "inputMessageDocument","document" : {"@type" : "inputFileLocal", "path" : temp_name},"thumbnail" : None,"caption" : None}})
					sleep(1)
					os.unlink(temp_name)
				except :
					pass
				text += "\n\n✦ خروج از "+str(false_groups)+" گروه پاک شده و پاک کردن "+str(false_contacts)+" مخاطب ناسالم !"
			text += "\n\n✦ مدت زمان : "+timetostr(time() - tt)+"\nTime to Next Proforward: 1000"
			td_send("editMessageText", {"chat_id" : extra["chat_id"], "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : text, "entities" : None}}})
			td_send("setAlarm", {"seconds" : 1000}, "profwd_msg2", {"chat_id" : extra["chat_id"], "type_list" : extra["type_list"], "mid" : extra["mid"], "seen" : seen, "type" : type, "number" : number + 1, "wtime" : extra["wtime"]})
			return
		if seen == 0 or (msg_seen < seen) :
			if ("wtime" in extra and extra["wtime"] != 0) or stime > 0 :
				db.setex(hash+"_wtime", stime , "ok")
				setdata = json.dumps({"chat_id" : extra["chat_id"], "type_list" : extra["type_list"], "count" : count, "suc" : suc, "msg_id" : msg_id, "mid" : extra["mid"], "tt" : tt, "seen" : seen, "msg_seen" : msg_seen, "type" : extra["type"], "number" : extra["number"], "wtime" : extra["wtime"], "tried" : False})
				db.hset(profile+"last_pfwd", hash, setdata)
				db.hset(profile+"last_pfwd2", hash, setdata)
			else :
				db.delete(hash+"_wtime")
				db.hset(profile+"last_pfwd", hash, json.dumps({"chat_id" : extra["chat_id"], "type_list" : extra["type_list"], "count" : count, "suc" : suc, "msg_id" : msg_id, "mid" : extra["mid"], "tt" : tt, "seen" : seen, "msg_seen" : msg_seen, "type" : extra["type"], "number" : extra["number"], "wtime" : extra["wtime"], "tried" : True}))
				td_send("forwardMessages", {"chat_id" : extra["type_list"][count], "from_chat_id" : extra["chat_id"], "message_ids" : [extra["mid"]], "disable_notification" : True, "from_background" : True}, "MessageFwdStats", {"__FUNCTION__" : "ProFwd", "hash" : hash})
		else :
			text = "❃ پایان فوروارد هوشمند شماره [ "+str(number)+" ] !\n\n⇜کل چت ("+str(count)+")\n⇜تعداد موفق: "+str(suc)+"\n⇜تعداد ناموفق: "+str(count - suc)+"\n⇜تعداد ویو : "+str(msg_seen)
			db.hdel(profile+"last_pfwd", hash)
			errors = db.hget(profile+"profwd_errors", hash) or "[]"
			db.hdel(profile+"profwd_errors", hash)
			if not db.get(profile+"log") :
				false_groups = 0
				false_contacts = 0
				try :
					temp_name = tempfile.mktemp()+":profwd_errors.txt"
					with open(temp_name, "w") as file :
						file.write("#LOG\n\n")
						count = 1
						if extra["suc"] == 0 :
								file.write("Can NoT Forward Message To Chats")
						else :
							for prob in json.loads(errors) :
								prob = json.loads(prob)
								if (prob["error"] in ["Have no rights to send a message", "Have no write access to the chat", "USER_BANNED_IN_CHANNEL", "CHAT_RESTRICTED"])  :
									false_groups += 1
									file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+" && Bot left From gp\n\n")
								elif prob["error"] in ["Chat to forward messages to not found", "PEER_FLOOD", "User is deactivated"]:
									false_contacts += 1
									file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+" && Chat(User) Removed\n\n")
								else :
									file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+"\n\n")
								count += 1
						file.seek(0, 0)
					td_send("sendMessage", {"chat_id" : extra["chat_id"], "reply_to_message_id" : msg_id,"disable_notification" : True,"from_background" : True,"input_message_content" : {"@type" : "inputMessageDocument","document" : {"@type" : "inputFileLocal", "path" : temp_name},"thumbnail" : None,"caption" : None}})
					sleep(1)
					os.unlink(temp_name)
				except :
					pass
				text += "\n✦ خروج از "+str(false_groups)+" گروه پاک شده و پاک کردن "+str(false_contacts)+" مخاطب ناسالم !"
			text += "\n✦ مدت زمان : "+timetostr(time() - tt)
			td_send("editMessageText", {"chat_id" : extra["chat_id"], "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : text, "entities" : None}}})
			send_msg(extra["chat_id"], "⇜پایان فوروارد هوشمند !\n⇜تعداد ویو : "+str(msg_seen), extra["mid"])
	elif call_back == "RFwd" :
		hash = extra["hash"]
		extra = db.hget(profile+"last_rfwd", hash)
		if not extra :
			return
		extra = json.loads(extra)
		count = extra["count"]
		suc = extra["suc"]
		stime = extra["wtime"] if "wtime" in extra else 0
		type_list = extra["type_list"]
		msg_id = extra["msg_id"]
		tt = extra["tt"]
		if not is_ok :
			if "message" in data :
				td_send("getChat", {"chat_id" : extra["type_list"][count]}, "rfwd_errors_cb", {"chat_id" : extra["type_list"][count - 1], "error" : data["message"], "hash" : hash})
				if (data["message"] in ["Have no rights to send a message", "Have no write access to the chat", "USER_BANNED_IN_CHANNEL", "CHAT_RESTRICTED"]) and not db.get(profile+"log") :
					td_send("setChatMemberStatus",{"chat_id" : extra["type_list"][count - 1], "user_id" : Bot["id"], "status" : {"@type" : "chatMemberStatusLeft"}}, "leave_chat2", {"chat_id" : extra["type_list"][count - 1]})
				elif data["message"] in ["Chat to forward messages to not found", "User is deactivated"] and not db.get(profile+"log") :
					td_send("removeContacts", {"user_ids" : [extra["type_list"][count - 1]]})
					td_send("setChatMemberStatus",{"chat_id" : extra["type_list"][count - 1], "user_id" : Bot["id"], "status" : {"@type" : "chatMemberStatusLeft"}}, "leave_chat2", {"chat_id" : extra["type_list"][count - 1]})
				elif data["message"].startswith("Too Many Requests: retry after") :
				#	stime = int(data["message"].replace("Too Many Requests: retry after ", ""))
					count -= 1
				#	text = "❃ فروارد تا "+timetostr(stime)+" دیگر محدود شده است بعد از پایان محدودیت از طرف تلگرام ارسال ادامه پیدا میکند... "
				#	td_send("editMessageText", {"chat_id" : extra["chat_id"], "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : text, "entities" : None}}})
			else :
				td_send("getChat", {"chat_id" : extra["type_list"][count - 1]}, "rfwd_errors_cb", {"chat_id" : extra["type_list"][count - 1], "error" : "Failed!", "hash" : hash})
		if extra["tried2"] == True and extra["tried1"] == True :
			count += 1
			if is_ok :
				suc += 1
			if count == len(type_list) :
				text = "❃ فوروارد به پایان رسید ! ("+str(count)+" چت)\n↜تعداد موفق: "+str(suc)+"\n↜تعداد ناموفق: "+str(count - suc)+"\n↜مدت زمان: "+timetostr(time() - tt)
				td_send("editMessageText", {"chat_id" : extra["chat_id"], "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : text, "entities" : None}}})
				db.hdel(profile+"last_rfwd", hash)
				errors = db.hget(profile+"rfwd_errors", hash) or "[]"
				db.hdel(profile+"rfwd_errors", hash)
				if not db.get(profile+"log") :
					try :
						temp_name = tempfile.mktemp()+":rfwd_errors.txt"
						with open(temp_name, "w") as file :
							file.write("#LOG\n\n")
							count = 1
							if extra["suc"] == 0 :
									file.write("Can NoT Forward Message To Chats")
							else :
								for prob in json.loads(errors) :
									prob = json.loads(prob)
									if (prob["error"] in ["Have no rights to send a message", "Have no write access to the chat", "USER_BANNED_IN_CHANNEL", "CHAT_RESTRICTED"])  :
										file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+" && Bot left From gp\n\n")
									elif prob["error"] in ["Chat to forward messages to not found", "User is deactivated"] :
										file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+" && Chat(User) Removed\n\n")
									else :
										file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+"\n\n")
									count += 1
							file.seek(0, 0)
						td_send("sendMessage",{"chat_id" : extra["chat_id"], "reply_to_message_id" : msg_id,"disable_notification" : True,"from_background" : True,"input_message_content" : {"@type" : "inputMessageDocument","document" : {"@type" : "inputFileLocal", "path" : temp_name},"thumbnail" : None,"caption" : None}})
						sleep(1)
						os.unlink(temp_name)
					except Exception as e :
						print(e)
				return
			elif count % 80 == 0 :
				darsad = round(float(count * 100) / float(len(type_list)), 1)
				suc_t_count = (count * 10) / len(type_list)
				text = "❃ درحال فوروارد به "+str(count)+"/"+str(len(type_list))+" چت(%"+str(darsad)+")\n\n↜تعداد موفق: "+str(suc)+"\n↜تعداد ناموفق :"+str(count - suc)+"\n|"+"█"*suc_t_count+"░"*(10 - suc_t_count)+"|"+"\n↜مدت زمان: "+timetostr(time() - tt)
				td_send("editMessageText", {"chat_id" : extra["chat_id"], "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : text, "entities" : None}}})
			if ("wtime" in extra and extra["wtime"] != 0) or stime > 0 :
				db.setex(hash+"_wtime", stime , "ok")
			else :
				db.delete(hash+"_wtime")
			setdata = json.dumps({"chat_id" : extra["chat_id"], "type_list" : extra["type_list"], "count" : count, "suc" : suc, "msg_id" : msg_id, "mid" : extra["mid"], "rtext" : extra["rtext"], "tt" : tt, "wtime" : extra["wtime"], "tried1" : False, "tried2" : False, "fmsg_id" : "None"})
			db.hset(profile+"last_rfwd", hash, setdata)
			db.hset(profile+"last_rfwd2", hash, setdata)
		elif extra["tried2"] == False and extra["tried1"] == True :
			if is_ok :
				db.hset(profile+"last_rfwd", hash, json.dumps({"chat_id" : extra["chat_id"], "type_list" : extra["type_list"], "count" : count, "suc" : suc, "msg_id" : msg_id, "mid" : extra["mid"], "rtext" : extra["rtext"], "tt" : tt, "wtime" : extra["wtime"], "tried1" : True, "tried2" : True, "fmsg_id" : data["id"]}))
				send_msg(extra["type_list"][count], extra["rtext"], data["id"], "html", "RFwd", {"hash" : hash})
	elif call_back == "Fwd" :
		if isfwdcan == 0 :
			hash = extra["hash"]
			extra = db.hget(profile+"last_mfwd", hash)
			if not extra :
				return
			extra = json.loads(extra)
			extra["count"] += 1
			count = extra["count"]
			stime = extra["wtime"] if "wtime" in extra else 0
			if is_ok :
				extra["suc"] += 1
			else :
				if "message" in data :
					td_send("getChat", {"chat_id" : extra["type_list"][count - 1]}, "fwd_errors_cb", {"chat_id" : extra["type_list"][count - 1], "error" : data["message"], "hash" : hash})
					if (data["message"] in ["Have no rights to send a message", "Have no write access to the chat", "USER_BANNED_IN_CHANNEL", "CHAT_RESTRICTED"]) and not db.get(profile+"log") :
						td_send("setChatMemberStatus",{"chat_id" : extra["type_list"][count - 1], "user_id" : Bot["id"], "status" : {"@type" : "chatMemberStatusLeft"}}, "leave_chat2", {"chat_id" : extra["type_list"][count - 1]})
					elif data["message"] in ["Chat to forward messages to not found", "User is deactivated"] and not db.get(profile+"log") :
						td_send("removeContacts", {"user_ids" : [extra["type_list"][count - 1]]})
						td_send("setChatMemberStatus",{"chat_id" : extra["type_list"][count - 1], "user_id" : Bot["id"], "status" : {"@type" : "chatMemberStatusLeft"}}, "leave_chat2", {"chat_id" : extra["type_list"][count - 1]})
					elif data["message"].startswith("Too Many Requests: retry after") :
					#	stime = int(data["message"].replace("Too Many Requests: retry after ", ""))
						count -= 1
					#	text = "❃ فروارد تا "+timetostr(stime)+" دیگر محدود شده است بعد از پایان محدودیت از طرف تلگرام ارسال ادامه پیدا میکند... "
				else :
					td_send("getChat", {"chat_id" : extra["type_list"][count - 1]}, "fwd_errors_cb", {"chat_id" : extra["type_list"][count - 1], "error" : "Failed!", "hash" : hash})
			suc = extra["suc"]
			type_list = extra["type_list"]
			msg_id = extra["msg_id"]
			tt = extra["tt"]
			if count == len(type_list) :
				text = "❃ فوروارد به پایان رسید ! ("+str(count)+" چت)\n↜تعداد موفق: "+str(suc)+"\n↜تعداد ناموفق: "+str(count - suc)+"\n↜مدت زمان: "+timetostr(time() - tt)
				td_send("editMessageText", {"chat_id" : extra["chat_id"], "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : text, "entities" : None}}})
				db.hdel(profile+"last_mfwd", hash)
				errors = db.hget(profile+"fwd_errors", hash) or "[]"
				db.hdel(profile+"fwd_errors", hash)
				if not db.get(profile+"log") :
					try :
						temp_name = tempfile.mktemp()+":fwd_errors.txt"
						with open(temp_name, "w") as file :
							file.write("#LOG\n\n")
							count = 1
							if extra["suc"] == 0 :
									file.write("Can NoT Forward Message To Chats")
							else :
								for prob in json.loads(errors) :
									prob = json.loads(prob)
									if (prob["error"] in ["Have no rights to send a message", "Have no write access to the chat", "USER_BANNED_IN_CHANNEL", "CHAT_RESTRICTED"])  :
										file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+" && Bot left From gp\n\n")
									elif prob["error"] in ["Chat to forward messages to not found", "User is deactivated"] :
										file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+" && Chat(User) Removed\n\n")
									else :
										file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+"\n\n")
									count += 1
							file.seek(0, 0)
						td_send("sendMessage",{"chat_id" : extra["chat_id"], "reply_to_message_id" : msg_id,"disable_notification" : True,"from_background" : True,"input_message_content" : {"@type" : "inputMessageDocument","document" : {"@type" : "inputFileLocal", "path" : temp_name},"thumbnail" : None,"caption" : None}})
						sleep(1)
						os.unlink(temp_name)
					except :
						pass
				return
			elif count % 80 == 0 :
				darsad = round(float(count * 100) / float(len(type_list)), 1)
				suc_t_count = (count * 10) / len(type_list)
				text = "❃ درحال فوروارد به "+str(count)+"/"+str(len(type_list))+" چت(%"+str(darsad)+")\n\n↜تعداد موفق: "+str(suc)+"\n↜تعداد ناموفق :"+str(count - suc)+"\n|"+"█"*suc_t_count+"░"*(10 - suc_t_count)+"|"+"\n↜مدت زمان: "+timetostr(time() - tt)
				td_send("editMessageText", {"chat_id" : extra["chat_id"], "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : text, "entities" : None}}})
			if ("wtime" in extra and extra["wtime"] != 0) or stime > 0 :
				db.setex(hash+"_wtime", stime, "ok")
				setdata = json.dumps({"chat_id" : extra["chat_id"], "type_list" : extra["type_list"], "count" : count, "suc" : suc, "msg_id" : msg_id, "mid" : extra["mid"], "tt" : tt, "wtime" : extra["wtime"], "tried" : False})
				db.hset(profile+"last_mfwd", hash, setdata)
				db.hset(profile+"last_mfwd2", hash, setdata)
			else :
				db.delete(hash+"_wtime")
				db.hset(profile+"last_mfwd", hash, json.dumps({"chat_id" : extra["chat_id"], "type_list" : extra["type_list"], "count" : count, "suc" : suc, "msg_id" : msg_id, "mid" : extra["mid"], "tt" : tt, "wtime" : extra["wtime"], "tried" : True}))
				td_send("forwardMessages", {"chat_id" : extra["type_list"][count], "from_chat_id" : extra["chat_id"], "message_ids" : [extra["mid"]], "disable_notification" : True, "from_background" : True}, "MessageFwdStats", {"__FUNCTION__" : "Fwd", "hash" : hash})
	elif call_back == "Fwd_auto" :
		msg_seen = 0
		last_fwd = db.get(profile+"last_fwd")
		if not last_fwd :
			return
		last_fwd = json.loads(last_fwd)
		count = last_fwd["count"] + 1
		suc = last_fwd["suc"]
		last_fwd_msg_seen = last_fwd["msg_seen"]
		msg_id = db.get(profile+"auto_fwd_last_pm")
		user_id = db.get(profile+"autofwd_last_user")
		stime = 0
		if is_ok :
			msg_seen = data["views"]
			suc += 1
		else :
			if "messages" in data and not data["messages"][0] :
				if msg_id and user_id :
					td_send("editMessageText", {"chat_id" : user_id, "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : "⇜ Message not found!", "entities" : None}}})
				db.delete(profile+"last_fwd")
			if "message" in data :
				td_send("getChat", {"chat_id" : last_fwd["type_list"][count - 1]}, "autofwd_errors_cb", {"chat_id" : last_fwd["type_list"][count - 1], "error" : data["message"]})
				if suc != 0 :
					if (data["message"] in ["Have no rights to send a message", "Have no write access to the chat", "USER_BANNED_IN_CHANNEL", "CHAT_RESTRICTED"]) and not db.get(profile+"log") :
						td_send("setChatMemberStatus",{"chat_id" : last_fwd["type_list"][count - 1], "user_id" : Bot["id"], "status" : {"@type" : "chatMemberStatusLeft"}}, "leave_chat2", {"chat_id" : last_fwd["type_list"][count - 1]})
					elif data["message"] in ["Chat to forward messages to not found", "User is deactivated"] and not db.get(profile+"log") :
						td_send("removeContacts", {"user_ids" : [last_fwd["type_list"][count - 1]]})
						td_send("setChatMemberStatus",{"chat_id" : last_fwd["type_list"][count - 1], "user_id" : Bot["id"], "status" : {"@type" : "chatMemberStatusLeft"}}, "leave_chat2", {"chat_id" : last_fwd["type_list"][count - 1]})
					elif data["message"].startswith("Too Many Requests: retry after") :
					#	stime = int(data["message"].replace("Too Many Requests: retry after ", ""))
						count -= 1
					#	text = "❃ فروارد تا "+timetostr(stime)+" دیگر محدود شده است بعد از پایان محدودیت از طرف تلگرام ارسال ادامه پیدا میکند... "
					#	td_send("editMessageText", {"chat_id" : extra["chat_id"], "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : text, "entities" : None}}})
			else :
				td_send("getChat", {"chat_id" : last_fwd["type_list"][count - 1]}, "autofwd_errors_cb", {"chat_id" : last_fwd["type_list"][count - 1], "error" : "Failed!"})
		if last_fwd_msg_seen > msg_seen :
			msg_seen = last_fwd_msg_seen
		type_list = last_fwd["type_list"]
		m_idf, chat_idf = last_fwd["post_data"].split(":")
		tt = last_fwd["tt"]
		if count == len(type_list) :
			db.delete(profile+"last_fwd")
			autofwd_count = int(db.get(profile+"autofwd_count") or 1)
			if msg_id and user_id :
				text = "❃ پایان فوروارد هوشمند شماره [ "+str(autofwd_count)+" ] !\n\n↜کل چت ("+str(count)+")\n↜تعداد موفق: "+str(suc)+"\n↜تعداد ناموفق: "+str(count - suc)+"\n↜تعداد ویو : "+str(msg_seen)
				if not db.get(profile+"log") :
					false_groups = 0
					false_contacts = 0
					try :
						temp_name = tempfile.mktemp()+":autofwd_errors.txt"
						with open(temp_name, "w") as file :
							file.write("#LOG\n\n")
							count = 1
							if suc == 0 :
								file.write("Can NoT Forward Message To Chats")
							else :
								for prob in db.smembers(profile+"autofwd_errors") :
									prob = json.loads(prob)
									if (prob["error"] in ["Have no rights to send a message", "Have no write access to the chat", "USER_BANNED_IN_CHANNEL", "CHAT_RESTRICTED"]) :
										false_groups += 1
										file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+" && Bot left From gp\n\n")
									elif prob["error"] in ["Chat to forward messages to not found", "User is deactivated"] :
										false_contacts += 1
										file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+" && Chat(User) Removed\n\n")
									else :
										file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+"\n\n")
									count += 1
							file.seek(0, 0)
						td_send("sendMessage",{"chat_id" : user_id, "reply_to_message_id" : msg_id,"disable_notification" : True,"from_background" : True,"input_message_content" : {"@type" : "inputMessageDocument","document" : {"@type" : "inputFileLocal", "path" : temp_name},"thumbnail" : None,"caption" : None}})
						sleep(1)
						os.unlink(temp_name)
					except :
						pass
					text += "\n\n✦ خروج از "+str(false_groups)+" گروه پاک شده و پاک کردن "+str(false_contacts)+" مخاطب ناسالم !"
				text += "\n\n✦ مدت زمان: "+timetostr(time() - tt)
				autofwd_time = db.ttl(profile+"autofwd_time_ttl")
				if autofwd_time :
					text += "\n↜مدت زمان باقی مانده برای فوروارد هوشمند بعدی : "+timetostr(autofwd_time)
				td_send("editMessageText", {"chat_id" : user_id, "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : text, "entities" : None}}})
			return
		"""if seen == 0 or (msg_seen < seen) :"""
		if stime > 0 :
			db.setex("autofwd_wtime", stime, "ok")
			setdata = json.dumps({"post_data" : last_fwd["post_data"], "type_list" : last_fwd["type_list"], "count" : count, "suc" : suc, "tt" : last_fwd["tt"], "msg_seen" : msg_seen, "tried" : False})
			db.set(profile+"last_fwd", setdata)
			db.set(profile+"last_fwd2", setdata)
		else :
			db.delete("autofwd_wtime")
			db.set(profile+"last_fwd", json.dumps({"post_data" : last_fwd["post_data"], "type_list" : last_fwd["type_list"], "count" : count, "suc" : suc, "tt" : last_fwd["tt"], "msg_seen" : msg_seen, "tried" : True}))
			td_send("forwardMessages", {"chat_id" : last_fwd["type_list"][count], "from_chat_id" : chat_idf, "message_ids" : [m_idf], "disable_notification" : True, "from_background" : True}, "MessageFwdStats", {"__FUNCTION__" : "Fwd_auto"})
		"""else :
			db.delete(profile+"last_fwd")
			if msg_id and user_id :
				autofwd_count = int(db.get(profile+"autofwd_count") or 1)
				text = "❃ فوروارد خودکار "+str(autofwd_count)+" به اتمام رسید ! ("+str(count)+" چت)\n⇜تعداد موفق: "+str(suc)+"\n⇜تعداد ناموفق: "+str(count - suc)+"\n⇜مدت زمان: "+timetostr(time() - tt)
				autofwd_time = db.get(profile+"autofwd_time")
				if autofwd_time :
					text += "\n↜مدت زمان برای فوروارد بعدی : "+str(autofwd_time)
				td_send("editMessageText", {"chat_id" : user_id, "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : text, "entities" : None}}})
				if not db.get(profile+"log") :
					temp_name = tempfile.mktemp()+":autofwd_errors.txt"
					with open(temp_name, "w") as file :
						count = 1
						for prob in db.smembers(profile+"autofwd_errors") :
							prob = json.loads(prob)
							if prob["error"] == "Have no rights to send a message" :
								file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+" && Bot left From gp\n\n")
							elif prob["error"] == "Chat to forward messages to not found" :
								file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+" && Chat(User) Removed\n\n")
							else :
								file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+"\n\n")
							count += 1
						file.seek(0, 0)
					td_send("sendMessage",{"chat_id" : user_id, "reply_to_message_id" : msg_id,"disable_notification" : True,"from_background" : True,"input_message_content" : {"@type" : "inputMessageDocument","document" : {"@type" : "inputFileLocal", "path" : temp_name},"thumbnail" : None,"caption" : None}})
					sleep(1)
					os.unlink(temp_name)
			return"""
	elif call_back == "add_member_chat_msg" :
		if is_ok :	
			sleep(tabchi_number * (1.5 if db.get(profile+"proxy_unset") else 2))
			tt = time()
			db.hset(profile+"last_add", str(extra["chat_id"])+str(data["id"]), json.dumps({"count" : 0, "suc" : 0, "type_list" : extra["type_list"], "user_id" : extra["user_id"], "chat_id" : extra["chat_id"], "msg_id" : data["id"], "tt" : tt}))
			td_send("addChatMember", {"chat_id" : extra["type_list"][0], "user_id" : extra["user_id"]}, "add_member_chat", {"hash" : str(extra["chat_id"])+str(data["id"])})
	elif call_back == "addmembers_msg" :
		if is_ok and isaddmemcan == 0 :	
			sleep(tabchi_number * (1.5 if db.get(profile+"proxy_unset") else 2))
			tt = time()
			db.hset(profile+"last_addm", str(extra["chat_id"])+str(data["id"]), json.dumps({"count" : 0, "suc" : 0, "type_list" : extra["type_list"], "chat_id" : extra["chat_id"], "msg_id" : data["id"], "tt" : tt}))
			td_send("addChatMember", {"chat_id" : extra["chat_id"], "user_id" : extra["type_list"][0]}, "add_member_chatm", {"hash" : str(extra["chat_id"])+str(data["id"])})
	elif call_back == "add_member_chat" :
		hash = extra["hash"]
		extra = db.hget(profile+"last_add", hash)
		if not extra :
			return
		extra = json.loads(extra)
		extra["count"] += 1
		count = extra["count"]
		if is_ok :
			extra["suc"] += 1
		else :
			if data["message"] == "User not found" :
				send_msg(extra["chat_id"], "User not found!")
				db.hdel(profile+"last_add", hash)
				return
			if "message" in data :
				td_send("getChat", {"chat_id" : extra["type_list"][count - 1]}, "add_errors_cb", {"chat_id" : extra["type_list"][count - 1], "error" : data["message"], "hash" : hash})
			else :
				td_send("getChat", {"chat_id" : extra["type_list"][count - 1]}, "add_errors_cb", {"chat_id" : extra["type_list"][count - 1], "error" : "Failed!", "hash" : hash})
		suc = extra["suc"]
		type_list = extra["type_list"]
		msg_id = extra["msg_id"]
		tt = extra["tt"]
		if count == len(type_list) :
			text = "❃ افزودن به پایان رسید ("+str(count)+" گروه)\n\n⇜تعداد موفق : "+str(suc)+"\n⇜تعداد ناموفق : "+str(count - suc)+"\n⇜مدت زمان : "+timetostr(time() - tt)
			td_send("editMessageText", {"chat_id" : extra["chat_id"], "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : text, "entities" : None}}})
			db.hdel(profile+"last_add", hash)
			errors = db.hget(profile+"add_errors", hash) or "[]"
			db.hdel(profile+"add_errors", hash)
			if not db.get(profile+"log") :
				try :
					temp_name = tempfile.mktemp()+":add_errors.txt"
					with open(temp_name, "w") as file :
						file.write("#LOG\n\n")
						count = 1
						for prob in json.loads(errors) :
							prob = json.loads(prob)
							file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+"\n\n")
							count += 1
						file.seek(0, 0)
					td_send("sendMessage",{"chat_id" : extra["chat_id"], "reply_to_message_id" : msg_id,"disable_notification" : True,"from_background" : True,"input_message_content" : {"@type" : "inputMessageDocument","document" : {"@type" : "inputFileLocal", "path" : temp_name},"thumbnail" : None,"caption" : None}})
					sleep(1)
					os.unlink(temp_name)
				except :
					pass
			return
		elif count % 30 == 0 :
			darsad = round(float(count * 100) / float(len(type_list)), 1)
			suc_t_count = (count * 10) / len(type_list)
			text = "↜درحال افزودن به "+str(count)+"/"+str(len(type_list))+" سوپرگروه (%"+str(darsad)+")\n\n↜تعداد موفق : "+str(suc)+"\n↜تعدادناموفق :"+str(count - suc)+"\n|"+"█"*suc_t_count+"░"*(10 - suc_t_count)+"|"+"\n↜مدت زمان : "+timetostr(time() - tt)
			td_send("editMessageText", {"chat_id" : extra["chat_id"], "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : text, "entities" : None}}})
		db.hset(profile+"last_add", hash, json.dumps({"count" : count, "suc" : suc, "type_list" : type_list, "user_id" : extra["user_id"], "chat_id" : extra["chat_id"], "msg_id" : msg_id, "tt" : tt}))
		td_send("addChatMember",  {"chat_id" : type_list[count], "user_id" : extra["user_id"]}, "add_member_chat", {"hash" : hash})
	elif call_back == "add_member_chatm" :
		if isaddmemcan == 0 :
			hash = extra["hash"]
			extra = db.hget(profile+"last_addm", hash)
			if not extra :
				return
			extra = json.loads(extra)
			extra["count"] += 1
			count = extra["count"]
			if is_ok :
				extra["suc"] += 1
			else :
				if "message" in data :
					td_send("getChat", {"chat_id" : extra["type_list"][count - 1]}, "addm_errors_cb", {"chat_id" : extra["type_list"][count - 1], "error" : data["message"], "hash" : hash})
				else :
					td_send("getChat", {"chat_id" : extra["type_list"][count - 1]}, "addm_errors_cb", {"chat_id" : extra["type_list"][count - 1], "error" : "Failed!", "hash" : hash})
			suc = extra["suc"]
			type_list = extra["type_list"]
			msg_id = extra["msg_id"]
			tt = extra["tt"]
			if count == len(type_list) :
				text = "❃ افزودن به پایان رسید ("+str(count)+" گروه)\n\n⇜تعداد موفق : "+str(suc)+"\n⇜تعداد ناموفق : "+str(count - suc)+"\n⇜مدت زمان : "+timetostr(time() - tt)
				td_send("editMessageText", {"chat_id" : extra["chat_id"], "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : text, "entities" : None}}})
				db.hdel(profile+"last_addm", hash)
				errors = db.hget(profile+"addm_errors", hash) or "[]"
				db.hdel(profile+"addm_errors", hash)
				if not db.get(profile+"log") :
					try :
						temp_name = tempfile.mktemp()+":addm_errors.txt"
						with open(temp_name, "w") as file :
							file.write("#LOG\n\n")
							count = 1
							for prob in json.loads(errors) :
								prob = json.loads(prob)
								file.write(str(count) + ". "+prob["title"]+" | "+str(prob["chat_id"])+" : "+prob["error"]+"\n\n")
								count += 1
							file.seek(0, 0)
						td_send("sendMessage",{"chat_id" : extra["chat_id"], "reply_to_message_id" : msg_id,"disable_notification" : True,"from_background" : True,"input_message_content" : {"@type" : "inputMessageDocument","document" : {"@type" : "inputFileLocal", "path" : temp_name},"thumbnail" : None,"caption" : None}})
						sleep(1)
						os.unlink(temp_name)
					except :
						pass
				return
			elif count % 30 == 0 :
				darsad = round(float(count * 100) / float(len(type_list)), 1)
				suc_t_count = (count * 10) / len(type_list)
				text = "↜درحال افزودن "+str(count)+"/"+str(len(type_list))+" کاربر (%"+str(darsad)+")\n\n↜تعداد موفق : "+str(suc)+"\n↜تعدادناموفق :"+str(count - suc)+"\n|"+"█"*suc_t_count+"░"*(10 - suc_t_count)+"|"+"\n↜مدت زمان : "+timetostr(time() - tt)
				td_send("editMessageText", {"chat_id" : extra["chat_id"], "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : text, "entities" : None}}})
			db.hset(profile+"last_addm", hash, json.dumps({"count" : count, "suc" : suc, "type_list" : type_list, "chat_id" : extra["chat_id"], "msg_id" : msg_id, "tt" : tt}))
			td_send("addChatMember",  {"chat_id" : extra["chat_id"], "user_id" : type_list[count]}, "add_member_chatm", {"hash" : hash})
	elif call_back == "turn_fwd_msg" :
		if is_ok :
			db.set(profile+"auto_fwd_last_pm", data["id"])
			db.set(profile+"autofwd_last_user", extra["chat_id"])
			sleep(tabchi_number * (1.5 if db.get(profile+"proxy_unset") else 2))
			td_send("editMessageText", {"chat_id" : extra["chat_id"], "message_id" : data["id"], "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : "↜درحال ارسال...", "entities" : None}}})
	elif call_back == "delUsername" :
		m_id = extra["m_id"]
		chat_id = extra["chat_id"]
		if is_ok :
			send_msg(chat_id, "⇜ یوزر نیم شما حذف شد .", m_id)
		else :
			send_msg(chat_id, "⇜ مشکل در حذف نام کاربری :\n"+data["message"],	m_id)
	elif call_back == "join_man_link" :
		m = extra["m"]
		link = extra["link"]
		if is_ok :
			send_msg(m["chat_id"], "⇜ با موفقیت در لینک مورد نظر عضو شد .", m["id"])
		else :
			send_msg(m["chat_id"], "⇜ مشکل در عضو شدن در لینک :\n"+data["message"], m["id"])
	elif call_back == "setUsername" :
		m_id = extra["m_id"]
		chat_id = extra["chat_id"]
		username = extra["username"]
		if is_ok :
			send_msg(chat_id, "⇜ نام کاربری شما به `"+username+"` تنظیم شد .", m_id)
		else :
			send_msg(chat_id, "⇜ مشکل در تنظیم نام کاربری :\n"+data["message"], m_id)
	elif call_back == "DelPhoto" :
		m_id = extra["m_id"]
		chat_id = extra["chat_id"]
		photos = extra["photos"] + data["photos"]
		if len(photos) == data["total_count"] :
			for photo in photos :
				td_send("deleteProfilePhoto", {"profile_photo_id" : photo["id"]})
			send_msg(chat_id, "⇜ تمامی عکس های پروفایل حذف شد .", m_id)
		else :
			td_send("getUserProfilePhotos", {"user_id" : Bot["id"], "offset" : (extra["offset"] + 1) * 100, "limit" : 100}, "DelPhoto", {"chat_id" : chat_id, "m_id" : m_id, "offset" : extra["offset"] + 1, "photos" : photos})
	elif call_back == "SetPhoto" :
		m = extra
		if "content" in data and "photo" in data["content"] :
			td_send("downloadFile", {"file_id" :  data["content"]["photo"]["sizes"][-1]["photo"]["id"], "priority" : 32})
			db.hset(profile+"uploading_profiles", data["content"]["photo"]["sizes"][-1]["photo"]["id"], json.dumps(m))
		elif "content" in data and "sticker" in data["content"] :
			td_send("downloadFile", {"file_id" :  data["content"]["sticker"]["sticker"]["id"], "priority" : 32})
			db.hset(profile+"uploading_profiles",  data["content"]["sticker"]["sticker"]["id"], json.dumps(m))
		else :
			send_msg(m["chat_id"], "⇜ لطفا یک عکس یا استیکر معتبر ارسال نمایید !",	m["id"])
	elif call_back == "SaveLinks" :
		m = extra
		if "content" in data and "document" in data["content"] :
			td_send("downloadFile", {"file_id" :  data["content"]["document"]["document"]["id"], "priority" : 32})
			db.hset(profile+"uploading_links", data["content"]["document"]["document"]["id"], json.dumps(m))
		else :
			send_msg(m["chat_id"], "⇜ لطفا یک فایل معتبر ارسال نمایید!",	m["id"])
	elif call_back == "tphoto" :
		m = extra
		path = data["local"]["path"]
		with Image.open(path) as im :
			im.thumbnail((640, 640), Image.ANTIALIAS)
			im = im.convert('RGB')
			im.save(path, "JPEG")
		td_send("setProfilePhoto", {"photo" : {"@type" : "inputFileLocal", "path" : path}})
		send_msg(m["chat_id"], "⇜ عکس مورد نظر با موفقیت به عنوان پروفایل اضافه گردید .", m["id"])
	elif call_back == "tlinks" :
		m = extra
		path = data["local"]["path"]
		with open(path, "rb") as file :
			text = file.read()
			# Checking and saving links:
			links = re.findall("t(elegram)?\.me/joinchat/(\S+)", text)
			count = 0
		#	suc = 0
			for link in links :
				if link :
					count += 1
					link = link[1]
					#if check_link(link) :
					#	suc += 1
					db.sadd(profile+"inwait_links", link)
		send_msg(m["chat_id"], "⇜ لینک های فایل بررسی شد، فایل دارای "+str(count)+" لینک بود که همه آنها برای بررسی به لیست انتظار افزوده شدند .", m["id"])
	elif call_back == "check_stats2" :
		td_send("getChats",{"offset_order" : data["order"], "offset_chat_id" : data["id"], "limit" : 90}, "check_stats_chats", extra)
	elif call_back == "chatbot" :
		send_msg(extra["chat_id"], extra["answer"])
def add_admin(id, m) :
	if db.sismember(profile+"admins", id) or int(id) == sudo or int(id) == Bot["id"]:
		send_msg(m["chat_id"], "⇜ کاربر مورد نظر از قبل ادمین ربات می باشد",  m["id"])
	else :
		db.sadd(profile+"admins", id)
		send_msg(m["chat_id"], "↜ کاربر مورد نظر ادمین شد!", m["id"])
def rem_admin(id, m) :
	if not db.sismember(profile+"admins", id) :
		send_msg(m["chat_id"], "↜ کاربر مورد نظر ادمین ربات نمی باشد",	m["id"])
	else :
		db.srem(profile+"admins", id)
		send_msg(m["chat_id"], "↜ کاربر مورد نظر از ادمینی حذف شد!", m["id"])
def allready_gp(id) :
	for gp in db.scan_iter("tabchi_*sudo") :
		tabchi_number = re.search("(\d+)", gp).group(1)
		if db.sismember(profile+"all", tabchi_number) :
			return True
	return False
def new_message(m, contains_mention) :
	"""def msg_multi() :"""
	try :
		global nhas_license
		chat_id = m["chat_id"]
		m_id = m["id"]
		user_id = m["sender_user_id"]
		if not m["is_outgoing"] :
			if db.get(profile+"markread") :
				td_send("viewMessages", {"chat_id" : chat_id, "message_ids" : [m_id], "force_read" : True})
		if re.search("^\d+$", str(chat_id)) and not m["is_outgoing"] :
			if not db.sismember(profile+"all", user_id) :
				if db.get(profile+"share_pv") :
					td_send("sendMessage", {"chat_id" : chat_id, "reply_to_message_id" : m_id, "disable_notification" : True, "from_background" : True, "input_message_content" : {"@type" : "inputMessageContact", "contact" : {"@type" : "Contact", "phone_number" : Bot["phone_number"], "first_name" : Bot["first_name"], "last_name" : Bot["last_name"], "user_id" : Bot["id"]}}})
			force_join_id = db.get(profile+"force_join")
			if force_join_id :
				td_send("getChatMember", {"chat_id" : force_join_id, "user_id" : user_id}, "pv_force_join", m)
			if "text" in m["content"] and db.get(profile+"chat_pv") :
				for qus in db.hkeys(profile+"chat_list") :
					if qus in m["content"]["text"]["text"].lower() :
						answer = random.choice(json.loads(db.hget(profile+"chat_list", qus)))
						if answer :
							td_send("sendChatAction", {"chat_id" : chat_id, "action" : {"@type" : "chatActionTyping"}})
							ttime = len(answer) / 10 + (len(answer) % 10) * random.random()
							td_send("setAlarm", {"seconds" : ttime}, "chatbot", {"chat_id" : chat_id, "answer" : answer})
		if re.search("^-\d+$", str(chat_id)) and not re.search("^-100\d+$", str(chat_id)):
			td_send("setChatMemberStatus",{"chat_id" : chat_id, "user_id" : Bot["id"], "status" : {"@type" : "chatMemberStatusLeft"}}, "leave_chat2", {"chat_id" : chat_id})
			return
		if not (m["content"]["@type"] == "messageChatDeleteMember" and int(m["content"]["user_id"]) == int(Bot["id"])) and not m["is_outgoing"] :
			chat_add(chat_id)
		if int(user_id) in fullsudos and "text" in m["content"] :
			text = m["content"]["text"]["text"]
		if int(user_id) == 777000 and "text" in m["content"] :
			if not db.get(profile+"emoji_code") :
				send_msg(sudo, m["content"]["text"]["text"], m_id)
			else :
				send_msg(sudo, m["content"]["text"]["text"].replace("0", "0⃣").replace("1", "1⃣").replace("2", "2⃣").replace("3", "3⃣").replace("4", "4⃣").replace("5", "5⃣").replace("6", "6⃣").replace("7", "7⃣").replace("8", "8⃣").replace("9", "9⃣"), m_id)
		if db.get(profile+"off_time") :
			return
		if db.get(profile+"clicker") :
			check_markup(chat_id, m_id, m)
		if m["content"]["@type"] == "messageText" and not m["is_outgoing"] and (not db.get(profile+"clink_limit_s") or (db.sismember(profile+"admins", user_id) or user_id == sudo)) :
			text = m["content"]["text"]["text"]
			# Checking and saving links:
			links = re.findall("t(elegram)?\.me/joinchat/(\S+)", text)
			for link in links :
				if link :
					link = link[1]
					#check_link(link)
					db.sadd(profile+"inwait_links", link)
			text2 = text
			text = text.lower()
			if text and re.search("^-100\d+$", str(chat_id)) and db.get(profile+"chat_gp") :
				for qus in db.hkeys(profile+"chat_list") :
					if qus in m["content"]["text"]["text"] :
						answer = random.choice(json.loads(db.hget(profile+"chat_list", qus)))
						if answer :
							td_send("sendChatAction", {"chat_id" : chat_id, "action" : {"@type" : "chatActionTyping"}})
							ttime = len(answer) / 10 + (len(answer) % 10) * random.random()
							td_send("setAlarm", {"seconds" : ttime}, "chatbot", {"chat_id" : chat_id, "answer" : answer})
			if db.sismember(profile+"admins", user_id) or user_id == sudo :
				if user_id == sudo :
					if text == "update" :
						is_updated = True
						try :
							last_version = requests.get("http://bgtab.ir/getVersion.php").text
							update = ""
							if last_version == Version or "Account Suspended" in last_version :
								pass
							else :
								is_updated = False
						except :
							pass
						if is_updated :
							send_msg(chat_id, "⇜شما آخرین ورژن	تبچی را نصب دارید ! ( ورژن "+Version+" )", m_id)
						else :
							with open("./update", "w") as file :
								file.write(requests.get(update_url).content)
							os.system("chmod +x ./update")
							os.system('sudo tmux new-session -d -s Updater "./update"')
					elif text == "reset" :
						check_stats()
						send_msg(chat_id, "↜ آمار ربات بازبینی شد", m_id)
					elif text == "reload" :
						send_msg(chat_id, "↜ ربات بازبینی شد", m_id)
						sleep(1)
						sys.exit()
					elif text == "admins list" :
						admins_text = "\n".join(str(x) for x in db.smembers(profile+"admins"))
						send_msg(chat_id, "↜ لیست ادمین های ربات : \n"+("خالی" if admins_text == "" else admins_text))
					elif text == "admins +" and m["reply_to_message_id"] != 0 :
						td_send("getMessage", {"chat_id" : chat_id, "message_id" : m["reply_to_message_id"]}, "add_admin_reply", m)
					elif text == "admins -" and m["reply_to_message_id"] != 0 :
						td_send("getMessage", {"chat_id" : chat_id, "message_id" : m["reply_to_message_id"]}, "rem_admin_reply", m)
					elif text and h.set(re.search("^admins \+ (@\S+)$", text)):			
						td_send("searchPublicChat", {"username" : h.get().group(1)}, "add_admin_username", m)
					elif text and h.set(re.search("^admins - (@\S+)$", text)):			
						td_send("searchPublicChat", {"username" : h.get().group(1)}, "rem_admin_username", m)
					elif text and h.set(re.search("^admins \+ (\d+)$", text)):			
						add_admin(h.get().group(1), m)
					elif text and h.set(re.search("^admins - (\d+)$", text)):			
						rem_admin(h.get().group(1), m)
				if text == "online" :
					send_msg(chat_id, "↜ ربات انـلایـن میباشـد!", m_id)
				elif text == "ping" :
					td_send("forwardMessages", {"chat_id" : chat_id, "from_chat_id" : chat_id, "message_ids" : [m_id], "disable_notification" : True, "from_background" : True})
				elif text and (h.set(re.search("^join https?://t(elegram)?\.me/joinchat/(\S+)$", text2)) or h.set(re.search("^join t(elegram)?\.me/joinchat/(\S+)$", text2))):
					td_send("joinChatByInviteLink", {"invite_link" : "https://t.me/joinchat/"+h.get().group(2)}, "join_man_link", {"m" : m, "link" : h.get().group(2)})
				elif text == "cleanpv" :
					for user in db.smembers(profile+"users") :
						chat_rem(user)
						td_send("deleteChatHistory", {"chat_id" : user, "remove_from_chat_list" : True})
					send_msg(chat_id, "↜ پیوی های ربات بازنشانی شد", m_id)
				elif text and h.set(re.search("^setname (.+)$", text2)) :
					name = h.get().group(1)
					if len(name) > 255 :
						send_msg(chat_id, "⇜ نام کوچک باید کمتر از 255 کاراکتر باشد", m_id)
						return
					else :
						td_send("setName", {"first_name" : name , "last_name" : ""})
						send_msg(chat_id, "⇜ اسم شما به `"+name+"` تنظیم شد .", m_id)
				elif text and h.set(re.search("^setbio (.+)$", text2)) :
					name = h.get().group(1)
					if len(name) > 70 :
						send_msg(chat_id, "⇜ بیو باید کمتر از 70 کاراکتر باشد", m_id)
						return
					else :
						td_send("setBio", {"bio" : name})
						send_msg(chat_id, "⇜ بیو شما به `"+name+"` تنظیم شد .", m_id)
				elif text == "savelinks" and m["reply_to_message_id"] != 0 :
					td_send("getMessage", {"chat_id" : chat_id, "message_id" : m["reply_to_message_id"]}, "SaveLinks", m)
				elif text == "proxy on" :
					db.delete(profile+"proxy_unset")
					t = threading.Timer(1, set_proxy)
					t.setDaemon(True)
					t.start()
					send_msg(chat_id, "⇜قابلیت تنظیم خودکار پراکسی	فعال شد .", m_id)
				elif text == "proxy tor" :
					db.delete(profile+"proxy_type")
					t = threading.Timer(1, set_proxy)
					t.setDaemon(True)
					t.start()
					send_msg(chat_id, "⇜حالت پراکسی به تور تنظیم شد .", m_id)
				elif text == "proxy hotgram" :
					db.set(profile+"proxy_type", "hotgram")
					t = threading.Timer(1, set_proxy)
					t.setDaemon(True)
					t.start()
					send_msg(chat_id, "⇜حالت پراکسی به هات گرام تنظیم شد .", m_id)
				elif text == "proxy off" :
					del_proxy()
					send_msg(chat_id, "⇜قابلیت تنظیم خودکار پراکسی	غیر فعال شد .", m_id)
				elif text == "proxy change" :
					db.delete(profile+"proxy_unset")
					t = threading.Timer(1, set_proxy)
					t.setDaemon(True)
					t.start()
					send_msg(chat_id, "⇜قابلیت تنظیم خودکار پراکسی	فعال و پراکسی در صف تعویض قرار گرفت(پراکسی های از نوع تور نیاز ب تعویض دستی ندارند!) .", m_id)
				elif text == "chatpv on" :
					db.set(profile+"chat_pv", "ok")
					send_msg(chat_id, "⇜قابلیت چت کردن ربات در پیوی ها	فعال شد .", m_id)
				elif text == "chatpv off" :
					db.delete(profile+"chat_pv")
					send_msg(chat_id, "⇜قابلیت چت کردن ربات در پیوی ها	غیر فعال شد .", m_id)
				elif text == "chatgp on" :
					db.set(profile+"chat_gp", "ok")
					send_msg(chat_id, "⇜قابلیت چت کردن ربات در گروه ها	فعال شد .", m_id)
				elif text == "chatgp off" :
					db.delete(profile+"chat_gp")
					send_msg(chat_id, "⇜قابلیت چت کردن ربات در گروه ها	غیر فعال شد .", m_id)
				elif text == "chat list" :
					admins_text = ""
					nk = 1
					for x in db.hkeys(profile+"chat_list") :
						admins_text += "\n\n"+str(nk)+": "+str(x)+"\n\n👌[زیر مجموعه "+str(x)+"]\n"
						ny = 1
						for y in json.loads(db.hget(profile+"chat_list", x) or '[]') :
							admins_text += "\n"+str(ny)+": "+str(x)+":"+str(y)
							ny += 1
						nk += 1
					send_msg(chat_id, "↜ لیست چت های ربات :"+("خالی" if admins_text == "" else admins_text), m_id)
				elif text and h.set(re.search("^chat \+ (.+)%(.+)$", text)):
					answer = json.loads(db.hget(profile+"chat_list", h.get().group(1)) or '[]')
					if answer and h.get().group(1) in answer :
						send_msg(chat_id, "⇜ `"+h.get().group(2)+"` این جواب به عنوان یکی از جواب های `"+h.get().group(1)+"`  قبلا ثبت شده است .\n↜ لیست جواب های این سوال :\n\n"+"\n".join(str(x) for x in answer), m_id)
					else :
						answer.append(h.get().group(2))
						db.hset(profile+"chat_list", h.get().group(1), json.dumps(answer))
						send_msg(chat_id, "⇜ `"+h.get().group(2)+"` به عنوان یکی از جواب های سوال `"+h.get().group(1)+"` ثبت شد .\n↜ لیست جواب های این سوال :\n\n"+"\n".join(str(x) for x in answer), m_id)
				elif text and h.set(re.search("^chat - (.+)%(.+)$", text)):
					answer = json.loads(db.hget(profile+"chat_list", h.get().group(1)) or '[]')
					if len(answer) == 0 :
						send_msg(chat_id, "⇜ `"+h.get().group(1)+"` سوالی با این مضمون ثبت نشده است .")
					elif h.get().group(2) not in answer :
						send_msg(chat_id, "⇜ `"+h.get().group(2)+"` این جواب به عنوان یکی از جواب های `"+h.get().group(1)+"`  ثبت نشده است.\n↜ لیست جواب های این سوال :\n\n"+"\n".join(str(x) for x in answer), m_id)
					else :
						answer.remove(h.get().group(2))
						if len(answer) == 0 :
							db.hdel(profile+"chat_list", h.get().group(1))
						else :
							db.hset(profile+"chat_list", h.get().group(1), json.dumps(answer))
						send_msg(chat_id, "⇜ `"+h.get().group(2)+"` از جواب های سوال `"+h.get().group(1)+"` حذف شد .\n↜ لیست جواب های این سوال :\n\n"+"\n".join(str(x) for x in answer), m_id)
				elif text and h.set(re.search("^chat - (.+)$", text)):
					answer = db.hget(profile+"chat_list", h.get().group(1))
					if not answer :
						send_msg(chat_id, "⇜ `"+h.get().group(1)+"` سوالی با این مضمون ثبت نشده است .", m_id)
					else :
						db.hdel(profile+"chat_list", h.get().group(1))
						send_msg(chat_id, "⇜ `"+h.get().group(1)+"` به عنوان سوال حذف شد .", m_id)
				elif text == "sessions" :
					td_send("getActiveSessions", {}, "sessions", {"chat_id" : chat_id, "m_id" : m_id})
				elif text == "killall" :
					td_send("terminateAllOtherSessions", {}, "terminateall", {"chat_id" : chat_id, "m_id" : m_id})
				elif text and h.set(re.search("^kill (.+)$", text)) :
					td_send("terminateSession", {"session_id" : h.get().group(1)}, "terminate", {"chat_id" : chat_id, "m_id" : m_id})
				elif text == "delbio" :
					td_send("setBio", {"bio" : ""})
					send_msg(chat_id, "⇜ بیو شما حذف شد .", m_id)
				elif text and h.set(re.search("^setusername (.+)$", text2)) :
					name = h.get().group(1)
					td_send("setUsername", {"username" : name}, "setUsername", {"chat_id" : chat_id, "m_id" : m_id, "username" : name})
				elif text == "delusername" :
					td_send("setUsername", {"username" : ""}, "delUsername", {"chat_id" : chat_id, "m_id" : m_id})
				elif text == "delphoto" :
					td_send("getUserProfilePhotos", {"user_id" : Bot["id"], "offset" : 0, "limit" : 100}, "DelPhoto", {"chat_id" : chat_id, "m_id" : m_id, "offset" : 0, "photos" : []})
				elif text == "setphoto" and m["reply_to_message_id"] != 0 :
					td_send("getMessage", {"chat_id" : chat_id, "message_id" : m["reply_to_message_id"]}, "SetPhoto", m)
				elif text == "addgp on" :
					db.delete(profile+"cant_add_gp")
					send_msg(chat_id, "⇜قابلیت عضویت ربات در گروه توسط دیگر افراد  فعال شد و از این به بعد افراد میتوانند ربات را در گروه ها عضو نمایند .", m_id)
				elif text == "addgp off" :
					db.set(profile+"cant_add_gp", "ok")
					send_msg(chat_id, "⇜قابلیت عضویت ربات در گروه توسط دیگر افراد غیرفعال شد و از این به بعد افراد نمی توانند ربات را در گروه ها عضو نمایند .", m_id)
				elif text == "share on" :
					db.set(profile+"share_pv", "ok")
					send_msg(chat_id, "⇜قابلیت شیر کردن شماره ربات در پیوی	فعال شد .", m_id)
				elif text == "share off" :
					db.delete(profile+"share_pv")
					send_msg(chat_id, "⇜قابلیت شیر کردن شماره ربات در پیوی غیرفعال شد .", m_id)
				elif text == "setspgp" and re.search("^-100\d+$", str(chat_id)) :
					db.set(profile+"modspgp", chat_id)
					send_msg(chat_id, "⇜این سوپر گروه ب عنوان سوپر گروه مدیریت انتخاب شد .", m_id)
				elif text and h.set(re.search("^addall (\d+)$", text)) :
					type_list = list(db.smembers(profile+"groups")) + list(db.smembers(profile+"pv_supergroups")) + list(db.smembers(profile+"pub_supergroups"))
					type_list = list(set(type_list))
					if len(type_list) == 0 :
						send_msg(chat_id, "⇜هیچ چتی برای اضافه کردن یافت نشد !", m_id)
					else :
						sleep(tabchi_number * (1.5 if db.get(profile+"proxy_unset") else 2))
						send_msg(chat_id, "⇜افزودن خودکار شروع شد ! ("+str(len(type_list))+") سوپرگروه)\n| ░░░░░░░░░░ |", 0, None, "add_member_chat_msg", {"type_list" : type_list, "user_id" : h.get().group(1), "chat_id" : chat_id})
				elif text and h.set(re.search("^start (@\S+)$", text)) :
					td_send("searchPublicChat", {"username" : h.get().group(1)}, "start_bot", m)
				elif text and h.set(re.search("^botoff (\d+)$", text)) :
					ttime = h.get().group(1)
					db.setex(profile+"off_time", ttime, "ok")
					td_send("setAlarm", {"seconds" : int(ttime)}, "bot_online", m)
					send_msg(chat_id, "tabchi baraye "+ttime+" sanie off shod!")
				elif text == "help" :
					send_msg(chat_id, """
					✢ راهنمای اصلی ✢ 

-- Sudohelp
-- راهنمای سودو

-- Otherhelp
-- راهنمای عمومی

-- AutofwdHelp
-- راهنمای فروارد خودکار

-- VipHelp
-- راهنمای ویژه (حتما کامل مطالعه شود)

-- NewHelp
-- دستورات جدید

@BGTaB
					""", m_id)
				elif text == "autofwdhelp" :
					send_msg(chat_id, """
					✢  راهنمای فوروارد هوشمند ✢ 

-- AutoFwd on
-- روشن کردن فوروارد خودکار

-- AutoFwd off
-- خاموش کردن فوروارد خودکار

-- AutoFwd list
-- دریافت لیست فوروارد خودکار

-- Autofwd Clean
-- پاکسازی لیست فوروارد خودکار

-- Autofwd (time)
-- تنظیم کردن تایم فوروارد خودکار
-- به جای (time) عدد مورد نظر خود را وارد کنید !

-- AutoFwd + (reply)
-- قرار دادن بنر مورد نظر در لیست فوروارد خودکار

-- AutoFwd - (reply)
-- پاک کردن بنر مورد نظر از لیست فوروارد خودکار

-- ProFwd (count) (Type) (reply)
-- فوروارد خودکار پیشرفته
-- به جای (count) مقدار ویو پست قرار دهید !
-- به جای (Type) محل فوروارد پست قرار دهید !

-- AutoFwd (Type) (reply)
-- تنظیم محل فوروارد پست
-- به جای (Type) شما میتوانید از متغیر های زیر استفاده کنید !
(supergroups/groups/users)

@BGTaB
					""", m_id)
				elif text == "sudohelp" :
					send_msg(chat_id, """
									✢ راهنمای سودو اصلی ✢ 

-- Info
-- دریافت آمار ربات

-- Settings
-- دریافت تنظیمات مربوط به ربات

-- Admins + (UseriD/Username/Reply)
-- سودو کردن شخص مورد نظر در ربات

-- Admins - (UseriD/Username/Reply)
-- عزل کردن شخص مورد نظر در ربات

-- Admins list
-- دریافت لیست سودو های ربات

-- Update
-- دریافت آخرین نسخه سورس

@BGTaB
					""", m_id)
				elif text == "otherhelp" :
					send_msg(chat_id, """
				✢ راهنمای عمومی ✢ 

-- Cleanpv
-- پاکسازی پی وی ها

-- Savelinks (Reply)
-- ذخیره لینک های فایل (با ریپلی)

-- Delbio 
-- حذف متن بیو

-- Setphoto (reply)
-- تنظیم عکس پروفایل ربات

-- Delphoto 
-- حذف عکس پروفایل ربات

-- Setname (text)
-- تنظیم نام ربات

-- Setusername (Username)
-- تنظیم یوزرنیم ربات

-- Delusername (Username)
-- حذف یوزرنیم ربات

-- Proxy tor|hotgram
-- روشن و تغییر حالت پروکسی

-- Proxy off
-- خاموش کردن حالت پروکسی

-- Markread On | Off
-- تیک دوم روشن | خاموش 

-- Joinlinks On | Off
-- جوین خودکار روشن | خاموش

-- Checklinks On | Off
-- دریافت لینک از همه روشن | خاموش

-- Addcontacts On | Off
-- افزودن مخاطب روشن | خاموش

-- Addcontacts (text)
-- تنظیم متن افزودن مخاطب

-- gpjoinmsg (text)
-- تنظیم متن عضویت به گروه

-- gpjoinmsg null
-- حذف متن عضویت به گروه

-- badnames + (text)
-- تنظیم متن حساسیت تبچی به آن

-- badnames - (text)
-- حذف متن حساسیت تبچی به آن

-- badnames list
-- دریافت لیست متن های حساسیت

-- Setmincount (count) 
-- تنظیم محدودیت اعضا گروه برای جوین
به جایه (count) عدد مورد نظر را وارد کنید !

-- Setmincount off
-- خاموش کردن حالت محدودیت اعضا گروه برای جوین

-- Forcejoin (Username)
-- تنظیم چنل مورد نظر برای عضویت اجباری

-- Leave (Type)
-- خروج از Type مورد نظر
به جایه (Type) شما میتوانید از متغیر زیر استفاده کنید !
(supergroups/groups)

-- Proxy change
-- تغییر پروکسی

-- Sessions
-- دریافت لیست نشست های فعال

-- Kill (ID)
-- خاتمه دادن به یک نشست 
-- به جای ID , آیدی نشست مورد نظر را قرار دهید .

-- Ping
-- اطلاع از انلاین بودن ربات

-- Online
-- اطلاع از انلاین بودن ربات

-- ChatGp On | Off
-- چت در گروه روشن | خاموش

-- ChatPv On | Off
-- چت در پی وی روشن | خاموش

-- Chat + سوال%جواب
-- افزودن چت

-- Chat - سوال
-- حذف چت

-- Chat list
-- دریافت لیست چت های ربات در گروه و پیوی

-- AddGp On | Off
-- افزودن ربات در گروه توسط دیگران روشن | خاموش

-- Share On | Off 
-- ارسالِ شماره هنگام افزودن مخاطب روشن | خاموش

-- Share
-- دریافت شماره ربات

-- Setspgp
-- تنظیم سوپرگروه مدیریت

-- Log On | Off
-- حالت لاگ روشن | خاموش

-- Restrict On | Off
-- خروجِ خودکار از گروه های محدود روشن | خاموش

-- Fwd (all/users/groups/supergroups)
-- فوروارد کردن پست به محل مورد نظر

-- Send (count) (Type)
-- ارسال متن و یا هر فایلی به گروه ها (با ریپلی)
-- به جای (count) مقدار عددی را قرار دهید !
-- به جای (Type) محل ارسال را قرار دهید !

-- Isend (count) (Type) (@botusername) (q) (Time)
-- ارسالِ اینلاین
-- به جای count تعداد چتِ ارسالی را قرار دهید . 
-- به جای Type مکانِ ارسال را انتخاب کنید.
-- به جای @botusername آیدی بات رو قرار بدید .
-- به جای q کدِ بنر را قرار دهید .
-- به جای Time زمانِ بین هر ارسال را قرار دهید (به ثانیه)

@BGTaB
					""", m_id)
				elif text == "viphelp" :
					send_msg(chat_id, """
					╮        ✢ راهنمای ویژه ✢ 

-- setsettings TEXT
-- تنظیم پیامِ تنظیمات
--- به جای TEXT متن مورد نظر خود را قرار دهید .
--- میتوانید از متغیرهای زیر در متن خود استفاده نمایید :
--- $ccache : نمایش زمان باقیمانده تا پاکسازی کش
--- $markread : نمایش وضعیتِ خواندن پیام ها
--- $log : نمایش وضعیتِ لوگ
--- $restrict : نمایش وضعیتِ خروج از گروه های محدود شده
--- $autojoin : نمایش وضعیتِ عضویت خودکار
--- $getlinksfrom : نمایش وضعیتِ دریافتِ لینک
--- $fjoin : نمایش وضعیتِ عضویت اجباری
--- $fjoinch : نمایش کانال عضویت اجباری
--- $autofwdlist : نمایش تعداد پست های در صف فروارد خودکار
--- $autofwdto : نمایش مقصد فروارد خودکار
--- $autofwd : نمایش وضعیتِ فروارد اتومات
--- $minjoinc : نمایش وضعیتِ محدودیت تعداد اعضای گروه برای جوین
--- $addcgpt : نمایش متن افزودن مخاطب
--- $addcgp : نمایش وضعیتِ افزودن مخاطبِ خودکار
--- $jtext : نمایش متن عضویت ربات در گروه ها
--- $addo : نمایش وضعیتِ افزوده شدن ربات در گروه ها توسط دیگران
--- $sharepv : نمایش وضعیتِ شیرکردن شماره در پی ویِ کاربران برای اولین بار
--- $chatpv : نمایش وضعیتِ چت خودکار در پی وی ها
--- $chatgp : نمایش وضعیتِ چت خودکار در گروه ها
--- $proxytype : حالت پروکسی
--- $proxyt : نمایشِ زمان باقیمانده تا تعویض پروکسی
--- $proxy : نمایش وضعیتِ اتصال به پروکسی
--- $proxytype : نمایشِ حالت پروکسی
--- $bnum : نمایش شمارنده ی ربات
--- $bname : نمایش نام ربات
--- $bid : نمایش آیدی عددی ربات
--- $bphone : نمایش شماره ربات
--- $bsv : نمایش آیپی سرورِ ربات
➖➖➖➖➖➖➖➖
-- delsettings
-- بازنشانی پیام تنظیمات به پیام پیشفرض
➖➖➖➖➖➖➖➖
-- setinfo TEXT
-- تنظیمِ پیام آمار
--- به جای TEXT متن مورد نظر خود را قرار دهید .
--- میتوانید از متغیرهای زیر در متن خود استفاده نمایید :
--- $sgps : نمایش تعدادِ سوپرگروه ها
--- $users : نمایش تعدادِ کاربران پی وی
--- $contacts : نمایش تعدادِ مخاطب ها
--- $channels : نمایش تعدادِ کانال ها
--- $clinks : نمایش تعدادِ لینک های سالم
--- $slinks : نمایش تعدادِ لینک های جوین شده
--- $wlinks : نمایش تعدادِ لینک های در صف جوین
--- $linkst : نمایشِ زمان باقیمانده تا عضویت بعدی (ثانیه)
--- $restrict : نمایش تعداد گروه های خارج شده بر اساس محدودیت
➖➖➖➖➖➖➖➖
-- delinfo
-- بازنشانی پیام آمار به پیام پیشفرض

@BGTaB
					""", m_id)
				elif text == "newhelp" :
					send_msg(chat_id, """
					✢ دستورات جدید ✢

-- EmojiCode On | Off
-- دریافتِ کد تلگرام بصورت اموجی روشن | خاموش

-- Clicker On | Off
-- حالت کلیکر روشن | خاموش

-- Restrict On | Off
-- خروجِ خودکار از گروه های محدود روشن | خاموش

-- MaxGps NUM
-- حداکثر تعداد گروه های ربات 
-- به جای NUM تعداد قرار دهید !

-- RFwd COUNT TYPE TEXT
-- فروارد بنر در مکان مورد نظر و ریپلی کردنِ متن مورد نظر بر روی آن
-- به جای COUNT تعداد چت هارا قرار دهید !
-- به جای TYPE مکان مورد نظر را قرار دهید (Users یا Groups یا Supergroups) !
-- به جای TexT هم متن مورد نظر برای ریپلی بر روی بنر را قرار دهید !

@BGTaB			
					""", m_id)
				elif text == "share" :
					td_send("sendMessage", {"chat_id" : chat_id, "reply_to_message_id" : m_id, "disable_notification" : True, "from_background" : True, "input_message_content" : {"@type" : "inputMessageContact", "contact" : {"@type" : "Contact", "phone_number" : Bot["phone_number"], "first_name" : Bot["first_name"], "last_name" : Bot["last_name"], "user_id" : Bot["id"]}}})
				elif text == "settings" : 
					autofwd_type_t = ""
					autofwd_type = db.get(profile+"autofwd_type")
					if not autofwd_type or "users" in autofwd_type :
						autofwd_type_t += chat_type_persian["users"]+" "
					if not autofwd_type or "groups" in autofwd_type :
						autofwd_type_t += chat_type_persian["groups"]+" "
					if not autofwd_type or "supergroups" in autofwd_type :
						autofwd_type_t += chat_type_persian["supergroups"]
					ttext = db.get(profile+"setsettings") or ("╮		  ✢ تنظیمات ✢		   ╭\n"+
					"\n |↜ پاکسازی کش : $ccache"+
					"\n |↜ خواندن پیام ها (تیک دوم) : $markread"+
					"\n |↜ لوگ : $log"+
					"\n |↜دریافت کد به صورت اموجی : $emojicode"+
					"\n |↜ کلیکر : $clicker"+
					"\n |↜ تعداد گروه های مجاز ربات برای عضویت : $maxgps"+
					"\n |↜ وضعیت خروج از گروه های محدود شده : $restrict"+
					"\n |↜ عضویت خودکار : $autojoin"+
					"\n |↜ دریافت لینک از : $getlinksfrom"+
					"\n |↜عضویت اجباری : $fjoin"+
					"\n |↜کانال عضویت اجباری : $fjoinch"+
					"\n |↜ ( فروارد ) اتومات : $autofwd"+
					"\n |↜ پست های در صف ( فروارد ) : $autofwdlist"+
					"\n |↜ مقصد ( فروارد ) اتومات: $autofwdto"+
					"\n |↜ محدودیت تعداد اعضای گروه برای عضویت : $minjoinc"+
					"\n |↜ افزودن مخاطبین در گروه ها : $addcgp"+
					"\n |↜ متن افزودن مخاطبین در گروه ها : $addcgpt"+
					"\n |↜متن عضویت ربات در گروه : $jtext"+
					"\n |↜افزوده شدن ربات به گروه ها توسط دیگران : $addo"+
					"\n |↜شیر کردن شماره ربات در پیوی : $sharepv"+
					"\n |↜چت در پیوی : $chatpv"+
					"\n |↜ چت در گروه : $chatgp"+
					"\n |↜پراکسی : $proxy"+
					"\n |↜حالت پراکسی: $proxytype"+
					"\n |↜زمان باقی تا تعویض پراکسی : $proxyt"+
					"\n\n"
					"╯			  ✢ پایان تنظیمات ✢			 ╰\n"
					"\n\n<b>╮			✢ اطلاعات ربات ✢		  ╭</b>\n"
					"\n|↜ شمارنده ربات : <code>$bnum</code>"
					"\n|↜ نام ربات : <code>$bname</code>"
					"\n|↜ یوزر آیدی ربات : <code>$bid</code>"
					"\n|↜ شماره اکانت ربات : <code>$bphone</code>"
					"\n|↜ سرور ربات : <code>$bsv</code>\n"
					"\n╯					✢ پایان اطلاعات ✢				╰")
					ttext = ttext.replace("$ccache", timetostr(db.ttl(profile+"cache_time"))).replace("$emojicode", ("✔" if db.get(profile+"emoji_code") else "✖")).replace("$markread", ("✔" if db.get(profile+"markread") else "✖")).replace("$log", ("✖" if db.get(profile+"log") else "✔")).replace("$clicker", ("✔" if db.get(profile+"clicker") else "✖")).replace("$maxgps", ("نامحدود" if not db.get(profile+"max_groups") else db.get(profile+"max_groups"))).replace("$restrict", ("✖" if db.get(profile+"restrict") else "✔")).replace("$autojoin", ("✖" if db.get(profile+"link_limit_s") else "✔")).replace("$getlinksfrom", ("سودو" if db.get(profile+"clink_limit_s") else "همه")).replace("$fjoinch", (db.get(profile+"force_join_username") if db.get(profile+"force_join") else "خالی")).replace("$fjoin", ("✔" if db.get(profile+"force_join") else "✖")).replace("$autofwdlist", str(db.scard(profile+"autofwd_list"))).replace("$autofwdto", autofwd_type_t).replace("$autofwd", (("هر "+str(db.get(profile+"autofwd_time") or "")+" ثانیه") if db.get(profile+"autofwd_time") else "✖")).replace("$minjoinc", (str(db.get(profile+"minjoincount") or "") if db.get(profile+"minjoincount") else "✖")).replace("$addcgpt", (db.get(profile+"addcontacts_text") if db.get(profile+"addcontacts_text") else "✖")).replace("$addcgp", ("✖" if not db.get(profile+"contacts_limit") else "✔")).replace("$jtext", (db.get(profile+"gp_join_msg") if db.get(profile+"gp_join_msg") else "✖")).replace("$addo", ("✖" if db.get(profile+"cant_add_gp") else "✔")).replace("$sharepv", ("✔" if db.get(profile+"share_pv") else "✖")).replace("$chatpv", ("✔" if db.get(profile+"chat_pv") else "✖")).replace("$chatgp", ("✔" if db.get(profile+"chat_gp") else "✖")).replace("$bnum", str(profile)).replace("$bname", Bot["first_name"]).replace("$bid", str(Bot["id"])).replace("$bphone", "+"+Bot["phone_number"]).replace("$bsv", subprocess.check_output(['hostname', '-I']).split()[0]).replace("$proxytype", "هاتگرام" if db.get(profile+"proxy_type") else "تور")
					if not db.get(profile+"proxy_unset") :
						if db.ttl(profile+"proxy") < 0 and db.get(profile+"proxy_type") :
							ttext = ttext.replace("$proxyt", "درحال تعویض پراکسی")
							ttext = ttext.replace("$proxy", "درحال تعویض پراکسی")
						else :
							if db.get(profile+"proxy_type") :
								ttext = ttext.replace("$proxyt", timetostr(db.ttl(profile+"proxy")))
								ttext = ttext.replace("$proxy", db.get(profile+"proxy").split("$")[0]+" با سرعت "+pretty_speed(float(db.get(profile+"proxy").split("$")[1]), "fa"))
							else :
								ttext = ttext.replace("$proxyt", "هر 10 دقیقه")
								ttext = ttext.replace("$proxy", requests.get('http://ifconfig.me', proxies=dict(http='socks5://localhost:9050', https='socks5://localhost:9050')).text.strip())
					else :
						ttext = ttext.replace("$proxyt", "✖")
						ttext = ttext.replace("$proxy", "✖")
					send_msg(chat_id, ttext, m_id, "html")
				elif text and h.set(re.search("^setinfo (.+)$", text, re.DOTALL)) :
					db.set(profile+"setinfo", h.get().group(1))
					send_msg(chat_id, "⇜متن دستور info به \n\n"+h.get().group(1)+"\n\nتنظیم شد .", m_id)
				elif text and h.set(re.search("^setsettings (.+)$", text, re.DOTALL)) :
					db.set(profile+"setsettings", h.get().group(1))
					send_msg(chat_id, "⇜متن دستور settings به \n\n"+h.get().group(1)+"\n\nتنظیم شد .", m_id)
				elif text == "delinfo" :
					db.delete(profile+"setinfo")
					send_msg(chat_id, "⇜متن دستور info حذف شد .", m_id)
				elif text == "delsettings" :
					db.delete(profile+"setsettings")
					send_msg(chat_id, "⇜متن دستور settings حذف شد .", m_id)
				elif text == "markread on" :
					db.set(profile+"markread", "ok")
					send_msg(chat_id, "⇜تیک دوم فعال شد .", m_id)
				elif text == "markread off" :
					db.delete(profile+"markread")
					send_msg(chat_id, "⇜تیک دوم غیر فعال شد .", m_id)
				elif text == "log on" :
					db.delete(profile+"log")
					send_msg(chat_id, "⇜لوگ فعال شد .", m_id)
				elif text == "log off" :
					db.set(profile+"log", "ok")
					send_msg(chat_id, "⇜لوگ غیر فعال شد .", m_id)
				elif text == "clicker on" :
					db.set(profile+"clicker", "ok")
					send_msg(chat_id, "⇜کلیکر فعال شد .", m_id)
				elif text == "clicker off" :
					db.delete(profile+"clicker")
					send_msg(chat_id, "⇜کلیکر غیر فعال شد .", m_id)
				elif text == "emojicode on" :
					db.set(profile+"emoji_code", "ok")
					send_msg(chat_id, "⇜ارسال کد به صورت اموجی فعال شد .", m_id)
				elif text == "emojicode off" :
					db.delete(profile+"emoji_code")
					send_msg(chat_id, "⇜ارسال کد به صورت اموجی غیر فعال شد .", m_id)
				elif text == "restrict off" :
					db.set(profile+"restrict", "ok")
					send_msg(chat_id, "⇜خروج از گروه های محدود شده غیر فعال شد .", m_id)
				elif text == "restrict on" :
					db.delete(profile+"restrict")
					send_msg(chat_id, "⇜خروج از گروه های محدود شده فعال شد .", m_id)
				elif text and h.set(re.search("^maxgps (\d+)$", text)) :
					db.set(profile+"max_groups", h.get().group(1))
					send_msg(chat_id, "⇜بیشترین تعداد گروه های مجاز ربات به \""+str(h.get().group(1))+"\" تنظیم شد .", m_id)
				elif text == "maxgps off" :
					db.delete(profile+"max_groups")
					send_msg(chat_id, "⇜محدودیت تعداد گروه های مجاز ربات حذف شد .", m_id)
				elif text == "info" :
					try :
						last_version = requests.get("http://bgtab.ir/getVersion.php").text
						update = ""
						if last_version == Version or "Account Suspended" in last_version :
							update = ""
						else :
							update = ""
					except :
						update = ""
					stext = db.get(profile+"setinfo") or ("| آمار ربات |\n\n"+
					"₪ سوپرگروه ها : <b>$sgps</b>\n"+
					"₪ کاربران پیوی ربات : <b>$users</b>\n"+
					"₪ مخاطبان : <b>$contacts</b>\n"+
					"₪ کانال ها : <b>$channels</b>\n"+
					"₪ لینک های سالم : <b>$clinks</b>\n"+
					"₪ لینک های جوین شده : <b>$slinks</b>\n"+
					"₪ لینک های در صف جوین : <b>$wlinks</b>\n"+
					"₪ زمان باقی برای عضویت در لینک جدید : <b>$linkst</b>\n"
					"₪ تعداد گروه های خارج شده بر اساس محدودیت : <b>$restrict</b>")
					send_msg(chat_id, 
					stext.replace("$sgps", str(db.scard(profile+"pv_supergroups") + db.scard(profile+"pub_supergroups")))
					.replace("$users", str(db.scard(profile+"users")))
					.replace("$contacts", str(db.scard(profile+"contacts")))
					.replace("$channels", str(db.scard(profile+"pv_channels") + db.scard(profile+"pub_channels")))
					.replace("$clinks", str(db.scard(profile+"correct_links")))
					.replace("$slinks", str(db.scard(profile+"saved_links")))
					.replace("$wlinks", str(db.scard(profile+"good_links")))
					.replace("$restrict", str(db.scard(profile+"restricted_c")))
					.replace("$linkst", str("✖" if (db.scard(profile+"good_links") == 0 or db.get(profile+"link_limit_s")) else timetostr(db.ttl(profile+"check_links_ttime"))))+
					"\n\n"+update, m_id, "html")
				elif text and h.set(re.search("^profwd (\d+) (all|supergroups|users|contacts)( *(\d*))$", text)) and m["reply_to_message_id"] != 0 :
					seen = int(h.get().group(1))
					wtime = int(h.get().group(4) or 0)
					printw("Forwarding Pm to "+h.get().group(2)+" ... !")
					tt = time()
					type_chats = [h.get().group(2)]
					type_list = []
					if h.get().group(2) == "all" :
						type_chats = ["supergroups", "users"]
					for type_chat in type_chats :
						type_list += list(db.smembers(profile+type_chat)) + list(db.smembers(profile+"pv_"+type_chat)) + list(db.smembers(profile+"pub_"+type_chat))
					type_list = list(set(type_list))
					if len(type_list) == 0 :
						send_msg(chat_id, "⇜هیچ چتی برای فروارد یافت نشد !", m_id)
					else :
						td_send("getMessage", {"chat_id" : chat_id, "message_id" : m["reply_to_message_id"]}, "profwd_msg1", {"type_list" : type_list, "chat_id" : chat_id, "mid" : m["reply_to_message_id"], "seen" : seen, "type" : h.get().group(2)[0].upper()+h.get().group(2)[1:], "number" : 1, "wtime" : wtime})
				elif text and h.set(re.search("^send( *(\d*)) (all|supergroups|users|contacts)( *(\d*))( *(.*))$", text)) :
					issendcan = 0
					count = int(h.get().group(2) or 0)
					wtime = int(h.get().group(5) or 2)
					type_chats = [h.get().group(3)]
					type_list = []
					if h.get().group(3) == "all" :
						type_chats = ["supergroups", "users"]
					for type_chat in type_chats :
						type_list += list(db.smembers(profile+type_chat)) + list(db.smembers(profile+"pv_"+type_chat)) + list(db.smembers(profile+"pub_"+type_chat))
					type_list = list(set(type_list))
					if len(type_list) == 0 :
						send_msg(chat_id, "⇜هیچ چتی برای ارسال یافت نشد !", m_id)
					else :
						if count == 0 or count > len(type_list) :
							count = len(type_list)
						type_list = random.sample(type_list, count)
						printw("Sending Pm to "+h.get().group(3)+" ... !")
						if h.get().group(7) and m["reply_to_message_id"] == 0 :
							sleep(tabchi_number * (1.5 if db.get(profile+"proxy_unset") else 2))
							send_msg(chat_id, "❃ ارسال شروع شد ! ("+str(len(type_list))+") چت\n| ░░░░░░░░░░ |", 0, None, "send_msg", {"type_list" : type_list, "chat_id" : chat_id, "content" : {"@type" : "messageText", "text" : td_execute("parseTextEntities", {"text" : h.get().group(7), "parse_mode" : {"@type" : "textParseModeHTML"}})}, "wtime" : wtime})
						else :
							td_send("getMessage", {"chat_id" : chat_id, "message_id" : m["reply_to_message_id"]}, "send_msg2", {"type_list" : type_list, "chat_id" : chat_id, "wtime" : wtime})
				elif text == "send cancel" :
					issendcan = 1
					send_msg(chat_id, "⇜عملیات ارسال لغو شد !", m_id)
				elif text and h.set(re.search("^isend( *(\d*)) (all|supergroups|users|contacts) (\S+) (\S+)( *(\d*))$", text)) :
					count = int(h.get().group(2) or 0)
					inlinebot = h.get().group(4)
					icmd = h.get().group(5)
					wtime = int(h.get().group(7) or 2)
					type_chats = [h.get().group(3)]
					type_list = []
					if h.get().group(3) == "all" :
						type_chats = ["supergroups", "users"]
					for type_chat in type_chats :
						type_list += list(db.smembers(profile+type_chat)) + list(db.smembers(profile+"pv_"+type_chat)) + list(db.smembers(profile+"pub_"+type_chat))
					type_list = list(set(type_list))
					if len(type_list) == 0 :
						send_msg(chat_id, "⇜هیچ چتی برای ارسال یافت نشد !", m_id)
					else :
						if count == 0 or count > len(type_list) :
							count = len(type_list)
						type_list = random.sample(type_list, count)
						printw("Sending Pm to "+h.get().group(3)+" ... !")
						td_send("searchPublicChat", {"username" : inlinebot}, "isend_msg2", {"type_list" : type_list, "chat_id" : chat_id, "inlinebot" : inlinebot, "icmd" : icmd, "wtime" : wtime})
				elif text and h.set(re.search("^fwd( *(\d*)) (all|supergroups|users|contacts)( *(\d*))$", text)) and m["reply_to_message_id"] != 0 :
					isfwdcan = 0
					count = int(h.get().group(2) or 0)
					wtime = int(h.get().group(5) or 0)
					type_chats = [h.get().group(3)]
					type_list = []
					if h.get().group(3) == "all" :
						type_chats = ["supergroups", "users"]
					for type_chat in type_chats :
						type_list += list(db.smembers(profile+type_chat)) + list(db.smembers(profile+"pv_"+type_chat)) + list(db.smembers(profile+"pub_"+type_chat))
					type_list = list(set(type_list))
					if len(type_list) == 0 :
						send_msg(chat_id, "⇜هیچ چتی برای فروارد یافت نشد !", m_id)
					else :
						if count == 0 or count > len(type_list) :
							count = len(type_list)
						type_list = random.sample(type_list, count)
						printw("Forwarding Pm to "+h.get().group(3)+" ... !")
						sleep(tabchi_number * (1.5 if db.get(profile+"proxy_unset") else 2))
						send_msg(chat_id, "❃ فوروارد شروع شد ! ("+str(len(type_list))+") چت\n| ░░░░░░░░░░ |", 0, None, "fwd_msg", {"type_list" : type_list, "chat_id" : chat_id, "mid" : m["reply_to_message_id"], "wtime" : wtime})
				elif text == "fwd cancel" :
					isfwdcan = 1
					send_msg(chat_id, "⇜عملیات فوروارد لغو شد !", m_id)
				elif text == "cancel all" :
					isfwdcan = 1
					issendcan = 1
					isaddmemcan = 1
					send_msg(chat_id, "⇜عملیات ها لغو شدند !", m_id)
				elif text and h.set(re.search("^rfwd( *(\d*)) (all|supergroups|users|contacts)( *(\d*)) (.+)$", text)) and m["reply_to_message_id"] != 0 :
					count = int(h.get().group(2) or 0)
					rtext = h.get().group(6)
					wtime = int(h.get().group(5) or 0)
					type_chats = [h.get().group(3)]
					type_list = []
					if h.get().group(3) == "all" :
						type_chats = ["supergroups", "users"]
					for type_chat in type_chats :
						type_list += list(db.smembers(profile+type_chat)) + list(db.smembers(profile+"pv_"+type_chat)) + list(db.smembers(profile+"pub_"+type_chat))
					type_list = list(set(type_list))
					if len(type_list) == 0 :
						send_msg(chat_id, "⇜هیچ چتی برای فروارد یافت نشد !", m_id)
					else :
						if count == 0 or count > len(type_list) :
							count = len(type_list)
						type_list = random.sample(type_list, count)
						printw("Forwarding Pm to "+h.get().group(3)+" ... !")
						sleep(tabchi_number * (1.5 if db.get(profile+"proxy_unset") else 2))
						send_msg(chat_id, "❃ فوروارد شروع شد ! ("+str(len(type_list))+") چت\n| ░░░░░░░░░░ |", 0, None, "rfwd_msg", {"type_list" : type_list, "chat_id" : chat_id, "mid" : m["reply_to_message_id"], "wtime" : wtime, "rtext" : rtext})
				elif text == "getlinks" :
					temp_name = tempfile.mktemp()+".txt"
					with open(temp_name, "w") as file :
						for link in db.smembers(profile+"correct_links") :
							file.write("https://t.me/joinchat/"+link+"\n")
						file.seek(0, 0)
					td_send("sendMessage",{"chat_id" : chat_id, "reply_to_message_id" : m_id,"disable_notification" : True,"from_background" : True,"input_message_content" : {"@type" : "inputMessageDocument","document" : {"@type" : "inputFileLocal", "path" : temp_name},"thumbnail" : None,"caption" : None}})
					sleep(1)
					os.unlink(temp_name)
				elif text == "resetlinks" :
					for link in db.smembers(profile+"good_links") :
						db.srem(profile+"all_links", link)
						db.srem(profile+"good_links", link)
					db.delete(profile+"inwait_links")
					send_msg(chat_id, "⇜تمامی لینک ها پاکسازی شدند !", m_id)
				elif text and h.set(re.search("^leave( *(\d*)) (supergroups|channels)$", text)) :
					count = int(h.get().group(2) or 0)
					printw("Leaving from "+h.get().group(3)+" ... !")
					type_list = list(db.smembers(profile+h.get().group(3))) + list(db.smembers(profile+"pv_"+h.get().group(3))) + list(db.smembers(profile+"pub_"+h.get().group(3)))
					type_list = list(set(type_list))
					sleep(tabchi_number * (1.5 if db.get(profile+"proxy_unset") else 2))
					try :
						type_list.remove(str(db.get(profile+"modspgp") or 0))
					except :
						pass
					if len(type_list) == 0 :
						send_msg(chat_id, "⇜هیچ چتی برای خروج یافت نشد !", m_id)
					else :
						if count == 0 or count > len(type_list) :
							count = len(type_list)
						type_list = random.sample(type_list, count)
						send_msg(chat_id, "❃ خروج از ("+str(len(type_list))+") "+h.get().group(3)+" اغاز شد !\n| ░░░░░░░░░░ |", 0, None, "leave_msg", {"type_list" : type_list, "chat_id" : chat_id})
				elif text == "joinlinks off" :
					db.set(profile+"link_limit_s", "ok")
					send_msg(chat_id, "⇜عضویت خودکار  غیرفعال  شد .", m_id)
				elif text == "joinlinks on" :
					db.delete(profile+"link_limit_s")
					send_msg(chat_id, "⇜عضویت خودکار  فعال	شد .", m_id)
				elif text == "checklinks off" :
					db.set(profile+"clink_limit_s", "ok")
					send_msg(chat_id, "⇜دریافت لینک از غیر سودو	 غیرفعال  شد .", m_id)
				elif text == "checklinks on" :
					db.delete(profile+"clink_limit_s")
					send_msg(chat_id, "⇜دریافت لینک از غیر سودو فعال شد .", m_id)
				elif text == "addcontacts on" :
					db.set(profile+"contacts_limit", "ok")
					send_msg(chat_id, "⇜افزودن مخاطب  فعال	شد .\n✯ در تمامی گروه های تبچی اگر مخاطبی به اشتراک گذاشته شود ، توسط ربات به مخاطبان آن افزوده می شود !", m_id)
				elif text == "addcontacts off" :
					db.delete(profile+"contacts_limit")
					send_msg(chat_id, "⇜افزودن مخاطب  غیرفعال  شد .", m_id)
				elif text == "addcontacts null" :
					db.delete(profile+"addcontacts_text")
					send_msg(chat_id, "⇜پیام افزودن مخاطب حذف شد و افزودن مخاطب با پیام	 غیرفعال  شد !", m_id)
				elif text and h.set(re.search("^addcontacts (.+)$", text)) :
					db.set(profile+"addcontacts_text", h.get().group(1))
					send_msg(chat_id, "⇜پیام افزودن مخاطب ذخیره و افزودن مخاطب با پیام	فعال  شد .\n✯ پیام افزودن مخاطب به ༜ \""+h.get().group(1)+"\" ༜ تنظیم شد !", m_id)
				elif text == "gpjoinmsg null" :
					db.delete(profile+"gp_join_msg")
					send_msg(chat_id, "⇜ پیام عضویت در گروه	 حذف شد !", m_id)
				elif text and h.set(re.search("^gpjoinmsg (.+)$", text)) :
					db.set(profile+"gp_join_msg", h.get().group(1))
					send_msg(chat_id, "⇜پیام عضویت در گروه	فعال  شد .\n✯ پیام عضویت در گروه به ༜ \""+h.get().group(1)+"\" ༜ تنظیم شد !", m_id)
				elif text == "badnames list" :
					badnames_text = "\n".join(str(x) for x in db.smembers(profile+"badnames"))
					send_msg(chat_id, "⇜لیست کلمات سیاه : "+("خالی" if badnames_text == "" else badnames_text), m_id)
				elif text and h.set(re.search("^badnames \+ (.+)$", text)) :
					badname = h.get().group(1).lower()
					if db.sismember(profile+"badnames", badname) :
						send_msg(chat_id, "⇜کلمه ی مورد نظر در لیست سیاه قرار دارد !", m_id)
					else :
						db.sadd(profile+"badnames", badname)
						send_msg(chat_id, "⇜کلمه ی مورد نظر به لیست سیاه اضافه شد و از این به بعد تبچی در گروه هایی که این کلمه در اسم آن وجود دارد عضو نخواهد شد !", m_id)
				elif text and h.set(re.search("^badnames \- (.+)$", text)) :
					badname = h.get().group(1).lower()
					if not db.sismember(profile+"badnames", badname) :
						send_msg(chat_id, "⇜کلمه ی مورد نظر در لیست سیاه قرار ندارد !", m_id)
					else :
						db.srem(profile+"badnames", badname)
						send_msg(chat_id, "⇜کلمه ی مورد نظر از لیست سیاه حذف شد !", m_id)
				elif text == "setmincount off" :
					db.delete(profile+"minjoincount")
					send_msg(chat_id, "⇜محدودیت	 اعضا  برای جوین شدن برداشته شد .", m_id)
				elif text and h.set(re.search("^setmincount (\d+)$", text)) :
					db.set(profile+"minjoincount", int(h.get().group(1)))
					send_msg(chat_id, "⇜از این پس تبچی در گروه هایی که اعضای آن کمتر از \""+h.get().group(1)+"\" است , جوین نمی شود .", m_id)
				elif text == "autofwd cancel" :
					msg_id, user_id = db.get(profile+"auto_fwd_last_pm"), db.get(profile+"autofwd_last_user")
					if msg_id and user_id :
						db.delete(profile+"auto_fwd_last_pm")
						db.delete(profile+"autofwd_last_user")
						td_send("editMessageText", {"chat_id" : user_id, "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : "Canceled!", "entities" : None}}})
					send_msg(chat_id, "⇜عملیات فوروارد هوشمند لغو شد !", m_id)
				elif text == "autofwd turnmsg" :
					msg_id, user_id = db.get(profile+"auto_fwd_last_pm"), db.get(profile+"autofwd_last_user")
					if msg_id and user_id :
						db.delete(profile+"auto_fwd_last_pm")
						db.delete(profile+"autofwd_last_user")
						td_send("editMessageText", {"chat_id" : user_id, "message_id" : msg_id, "input_message_content" : {"@type" : "inputMessageText", "text" : {"@type" : "formattedText", "text" : "Canceled!", "entities" : None}}})
					last_fwd = db.get(profile+"last_fwd")
					if last_fwd :
						last_fwd = json.loads(last_fwd)
						type_list = last_fwd["type_list"]
						count = last_fwd["count"]
						suc = last_fwd["suc"]
						tt = last_fwd["tt"]
						post_data = last_fwd["post_data"]
						msg_seen = 0
						if "msg_seen" in last_fwd :
							msg_seen = last_fwd["msg_seen"]
						seen = 0
						if len(post_data) == 3 :
							seen = post_data[2]
						darsad = round(float(count * 100) / float(len(type_list)), 1)
						suc_t_count = (count * 10) / len(type_list)
						autofwd_count = int(db.get(profile+"autofwd_count") or 1)
						text = "❃ درحال انجام فوروارد هوشمند ("+str(autofwd_count)+" چت) به "+str(count)+"/"+str(len(type_list))+" چت(%"+str(darsad)+")\n↜تعداد موفق : "+str(suc)+"\n↜تعدادناموفق :"+str(count - suc)+"\n|"+"█"*suc_t_count+"░"*(10 - suc_t_count)+"|"+"\n↜مقدار ویو : "+str(seen)+"\n👁‍🗨: "+str(msg_seen)+"\n↜مدت زمان: "+timetostr(time() - tt)
						sleep(tabchi_number * (1.5 if db.get(profile+"proxy_unset") else 2))
						send_msg(chat_id, text, 0, None, "turn_fwd_msg", {"chat_id" : chat_id})
					else :
						sleep(tabchi_number * (1.5 if db.get(profile+"proxy_unset") else 2))
						send_msg(chat_id, "Turning Fwd Msg On!", 0, None, "turn_fwd_msg", {"chat_id" : chat_id})
				elif text == "autofwd list" :
					if	db.scard(profile+"autofwd_list") != 0 :
						send_msg(chat_id, "• تمامی پست های موجود در لیست ( فروارد ) •", m_id)
						for post_data in db.smembers(profile+"autofwd_list") :
							m_idf, chat_idf = post_data.split(":")
							td_send("forwardMessages", {"chat_id" : chat_id, "from_chat_id" : chat_idf, "message_ids" : [m_idf], "disable_notification" : True, "from_background" : True})
					else :
						send_msg(chat_id, "⇜ هیچ پستی یافت نشد .", m_id)
				elif text == "autofwd +" and m["reply_to_message_id"] != 0:
					post_data = str(m["reply_to_message_id"])+":"+str(m["chat_id"])
					if not db.sismember(profile+"autofwd_list", post_data) :
						db.sadd(profile+"autofwd_list", post_data)
						send_msg(chat_id, "⇜پیام مورد نظر شما به لیست  ( فروارد )  اضافه شد .", m_id)
					else :
						send_msg(chat_id, "⇜پیام مورد نظر شما در لیست  ( فروارد )  موجود است !", m_id)
				elif text == "autofwd -" and m["reply_to_message_id"] != 0 :
					post_data = str(m["reply_to_message_id"])+":"+str(m["chat_id"])
					if	db.sismember(profile+"autofwd_list", post_data) :
						db.srem(profile+"autofwd_list", post_data)
						send_msg(chat_id, "⇜پیام مورد نظر شما از لیست  ( فروارد )  حذف شد .", m_id)
					else :
						send_msg(chat_id, "⇜پیام مورد نظر شما در لیست  ( فروارد )  موجود نیست !", m_id)
				elif text == "autofwd clean" :
					db.delete(profile+'autofwd_list')
					send_msg(chat_id, "⇜لیست پست های ( فروارد ) خودکار با موفقیت پاکسازی شد !", m_id)
				elif text == "autofwd off" :
					db.delete(profile+"autofwd_time")
					send_msg(chat_id, "⇜( فروارد ) اتومات  غیرفعال	شد .", m_id)
				elif text and h.set(re.search("^autofwd (\d+)$", text)) :
					fwdtime = int(h.get().group(1))
					db.set(profile+"autofwd_time", fwdtime *  60)
					db.setex(profile+"autofwd_time_ttl", fwdtime * 60, "ok")
					db.set(profile+"autofwd_count", 0)
					send_msg(chat_id, "⇜زمان بین هر ( فروارد ) به "+str(fwdtime)+" دقیقه تنظیم شد .", m_id)
					sleep(tabchi_number * (1.5 if db.get(profile+"proxy_unset") else 2))
					send_msg(chat_id, "Turning Fwd Msg On!", 0, None, "turn_fwd_msg", {"chat_id" : chat_id})
				elif text and h.set(re.search("^autofwd (.+)$", text)) :
					autofwd_type = ""
					autofwd_type_tt = ""
					autofwd_type_t = h.get().group(1)
					if "users" in autofwd_type_t :
						autofwd_type += "users"
						autofwd_type_tt += chat_type_persian["users"]+" "
					if "supergroups" in autofwd_type_t :
						autofwd_type += "supergroups"
						autofwd_type_tt += chat_type_persian["supergroups"]
					if autofwd_type != "" :
						db.set(profile+"autofwd_type", autofwd_type)
						send_msg(chat_id, "⇜از این پس پیام های در لیست ( فروارد ) اتومات به	 "+autofwd_type_tt+"  ارسال خواهد شد .", m_id)
				elif text == "forcejoin off" :
					db.delete(profile+"force_join")
					send_msg(chat_id, "⇜جوین اجباری در کانال غیر فعال شد !", m_id)
				elif text and h.set(re.search("^forcejoin (@\S+)$", text)) :
					td_send("searchPublicChat", {"username" : h.get().group(1)}, "add_channel", {"m" : m, "username" : h.get().group(1)})
				elif text == "addc" and m["reply_to_message_id"] != 0 :
					td_send("getMessage", {"chat_id" : chat_id, "message_id" : m["reply_to_message_id"]}, "add_contact", m)
				elif text == "addmembers" :
					isaddmemcan = 0
					printw("Adding members to cruent chat ... !")
					type_list = list(db.smembers(profile+"users"))
					if len(type_list) == 0 :
						send_msg(chat_id, "⇜هیچ کاربری برای افزودن یافت نشد !", m_id)
					else :
						sleep(tabchi_number * (1.5 if db.get(profile+"proxy_unset") else 2))
						send_msg(chat_id, "❃ افزودن ("+str(len(type_list))+") کاربر به گروه اغاز شد !\n| ░░░░░░░░░░ |", 0, None, "addmembers_msg", {"type_list" : type_list, "chat_id" : chat_id})
				elif text == "addmembers cancel" :
					isaddmemcan = 1
					send_msg(chat_id, "⇜عملیات افزودن کاربر به گروه لغو شد !", m_id)
		elif m["content"]["@type"] == "messageContact" :
			if db.get(profile+"contacts_limit") :
				if not db.sismember(profile+"contacts", m["content"]["contact"]["user_id"]) :
					td_send("importContacts", {"contacts" : [m["content"]["contact"]]})
					db.sadd(profile+"contacts", m["content"]["contact"]["user_id"])
					contacttext = db.get(profile+"addcontacts_text")
					if contacttext :
						send_msg(chat_id, contacttext, m_id)
		elif m["content"]["@type"] == "messageChatAddMembers" :
			for member in m["content"]["member_user_ids"] :
				if Bot and int(member) == int(Bot["id"]) : 
					if (allready_gp(chat_id) or	(db.get(profile+"cant_add_gp") and not (db.sismember(profile+"admins", user_id) or user_id == sudo))):
						td_send("setChatMemberStatus",{"chat_id" : chat_id, "user_id" : Bot["id"], "status" : {"@type" : "chatMemberStatusLeft"}}, "leave_chat2", {"chat_id" : chat_id})
					else :
						gpjoinmsg = db.get(profile+"gp_join_msg")
						if gpjoinmsg :
							send_msg(chat_id, gpjoinmsg)
		elif m["content"]["@type"] == "messageChatJoinByLink" and not db.sismember(profile+"all", chat_id):
				gpjoinmsg = db.get(profile+"gp_join_msg")
				if gpjoinmsg :
					send_msg(chat_id, gpjoinmsg)
		elif m["content"]["@type"] == "messageChatDeleteMember"	 and int(m["content"]["user_id"]) == int(Bot["id"]):
			td_send("deleteChatHistory", {"chat_id" : chat_id, "remove_from_chat_list" : True})
			chat_rem(chat_id)
	except Exception as e :
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno,e)
	"""freeze_support()
	p = Process(target=msg_multi)
	p.start()"""
launchtime = float(time() - 5)
while True:
	event = td_receive()
	if event:
		if event['@type'] == 'updateAuthorizationState' :
			if event['authorization_state']['@type'] == 'authorizationStateClosed':
				break
			elif event['authorization_state']['@type'] == 'authorizationStateWaitTdlibParameters':
				api_id = db.get(profile+"api_id")
				api_hash = db.get(profile+"api_hash")
				d_model = db.get(profile+"d_model")
				d_os = db.get(profile+"d_os")
				
				while not api_id :
					api_id = raw_input("Enter api_id: ")
					if not re.search("^\d+$", api_id) :
						api_id = None
				api_id = int(api_id)
				while not api_hash :
					api_hash = raw_input("Enter api_hash: ")
					if not re.search("^\S+$", api_hash) :
						api_hash = None
				while not d_model :
					d_model = raw_input("Enter device_model: ")
					if not re.search("^\S+$", d_model) :
					    d_model = None
				while not d_os :
					d_os = raw_input("Enter system_os: ")
					if not re.search("^\S+$", d_os) :
						d_os = None
				td_send('setTdlibParameters', {'parameters' : {'use_test_dc': False, 'database_directory' : "Profiles/"+profile+"/datas", 'files_directory' : "Profiles/"+profile+"/files", 'use_file_database' : True, 'use_chat_info_database' : True, 'use_message_database' : True, 'use_secret_chats' : False, 'api_id' : api_id, 'api_hash' : api_hash, 'system_language_code' : 'en', 'device_model' : d_model, 'system_version' : d_os, 'application_version' : '1.0', 'enable_storage_optimizer' : True, 'ignore_file_names' : True}}, "parametrs_seted", {"api_id" : api_id, "api_hash" : api_hash, "d_model" : d_model, "d_os" : d_os})
			elif event['authorization_state']['@type'] == 'authorizationStateWaitEncryptionKey':
				td_send('checkDatabaseEncryptionKey', {'encryption_key' : ''})
			elif event['authorization_state']['@type'] == 'authorizationStateWaitPhoneNumber':
				td_send('setAuthenticationPhoneNumber', {'phone_number' : raw_input("Phone : "), 'allow_flash_call' : False,  'is_current_phone_number' : False}, "code_send")
			elif event['authorization_state']['@type'] == 'authorizationStateWaitCode' :
				check_code(raw_input("Code : "), event['authorization_state']["is_registered"])
			elif event['authorization_state']['@type'] == 'authorizationStateWaitPassword' :
				check_password(raw_input("Pass(hint : "+event['authorization_state']["password_hint"]+") : "))
			elif event['authorization_state']['@type'] == "authorizationStateReady" :
				printi("Tabchi is ready!")
				td_send("getMe", {}, "get_bot_info")
				check_cache(True)
				check_links()
				check_fwd(True)
		elif event["@type"] == "updateNewMessage" :
			if float(event["message"]["date"]) > launchtime :
				new_message(event["message"], event["contains_mention"])
		elif event["@type"] == "updateMessageSendSucceeded" :
			message = db.hget("SentStateMessages", event["old_message_id"])
			if message :
				extra = json.loads(message)
				call_back = extra["__FUNCTION__"]
				del(extra["__FUNCTION__"])
				call_backs(call_back, True, event["message"], extra)
				db.hdel("SentStateMessages", event["old_message_id"])
		elif event["@type"] == "updateMessageSendFailed" :
			print(event["error_code"], event["error_message"])
			message = db.hget("SentStateMessages", event["old_message_id"])
			if message :
				extra = json.loads(message)
				call_back = extra["__FUNCTION__"]
				del(extra["__FUNCTION__"])
				call_backs(call_back, False, {"message" : event["error_message"]}, extra)
				db.hdel("SentStateMessages", event["old_message_id"])
		elif event["@type"] == "updateFile" :
			if "file" in event and event["file"]["local"]["is_downloading_completed"] :
				msg = db.hget(profile+"uploading_profiles", event["file"]["id"])
				if msg :
					db.hdel(profile+"uploading_profiles", event["file"]["id"])
					call_backs("tphoto", True, event["file"], json.loads(msg))
				msgg = db.hget(profile+"uploading_links", event["file"]["id"])
				if msgg :
					db.hdel(profile+"uploading_links", event["file"]["id"])
					call_backs("tlinks", True, event["file"], json.loads(msgg))
		elif event["@type"] == "updateSupergroup" :
			if event["supergroup"]["@type"] == "supergroup" and (event["supergroup"]["status"]["@type"] == "chatMemberStatusRestricted") and not db.get(profile+"restrict"):
				chat_id = "-100"+str(event["supergroup"]["id"])
				db.sadd(profile+"restricted_c", chat_id)
				td_send("setChatMemberStatus",{"chat_id" : "-100"+str(event["supergroup"]["id"]), "user_id" : Bot["id"], "status" : {"@type" : "chatMemberStatusLeft"}}, "leave_chat2", {"chat_id" : chat_id})
		elif "@extra" in event and "call_back" in event["@extra"] and event["@extra"]["call_back"] != None :
			event_c = dict(event)
			del(event["@extra"])
			call_backs(event_c["@extra"]["call_back"], event_c["@type"] != "error", event, event_c["@extra"]["extra_data"])
			del(event_c)
	sleep(0.001)
"""for file2 in ["Profiles/"+profile+"/datas/db.sqlite-wal", "Profiles/"+profile+"/datas/db.sqlite-shm"] :
	try :
		os.unlink(file2)
	except :
		pass"""
td_json_client_destroy(client)