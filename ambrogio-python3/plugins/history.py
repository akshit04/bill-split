from datetime import datetime
class History():


	def history(ambrogio,message):
		def convert(date):
			p = []
			for i in date:
				p.append(i)
			p.sort(key=lambda date: datetime.strptime(date, '%d %b %Y'))	# sorting the dates
			return p
		user = message.sender
		temp_storage=ambrogio.store
		dates = set()
		map = {}
		con = {'01': 'Jan',  '02':  'Feb',
			   '03': 'Mar', '04' :  'Apr',
			   '05': 'May', '06':   'Jun',
			   '07': 'Jul', '08':  'Aug',
			   '09': 'Sep', '10': 'Oct',
			   '11': 'Nov', '12': 'Dec', }

		for x in temp_storage:
			if x[0:2] == user or x[2:4] == user:
				# extracting year, month, date from the key of temp_storage
				yy = x[4:8]
				mm = con[x[9:11]]
				dd = x[12:14]
				date = dd + ' ' + mm + ' ' + yy
				if date not in map:
					map[date] = []


				map[date].append(x)
				dates.add(date)		# dates is a set declared above


		dates = convert(dates)
		ans = ""
		for date in dates:
			for user_info in map[date]:
				p = user_info[4:14]
				dd = p[8:]
				mm = p[5:7]
				yy = p[2:4]
				details = user_info[14:]

				if ((user_info[0:2] == user) and (user_info[2:4] != user)):
					if len(details)==0:
						ans += dd + '/' + mm + '/' + yy + ' - you get back ' + temp_storage[user_info] + '\n'
					else:
						ans += dd + '/' + mm + '/' + yy + ' ' + details + ' - you get back ' + temp_storage[user_info] + '\n'

				elif ((user_info[2:4] == user) and (user_info[0:2] != user)):
					if len(details)==0:
						ans += dd + '/' + mm + '/' + yy + ' - you pay back ' + temp_storage[user_info] + '\n'
					else:
						ans += dd + '/' + mm + '/' + yy + ' ' + details + ' - you pay back ' + temp_storage[user_info] + '\n'


		if len(ans) == 0:
			ambrogio.send_text("Done")
		else:
			ans=ans[:-1]
			ambrogio.send_text(ans)