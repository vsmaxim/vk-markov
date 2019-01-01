# VK random content generator based on Markov chains.

This is yet another implementation of markov chains written from scratch.

## How to run

1. Create and activate virtualenv `virtualenv venv && source ./bin/activate`
2. Install requirements `pip install -r requirements.txt`
3. Specify settings in root of project.
4. Run python vk_markov 

## Configurations

All configurations keys are presented in .env-template file. To create your configuration, just copy the file into .env using `cp .env-template .env`, and specify settings.

### Description of settings
- VK_TOKEN - token from vk.com to authenticate
- GROUP_ID - id for group to sample from
- SAMPLES_COUNT - count for posts to sample
- CHAIN_LENGTH - count of words in markov chain

## Usefull features

You can retrain your already specified Markov chain, by using `--relearn` argument.