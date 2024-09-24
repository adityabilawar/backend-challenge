Aditya Bilawar's Fetch OA Submission.
solution.txt includes my part 2 responses

A User has points in their account to the payer which is the producer.

ex: 15 points to DANNON at 2:15 pm 9/24/24, spent rewards at 2:15 pm 10/24/24
    20 points to KELLOGG at 6:15 pm 9/24/24, spent rewards at 6:15 pm  10/24/24

    Route: /add
    Method: POST
Description: When a user has points added, we will use an /add route that accepts a transaction which contains
how many points will be added, what payer the points will be added through, and the timestamp for when the
transaction takes place. The request body for this endpoint will look like the following:
{
"payer" : "DANNON",
"points" : 5000,
"timestamp" : "2020-11-02T14:00:00Z"
}

If transaction was added successfully, then endpoint should respond with a status code of 200 (OK). dont need to include response body 

400 (BAD REQUEST) is a client-side error status, if the request has some syntax errors or invalid request parameters.

Route: /spend
Method: POST
Description: When a user goes to spend their points, they are not aware of what payer their points were added
through. Because of this, your request body should look like
{"points" : 5000}
When a spend request comes in, your service should use the following rules to decide which payer to spend points
through:
● We want the oldest points to be spent first (oldest based on transaction timestamp, not the order they’re
received)
● We want no payer's points to go negative

If a request was made to spend more points than what a user has in total, then we should return a status
code of 400 and a message saying the user doesn’t have enough points. This can be done through a text
response rather than a JSON response/

After your service has successfully
calculated who to remove points from, the endpoint should respond with a status code of 200 and a list of
payer names and the number of points that were subtracted. An example of a response body looks like the
following:
[
{ "payer": "DANNON", "points": -100 },
{ "payer": "UNILEVER", "points": -200 },
{ "payer": "MILLER COORS", "points": -4,700 }
]

Route: /balance
Method: GET
Description: This route should return a map of points the user has in their account based on the payer they were
added through. This endpoint can be used to see how many points the user has from each payer at any given
time. Because this is a GET request, there is no need for a request body. This endpoint should always
return a 200 and give a response body similar to the following:
{
"DANNON": 1000,
”UNILEVER” : 0,
"MILLER COORS": 5300
}




