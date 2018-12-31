import vk_api
from .utils import retreive_n_posts
import os
from .markov import MarkovWeightedMatrix


if __name__ == '__main__':
    vk_session = vk_api.VkApi(token=os.getenv("VK_TOKEN"))
    api = vk_session.get_api()
    posts_to_learn = retreive_n_posts(api, 92876084, 2000)
    markov = MarkovWeightedMatrix()
    for post in posts_to_learn:
        markov.learn(post)
    print(markov.generate_sentence())
    print(markov.generate_sentence())
