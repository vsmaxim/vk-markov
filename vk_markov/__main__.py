import os
import argparse
import pickle

import vk_api
from dotenv import load_dotenv

from vk_markov.markov import MarkovWeightedMatrix
from vk_markov.utils import retreive_n_posts

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument(
    "--relearn",
    help="Relearns markov chain with adjusted settings in .env",
    action="store_true"
)
args = parser.parse_args()
try:
    with open("markov", "rb") as file:
        markov = pickle.load(file)
except (FileNotFoundError, pickle.PicklingError, EOFError):
    markov = None
if args.relearn or markov is None:
    vk_session = vk_api.VkApi(token=os.getenv("VK_TOKEN"))
    api = vk_session.get_api()
    posts_to_learn = retreive_n_posts(
        api,
        int(os.getenv("GROUP_ID")),
        int(os.getenv("SAMPLES_COUNT")),
    )
    chain_length = int(os.getenv("CHAIN_LENGTH"))
    markov = MarkovWeightedMatrix(chain_length=chain_length)
    for post in posts_to_learn:
        markov.learn(post)
    with open("markov", "wb") as file:
        pickle.dump(markov, file)
print(markov.generate_sentence())
