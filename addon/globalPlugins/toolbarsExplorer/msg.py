# -*- coding: UTF-8 -*-
# A simple module to bypass the addon translation system,
# so it can take advantage from the NVDA translations directly.
# Copyright 2018 Alberto Buffolino, released under GPL

def message(message):
	"""Return translated message according to NVDA local translations."""
	if message == "":
		# blank string translated reports NVDA information, so...
		return message
	return _(message)
