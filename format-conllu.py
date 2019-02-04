import argparse

# Converts CoNLL-U files to adopt the format from "en-ud-train.conll".
parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'))
args = parser.parse_args()

# Punctuation Mapping
# Key: Value from current data
# Value: Tuple to transform to: first value is FORM, second is XPOS (Language-specific POS tag)
punct = {'`': ('\'', '``'),
         '<': ('\'', '\'\''),
         '``': ('"', '``'),
         '<<': ('"', '\'\''),
         '.': ('.', '.'),
         '?': ('?', '.'),
         '!': ('!', '.'),
         ':': (':', ':'),
         '(': ('(', '-LRB-'),
         ')': (')', '-RRB-'),
         '[': ('[', '-LRB-'),
         ']': (']', '-RRB-'),
         }
# punct keys in replace order. '``' and '<<' need to be replaced before '`' and '<'
# Each key is checked with .replace instead of key-in-dict is because of cases like "n<t" or "<s"
punct_replace_list = ['``', '<<', '`', '<', '.', '?', '!', ':', '(', '[', ']']

with open('data/wh_treebank_ud2_format.conllu', 'w') as file_new:
    with open(args.file.name) as file:
        for line in iter(file):
            new_line = line

            if new_line.strip() == '':
                pass

            # Comment line
            elif new_line.startswith('#'):
                # Replace punctuation with FORM, first value of tuple
                for key in punct_replace_list:
                    new_line = new_line.replace(key, punct[key][0])

            # Non-comment line
            else:
                row = line.split('\t')
                # 0: ID
                # 1: FORM: Word form or punctuation symbol.
                #       Replace punctuation with FORM, first value of tuple
                for key in punct_replace_list:
                    row[1] = row[1].replace(key, punct[key][0])
                # 2: LEMMA: Lemma or stem of word form.
                #       Replace punctuation with FORM, first value of tuple
                for key in punct_replace_list:
                    row[2] = row[2].replace(key, punct[key][0])
                # 3: UPOS: Universal part-of-speech tag.
                # 4: XPOS: Language-specific part-of-speech tag; underscore if not available.
                # 5: FEATS: List of morphological features from the universal feature inventory; underscore if n/a.
                #       Remove FEATS for punctuation
                if row[3] == 'PUNCT':
                    row[5] = '_'
                # 6: HEAD: Head of the current word, which is either a value of ID or zero (0).
                # 7: DEPREL: Universal dependency relation to the HEAD (root iff HEAD = 0).
                # 8: DEPS: Enhanced dependency graph in the form of a list of head-deprel pairs.
                # 9: MISC: Any other annotation.
                new_line = '\t'.join(row)

            file_new.write(new_line)
