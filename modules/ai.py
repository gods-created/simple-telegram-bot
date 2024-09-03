import os
import boto3
import threading
import random
import string
import json
import base64
from loguru import logger
from botocore.response import StreamingBody

class AI:
    def __init__(self):
        pass
    
    def __enter__(self):
        self.bedrock_client = boto3.client(
            'bedrock-runtime',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name='us-east-1'
        )
        
        return self
        
    def __generate_image_name(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(50)) + '.png'
        
    def __save_image_local(self, body: StreamingBody, image_name: str):
        image_data = json.loads(body.read())
        base64_image = image_data.get('images')[0]
        base64_bytes = base64_image.encode('ascii')
        image_bytes = base64.b64decode(base64_bytes)
        
        with open(image_name, 'wb') as image:
            image.write(image_bytes)
        
    async def generate_image(self, text: str) -> dict:
        response_json = {
            'status': 'error',
            'response': '',
            'image_name': ''
        }
        
        try:
            invoke_model_response = self.bedrock_client.invoke_model(
                modelId='amazon.titan-image-generator-v1',
                body=f'{{"textToImageParams":{{"text":"{text}"}}, "taskType":"TEXT_IMAGE", "imageGenerationConfig":{{"cfgScale":8, "seed":0, "width":1024, "height":1024, "numberOfImages":1}}}}'
            )
            
            body = invoke_model_response.get('body')
            if body is None:
                response_json['response'] = 'The image din\'t created.'
                return response_json
            
            image_name = self.__generate_image_name()
            self.__save_image_local(body, image_name)
            
            response_json['status'] = 'success'
            response_json['response'] = 'The image is preparing.'
            response_json['image_name'] = image_name
            
        except Exception as e:
            response_json['response'] = str(e)
        
        finally:
            logger.debug(response_json)
            return response_json
        
    def __exit__(self, *args):
        self.bedrock_client.close()

    
