"""Wrapper functions around Django's core cache to implement
stale-while-revalidating cache. Has the standard Django cache
interface. The timeout passed to ``set'' is the time at which
the cache will be revalidated; this is different from the 
built-in cache behavior because the object will still be available
from the cache for MINT_DELAY additional seconds.
"""
from datetime import timedelta

try:
    from django.utils.timezone import now
except ImportError:
    from datetime import datetime
    now = datetime.now

from redis_cache import RedisCache

class Marker(object):
    pass

MARKER = Marker()

# TODO: if item is out of cache and then suddenly gets hits still have the herd problem. this is unlikely tho, but should fix at some point
class RedisHerdCache(RedisCache):
    # HERD_DELAY is an upper bound on how long any value should take to 
    # be generated (in seconds)
    HERD_DELAY = 30
    
    def _pack_value(self, value, timeout):
        """
        Packs a value to include a marker (to indicate that it's a packed
        value), the value itself, and the value's timeout information.
        """
        refresh_time = timedelta(seconds=timeout) + now()
        return (MARKER, value, refresh_time)
    def _unpack_value(self, value, default=None):
        """
        Unpacks a value and returns a tuple whose first element is the value,
        and whose second element is whether it needs to be herd refreshed.
        """
        try:
            marker, unpacked, herd_timeout = value
        except (ValueError, TypeError):
            return value, False
        if not isinstance(marker, Marker):
            return value, False
        if herd_timeout < now():
            return unpacked, True
        return unpacked, False
    
    def get(self, key, default=None, version=None):
        """
        Retrieve a value from the cache.

        Returns unpickled value if key is found, the default if not.
        """
        packed_val = super(RedisHerdCache, self).get(key, default, version)
        if packed_val == default:
            return default
        value, refresh = self._unpack_value(packed_val, default)
        if refresh:
            # Store the stale value while the cache revalidates for another
            # HERD_DELAY seconds.
            super(RedisHerdCache, self).set(key, value, timeout=self.HERD_DELAY, version=version)
            return default
        return value

    def set(self, key, value, timeout=None, version=None, client=None, _add_only=False, herd=True):
        """
        Persist a value to the cache, and set an optional expiration time.
        """
        if timeout is None: timeout = self.default_timeout
        if herd:
            packed_val = self._pack_value(value, timeout)
            real_timeout = timeout + self.HERD_DELAY*4
        else:
            packed_val = value
            real_timeout = timeout
        return super(RedisHerdCache, self).set(key, packed_val, real_timeout, version=version, client=client, _add_only=_add_only)
    
    def add(self, key, value, timeout=None, version=None, herd=True):
        """
        Persist a value to the cache, and set an optional expiration time.
        """
        if timeout is None: timeout = self.default_timeout
        if herd:
            packed_val = self._pack_value(value, timeout)
            real_timeout = timeout + self.HERD_DELAY*4
        else:
            packed_val = value
            real_timeout = timeout
        return super(RedisHerdCache, self).add(key, packed_val, real_timeout, version=version)
    
    def delete(self, key, version=None):
        """
        Remove a key from the cache.
        """
        packed_val = super(RedisHerdCache, self).get(key, None, version)
        if packed_val is not None:
            value, refresh = self._unpack_value(packed_val)
            # protect deletes from thundering herd
            # TODO: fix race condition where delete is executed after another process starts computing, but before they set (they will overwrite)
            self.set(key, value, 0, version)

    def delete_many(self, keys, version=None):
        """
        Remove multiple keys at once.
        """
        packed_resp = super(RedisHerdCache, self).get_many(keys, version)
        
        reinsert = {}
                
        for key, packed in packed_resp.iteritems():
            # If it was a miss, treat it as a miss to our response & continue
            if packed is not None:
                val, refresh = self._unpack_value(packed)
                # TODO: fix race condition where delete is executed after another process starts computing, but before they set (they will overwrite)
                reinsert[key] = val

        if reinsert:
            # protect deletes from thundering herd
            self.set_many(reinsert, 0, version)
    
    
    def get_many(self, keys, version=None):
        packed_resp = super(RedisHerdCache, self).get_many(keys, version)
        
        resp = {}
        reinsert = {}
                
        for key, packed in packed_resp.iteritems():
            # If it was a miss, treat it as a miss to our response & continue
            if packed is None:
                resp[key] = packed
                continue
            
            val, refresh = self._unpack_value(packed)
            if refresh:
                reinsert[key] = val
                resp[key] = None
            else:
                resp[key] = val
        
        # If there are values to re-insert for a short period of time, then do
        # so now.
        if reinsert:
            self._cache.set_multi(reinsert, timeout=self.HERD_DELAY, version=version)
        
        return resp
