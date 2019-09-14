class UnevenSplit():
	def uneven_split(ambrogio,message,flag=True,date='',source=''):

		if flag==True:
			msg = message.text
			date = message.date
			source = message.sender
		else:
			msg = message
			date = date
			source = source
		index_of_handle = msg.find('|')
		amount = round(float(msg[0:index_of_handle]),2)

		if '"' in msg:
			detail_index = msg.find('"')
			msg = msg[index_of_handle+1:detail_index-1]

		else:	
			msg = msg[index_of_handle+1:]

		users = msg.split(',')
		l = [0,0]
		person_contribution = dict()
		for user in users:
			index_of_plus = -1
			index_of_mul = -1
			x_mul = 1
			x_add = 0
			
			if user.find('+'):
				index_of_plus = user.find('+')

			if user.find('*'):
				index_of_mul = user.find('*')

			if index_of_mul != -1:

				if index_of_plus != -1:
					if index_of_plus < index_of_mul:
						x_mul = round(float(user[index_of_mul+1:len(user)]),2)
					else:
						x_mul = round(float(user[index_of_mul+1:index_of_plus]),2)
				else:
					x_mul = round(float(user[index_of_mul+1:len(user)]),2)


			if index_of_plus != -1:

				if index_of_mul != -1:
					if index_of_mul < index_of_plus:
						x_add = round(float(user[index_of_plus+1:len(user)]),2)
						if x_add > amount:
							ambrogio.send_text("Done")
							return
					else:
						x_add = round(float(user[index_of_plus+1:index_of_mul]),2)
						if x_add > amount:
							ambrogio.send_text("Done")
							return
				else:
					x_add = round(float(user[index_of_plus+1:len(user)]),2)
					if x_add > amount:
						ambrogio.send_text("Done")
						return


			l[0] += x_mul
			l[1] += x_add
			person_contribution[user[:2]] = (x_mul,x_add)

		if amount>0:
			amount -= l[1]
			amount /= l[0]


		date = str(date)
		index = date.find(' ')
		date = date[:index]

		for key,value in person_contribution.items():

			x = value[0]
			y = value[1]


			if '"' in msg:
				store_key = str(source) + str(key) + str(date) + str(detail)
			else:
				store_key = str(source) + str(key) + str(date)
			store_value = str(amount*x+y)
			ambrogio.store_value(store_key,store_value)