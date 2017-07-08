class UrlMiddleware:
    def process_view(self, request, view_func, view_args, view_kwargs):
        print request.path
        if request.path not in ['/user/login/',
                                '/user/login_handle/',
                                '/user/register/',
                                '/user/register_handle/',
                                '/user/register_valid/',
                                '/user/logout/',
                                ]:
            request.session['url_path'] = request.get_full_path()