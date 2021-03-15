from transformers import XLNetTokenizer, XLNetForMultipleChoice
import torch


class Xlnet():
    def __init__(self, config):
        model_path = config['model_path']

        self.tokenizer = XLNetTokenizer.from_pretrained(model_path)
        self.model = XLNetForMultipleChoice.from_pretrained(model_path)

    def predict(self, choices):
        input_ids = torch.tensor([self.tokenizer.encode(s) for s in choices]).unsqueeze(0)  # Batch size 1, 2 choices
        labels = torch.tensor(3).unsqueeze(0)  # Batch size 1

        outputs = self.model(input_ids, labels=labels)
        loss, classification_scores = outputs[:3]

        return classification_scores