from rest_framework import pagination

class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total pages': self.page.paginator.count/page_size,
            'page':self.page_query_param,
            'page_size':self.page_size,
            'results': data
        })
