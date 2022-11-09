import base64
import requests

from flask import Blueprint, jsonify, request
from kikiutils.check import isstr

from ..main.dun360 import Dun360


uncaptcha_api = Blueprint('uncaptcha_api', __name__, url_prefix='/uncaptcha')


@uncaptcha_api.post('/dun360')
def uncaptcha_dun360():
    bg = (
        request.values.get('bgUrl')
        or request.files.get('bgFile')
    )

    slide = (
        request.values.get('slideUrl')
        or request.files.get('slideFile')
    )

    if not bg or not slide:
        return '', 422

    dun360 = Dun360(bg, slide)
    result = dun360.get_slide_move_x()
    return jsonify(result)


@uncaptcha_api.post('/sogou')
def uncaptcha_sogou():
    image = (
        request.values.get('imageBase64')
        or request.files.get('imageFile')
    )

    if not image:
        return '', 422

    if isstr(image):
        response = requests.post(
            'http://127.0.0.1:12004/ocr/b64/text',
            data=image
        )
    else:
        response = requests.post(
            'http://127.0.0.1:12004/ocr/file',
            {
                'image': image
            }
        )

    return response.text
