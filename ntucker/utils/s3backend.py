from __future__ import absolute_import
import gzip
from django.core.files.storage import get_storage_class
from storages.backends.s3boto import S3BotoStorage
from cached_s3_storage import CachedS3BotoStorage

class FixedStorageMixin(object):
    def url(self, name):
        url = super(FixedStorageMixin, self).url(name)
        if name.endswith('/') and not url.endswith('/'):
            url += '/'
        return url

class CachedRootS3BotoStorage(FixedStorageMixin, CachedS3BotoStorage):
    "S3 storage backend that sets the static bucket."
    def __init__(self, *args, **kwargs):
        kwargs['location'] = 'static'
        super(CachedRootS3BotoStorage, self).__init__(*args, **kwargs)
class StaticRootS3BotoStorage(CachedRootS3BotoStorage):
    "S3 storage backend that sets the static bucket."
    def __init__(self, *args, **kwargs):
        kwargs['gzip'] = False
        super(StaticRootS3BotoStorage, self).__init__(*args, **kwargs)

class MediaRootS3BotoStorage(FixedStorageMixin, S3BotoStorage):
    "S3 storage backend that sets the media bucket."
    def __init__(self, *args, **kwargs):
        super(MediaRootS3BotoStorage, self).__init__(location='media',
                                              *args, **kwargs)
        