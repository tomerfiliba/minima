import re
import functools
import inspect
import json
import sys
import traceback
from minima.webapp2_integration.base import IS_DEBUG_SERVER


class ValidationError(Exception):
    HTTP_STATUS = 401

class APIException(Exception):
    HTTP_STATUS = 500

def json_api(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        jsonobj = {"success" : True, "error" : None, "data" : None}
        try:
            result = func(self, *args, **kwargs)
            try:
                json.dumps(result)
            except Exception:
                if IS_DEBUG_SERVER:
                    raise
                raise APIException("JSON encoding error")
            jsonobj["data"] = result
        except (APIException, ValidationError) as ex:
            jsonobj["error"] = str(ex)
            if IS_DEBUG_SERVER:
                jsonobj["traceback"] = "".join(traceback.format_exception(*sys.exc_info()))
            self.response.set_status(ex.HTTP_STATUS)
        except Exception as ex:
            jsonobj["error"] = type(ex).__name__
            if IS_DEBUG_SERVER:
                jsonobj["traceback"] = "".join(traceback.format_exception(*sys.exc_info()))
            self.response.set_status(500)
        
        data = json.dumps(jsonobj)
        self.response.headers.add_header('Content-type', 'application/json')
        self.response.out.write(data)
    
    return wrapper


def validate(**kwargs):
    def deco(func):
        args, _, _, defaults = inspect.getargspec(func)
        if not defaults:
            with_defaults = ()
        else:
            with_defaults = set(args[-len(defaults):])
        @functools.wraps(func)
        def wrapper(self):
            func_kwargs = {}
            matched = set()
            for arg_name, validator in kwargs.items():
                info = validator._validation_info if hasattr(validator, "_validation_info") else {}
                param_name = info.get("param_name", arg_name)
                values = self.request.get_all(param_name)
                matched.add(param_name)
                if not values and arg_name in with_defaults:
                    continue
                try:
                    if info.get("list"):
                        func_kwargs[arg_name] = validator(values)
                    elif not values:
                        raise ValueError("No value specified")
                    elif len(values) != 1:
                        raise ValueError("Expected a single value, got %r" % (len(values,)))
                    else:
                        func_kwargs[arg_name] = validator(values[0])
                except Exception as ex:
                    raise ValidationError("Parameter %r: %s" % (param_name, ex))

            # Don't allow unknown parameters
            unknown = set(self.request.arguments()) - matched
            if unknown:
                raise ValidationError("Unknown parameters: %s" % (", ".join(unknown),))
            return func(self, **func_kwargs)
        return wrapper
    return deco

def _set_info(validator, child_validator, **kwargs):
    validator._validation_info = child_validator._validation_info if hasattr(child_validator, "_validation_info") else {}
    validator._validation_info.update(kwargs)

def list_of(validator, minlen = 1, maxlen = None):
    def list_validator(values):
        if not isinstance(values, (list, tuple)):
            raise ValueError("Expected a list")
        if len(values) < minlen:
            raise ValueError("Expected at least %d items" % (minlen,))
        if maxlen is not None and len(values) > maxlen:
            raise ValueError("Expected at most %d items" % (maxlen,))
        return [validator(v) for v in values]
    _set_info(list_validator, validator, list = True)
    list_validator.__name__ = "list_of(%s)" % (validator.__name__,)
    return list_validator

def regexp(pattern, flags = 0):
    pat = re.compile(pattern, flags)
    def validator(value):
        match = pat.match(value)
        if not match:
            raise ValueError("Does not match regexp")
        return match
    validator.__name__ = "regexp(%r)" % (pattern,)
    return validator

def param_name(validator, field_name):
    def validator2(values):
        return validator(values)
    _set_info(validator2, validator, field_name = field_name)
    validator2.__name__ = "param_name(%s, %r)" % (validator.__name__, field_name)
    return validator2

