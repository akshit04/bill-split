# -*- coding: utf-8 -*-
from ambrogio.bot import  Ambrogio
from ambrogio.plugin import Plugin
from plugins.add_expense import AddExpense
from plugins.history import History
from plugins.uneven_split import  UnevenSplit
from plugins.balance import Balance
from plugins.create_group import CreateGroup


class Treasurer(Plugin):
	def receive_message(self, ambrogio, message):
		msg = message.text
		create_group_flag = False
		if msg.find('|') != -1:
			handle_pos = msg.find('|')
			detail_pos = msg.find('"')
			if detail_pos != -1:
				users = msg[handle_pos+1:detail_pos-1]
			else:
				users = msg[handle_pos+1:]
			users = users.split(',')
			for  user in users:
				mul_index = user.find('*')
				add_index = user.find('+')
				if (mul_index != -1) or (add_index != -1):
					add_index = (10000 if add_index == -1 else add_index)
					mul_index = (10000 if mul_index == -1 else mul_index)
					index = min(add_index,mul_index)
					user_name = user[:index]

					if len(user_name)>2:
						create_group_flag = True
						break
				else:
					if len(user)>2:
						create_group_flag = True
						break
		if (('|' in msg) and not(('+' in msg) or ('*' in msg)) and not (create_group_flag)):
			AddExpense.add_expense(ambrogio,message,True)
		elif ('HISTORY' in msg):
			History.history(ambrogio,message)
		elif (('|' in msg) and (('+' in msg) or ('*' in msg)) and not (create_group_flag)):
			UnevenSplit.uneven_split(ambrogio,message,True)
		elif ('BALANCE' in msg):
			Balance.balance(ambrogio,message)
		elif (('CREATE' in msg) or ('ADD' in msg) or ('DELETE' in msg) or (create_group_flag)):
			CreateGroup.create_group(ambrogio,message)

	def init_plugin(self, ambrogio):
		pass