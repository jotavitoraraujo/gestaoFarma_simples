from datetime import datetime
from typing import Any

class GestaoFarmaBaseError(Exception):
    def __init__(self, message: str, error_input: Any = None, error_original: Any = None):
        super().__init__(message)
        self.error_input = error_input
        self.error_original = error_original
        self.timestamp = datetime.now()

    def __str__(self):
        main_message: str = self.args[0]
        timestamp_fmt: datetime = self.timestamp.strftime('%d/%m/%Y, %H:%M:%S')
        class_name = self.__class__.__name__
        report: str = (
            f'''
                \n[ERRO]: Timestamp: {timestamp_fmt}
                \n[ERRO]: Exceptoion Type: {class_name}
                \n[ERRO]: Message: {main_message}
            '''
        )
        if hasattr(self, 'error_input') and self.error_input is not None:
            report += f'\n[ERRO] Context Data (Input): {self.error_input}'
        if hasattr(self, 'error_original') and self.error_original is not None:
            original_type: Any = type(self.error_original).__name__
            report += f'\n[ERRO] Root Cause: {original_type} -> {self.error_original}'
        return report

class ConversionError(GestaoFarmaBaseError):
    def __init__(self, message: str, error_input: Any = None, error_original: Any = None):
        super().__init__(message)
        self.error_input = error_input
        self.error_original = error_original

class UserAlreadyExistsError(GestaoFarmaBaseError):
    def __init__(self, message: str, error_input: Any = None, error_original: Any = None):
        super().__init__(message)
        self.error_input = error_input
        self.error_original = error_original
    
class ProductNotFoundError(GestaoFarmaBaseError):
    def __init__(self, message: str, error_input: Any = None, error_original: Any = None):
        super().__init__(message)
        self.error_input = error_input
        self.error_original

class InsufficientStockError(GestaoFarmaBaseError):
    def __init__(self, message: str, error_input: Any = None, error_original: Any = None):
        super().__init__(message)
        self.error_input = error_input
        self.error_original = error_original

class CartEmptyError(GestaoFarmaBaseError):
    def __init__(self, message: str, error_input: Any = None, error_original: Any = None):
        super().__init__(message)
        self.error_input = error_input
        self.error_original = error_original