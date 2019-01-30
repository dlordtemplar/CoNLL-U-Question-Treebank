# CoNLL-U Question Treebank

Conversion of Penn Treebank sentences into [CoNLL-U](https://universaldependencies.org/guidelines.html) format.

### Requirements

* Python 3
* Java
* [Stanford Parser](https://nlp.stanford.edu/software/stanford-dependencies.html)
* [Udapy](https://github.com/udapi/udapi-python/tree/master/udapi/block/ud)
* Perl

### 1. Treebank to CoNLL-U

Parse treebank into CoNLL-U format. Unfortunately, Stanford Parser currently only supports Universal Dependencies version 1, so we will convert it to version 2 in the next step.

https://nlp.stanford.edu/software/stanford-dependencies.html

```java
java -cp "*" -mx1g edu.stanford.nlp.trees.ud.UniversalDependenciesConverter -treeFile "wh_treebank.txt" > "wh_treebank2.conllu"
```

### 2. UD1 to UD2

Use the conversion script provided to update Universal Dependencies 1 to 2.

https://github.com/udapi/udapi-python/tree/master/udapi/block/ud

```bash
udapy -s ud.Convert1to2 < "wh_treebank2.conllu" > "wh_treebank2_convert.conllu"
```

### 3. Convert tags to UPOS

Use Perl to convert Part of Speech (POS) tags to Universal Part of Speech (UPOS) tags.

https://github.com/udapi/udapi-python/tree/master/udapi/block/ud

```perl
cpanm Lingua::Interset

perl conll_convert_tags_to_uposf.pl -f en::conll < "wh_treebank2.conllu" > "wh_treebank2_upos.conllu"
```

### 4. Validate

Use the validation script to check results.

https://github.com/udapi/udapi-python/tree/master/udapi/block/ud

```python
python validate.py "wh_treebank2_upos.conllu" --lang en --max-err 0
```

### Fix validation errors

Fix major violations and manually check trees. You can get different trees depending on your parser. There are some online parsers you can try:

http://lindat.mff.cuni.cz/services/udpipe/

I used the above parser to try to fix sentences that were incorrectly parsed to have 2 subjects (nsubj).

If you use other parsers, be sure to standardize your output so it is uniform.

These are the first steps to convert Penn treebank trees to CoNLL-U files. The rest of the readme will consist of fixing trees and molding the format to that of [en-ud-train.conll](data/en-ud-train.conll).