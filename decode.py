# simple message decoder for dacp
# released gplv3 by jeffrey sharkey

import sys, struct, re

# Set up a grouped property list for recursion
GROUPS = ['cmst','mlog','agal','mlcl','mshl','mlit','abro','abar','apso','caci','avdb','cmgt','aply','adbs','cmpa']

# Regex searching for binary data
REBINARY = re.compile('[^\x20-\x7e]')

def pullString(queue, size):
	pull = ''.join(queue[0:size])
	del queue[0:size]
	return pull

def asHex(s): 
	return ''.join([ "%02x" % ord(c) for c in s ])

def asByte(s): 
	return struct.unpack('>B', s)[0]

def asInt(s): 
	return struct.unpack('>I', s)[0]

def asLong(s): 
	return struct.unpack('>Q', s)[0]


def decode(raw, unprocessedLength, indent, root):
	while unprocessedLength >= 8:
		
		# read word data type and length
		propertyType = pullString(raw, 4)
		propertyValueLength = asInt(pullString(raw, 4))

		# Mark the used length as processed 
		unprocessedLength -= 8 + propertyValueLength
		
		# recurse into groups
		if propertyType in GROUPS:
			root[propertyType] = {}
			decode(raw, propertyValueLength, indent + 1, root[propertyType])
		else:
			# read and parse data
			propertyValue = pullString(raw, propertyValueLength)
			
			nice = '%s' % asHex(propertyValue)
			if propertyValueLength == 1: nice = asByte(propertyValue)
			if propertyValueLength == 4: nice = asInt(propertyValue)
			if propertyValueLength == 8: nice = asLong(propertyValue)
			
			if REBINARY.search(propertyValue) is None:
				nice = propertyValue
			
			root[propertyType] = nice
	return root

# Debug-only print helper
def format(c):
	if ord(c) >= 128: return "(byte)0x%02x"%ord(c)
	else: return "0x%02x"%ord(c)

if __name__ == "__main__":
	# Read stdin as raw bytes to an arary
	raw = []
	for c in sys.stdin.read(): raw.append(c)

	# Print a formatted version of the initial string to stdout for debug
	print ','.join([ format(c) for c in raw ])

	# Begin decoding the string
	print decode(raw, len(raw), 0, {})

