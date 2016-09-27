from django.apps import AppConfig


class PostsConfig(AppConfig):
    name = 'posts'
    verbose_name = 'Posts'

    def ready(self):
        # import signal handlers
        import posts.signals
