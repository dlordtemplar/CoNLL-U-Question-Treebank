import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'))
args = parser.parse_args()

with open('data/dep_sentences.txt', 'w') as file_new:
    with open(args.file.name) as file:
        iter_dep = iter(file)

        dep_sentences = []
        conllu_current = []

        for line_dep in iter_dep:
            # If the current CoNLL-U is completely parsed
            if line_dep.strip() == '':
                for row_num in range(0, len(conllu_current)):
                    new_row = conllu_current[row_num]

                    # If the CoNLL-U contains "dep", add it to the list of sentences to write out
                    if not new_row[0].startswith('#') and new_row[7] == 'dep':
                        dep_sentences.append(conllu_current[1])
                        conllu_current.append(new_row)
                        break

                conllu_current = []

            # Continue building CoNLL-U
            else:
                tokens_dep = line_dep.split('\t')
                conllu_current.append(tokens_dep)

        for sentence in dep_sentences:
            # Remove "# text = " in each sentence
            current_sen = sentence[0].split(' ')
            current_sen = current_sen[3:]
            for word_index in range(0, len(current_sen)):
                # Replace '<<\n' with '"\n'
                if current_sen[word_index] == '<<\n':
                    current_sen[word_index] = '"\n'
                # Replace '``' and '<<' with '"'
                elif current_sen[word_index] == '``' or current_sen[word_index] == '<<':
                    current_sen[word_index] = '"'
                # Replace '<s' with "'s"
                elif current_sen[word_index] == '<s':
                    current_sen[word_index] = "'s"
                # Replace '<t' with "'t"
                elif current_sen[word_index] == '<t':
                    current_sen[word_index] = "'t"
                # Replace '<re' with "'re"
                elif current_sen[word_index] == '<re':
                    current_sen[word_index] = "'re"
                # Replace '<ll' with "'ll"
                elif current_sen[word_index] == '<ll':
                    current_sen[word_index] = "'ll"
                # Replace 'n<t' with "n't"
                elif current_sen[word_index] == 'n<t':
                    current_sen[word_index] = "n't"
                # Replace '`' and '<' with "'"
                elif current_sen[word_index] == '`' or current_sen[word_index] == '<':
                    current_sen[word_index] = "'"

                # There will still be '<' tokens left, but handle those manually
            file_new.write(' '.join(current_sen))
