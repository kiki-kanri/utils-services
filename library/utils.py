from flask import request
from functools import wraps
from importlib import import_module
from kikiutils.check import isint, isstr
from validator import validate as _validate

# from .p2p import node


# Decorators

def validate(rules: dict):
    """Validate request data."""

    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            request_data = request.values.to_dict()

            for k, v in request_data.copy().items():
                if isstr(v):
                    request_data[k] = v.strip()

            result, data, _ = _validate(request_data, rules, True)

            if result:
                kwargs['data'] = data
                return view_func(*args, **kwargs)

            return '', 422

        return wrapped_view

    return decorator


# Import module

def import_attribute(path: str):
    pkg, attr = path.rsplit('.', 1)
    return getattr(import_module(pkg), attr)


# Ip

def ip2int(ip: str):
    """Convert string ip to int."""

    if isint(ip):
        return ip

    int_ip = 0
    for i in ip.split('.'):
        int_ip = int_ip << 8 | int(i)
    return int_ip


def int2ip(int_ip: int):
    """Convert int ip to string."""

    if isstr(int_ip):
        return int_ip

    ip = []

    for _ in range(4):
        ip.append(str(int_ip & 255))
        int_ip >>= 8

    return '.'.join(ip[::-1])


# Request

def get_request_ip():
    return request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
