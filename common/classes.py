import hashlib

class DocContent(str):
    pass

class Url(str):
    def hash(self) -> str:
        return hashlib.md5(self.encode()).hexdigest()[:8].lower()

class OfferID(str):
    pass