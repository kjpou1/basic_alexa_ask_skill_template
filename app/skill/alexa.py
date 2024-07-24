import json
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_webservice_support.webservice_handler import WebserviceSkillHandler
from bottle import Bottle, request, response

from app.helpers.utilities import Utilities

# Import and register the request handlers
from app.skill.intent_handlers import (
    CustomIntentHandler,
    FallbackIntentHandler,
    GoodbyeIntentHandler,
    HelpIntentHandler,
    LaunchRequestHandler,
    SessionEndedRequestHandler,
    StopIntentHandler,
)

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Initialize Bottle app
app = Bottle()

# Create a SkillBuilder instance
sb = SkillBuilder()


# Register the request handlers to the skill builder
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CustomIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(GoodbyeIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(StopIntentHandler())

# Create a WebserviceSkillHandler instance
skill_handler = WebserviceSkillHandler(skill=sb.create())


@app.route("/", method=["POST"])
def alexa_skill():
    try:
        # Read and decode the Alexa request
        body = request.body.read().decode("utf-8")
        alexa_request = json.loads(body)
        logger.debug(
            "Received Alexa request: %s", Utilities.pretty_print_json(alexa_request)
        )

        # Process the request using the WebserviceSkillHandler
        alexa_response = skill_handler.verify_request_and_dispatch(
            http_request_body=body, http_request_headers=dict(request.headers)
        )

        # Return the response
        response.content_type = "application/json"
        return alexa_response

    except Exception as e:
        logger.error("Error handling Alexa request: %s", e)
        response.status = 500
        return json.dumps({"error": "Internal Server Error"})
