from .create_group_dict import group_dict as db
from .add_expense import AddExpense
from .uneven_split import UnevenSplit

class CreateGroup():
	def create_group(ambrogio,message):

		msg=message.text
		if 'CREATE' in msg:
			group_name = msg[7:]

			if (len(group_name)<3) or (len(group_name) > 12):
				return

			for char in group_name:
				if (char<'A') or (char>'Z'):
					return

			if group_name in db:
				return

			else:
				db[group_name]=[]
				ambrogio.send_text("Done")

		elif 'ADD' in msg:
			user = msg[4:6]
			group_name = msg[7:]
			if group_name in db:
				if user in db[group_name]:
					return
				else:
					db[group_name].append(user)
					ambrogio.send_text("Done")
			else:
				return

		elif 'DELETE' in msg:
			user = msg[7:9]
			group_name = msg[10:]
			if group_name in db:
				if user in db[group_name]:
					db[group_name].remove(user)
					ambrogio.send_text("Done")
				else:
					return
			else:
				return

		elif ('|' in msg) and not(('+' in msg) or ('*' in msg)):	# normal add expense case (even split)
			handle_pos = msg.find('|')
			new_message = ""
			new_message += msg[0:handle_pos+1]
			user_string = msg[handle_pos+1:]
			users = user_string.split(',')
			size = len(users)
			count = 0
			users_set = set()

			for i in range(size):
				if len(users[i])==2:
					new_message += users[i]
					count += 1
					users_set.add(users[i])
					if i<(size-1):
						new_message += ","
				else:
					group_name = users[i]
					if group_name in db:
						for x in db[group_name]:
							new_message += x
							new_message += ","
							users_set.add(x)
							count += 1
						new_message = new_message[:-1]	#remove the last inserted comma(,)

						if i<(size-1):
							new_message += ","
					else:
						return

			if len(users_set) != count:
				return

			else:
				AddExpense.add_expense(ambrogio,new_message,False,message.date,message.sender)

		elif ('|' in msg) and (('+' in msg) or ('*' in msg)):	# normal add expense case (even split)
			handle_pos = msg.find('|')
			new_message = ""
			if ':' in msg:
				source = msg[0:2]
			else:
				source="XY"

			new_message += msg[0:handle_pos+1]
			user_string = msg[handle_pos+1:]
			users = user_string.split(',')
			size = len(users)
			count = 0
			users_set = set()

			for user in users:
				add_index = user.find('+')
				mul_index = user.find('*')
				index = -1

				if add_index != -1 and mul_index != -1:

					index = min(add_index,mul_index)

					user_name = user[:index]
					
				else:
					add_index = (10000 if add_index == -1 else add_index)
					mul_index = (10000 if mul_index == -1 else mul_index)

					index = min(add_index,mul_index)
					user_name = user[:index]

				if len(user_name) == 2:
					users_set.add(user_name)
					count += 1
					new_message += (user_name + user[index:])
					new_message += ','

				else:
					group_name = user_name
					if group_name in db:
						for x in db[group_name]:
							new_message += (x + user[index:])
							new_message += ","
							users_set.add(x)
							count += 1
					else:
						return
			
			if len(users_set) != count:
				return

			new_message = new_message[:-1]


			UnevenSplit.uneven_split(ambrogio,new_message,False,message.date,message.sender)