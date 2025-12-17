### --- IMPORTS --- ###
from typing import Any
import threading as th
import time as t
import functools as ft
import tracemalloc as tm
import logging as log
import sys
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

def memory_monitor(func):
    'This decorator is intended to measure the amount of memory a given function uses during its execution'

    @ft.wraps(func)
    def wrapper(*args, **kwargs):
        tm.start()
        result: Any = func(*args, **kwargs)
        current, peak = tm.get_traced_memory()
        tm.stop()
        current_mb: int = current / 10**6
        peak_mb: int = peak / 10**6
        log.info(f'[MEMORIA] Função: {func.__name__} | Atual: {current_mb:.2f} MBs | [MEMORIA] Pico Máximo: {peak_mb:.2f} MBs')
        return result
    return wrapper

def run_background(func):
    'This decorator is designed to execute the decorated function/method in another thread, relieving a specific task from the main thread'

    @ft.wraps(func)
    def wrapper(*args, **kwargs):
        def thread_runner():
            try:
                start: t = t.time()
                func(*args, **kwargs)
                end: t = t.time()
                log.info(f'[THREAD] Função: {func.__name__}')
                log.info(f'[SUCESSO] Importação finalizada em {end - start:.2f} segundos')
            except Exception as error:
                log.error(f'[FATAL ERROR] The task executed by the thread failed.')
                log.error(f'[FATAL ERROR] Cause: {error}')

        thread = th.Thread(target = thread_runner, daemon = True)
        thread.start()
        string: str = '[AGUARDE] Processando'
        while thread.is_alive():
            for dots in ['. ', '.. ', '...']:
                sys.stdout.write(f'\r{string}{dots}')
                sys.stdout.flush()
                t.sleep(0.5)
                if not thread.is_alive(): break
        sys.stdout.write('\r' + ' ' * 50 + '\r')
        return thread
    return wrapper

    
