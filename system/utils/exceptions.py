### --- IMPORTS --- ###
import xml.etree.ElementTree as ET
from datetime import datetime

### --- CLASS CONVERSION ERROR --- ###
class ConversionError(Exception):
    'an exclusive class for custom erros'

    def __init__(self, error_message: str, error_input = None, error_original = None):
        super().__init__(error_message)
        self.error_input = error_input
        self.error_original = error_original
        self.timestamp = datetime.now()

    def __str__(self):
        main_message = self.args[0]
        timestamp_formated = self.timestamp.strftime('%d/%m/%Y, %H:%M:%S')
        info_message = (
            f'''
            [ERROR]: Timestamp: {timestamp_formated}
            [ERROR]: Conversion Error: {main_message}
            [ERROR]: Corrupted Data is: {self.error_input}
            '''
            )
        if self.error_original:
            type_error_original = type(self.error_original).__name__
            info_message += f'[ERROR]: Main Cause: {type_error_original}'
        
        return info_message

### --- CLASS MISSING TAG ERROR --- ###
class MissingTagError(ValueError):
    'an exclusive class for missing tags of the xml'

    def __init__(self, error_message: str, missing_tag: list[str] = None, nItem_det: str = None):
        super().__init__(error_message)
        self.missing_tag = missing_tag
        self.nItem_det = nItem_det
        self.timestamp = datetime.now()

    def __str__(self):
        main_message = self.args[0]
        timestamp_formated = self.timestamp.strftime('%d/%m/%Y, %H:%M:%S')
        info_message = (
            f'''
            [ERRO]: Timestamp: {timestamp_formated}
            [ERRO]: Tag Error: {main_message}
            [ERRO]: The elements of the list with tags missing data is: {self.missing_tag}
            [ERRO]: The DET Number with missing tag data is: {self.nItem_det}
            '''
        )
        return info_message