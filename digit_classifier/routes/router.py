from flask import Blueprint, jsonify, request
from digit_classifier.services.service import DigitClassifierService
from digit_classifier.services.voting_service import VotingService
from auth.utils.jwt import token_required

digit_classifier_bp = Blueprint('digit_classifier', __name__)
digit_classifier_service = DigitClassifierService()
voting_service = VotingService()


@digit_classifier_bp.route('', methods=['POST'])
@token_required
def infer(payload):

    user_id = payload.get('user_id')

    if not request.content_type != 'multipart/form-data':
        return jsonify({'error': 'Content type must be multipart/form-data'}), 400

    if not 'image' in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_bytes = request.files['image'].read()
    true_label = int(request.form.get('true_label', -1))

    if not image_bytes:
        return jsonify({'error': 'No image provided'}), 400

    if not digit_classifier_service.load_model(repo_name="mnist-digit-classifier", filename="mnist_model.pth"):
        return jsonify({'error': 'Failed to load model'}), 500

    try:
        inference_result = digit_classifier_service.infer(image_bytes)
        prediction = inference_result.argmax(dim=1).item()

        print(f"Model predicted: {prediction}, true label: {true_label}")

        voting_record = voting_service.record_vote(
            predicted_label=prediction,
            true_label=true_label,
            user_id=user_id
        )

        return jsonify(voting_record), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# @digit_classifier_bp.route('/vote', methods=['POST'])
# @token_required
# def vote():
#     data = request.get_json()
#     user_id = data.get('user_id')
#     predicted_label = data.get('predicted_label')
#     true_label = data.get('true_label')

#     if user_id is None or predicted_label is None or true_label is None:
#         return jsonify({'error': 'user_id, predicted_label, and true_label are required'}), 400

#     try:
#         voting_service.record_vote(user_id, predicted_label, true_label)
#         return jsonify({'message': 'Vote recorded successfully'}), 200
#     except Exception as e:
#         return jsonify({'error': 'Failed to record vote', 'details': str(e)}), 500


@digit_classifier_bp.route('/stats', methods=['GET'])
@token_required
def get_votes_distribution(payload):
    distribution = voting_service.get_voter_distribution()
    return jsonify(distribution), 200
  