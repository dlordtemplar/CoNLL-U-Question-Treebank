"""
Create train, dev, test datasets from corpus
https://cs230-stanford.github.io/train-dev-test-split.html
"""

import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'))
args = parser.parse_args()

conllus = []
with open(args.file.name) as file:
    file_iter = iter(file)

    conllu_current = []

    for line in file_iter:
        # If the current CoNLL-U is completely parsed
        if line.strip() == '':
            conllu_current.append(line)
            conllus.append(conllu_current)
            conllu_current = []

        # Continue building CoNLL-U
        else:
            # Remove sentence IDs as they will all be wrong
            if not line.startswith('# sent_id ='):
                conllu_current.append(line)

# 3998
print('Total sentences:', len(conllus))

random.seed(8879)
# shuffles conllus (deterministic given the chosen seed)
random.shuffle(conllus)

split_1 = int(0.8 * len(conllus))
split_2 = int(0.9 * len(conllus))
train = conllus[:split_1]
dev = conllus[split_1:split_2]
test = conllus[split_2:]

# 3198
print('Train:', len(train))
# 400
print('Dev:', len(dev))
# 400
print('Test:', len(test))

with open('data/train.conllu', 'w') as file:
    for conllu in train:
        for line in conllu:
            file.write(line)

with open('data/dev.conllu', 'w') as file:
    for conllu in dev:
        for line in conllu:
            file.write(line)

with open('data/test.conllu', 'w') as file:
    for conllu in test:
        for line in conllu:
            file.write(line)
