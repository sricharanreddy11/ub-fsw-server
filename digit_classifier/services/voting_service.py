from auth.models.index import db, VoteSample
from sqlalchemy import func 

class VotingService:
    def __init__(self):
        print("VotingService initialized")
    
    def get_voter_distribution(self):
        distribution = []

        result = []
        for record in distribution:
            result.append({
                'voted_by': record.voted_by,
                'predictions': record.predictions,
                'accuracy': float(record.accuracy)
            })
        return result

    def calculate_accuracy(self):
        total_votes = db.session.query(VoteSample).count()

        correct_votes = db.session.query(VoteSample).filter(
            VoteSample.predicted_label == VoteSample.true_label
        ).count()

        return correct_votes / total_votes if total_votes > 0 else 0.0
    
    def record_vote(self, predicted_label: int, true_label: int, user_id: int):
        vote_sample = VoteSample.create_vote_sample(
            predicted_label=predicted_label,
            true_label=true_label,
            voted_by=user_id
        )
        return vote_sample.to_dict()
    