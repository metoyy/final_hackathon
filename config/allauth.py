from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def authentication_error(self, request, provider_id, error, exception, extra_context):
        print(f'{error}\n\n{exception}\n\n{extra_context}\n\n{provider_id}\n\n{request}')

