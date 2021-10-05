#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib
import os
import string
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot,MessageEntity

from io import BytesIO

key = ""
chat_id = ""
push_bot = ""

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

	#GET is not supported
	def do_GET(self):
		self.send_response(404)
		self.end_headers()

	#Only accept POST
	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		body = urllib.parse.unquote(self.rfile.read(content_length).decode("utf-8"))
		self.send_response(200)
		self.end_headers()
		post_data = body.split("&") #Gather the parameters from the request body
		response = BytesIO()

		needed_vars = ["title", "message", "key"] #These are needed in order to work
		found_vars = []


		title = ""
		message = ""
		posted_key = ""

		post_is_ok = True
		for param in post_data:
			variable = param.split("=")[0]
			value = param.split("=")[1]
			if variable in needed_vars:
				if variable in found_vars:
					response.write(b'Invalid Request - Duplicated Params') #Only use each param once
					self.wfile.write(response.getvalue())
					post_is_ok = False
					break
				else:
					if variable == "title":
						title = value
					if variable == "message":
						message = value
					if variable == "key":
						posted_key = value
					found_vars.append(variable)
			else:
				response.write(b'Invalid Request - Unknown Parameter sent') #Only allow the three parameters above
				self.wfile.write(response.getvalue())
				post_is_ok = False
				break
		if post_is_ok: #The post seems to be ok, however we don't know yet if everything we need was sent
			all_vars_there = True
			for needed_var in needed_vars:
				if not needed_var in found_vars:
					response.write(b'Invalid Request - One or more of title, message, or key params missing')
					self.wfile.write(response.getvalue())
					all_vars_there = False
					break
			if all_vars_there:
				if key == posted_key: #The key from keyfile has to be exactly the same as the key which was posted
					title_entity = MessageEntity(type=MessageEntity.BOLD, offset=0, length=len(title))
					#Send message as "Code", so we don't have formatting problems in telegram
					message_entity = MessageEntity(type=MessageEntity.CODE, offset=len(title), length=len((os.linesep)*2 + message))
					push_bot.sendMessage(chat_id=chat_id, text=title + (os.linesep)*2 + message, entities=[title_entity, message_entity])
				else:
					response.write(b'Invalid Request - Key Invalid')
					self.wfile.write(response.getvalue())

if __name__ == "__main__":

	with open(os.path.dirname(os.path.realpath(__file__)) + "/keyfile.key", "r") as keyfile:
		key = keyfile.read()

	BOT_TOKEN = ""

	with open(os.path.dirname(os.path.realpath(__file__)) + "/bottoken.key", "r") as keyfile:
		BOT_TOKEN = keyfile.read()

	with open(os.path.dirname(os.path.realpath(__file__)) + "/chatid.key", "r") as keyfile:
		chat_id = keyfile.read()

	updater = Updater(token=BOT_TOKEN, use_context=True)
	dispatcher = updater.dispatcher
	push_bot = Bot(token=BOT_TOKEN)

	#Ping is only used to check if the bot-bridge is alive
	def ping(update, context):
		context.bot.send_message(chat_id=update.effective_chat.id, text="Pong")

	ping_handler = CommandHandler('ping', ping)
	dispatcher.add_handler(ping_handler)
	updater.start_polling()
	print ("Bot running")

	httpd = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
	httpd.serve_forever() #Spin up the HTTP Server

	print ("Server running")
