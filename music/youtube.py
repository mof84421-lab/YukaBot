import asyncio
import yt_dlp

YDL_OPTIONS = {
    "format": "bestaudio/best",
    "default_search": "ytsearch",
    "quiet": True,
    "noplaylist": True,
    "extract_flat": False,
}

ytdl = yt_dlp.YoutubeDL(YDL_OPTIONS)


class YouTube:

    @staticmethod
    async def search(query: str):

        loop = asyncio.get_event_loop()

        data = await loop.run_in_executor(
            None,
            lambda: ytdl.extract_info(
                query,
                download=False
            )
        )

        if "entries" in data:
            data = data["entries"][0]

        return {
            "title": data.get("title"),
            "url": data.get("url"),
            "webpage": data.get("webpage_url"),
            "thumbnail": data.get("thumbnail"),
            "duration": data.get("duration", 0),
            "uploader": data.get("uploader", "Unknown"),
        }

    @staticmethod
    def format_time(seconds):

        if seconds is None:
            return "00:00"

        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)

        if h:
            return f"{h:02}:{m:02}:{s:02}"

        return f"{m:02}:{s:02}"