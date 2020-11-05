import re
import smtplib
import dns.resolver

fromAddress = 'mailtest@gmail.com'

# Simple Regex for syntax checking
regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'

filename = input('Filename or Path:')
file = open(filename, 'r')
Lines = file.readlines()

for line in Lines:
	inputAddress = str(line.strip())
	print("********       {}       ***********".format(inputAddress))
	addressToVerify = str(inputAddress)

	# Syntax check
	match = re.match(regex, addressToVerify)
	if match == None:
		print('Bad Syntax')
	else:
		# Get domain for DNS lookup
		splitAddress = addressToVerify.split('@')
		domain = str(splitAddress[1])
		print('Domain:', domain)

		# MX record lookup
		try:
			records = dns.resolver.query(domain, 'MX')
		except dns.resolver.NXDOMAIN:
			print("domain not found")
		except: 
			print("domain not found 2 ")
		mxRecord = records[0].exchange
		mxRecord = str(mxRecord)
		print('MX: ', mxRecord)

		server = smtplib.SMTP()
		server.set_debuglevel(0)

		# SMTP Conversation
		try:
			server.connect(mxRecord)
			server.helo(server.local_hostname)
			server.mail(fromAddress)
			code, message = server.rcpt(str(addressToVerify))
			server.quit()
			# if the rcpt is accepted, the code will be 250
			if code == 250:
				print('Email exists')
			else:
				print('Email not exists')
		except:
			print('There seems to be a problem connecting with the server :C')
