# CoNLL-U Question Treebank

Conversion of Penn Treebank sentences into [CoNLL-U](https://universaldependencies.org/guidelines.html) format.

### Requirements

* Python 3
* Java
* [Stanford Parser](https://nlp.stanford.edu/software/stanford-dependencies.html)
* [Udapy](https://github.com/udapi/udapi-python/tree/master/udapi/block/ud)
* Perl

### 1. Treebank to CoNLL-U

Parse treebank into CoNLL-U format.
Unfortunately, Stanford Parser currently only supports Universal Dependencies version 1, so we will convert it to version 2 in the next step.

https://nlp.stanford.edu/software/stanford-dependencies.html

```bash
java -cp "*" -mx1g edu.stanford.nlp.trees.ud.UniversalDependenciesConverter -treeFile "wh_treebank.txt" > "wh_treebank_ud1.conllu"
```

### 2. UD1 to UD2

Use the conversion script provided to update Universal Dependencies 1 to 2.

https://github.com/udapi/udapi-python/tree/master/udapi/block/ud

```bash
udapy -s ud.Convert1to2 < "wh_treebank_ud1.conllu" > "wh_treebank_ud2.conllu"
```

### 3. Convert tags to UPOS

Use Perl to convert Part of Speech (POS) tags to Universal Part of Speech (UPOS) tags.

https://github.com/universaldependencies/tools

```perl
cpanm Lingua::Interset
```
```bash
perl conll_convert_tags_to_uposf.pl -f en::conll < "wh_treebank_ud2.conllu" > "wh_treebank_ud2_upos.conllu"
```

### 4. Validate

Use the validation script to check results.

https://github.com/universaldependencies/tools

```bash
python validate.py "wh_treebank_ud2_upos.conllu" --lang en --max-err 0
```

### Fix validation errors

Fix major violations and manually check trees.
You can get different trees depending on your parser.
There are some online parsers you can try:

http://lindat.mff.cuni.cz/services/udpipe/

I used the above parser to try to fix sentences that were incorrectly parsed to have 2 subjects (nsubj).

If you use other parsers, be sure to standardize your output so it is uniform.

These are the first steps to convert Penn treebank trees to CoNLL-U files.
The rest of the readme will consist of fixing trees and molding the format to that of [en-ud-train.conll](data/en-ud-train.conll).

### Uniform formatting

I wrote [format-conllu.py](format-conllu.py) to convert punctuation marks from this new treebank to previous training data [en-ud-train.conll](data/en-ud-train.conll).
I created a mapping of punctuation differences and then replaced them to get [wh_treebank_ud2_format.conllu](data/wh_treebank_ud2_format.conllu).

| Current | Target FORM | Target XPOS |
|:--------:|:-------------:|:-----:|
| ` | ' | `` |
| < | ' | '' |
| `` | " | `` |
| << | " | '' |
| . | . | . |
| ? | ? | . |
| ! | ! | . |
| : | : | : |
| ( | ( | -LRB- |
| ) | ) | -RRB- |
| [ | [ | -LRB- |
| ] | ] | -RRB- |

### Split into train, dev, test

I wrote [train-dev-test-split.py](train-dev-test-split.py) to randomly split the sentences into [dev](data/dev.conllu) (80%), [train](data/train.conllu) (10%), and [test](data/test.conllu) (10%).

```bash
Total sentences: 3998
Train: 3198
Dev: 400
Test: 400
```

### Manual Correction

The goal is to have a 100% correct corpus, but manually correcting 4000 sentences is time-consuming.
First, dev and test, the smaller subsets, will be corrected, and then the large training set will be revisited.

#### Getting rid of 'dep'

I wrote [get-dep-sentences.py](get-dep-sentences.py) to procure a list of all sentences containing a dependency relation of 'dep' and saved them as [dep_sentences.txt](data/dep_sentences.txt).
'dep' is not good- it means the parser was not sure which relation to use.
I corrected the sentences manually and saved the result as [dep_sentences_corrected.txt](data/dep_sentences_corrected.txt).
I then input them into the English parsers [here](http://lindat.mff.cuni.cz/services/udpipe/) and took the result I thought was most likely.
I replaced the old parse with the new one after making sure the formatting fits as mentioned in [Uniform formatting](#uniform-formatting).