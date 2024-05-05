GET http://localhost:8000/heartbeat
HTTP 200
[Asserts]
jsonpath "$.version" == "0.0.1"
jsonpath "$.description" == "Events API"

GET http://localhost:8000/events?league=NFL
HTTP 200
Content-Type: application/json			   # Implicit assert on Content-Type Header
[Asserts]                                          # Explicit asserts section
header "x-request-id" != null                      # Request Id Header present
jsonpath "$" count == 5
jsonpath "$[0].eventId" != null
