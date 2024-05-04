from request_factory import RequestFactory

class GetRequestFactory(RequestFactory):

    def create_request(self, url):
        response = self.rest_client.request(method_name='get', url=url)
        return response
    
