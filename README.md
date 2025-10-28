# Fullstack Web Development (React + Flask) Workshop

Access git handbook [here](docs/git_hand_book.md)

To follow along fork this repository first and clone it.

Then switch to the branch

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

> GET /api/digit-classifier/stats
