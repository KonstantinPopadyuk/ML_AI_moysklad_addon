
from fastapi import HTTPException
import time
from functools import wraps

def retry_request_decorator(function):

    @wraps(function)
    def wrapper(*args, **kwargs):
        retry_attempts = 10
        retry_delay = 30
        for attempt in range(retry_attempts):
            try:
                return function(*args, **kwargs)
            except Exception as e:
                print(f"Error in function {wrapper.__name__} occured on attempt {attempt + 1}: {e}")
                if attempt < retry_attempts - 1:
                    print(f"Another try afet {retry_delay*(attempt+1)} seconds...")
                    time.sleep(retry_delay*(attempt+1))
                else:
                    raise HTTPException(status_code=500, detail=f"All attempts was used. Can't get data. {str(e)}")
    
    return wrapper

def tryexcept_decorator(function):

    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            print(f'Function {wrapper.__name__} was end with Error')
            raise HTTPException(status_code=400, detail=str(e))
        
    return wrapper