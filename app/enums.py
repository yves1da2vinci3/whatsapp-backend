import enum

class ChatType(enum.Enum):
    one_on_one = "1-on-1"
    group = "group"

class MessageType(enum.Enum):
    audio = "audio"
    video = "video"
    text = "text"
    image = "image"

class StoryType(enum.Enum):
    audio = "audio"
    video = "video"
    text = "text"
    image = "image"
