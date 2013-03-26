from __future__ import absolute_import
from storages.backends.s3boto import S3BotoStorage

class FixedStorageMixin(object):
    def url(self, name):
        url = super(FixedStorageMixin, self).url(name)
        if name.endswith('/') and not url.endswith('/'):
            url += '/'
        return url

class StaticRootS3BotoStorage(FixedStorageMixin, S3BotoStorage):
    "S3 storage backend that sets the static bucket."
    def __init__(self, *args, **kwargs):
        super(StaticRootS3BotoStorage, self).__init__(location='static',
                                              *args, **kwargs)
class MediaRootS3BotoStorage(FixedStorageMixin, S3BotoStorage):
    "S3 storage backend that sets the media bucket."
    def __init__(self, *args, **kwargs):
        super(MediaRootS3BotoStorage, self).__init__(location='media',
                                              *args, **kwargs)
        