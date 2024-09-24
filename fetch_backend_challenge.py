#Aditya Bilawar's submission for Fetch Rewards Backend Challenge
from flask import Flask, request, jsonify
from datetime import datetime
from collections import defaultdict, OrderedDict

app = Flask(__name__)

# Store transactions and maintain points balance for each payer
transactions = []  # List of all transactions in the system
points_balance = defaultdict(int)  # Dictionary to store the current balance of each payer

# Function to parse ISO 8601 timestamps, handling 'Z' as UTC indicator
def parse_timestamp(timestamp):
    # Ensure 'Z' at the end is replaced with '+00:00' to make it ISO 8601 compatible for Python's datetime
    if timestamp.endswith('Z'):
        timestamp = timestamp.replace('Z', '+00:00')
    return datetime.fromisoformat(timestamp)

@app.route('/add', methods=['POST'])
def add_points():
    """
    Endpoint to add points for a payer at a specific timestamp.
    Accepts a JSON payload with 'payer', 'points', and 'timestamp'.
    """
    data = request.json
    payer = data.get('payer')
    points = data.get('points')
    timestamp = data.get('timestamp')

    # Validate the input payload; all fields must be present
    if not payer or points is None or not timestamp:
        return "Invalid data", 400 
    
    # Convert the timestamp into a datetime object
    try:
        transaction_time = parse_timestamp(timestamp)
    except ValueError:
        return "Invalid timestamp format", 400
    
    # Handling positive points: simply add the transaction and update the balance
    if points >= 0:
        transactions.append({"payer": payer, "points": points, "timestamp": transaction_time})
        points_balance[payer] += points
    else:
        # For negative points, adjust the existing transactions
        remaining_points_to_deduct = abs(points)
        
        # Ensure transactions are processed in chronological order
        transactions.sort(key=lambda x: x['timestamp'])
        
        # Deduct the points from the oldest available positive transactions for this payer
        for transaction in transactions:
            if transaction['payer'] == payer and transaction['points'] > 0:
                points_to_deduct = min(transaction['points'], remaining_points_to_deduct)
                
                # Deduct points from the current transaction and update the balance
                transaction['points'] -= points_to_deduct
                points_balance[payer] -= points_to_deduct
                remaining_points_to_deduct -= points_to_deduct
                
                # Stop if the required deduction is complete
                if remaining_points_to_deduct == 0:
                    break
        
        # If there are still points to deduct, add a negative transaction record
        if remaining_points_to_deduct > 0:
            transactions.append({"payer": payer, "points": -remaining_points_to_deduct, "timestamp": transaction_time})
            points_balance[payer] -= remaining_points_to_deduct

    return '', 200

@app.route('/spend', methods=['POST'])
def spend_points():
    """
    Endpoint to spend points. Points are deducted from the oldest available transactions across all payers.
    Accepts a JSON payload with 'points' to indicate how many points to spend.
    """
    data = request.json
    points_to_spend = data.get("points")

    # Validate that points_to_spend is positive
    if points_to_spend is None or points_to_spend <= 0: 
        return "Invalid amount", 400

    # Check if the user has enough points in total
    total_points = sum(points_balance.values())
    if points_to_spend > total_points:
        return "User doesn’t have enough points", 400
    
    # Ensure transactions are processed in chronological order
    transactions.sort(key=lambda x: x['timestamp'])

    deducted_points = defaultdict(int)  # To keep track of points spent per payer
    points_spent = 0  # Total points spent so far

    # Deduct points from the oldest transactions
    for transaction in transactions:
        if points_spent >= points_to_spend: 
            break

        payer = transaction['payer']
        available_points = transaction['points']

        # Skip negative or zero-point transactions, as they don't contribute to spending
        if available_points <= 0:
            continue
        
        # Determine how many points to deduct from this transaction
        points_to_deduct = min(available_points, points_to_spend - points_spent)

        if points_to_deduct > 0:
            deducted_points[payer] -= points_to_deduct  # Track the points deducted for the payer
            points_balance[payer] -= points_to_deduct   # Update the payer's balance
            points_spent += points_to_deduct           # Increase the total points spent
            transaction['points'] -= points_to_deduct  # Update the remaining points in this transaction

    # Remove any transactions that have been fully utilized
    transactions[:] = [t for t in transactions if t['points'] != 0]

    # Prepare the response to return the list of deductions made
    response = [{"payer": payer, "points": points} for payer, points in deducted_points.items()]
    return jsonify(response), 200

@app.route('/balance', methods=['GET'])
def get_balance():
    """
    Endpoint to retrieve the current points balance for each payer.
    """
    # Use OrderedDict to maintain consistent ordering in the response
    ordered_balance = OrderedDict(sorted(points_balance.items(), key=lambda x: x[0]))
    return jsonify(ordered_balance), 200

# Start the Flask application
if __name__ == '__main__':
    app.run(port=8000)
