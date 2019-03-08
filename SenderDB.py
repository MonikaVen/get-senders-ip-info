import FillSenders

file_name = 'IP_list_biggest_senders.csv'
print('Database name is: InfoSenders, table name: senders')
print()
print('1. Add IPs from csv file.')
print('2. Add single IP to command line.')
choice = input('Please select a choice number: ')
print(choice)
if choice == '1':
	print("""Would you like to use another file? (default is 'IP_list_biggest_senders.csv')""")
	file_choice = input(""" If yes, enter 'f', for defaults just press 'Enter'""")
	if file_choice == 'f':
		file_name = input('Please enter a csv file address to read IPs from: ')
		FillSenders.RunOnFile(file_name)
	else:
		FillSenders.RunOnFile(file_name)
elif choice == '2':
	IP_string = input("Enter IP that you would like to put in a DB: ")
	FillSenders.RunOnIP(IP_string)




