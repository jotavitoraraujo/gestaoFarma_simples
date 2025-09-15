### --- IMPORTS --- ###
from datetime import datetime

### --- CLASS CONVERSIONERROR --- ###
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