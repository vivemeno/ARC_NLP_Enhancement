import configparser
import json


from elasticsearch_query import ElasticsearchQuery
from xlnet import Xlnet
from textual_entailment import TextualEntailment


class ARC():
    def __init__(self, config):
        textual_entailment_config = config['textual_entailment']
        elasticsearch_config = config['elasticsearch']
        xlnet_config = config['xlnet']

        self.elasticsearch = ElasticsearchQuery(elasticsearch_config)
        self.xlnet = Xlnet(xlnet_config)
        self.textual_entailment = TextualEntailment(textual_entailment_config)

    def get_candidates(self, question):
        elasticsearch_candidates = self.elasticsearch.shingles_request(
            question)
        candidates = self.textual_entailment.get_entailment_candidate_list(
            question, elasticsearch_candidates)

        return candidates

    def analyze_arc_dataset(self, path):
        with open(path) as f:
            data = f.readlines()
            for i, a in enumerate(data):
                b = json.loads(a)
                question = b['question']['stem']
                choices = b['question']['choices']
                answer_key = b['answerKey']
                candidates = arc.get_candidates(question)
                print(str(question) + '\n\n\n' + str(candidates) +
                      '\n\n\n' + str(choices) + '\n\n\n' + str(answer_key))
                d = input()


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('./arc_configuration.conf')

    arc = ARC(config)

    # arc.analyze_arc_dataset(
    #     '/home/nishanth/gits/arc-cse-576/dataset/ARC-V1-Feb2018/ARC-Challenge/ARC-Challenge-Test.jsonl')
    question = 'Which technology was developed most recently?'
    choices = ["cellular", "television", "refrigerator", "airplane"]
    candidates = arc.get_candidates(question)
    for candidate in candidates:
        test_set = [' '.join([candidate, question, x]) for x in choices]
        scores = self.xlnet.predict(test_set)
        print(scores)