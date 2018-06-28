# -*- coding: utf-8 -*-
"""Playbook app wrapper for TextBlob (https://github.com/sloria/TextBlob)."""

import traceback

from tcex import TcEx
from textblob import TextBlob


def parse_arguments():
    """Parse arguments coming into the app."""
    tcex.parser.add_argument('--string', help='String', required=True)
    tcex.parser.add_argument('--n_gram', help='n-gram length', required=False, default="3")
    return tcex.args


def main():
    """."""
    args = parse_arguments()
    # read the string from the playbook to get the actual value of the argument
    string = tcex.playbook.read(args.string)
    n_gram_number = int(tcex.playbook.read(args.n_gram))

    tcex.log.info('String value: {}'.format(string))
    tcex.log.info('n-gram number: {}'.format(n_gram_number))

    blob = TextBlob(string)

    tags = dict()
    for tag in blob.tags:
        tags[tag[0]] = tag[1]

    tcex.playbook.create_output('json', blob.json)
    tcex.playbook.create_output('nGrams', [str(n_gram) for n_gram in blob.ngrams(n=n_gram_number)])
    tcex.playbook.create_output('nounPhrases', blob.noun_phrases)
    tcex.playbook.create_output('npCounts', blob.np_counts[1])
    tcex.playbook.create_output('polarity', blob.polarity)
    tcex.playbook.create_output('sentences', [str(sentence) for sentence in blob.sentences])
    tcex.playbook.create_output('subjectivity', blob.subjectivity)
    tcex.playbook.create_output('tags', tags)
    tcex.playbook.create_output('tokens', blob.tokens)
    tcex.playbook.create_output('wordCounts', blob.word_counts[1])
    tcex.playbook.create_output('words', blob.words)

    tcex.exit(0)


if __name__ == "__main__":
    tcex = TcEx()
    try:
        # start the app
        main()
    except SystemExit:
        pass
    except Exception as e:  # if there are any strange errors, log it to the logging in the UI
        err = 'Generic Error.  See logs for more details ({}).'.format(e)
        tcex.log.error(traceback.format_exc())
        tcex.message_tc(err)
        tcex.exit(1)
