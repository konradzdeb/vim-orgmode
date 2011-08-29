# -*- coding: utf-8 -*-

"""
	OrgDate
	~~~~~~~~~~~~~~~~~~

	This module contains all date representations that exist in orgmode.

	Types a date can be
	* date
	* datetime
	* timerange

	They can be active or inactive
"""

import datetime
import re


_DATE_REGEX = re.compile(r"<(\d\d\d\d)-(\d\d)-(\d\d) [A-Z]\w\w>")


def get_orgdate(data):
	"""
	Parse the given data. Return an OrgDate if data contains a string
	representation of an OrgDate; otherwise return None.

	data also can be a list.
	"""
	if isinstance(data, list):
		return _findfirst(_text2orgdate, data)
	else:
		return _text2orgdate(data)
	# if no dates found
	return None


def _findfirst(f, seq):
	"""
	Return first item in sequence seq where f(item) == True.

	TODO: this is a general help function and it should be moved somewhere
	else; preferably into the standard lib :)
	"""
	for found in (f(item) for item in seq if f(item)):
		return found


def _text2orgdate(string):
	"""
	Transform the given string into an OrgDate.
	Return an OrgDate if data contains a string representation of an OrgDate;
	otherwise return None.
	"""
	result = _DATE_REGEX.search(string)
	if result:
		try:
			year, month, day = [int(m) for m in result.groups()]
			return OrgDate(True, year, month, day)
		except Exception:
			pass
			#return None
	else:
		pass
		#return None


class OrgDate(datetime.date):
	"""
	OrgDate represents a normal date like '2011-08-29 Mon'.

	OrgDates can be active or inactive.

	NOTE: date is immutable. Thats why there needs to be __new__().
	See: http://docs.python.org/reference/datamodel.html#object.__new__
	"""
	def __init__(self, active, year, month, day):
		self.active = active
		pass

	def __new__(cls, active, year, month, day):
		return datetime.date.__new__(cls, year, month, day)

	def __str__(self):
		if self.active:
			return self.strftime(u'<%Y-%m-%d %a>')
		else:
			return self.strftime(u'[%Y-%m-%d %a]')


class OrgDateRange(object):
	"""
	OrgDate represents a range of dates like
	* <2011-08-29 Mon>--<2011-08-30 Tue>
	* <2011-08-29 Mon 10:12>--<2011-08-29 Mon 14:30>
	* [2011-08-29 Mon]--[2011-08-30 Tue]
	* [2011-08-29 Mon 12:00]--[2011-08-30 Tue 14:00]
	"""
	def __init__(self):
		super(OrgDateRange, self).__init__()

# vim: set noexpandtab:
