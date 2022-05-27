# -*- coding: utf-8 -*-import functoolsimport timeitimport allureimport requests as requestsfrom basecase import BaseAssertfrom log import LOGGERfrom utility import Dict, attr_dictclass ApiClient(BaseAssert):    """    两种方式处理登录    :__init__:设置默认不失效的token    :login:提供跳过验证码的登陆接口    """    def get_method(self, url=None, data=None, header=None, ):        if header is not None:            res = requests.get(url=url, params=data, headers=header)        else:            res = requests.get(url=url, params=data)        return res.json()    def post_method(self, url, data=None, header=None):        if header is not None:            res = requests.post(url, json=data, headers=header)        else:            res = requests.post(url, json=data)        if str(res) == "<Response [200]>":            return res.json()        else:            return res.text    def run_method(self, method=None, url=None, data=None, header=None):        if method == 'get' or method == 'GET':            res = self.get_method(url, data, header)        elif method == 'post' or method == 'POST':            res = self.post_method(url, data, header)        else:            res = "请求方式不正确！"        return resdef api(path=None, method=None):    def wrapper(func):        @functools.wraps(func)        def _wrapper(self, **kwargs):            token = "ea2389592dbe0eda59f38f6f8ebbd396"            # token = yyzx.get_yyzx_token_value            # service_ip = yyzx.get_yyzx_ip_value            service_ip = "36.134.207.64:19092"            url = "http://" + service_ip + path            LOGGER.debug(url)            header = {"token": token}            LOGGER.debug(kwargs)            start = timeit.default_timer()            disable_log = False            with allure.step('req url: {}'.format(url)):                if not disable_log:                    LOGGER.debug("start request",                                 extra=dict(method=method,                                            parameters=kwargs,                                            url=url))                allure.attach(method, "request method")                allure.attach(url, "request url", allure.attachment_type.URI_LIST)                allure.attach(str(kwargs), "request params")                response = self.run_method(method=method, url=url, data=kwargs, header=header)                LOGGER.debug(response)                final_resp = Dict(response)                if not disable_log:                    latency = int((timeit.default_timer() - start) * 1000)                    # 调试用                    if '<html' in response or not response:                        LOGGER.debug("got response", extra=dict(response=response,                                                                latency=latency))                    else:                        LOGGER.debug(                            "got response", extra=dict(response=response,                                                       latency=latency))                if final_resp.code != 0:                    allure.attach(str(response['code']), "response code")                    allure.attach(str(response['msg']), "reponse context")                    allure.attach(str(latency), "response latency")                else:                    allure.attach(str(response['code']), "response code")                    allure.attach(str(response['msg']), "reponse context")                    allure.attach(str(response['data']), "response body")                    allure.attach(str(latency), "response latency")                try:                    return attr_dict(final_resp)                except ValueError:                    return attr_dict(final_resp.json())        return _wrapper    return wrapperget = functools.partial(api, method='get')post = functools.partial(api, method='post')