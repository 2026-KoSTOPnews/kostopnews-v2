import os
from transformers import BertTokenizer
import onnxruntime as ort

MODEL_PATH = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../../../model/kobert-kostop.onnx")
    )
TOKENIZER_NAME = "monologg/kobert"

def load_kobert_onnx():
    tokenizer = BertTokenizer.from_pretrained(TOKENIZER_NAME)

    session = ort.InferenceSession(MODEL_PATH)

    return session, tokenizer
