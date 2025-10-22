from digit_classifier.clients.hf_client import HFClient
from digit_classifier.model.network import NeuralNet
import torch
from digit_classifier.model.preprocess import preprocess_image

class DigitClassifierService:
    def __init__(self):
        self.hf_client = HFClient()

    def load_model(self, repo_name: str, filename: str = 'model.pth'):
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        try:
            self.model = self.hf_client.load_model(
                repo_id=repo_name,
                model_class=NeuralNet,
                device=device,
                filename=filename
            )
            print(f"Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            return False

        return True

    
    def infer(self, image_bytes: bytes):
        if not self.model:
            raise Exception("Model not loaded")
        try:
            image_tensor = preprocess_image(image_bytes)
            output = self.model(image_tensor)
            return output
        except Exception as e:
            print(f"Error classifying image: {e}")
            return False
        return True
