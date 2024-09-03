import os
from loguru import logger

class Env:
    file_dir = '.env'
    
    @classmethod
    def create(cls) -> bool:
        try:
            file_dir = cls.file_dir
            if not os.path.exists(file_dir):
                logger.error('.env file not found!')
                return False
                
            with open(file_dir, 'r') as file:
                list_data = file.readlines()
            
            if len(list_data) == 0:
                logger.error('.env file has no data!')
                return False
            
            json_data = {
                value.split('=')[0].strip(): value.split('=')[1].strip().replace('\n', '')
                for value in list_data if len(value.split('=')) == 2
            }
            
            for key in json_data.keys():
                value = json_data.get(key, '')
                os.environ[key] = value
            
            logger.success('Environment created!')
            return True
        
        except Exception as e:
            logger.error(str(e))
            return False
