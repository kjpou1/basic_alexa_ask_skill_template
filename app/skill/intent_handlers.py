import logging

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name, is_request_type

from app.config.config import Config
from app.helpers.template_renderer import JinjaTemplateRenderer

# Set up logging
logger = logging.getLogger(__name__)

# Initialize Jinja2 template renderer with YAML templates
# Make sure this is executed before any usage in the handlers.
JinjaTemplateRenderer.initialize(
    template_folder="views", yaml_file="app/resources/templates.yaml"
)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        logger.info("Handling LaunchRequest")
        template_renderer = JinjaTemplateRenderer()
        speech_text = template_renderer.render_string_template("welcome_text")
        return (
            handler_input.response_builder.speak(speech_text)
            .set_should_end_session(False)
            .response
        )


class CustomIntentHandler(AbstractRequestHandler):
    """Handler for Custom Intent."""

    intent = Config().intent

    def can_handle(self, handler_input):
        return is_intent_name(self.intent)(handler_input)

    def handle(self, handler_input):
        logger.info("Handling %s", self.intent)

        # Extract the firstname slot from the request
        slots = handler_input.request_envelope.request.intent.slots
        firstname = slots.get("firstname").value if slots.get("firstname") else None

        # Render response using the JinjaTemplateRenderer
        renderer = JinjaTemplateRenderer()

        if firstname is None:
            # No name given, prompt user to provide their name
            ask_name_text = renderer.render_string_template("ask_name")
            return (
                handler_input.response_builder.speak(ask_name_text)
                .ask(ask_name_text)  # Keeps the session open to receive further input
                .response
            )

        speech_text = renderer.render_string_template("hello", firstname=firstname)

        return (
            handler_input.response_builder.speak(speech_text)
            .set_should_end_session(True)
            .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        logger.info(
            "Session ended with reason: %s",
            handler_input.request_envelope.request.reason,
        )
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for AMAZON.FallbackIntent."""

    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("Handling AMAZON.FallbackIntent")
        # speech_text = "Sorry, I didn't understand that. Can you please rephrase?"
        template_renderer = JinjaTemplateRenderer()
        speech_text = template_renderer.render_string_template("ask_name_reprompt")
        return (
            handler_input.response_builder.speak(speech_text)
            .ask(speech_text)  # Keeps the session open to receive further input
            .response
        )


class GoodbyeIntentHandler(AbstractRequestHandler):
    """Handler for Goodbye Intent."""

    def can_handle(self, handler_input):
        return is_intent_name("GoodbyeIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("Handling GoodbyeIntent")
        template_renderer = JinjaTemplateRenderer()
        speech_text = template_renderer.render_string_template("goodbye")
        return (
            handler_input.response_builder.speak(speech_text)
            .set_should_end_session(True)
            .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for AMAZON.HelpIntent."""

    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("Handling AMAZON.HelpIntent")
        template_renderer = JinjaTemplateRenderer()
        speech_text = template_renderer.render_string_template("help")
        return (
            handler_input.response_builder.speak(speech_text)
            .ask(speech_text)  # Keeps the session open to receive further input
            .response
        )


class StopIntentHandler(AbstractRequestHandler):
    """Handler for AMAZON.StopIntent."""

    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("Handling AMAZON.StopIntent")
        template_renderer = JinjaTemplateRenderer()
        speech_text = template_renderer.render_string_template("stop")

        return (
            handler_input.response_builder.speak(speech_text)
            .set_should_end_session(True)
            .response
        )
