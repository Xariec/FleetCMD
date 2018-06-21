from dbOps import ts

def user():
	return {
	'pId' : "", # Id from users profile
	'pName' : "", # Player name
	'pRace' : "", # Player race
	'pCreditBalance' : "", # Player balance
	'pCreditHistory' : [], # History of transactions
	'pJoined' : ts(),
	'pProfile' : {},
	'pIn' : "",
	'suspended' : True,
	'accountConfirmation' : False,
	'registered' : False,
	}
	
