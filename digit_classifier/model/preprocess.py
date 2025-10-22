from torchvision import transforms as transforms
from PIL import Image
import io

def preprocess_image(image_bytes: bytes):
    image = Image.open(io.BytesIO(image_bytes))

    if image.size != (28, 28):
        raise ValueError("Image must be 28x28 pixels")
    
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    transform = transforms.Compose([
                    transforms.Grayscale(num_output_channels=1),
                    transforms.Resize((28, 28)),
                    transforms.ToTensor(),
                    transforms.Normalize((0.1307,), (0.3081,))
                ])
    
    image_tensor = transform(image)
    image_tensor = image_tensor.unsqueeze(0)
    return image_tensor