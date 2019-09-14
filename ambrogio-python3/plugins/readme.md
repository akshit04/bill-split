FILE DESCRIPTION:

	treasurer.py:

		It contains a menu-driven program, which passes on the message to relevant file based on few
		checks.
		Ex. if the message.text contains "CREATE" in it, then it should be passed to the file
		create_group.py through the menu-driven block.

		There's only one catch in this, when the user spends the bill (LQ: 132|AB,XY "Uber"), then
		this type of command has to be differentiated from uneven_split and add_expense. So we would
		use the search for '+' and '*' in the message.text, and if found the menu-driven should call
		uneven_split, else add_expense.


	add_expense.py:

		This will be called when there is a '|' in the message, but no '+' and '*' in the message.

		It adds the expenses in the store (dictionary initialized in ambrogio/bot.py).
		The key is taken as the combination of source + user + date + detail (detail is not taken
		if it is not provided in message.text).

		* source - who spent the money
		* user - who has to pay back to source (i.e., the one was involved in an expense, for which
		  someone else paid)
		* date - date of the expenditure
		* detail - the message involved (such as "Uber", "Take Away")

		add_expense can be called either directly, when an expense message is put on the Slack, or
		it is called from the create_group, after the group has been replaced by the actual member
		of the group, and then add_expense is called with the new mwssage (where the groups has been
		replaced by it's actual members).


	uneven_split:

		This will be called when there is a '|' in the message, and also '+' and '*' in the message.

		It functions pretty much same as add_expense (in terms of adding the expenditure in store
		dictionary).

		The logic can be easily deduced from the code. An array has been maintained to keep a track
		of '+' and '*' values, and later the contribution_per_person has been calculated accordingly.

		Just like add_expense, this can also be called directly from the message input in Slack, or
		from the create_group.


	create_group.py:

		It will simply replace the group with it's group members, then it will check if all users are
		distict in the expenditure, and if so, it will call add_expense or uneven_split according to
		the message (those conditions can be easily understood from the code).


	create_group_dict.py:

		It simply maintains a dictionary for the distinct groups, and the members in those groups.
		* key - group_name
		* value - list of group members added in the group_name


	history.py:

		It retreives data from the store dictionary. And search for the user in the key
		(source+user+date+detail), and if the user is found in the key, it sends it's history to
		ambrogio.send_text() including the amount, which can be retrieved from the value of the
		corresponding key.

		The user has to either "pay back" or "get back" the amount, which can be checked if the user
		is present at the source postition or user position in the key (since key is the combination
		of source+user+date+detail).

		If it is at source position, it will "get back" the money, else he/she has to "pay back".



	balance.py:

		It retreives data from the store dictionary, and make use of a 2-D graph to find the minimum
		cash flow. The code has been commented well to describe the logic of the applied algorithm.
