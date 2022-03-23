#!/usr/bin/python3

import sqlite3 # SQL (Database)
from flask import Flask, render_template, request # Web server

# Library for colors
from colorama import init, Fore
from colorama import Back
from colorama import Style

# Init methods
init(autoreset=True)

# Vars
webApp = Flask(__name__)
webApp.env = 'development'
webAppPort = 7001 # Port
webAppIPtoRun = '26.194.160.135' # You IP (default local, 127.0.0.1)
databaseFile = 'database.db'
is_loaded_db = False
debugModeState = False # Set to True if you want to enable Debug mode
prefix_name = '[DMessenger]'

# Logo
print('██████╗ ███╗   ███╗███████╗███████╗███████╗███████╗███╗   ██╗ ██████╗ ███████╗██████╗')
print('██╔══██╗████╗ ████║██╔════╝██╔════╝██╔════╝██╔════╝████╗  ██║██╔════╝ ██╔════╝██╔══██╗')
print('██║  ██║██╔████╔██║█████╗  ███████╗███████╗█████╗  ██╔██╗ ██║██║  ███╗█████╗  ██████╔╝')
print('██║  ██║██║╚██╔╝██║██╔══╝  ╚════██║╚════██║██╔══╝  ██║╚██╗██║██║   ██║██╔══╝  ██╔══██╗')
print('██████╔╝██║ ╚═╝ ██║███████╗███████║███████║███████╗██║ ╚████║╚██████╔╝███████╗██║  ██║')
print('╚═════╝ ╚═╝     ╚═╝╚══════╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝')
print()
print(Fore.YELLOW + '            Text | Server | Alpha 22.03.2022 | DragonFire Community')

# Database Class
class dmsg_database():
	def load():
		try:
			global sqlite_connection
			global cursor

			sqlite_connection = sqlite3.connect(databaseFile, check_same_thread=False)
			print("[DATABASE] Connected")

			cursor = sqlite_connection.cursor()

			is_loaded_db = True

		except sqlite3.Error as error:
			print("[DATABASE] Error: ", error)

	def requestSql(requestType):
		if requestType == 'getMessages':
			responce = cursor.execute('SELECT message FROM "messages" LIMIT 100')
			responce = cursor.fetchall()

			responce1 = str(responce)
			return responce1

	def init_db():
		if is_loaded_db == False:
			dmsg_database.load()
			dmsg_database.init_db()

		if is_loaded_db == True:
			print('[Init Database] Loading')

class dmsg_routes():
	# Errors
	@webApp.errorhandler(404)
	async def not_found(error):
		return "Route not found"

	# Routes disabled
	@webApp.route('/')
	@webApp.route('/api')
	@webApp.route('/api/v1')
	@webApp.route('/api/v1/message')
	async def route_disabled():
		return "Route not supported/disabled, or you don't have permissions to view this content"

	# API
	@webApp.route('/api/ping', methods = ['GET', 'POST'])
	async def ping_api():
		return "pong"

	@webApp.route('/api/v1/message/messages', methods = ['GET'])
	async def message_messages():
		messages = dmsg_database.requestSql(requestType = 'getMessages')
		if messages == None: return f'{prefix_name} No messages'
		if messages == '': return f'{prefix_name} No messages'
		else:
			return messages

	@webApp.route('/api/v1/message/send', methods = ['POST']) # SOON
	def message_send():
		username = request.headers.get('username', None)
		textMessage = request.headers.get('messageToSend', None)
		handledMsg = f'{username}: {textMessage}'
		cursor.execute(f'INSERT INTO messages VALUES {handledMsg}')

# Server Class
class dmsg_server():
	def run():
		webApp.run(
			host = webAppIPtoRun,
			port = webAppPort,
			debug = debugModeState
		)

dmsg_database.load() # Load database
dmsg_server.run() # Run server