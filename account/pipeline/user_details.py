from account.models import Profile

from requests import request, HTTPError

from django.core.files.base import ContentFile

            
def get_profile_picture(backend, user, response, details,
                         is_new=False,*args,**kwargs):
    url = None
    profile = Profile.objects.get_or_create(user=user)[0]

    if is_new and backend.name == 'facebook':
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']

        try:
            response = request('GET', url)
            response.raise_for_status()
        except HTTPError:
            pass
        else:
            profile.photo.save('{0}_social.jpg'.format(user.username),
                                   ContentFile(response.content))
    
    elif is_new and backend.name == "twitter":
    
        if response['profile_image_url'] != '':
            if not response.get('default_profile_image'):
                avatar_url = response.get('profile_image_url_https')
                if avatar_url:
                    avatar_url = avatar_url.replace('_normal.', '_bigger.')
        try:
            response = request('GET', avatar_url)
            response.raise_for_status()
        except HTTPError:
            pass
        else:
            profile.photo.save('{0}_social.jpg'.format(user.username),
                                   ContentFile(response.content))
        profile.save()

    elif backend.name == "google-oauth2":
        if response['image'].get('url') is not None:
            avatar_url_gmail = response['image'].get('url')
        try:
            response = request('GET', avatar_url_gmail)
            response.raise_for_status()
        except HTTPError:
            pass
        else:
            profile.photo.save('{0}_social.jpg'.format(user.username),
                                   ContentFile(response.content))
        profile.save()
