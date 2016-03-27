import decode, isPlaying
import time
from phue import Bridge

if __name__ == "__main__":
	hue_bridge = Bridge("192.168.0.58")
	
	dim_command = {'transitiontime' : 10, 'on' : True, 'bri' : 25}
	bright_command = {'transitiontime' : 40, 'on' : True, 'bri' : 230}

	playStatus = 0
	revisionNumber = 1
	while (True):
		newStatus = isPlaying.get_status(revisionNumber, 1)
		newPlayStatus = isPlaying.play_status(newStatus)
		oldRevisionNumber = revisionNumber
		revisionNumber = isPlaying.revision_number(newStatus)

		if (newPlayStatus != playStatus):
			playStatus = newPlayStatus

			if (playStatus == 4):
				hue_bridge.set_group(1, dim_command)
				print "playing"
			elif (playStatus == 3):
				hue_bridge.set_group(1, bright_command)
				print "paused"
			else:
				print "unknown: {}".format(playStatus)
				revisionNumber = oldRevisionNumber

