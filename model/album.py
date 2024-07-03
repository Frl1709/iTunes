from dataclasses import dataclass


@dataclass
class Album:
    AlbumId: int
    Title: str
    ArtistId: int
    totD: int

    def __hash__(self):
        return hash(self.AlbumId)

    def __str__(self):
        return f"{self.Title} -- {round(toMinutes(self.totD),2)}"

def toMinutes(d):
    return d/1000/60