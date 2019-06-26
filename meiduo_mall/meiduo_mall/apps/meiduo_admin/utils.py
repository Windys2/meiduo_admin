from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


def jwt_response_payload_handler(token, user=None, request=None):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.

    Example:

    def jwt_response_payload_handler(token, user=None, request=None):
        return {
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }

    """
    return {
        'token': token,
	    'username':user.username,
	    'id':user.id

    }


class PageNum(PageNumberPagination):
	page_size_query_param = 'pagesize'
	page_size = 5
	max_page_size = 10

	def get_paginated_response(self, data):

		return Response(OrderedDict([
			('count', self.page.paginator.count),

			('lists', data),
			('page', self.page.number),
			('pages', self.page.paginator.num_pages),
			('pagesize',self.page_size)
		]))

