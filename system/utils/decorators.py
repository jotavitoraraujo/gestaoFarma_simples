### --- IMPORTS --- ###
from typing import Any
import time as t
import functools as ft
import logging as log
##############

def timer(func):
    'this decorator is intended to be a timer, measuring how long algorithms take to complete their tasks'
    
    @ft.wraps(func)
    def wrapper(*args, **kwargs):
        start_time: float = t.perf_counter()
        result: Any = func(*args, **kwargs)
        end_time: float = t.perf_counter()
        elapsed_time: float = end_time - start_time
        log.info(f'[PERFORMANCE] Função: {func.__name__} | Tempo p/ conclusão: {elapsed_time:.4f} segundos.')
        return result
    return wrapper