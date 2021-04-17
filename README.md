# CPSC449-Project5
Group Members: Tevin Vu, Cindy Quach, Dalisa Nguyen 

How to create the database:\
    createTable.py: to create a dynamodb table\
        run: ```python3 createTable.py```\
    putDataOnTable.py: to add some data in DirectMessages table\
        run: `python3 putDataOnTable.py`

How to run program/start services:\
    - Need to download dynamodb local\
    - go to the folder dynamodb_local_latest\
    - to start the dynamodb local in port 8000 --> run the command:\
        `java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb`

   - Start the Direct Message API Web Service Back-end:
       `foreman start`

Client Contract: 
    **sendDirectMessage(to, from, message, quickReplies=None)**\
        Sends a DM to a user. The API call may or may not include a list of quickReplies.\
    Testing:
    ```
        `http --verbose POST http://localhost:8080/users/KevinAWortman/directMessages/ from=ProfAvery message="Good morning"`
        POST /users/KevinAWortman/directMessages/ HTTP/1.1
        Accept: application/json, */*;q=0.5
        Accept-Encoding: gzip, deflate
        Connection: keep-alive
        Content-Length: 48
        Content-Type: application/json
        Host: localhost:8080
        User-Agent: HTTPie/2.4.0
        {
            "from": "ProfAvery",
            "message": "Good morning"
        }
    ```
   Response:
   ```
        HTTP/1.0 201 Created
        Content-Length: 59
        Content-Type: text/html; charset=UTF-8
        Date: Sat, 17 Apr 2021 22:07:05 GMT
        Server: WSGIServer/0.2 CPython/3.6.0

   ProfAvery are successful to send a message to KevinAWortman
   ```
   
   **replyToDirectMessage(messageId, message)**\
        Replies to a DM. The message may either be text or a quick-reply number. If the message parameter is a quick-reply number, it must have been in response to a  messageId that included a quick-replies field.\
    Testing:
        `http --verbose POST http://localhost:8080/users/KevinAWortman/directMessages/b08fc995-93f3-466a-b48f-623d6da0de84/ message=1`
        POST /users/KevinAWortman/directMessages/b08fc995-93f3-466a-b48f-623d6da0de84/ HTTP/1.1
        Accept: application/json, */*;q=0.5
        Accept-Encoding: gzip, deflate
        Connection: keep-alive
        Content-Length: 16
        Content-Type: application/json
        Host: localhost:8080
        User-Agent: HTTPie/2.4.0
        {
            "message": "1"
        }
 
   Response:
```
HTTP/1.0 201 Created
Content-Length: 38
Content-Type: text/html; charset=UTF-8
Date: Sat, 17 Apr 2021 22:27:22 GMT
Server: WSGIServer/0.2 CPython/3.6.0
   
   KevinAWortman has replied to ProfAvery
```

   **listDirectMessagesFor(username)**\
    Lists a user's DMs.\
    Testing:
    ```
        `http --verbose GET http://localhost:8080/users/ProfAvery/directMessages/`
        GET /users/ProfAvery/directMessages/ HTTP/1.1
        Accept: */*
        Accept-Encoding: gzip, deflate
        Connection: keep-alive
        Host: localhost:8080
        User-Agent: HTTPie/2.4.0
    ```
    Response:
    ```
        HTTP/1.0 200 OK
        Content-Length: 939
        Content-Type: application/json
        Date: Sat, 17 Apr 2021 22:32:11 GMT
        Server: WSGIServer/0.2 CPython/3.6.0

   {
            "user": [
                {
                    "fromUsername": "KevinAWortman",
                    "message": "Do you want to get some boba?",
                    "messageId": "41675926-d93f-4e95-ac48-0ebb23a69eac",
                    "quickReplies": [
                        "Yes",
                        "No",
                        "Call me"
                    ],
                    "timestamps": "2021-04-17T21:36:01.176738+00:00",
                    "toUsername": "ProfAvery"
                },
                {
                    "fromUsername": "KevinAWortman",
                    "in-reply-to": "b08fc995-93f3-466a-b48f-623d6da0de84",
                    "message": "1",
                    "messageId": "aec4a289-31c9-4c64-85e9-0320754fc3b8",
                    "timestamps": "2021-04-17T22:27:22.137763+00:00",
                    "toUsername": "ProfAvery"
                },
                {
                    "fromUsername": "KevinAWortman",
                    "message": "Hey, Are you free?",
                    "messageId": "c4d0e3e2-d11e-44b5-914d-9e9aa78e46f0",
                    "timestamps": "2021-04-17T21:36:01.176675+00:00",
                    "toUsername": "ProfAvery"
                },
                {
                    "fromUsername": "KevinAWortman",
                    "message": "Where do you want to go?",
                    "messageId": "f12d35ac-cb90-4870-b3bf-7ffb8d116213",
                    "quickReplies": [
                        "OMOMO",
                        "Share Tea"
                    ],
                    "timestamps": "2021-04-17T21:36:01.176754+00:00",
                    "toUsername": "ProfAvery"
                }
            ]
        }
    ```

   **listRepliesTo(messageId)**\
    Lists the replies to a DM.\
    Testing:
        `http GET http://localhost:8080/users/KevinAWortman/directMessages/41675926-d93f-4e95-ac48-0ebb23a69eac/`
    Response:
    ```
        HTTP/1.0 200 OK
        Content-Length: 257
        Content-Type: application/json
        Date: Sat, 17 Apr 2021 23:09:42 GMT
        Server: WSGIServer/0.2 CPython/3.6.0

   {
            "KevinAWortman": [
                {
                    "fromUsername": "ProfAvery",
                    "in-reply-to": "41675926-d93f-4e95-ac48-0ebb23a69eac",
                    "message": "Yes",
                    "messageId": "6580cac5-4ca7-45ed-a060-dc41469f4f80",
                    "timestamps": "2021-04-17T21:36:01.176747+00:00",
                    "toUsername": "KevinAWortman"
                }
            ]
   }
    ```









