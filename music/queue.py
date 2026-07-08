from collections import deque
import random


class MusicQueue:

    def __init__(self):
        self.queues = {}
        self.loop = {}

    def create(self, guild_id):
        if guild_id not in self.queues:
            self.queues[guild_id] = deque()
            self.loop[guild_id] = False

    def add(self, guild_id, song):
        self.create(guild_id)
        self.queues[guild_id].append(song)

    def next(self, guild_id):

        self.create(guild_id)

        if len(self.queues[guild_id]) == 0:
            return None

        return self.queues[guild_id].popleft()

    def get_queue(self, guild_id):
        self.create(guild_id)
        return list(self.queues[guild_id])

    def clear(self, guild_id):
        self.create(guild_id)
        self.queues[guild_id].clear()

    def size(self, guild_id):
        self.create(guild_id)
        return len(self.queues[guild_id])

    def shuffle(self, guild_id):

        self.create(guild_id)

        songs = list(self.queues[guild_id])

        random.shuffle(songs)

        self.queues[guild_id] = deque(songs)

    def remove(self, guild_id, index):

        self.create(guild_id)

        songs = list(self.queues[guild_id])

        if index < 0 or index >= len(songs):
            return False

        songs.pop(index)

        self.queues[guild_id] = deque(songs)

        return True

    def enable_loop(self, guild_id):
        self.loop[guild_id] = True

    def disable_loop(self, guild_id):
        self.loop[guild_id] = False

    def is_loop(self, guild_id):
        return self.loop.get(guild_id, False)