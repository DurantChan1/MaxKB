# coding=utf-8
"""
    @project: maxkb
    @Author：虎
    @file： request_log_middleware.py
    @date：2026/6/10 13:56
    @desc: 请求日志中间件，在API请求入口打印请求路由、方式和输入参数
"""
from django.utils.deprecation import MiddlewareMixin
from common.utils.logger import maxkb_logger


class RequestLogMiddleware(MiddlewareMixin):

    def process_request(self, request):
        method = request.method
        path = request.path

        if method in {'GET', 'DELETE'}:
            params = dict(request.GET.lists())
            maxkb_logger.info(f'[{method}] {path} params={params}')

        elif method in {'POST', 'PUT', 'PATCH'}:
            content_type = request.META.get('CONTENT_TYPE', '')
            # JSON 请求体
            if 'application/json' in content_type:
                try:
                    body = request.body.decode('utf-8', errors='replace')
                    if len(body) > 2000:
                        body = body[:2000] + '...(truncated)'
                    maxkb_logger.info(f'[{method}] {path} body={body}')
                except Exception as e:
                    maxkb_logger.info(f'[{method}] {path} body=<read error: {e}>')
            # 表单请求（含文件上传）
            elif 'multipart/form-data' in content_type or 'application/x-www-form-urlencoded' in content_type:
                params = dict(request.POST.lists())
                maxkb_logger.info(f'[{method}] {path} params={params}')
            else:
                # 其他 Content-Type，尝试读取 body
                try:
                    body = request.body[:2000]
                    maxkb_logger.info(f'[{method}] {path} content_type={content_type} body={body}')
                except Exception:
                    maxkb_logger.info(f'[{method}] {path} content_type={content_type}')

        else:
            maxkb_logger.info(f'[{method}] {path}')
