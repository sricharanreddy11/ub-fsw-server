from flask import Blueprint, jsonify, request
from digit_classifier.services.service import DigitClassifierService

digit_classifier_bp = Blueprint('digit_classifier', __name__)
digit_classifier_service = DigitClassifierService()


@digit_classifier_bp.route('', methods=['POST'])
def infer():
    """Classify a digit image"""
    if not request.content_type != 'multipart/form-data':
        return jsonify({'error': 'Content type must be multipart/form-data'}), 400

    if not 'image' in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_bytes = request.files['image'].read()

    if not image_bytes:
        return jsonify({'error': 'No image provided'}), 400

    if not digit_classifier_service.load_model(repo_name="mnist-digit-classifier", filename="mnist_model.pth"):
        return jsonify({'error': 'Failed to load model'}), 500

    try:
        
        inference_result = digit_classifier_service.infer(image_bytes)
        prediction = inference_result.argmax(dim=1).item()
        return jsonify({'prediction': prediction}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 50


@digit_classifier_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'message': 'OK'}), 200