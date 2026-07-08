class MusicQueue:


    def __init__(self):

        self.queue = []



    def add(self, song):

        self.queue.append(song)



    def remove(self):

        if self.queue:

            return self.queue.pop(0)


        return None



    def clear(self):

        self.queue.clear()



    def get_all(self):

        return self.queue