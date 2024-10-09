from io import BytesIO
from PIL import Image
from pytesseract import image_to_string
import requests


class CaptchaMiddleware(object):

    def process_response(self, request, response, spider):
        if response.status == 302 and 'captcha' in response.headers.get('Location', ''):
            captcha_url = 'https://www.example.com/captcha.php'
            captcha_response = requests.get(captcha_url, stream=True)

            if captcha_response.status_code == 200:
                img = Image.open(BytesIO(captcha_response.content))
                captcha = image_to_string(img).strip()
                request.meta['captcha'] = captcha
                return request

        return response