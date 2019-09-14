class AddExpense():
	def add_expense(ambrogio,message,flag = True,date='',source=''):	# ADD EXPENSE
		
		if flag:
			msg = message.text
			date = message.date
			source = message.sender
		else:
			msg = message
			date = date
			source = source

		handle_pos = msg.find('|')
		total_amt = round(float(msg[0:handle_pos]),2)


		last_index = len(msg)-1
		if '"' in msg:	#if there is detail of the expenditure such as "Take away"
			first_quote_pos = msg.find('"')
			people_substring = msg[handle_pos+1 : first_quote_pos-1]

		else:	#no details
			people_substring = msg[handle_pos+1 : last_index+1]
		total_people = 1 + people_substring.count(",")
		amt_per_person = total_amt / total_people
		amt_per_person = round(amt_per_person,2)
		

		# users is the string array of all the people who used the services for which source paid
		# Example:
		# PB: 15|PB,AC
		# source="PB"    users=["PB","AC"]
		users=[]
		i=0
		for x in range(total_people):
			users.append(people_substring[i:i+2])
			i+=3

		date = str(date)
		index = date.find(' ')
		date = date[:index]

		for x in users:

			if '"' in msg:	 #if detail about the expense is present in the message
				#key->source+x+detail (where x is every element in users taken one at a time)
				#source -> person who paid for the service
				#users -> all such persons who need to pay back to source (source might also be one of th users)
				#detail -> information about the expense, ex. "Take Away"
				detail=msg[first_quote_pos+1:last_index]	#detail is the message, ex. "Take Away"
				key=str(source)+str(x)+str(date)+str(detail)

			else:	#if no details present in the message
				#key->source+x (where x is every element in users taken one at a time)
				key=str(source)+str(x)+str(date)
				
			value=str(round(amt_per_person,2))
			ambrogio.store_value(key,value)