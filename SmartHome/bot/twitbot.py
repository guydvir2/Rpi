from twython import Twython

from tw_auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)
twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)
message = "Hello world! :)\n@guydvir2\n#PyTwitBot"
twitter.update_status(status=message)
print("Tweeted: {}".format(message))