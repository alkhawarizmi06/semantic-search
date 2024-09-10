class Document:
    def __init__(self, url, title, score):
        self.url = url
        self.title = title
        self.score = score

    def to_dict(self):
        return {
            "url": self.url,
            "title": self.title,
            "score": self.score
        }

