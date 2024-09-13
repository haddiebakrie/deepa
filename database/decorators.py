from functools import wraps
import psycopg2

def failSilent(func):
    def wrapper(*args, **kwargs):

        try:
            return func(*args, **kwargs)
        
        except:
           pass

    return wrapper

def failNoise(func):
    def wrapper(*args, **kwargs):

        try:
            return func(*args, **kwargs)

        except Exception as e:
           print(e)

    return wrapper


def db_error_handler(func):

    def wrapper(*args, **kwargs):

        try:
            return func(*args, **kwargs)
        
        except Exception as e:
            print(f"Database error occurred: {e}")

    return wrapper