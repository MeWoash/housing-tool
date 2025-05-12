import hashlib

class DocContent(str):
    pass

class Url(str):
    def hash(self) -> str:
        return hashlib.md5(self.encode()).hexdigest()[:8].lower()
    
class SubUrl(str):
    """
    Part of URL without http(s) / base URL.
    """
    pass

class OfferId(str):
    pass

