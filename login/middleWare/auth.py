import re
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

EXEMPT_URLS=[]
if hasattr(settings,'LOGIN_EXEMPT_URLS'):
	EXEMPT_URLS+=[re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]


class AuthenticationMiddleware(object):
	def __init__(self, get_response):
		self.get_response = get_response
		# One-time configuration and initialization.

	def __call__(self, request):
		# Code to be executed for each request before
		# the view (and later middleware) are called.
		path=request.path_info.lstrip('/')
		url_is_exempt=any(url.match(path) for url in EXEMPT_URLS)
		if url_is_exempt!=True:
			print('checking....')
			if request.session.get('logged',False) is not True:
				print('Redirecting .....')
				return HttpResponseRedirect('/login/')
		path = request.path_info
		if path=='/':
			print('Redirecting .....')
			return HttpResponseRedirect('/home/')
		response = self.get_response(request)
		return response
