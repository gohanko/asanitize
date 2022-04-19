import time

from asanitize.services.discord import session

class HTTPMiddleware:
    def get(self, url):
        response = session.get(url)

        if response.status_code == 429:
            sleep_interval = int(response.headers.get('retry-after'))
            time.sleep(sleep_interval)
            return self.get(url)

        return response
    
    def patch(self, url, content):
        response = session.patch(
            url, 
            headers={'Content-type': 'application/json'}, 
            json={'content': content}
        )

        if response.status_code == 429:
            sleep_interval = int(response.headers.get('retry-after'))
            time.sleep(sleep_interval)
            return self.patch(url, content)

        return response

    def delete(self, url):
        response = session.delete(url)

        if response.status_code == 429:
            sleep_interval = int(response.headers.get('retry-after'))
            time.sleep(sleep_interval)
            return self.delete(url)

        return response