# Fullstack Web Development (React + Flask) Workshop

Access git handbook [here](docs/git_hand_book.md)

To follow along fork this repository first and clone it.

Then switch to the branch `f/health-api`

## Task - 1: Health Check API

> GET /api/health

Expected Response

```
    {
        'message': 'OK'
    }
```

### Solution

```
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'message': 'OK'}), 200

```

## Task - 2: Logic for fetching votes

switch to the branch `f/voting`

> GET /api/digit-classifier/stats

### setup

```

from app import app
from auth.models.index import db, User, VoteSample

app.app_context().push()

user1 = User.create_user('john', 'John Doe', 'device1')

VoteSample.create_vote_sample(predicted_label=3, true_label=3, voted_by=user1.id)
VoteSample.create_vote_sample(predicted_label=5, true_label=5, voted_by=user1.id)

```

### querying

```
db.session.query(User).all()
db.session.query(VoteSample.voted_by).group_by(VoteSample.voted_by)

### Example

db.select([SALES.c.company, db.func.sum(SALES.c.no_of_invoices)]) \
    .group_by(SALES.c.company)

```

Modify the file `digit_classifier/services/voting_service.py` the TODO section

Expected output

```
[
    {
        "accuracy": 0.5,
        "predictions": 2,
        "voted_by": "smotte"
    }
]
```
