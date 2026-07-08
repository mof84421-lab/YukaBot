class MusicQueue:


    def __init__(self):

        self.songs = []



    def add(self, song):

        self.songs.append(song)



    def next(self):

        if self.songs:

            return self.songs.pop(0)


        return None



    def clear(self):

        self.songs.clear()