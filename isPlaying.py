import requests
import decode
import sys

def fetch_status(revisionNumber, sessionId):
	try:
		response = requests.get(
				url="http://192.168.0.52:3689/ctrl-int/1/playstatusupdate",
				params={
					"revision-number": str(revisionNumber),
					"session-id": str(sessionId),
					},
				)
		return response.content
	except requests.exceptions.RequestException:
		print('HTTP Request failed')

def fetch_login(pairingCode)
	try:
		response = requests.get(
				url="http://192.168.0.52:3689/login",
				params={
					"pairing-guid": str(pairingCode),
					},
				)
		return response.content
	except requests.exceptions.RequestException:
		print('HTTP Request failed')

def login(pairingCode):
	content = list(login(pairingCode))
	return decode.decode(content, len(content), 0, {})

def get_session_id(login_result):
	return login_result["mlog"]["mlid"]

def get_status(revisionNumber, sessionId):
	content = list(fetch_status(revisionNumber, sessionId))
	return decode.decode(content, len(content), 0, {})

def revision_number(status):
	return status["cmst"]["cmsr"]

def play_status(status):
	return status["cmst"]["caps"]

if __name__ == "__main__":
	playStatus = play_status(get_status(1,1))

	if playStatus == 4:
		print("Playing")
		sys.exit(1)
	else:
		print("Not playing")
		sys.exit(0)

