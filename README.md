# twilio-automated-survey

First, install all the dependencies.

`pip install ngrok`

Run the NGROK proxy tunnel.

`ngrok http 8000`

Make sure the url provided by the NGROK is set in survey/survey/settings.py in `NGROK_URL`.
Make sure TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN and TWILIO_PHONE_NUMBER are set accordingly.

To start the project, run the command `docker-compose up -d`.

The API subscription route is at `<host>//twilio-survey/submit-contact/'.

Example call:

`POST` /twilio-survey/submit-contact/
`BODY` {
    "phone_number": "+4072222222",
    "name": "John Doe"
}

Example response:

`{
    "id": 16,
    "phone_number": "+4072222222",
    "name": "John Doe"
}`

Enjoy!
