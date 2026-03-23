import time

from app.utils.cache import TTLCache


def test_set_and_get():
    cache = TTLCache(ttl=10.0)
    cache.set("key", "value")
    assert cache.get("key") == "value"


def test_get_missing_key_returns_none():
    cache = TTLCache(ttl=10.0)
    assert cache.get("nonexistent") is None


def test_expired_entry_returns_none():
    cache = TTLCache(ttl=0.05)
    cache.set("key", "value")
    time.sleep(0.1)
    assert cache.get("key") is None


def test_delete_removes_entry():
    cache = TTLCache(ttl=10.0)
    cache.set("key", "value")
    cache.delete("key")
    assert cache.get("key") is None


def test_evict_removes_expired_entries():
    cache = TTLCache(ttl=0.05)
    for i in range(10):
        cache.set(f"key_{i}", i)
    time.sleep(0.1)
    cache._evict()
    assert len(cache._store) == 0


def test_overwrite_resets_ttl():
    cache = TTLCache(ttl=0.1)
    cache.set("key", "old")
    time.sleep(0.07)
    cache.set("key", "new")
    time.sleep(0.07)
    assert cache.get("key") == "new"
