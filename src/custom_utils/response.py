#!/user/bin/env python
# -*- encoding: utf-8 -*-

'''
@描述：自定义响应

'''


from fastapi.responses import JSONResponse, Response
from typing import Union


def response_success(*, data: Union[list, dict, str, int]) -> Response:
    """成功响应

    Args:
        data (Union[list, dict, str]): 返回的数据

    Returns:
        Response: 
    """    
    return JSONResponse(status_code=200,
                        content={
                            "code": 200,
                            "message": "success",
                            "data": data
                        })


def response_error(*,
                   data: str = None,
                   message: str = "BAD REQUEST",
                   code=400) -> Response:
    """响应错误

    Args:
        data (str, optional): 错误数据. Defaults to None.
        message (str, optional): 返回的错误信息. Defaults to "BAD REQUEST".
        code (int, optional): 错误状态码. Defaults to 400.

    Returns:
        Response: 
    """                   
    if code < 400:
        code = 400
    return JSONResponse(status_code=code,
                        content={
                            "code": code,
                            "message": message,
                            "data": data
                        })
