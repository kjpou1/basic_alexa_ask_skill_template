# BASIC_ALEXA_ASK_SKILL_TEMPLATE

This project is a basic template for creating an Alexa skill server using Bottle, ASK SDK, and supporting Gevent for running the server. It also includes environment configuration using dotenv and follows best practices for logging and configuration management.

## Table of Contents
- [BASIC\_ALEXA\_ASK\_SKILL\_TEMPLATE](#basic_alexa_ask_skill_template)
  - [Table of Contents](#table-of-contents)
  - [Important Architectural Notes](#important-architectural-notes)
    - [Initialization Order](#initialization-order)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the Server](#running-the-server)
    - [Running the Server](#running-the-server-1)
  - [Request Handlers](#request-handlers)
    - [LaunchRequestHandler](#launchrequesthandler)
    - [CustomIntentHandler](#customintenthandler)
    - [SessionEndedRequestHandler](#sessionendedrequesthandler)
    - [FallbackIntentHandler](#fallbackintenthandler)
    - [GoodbyeIntentHandler](#goodbyeintenthandler)
    - [HelpIntentHandler](#helpintenthandler)
    - [StopIntentHandler](#stopintenthandler)
  - [Logging](#logging)
  - [License](#license)
  - [Contributing](#contributing)
  - [Contact](#contact)

## Important Architectural Notes

### Initialization Order

To ensure proper initialization of the `JinjaTemplateRenderer` before it is used by any request handlers, the initialization is done in the `Host.__init__` method. This is critical to avoid premature initialization by the request handlers. Any future modifications should honor this initialization order.


## Installation

1. Clone the repository:

```bash
git clone https://github.com/kjpou1/BASIC_ALEXA_ASK_SKILL_TEMPLATE.git
cd BASIC_ALEXA_ASK_SKILL_TEMPLATE
```

2. Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Copy `example_env` to `.env` and configure your environment variables:

```bash
cp example_env .env
```

Edit `.env` and set the appropriate values for your configuration.

## Configuration

Configuration settings are managed using environment variables loaded from a `.env` file. The `Config` class in `app/config/config.py` handles loading these settings.

## Running the Server

The server is run using Gevent.

### Running the Server

```bash
python run.py
```

## Request Handlers

The Alexa skill uses several request handlers to manage different types of requests. Here are the handlers included in this project:

### LaunchRequestHandler

**Purpose**: Handles the launch request when the user starts the skill.

**Response**: Welcomes the user to the skill.

```python
class LaunchRequestHandler(AbstractRequestHandler):
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
```

### CustomIntentHandler

**Purpose**: Handles a custom intent specified in the configuration.

**Response**: Responds with a personalized message if the `firstname` slot is provided, otherwise prompts the user to provide their name.

```python
class CustomIntentHandler(AbstractRequestHandler):
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
```

### SessionEndedRequestHandler

**Purpose**: Handles the end of a session.

**Response**: Logs the reason for the session ending.

```python
class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        logger.info("Session ended with reason: %s", handler_input.request_envelope.request.reason)
        return handler_input.response_builder.response
```

### FallbackIntentHandler

**Purpose**: Handles unrecognized intents using the `AMAZON.FallbackIntent`.

**Response**: Asks the user to rephrase their request.

```python
class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("Handling AMAZON.FallbackIntent")
        template_renderer = JinjaTemplateRenderer()
        speech_text = template_renderer.render_string_template("ask_name_reprompt")
        return (
            handler_input.response_builder.speak(speech_text)
            .ask(speech_text)  # Keeps the session open to receive further input
            .response
        )
```

### GoodbyeIntentHandler

**Purpose**: Handles the `GoodbyeIntent`.

**Response**: Says goodbye to the user and ends the session.

```python
class GoodbyeIntentHandler(AbstractRequestHandler):
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
```

### HelpIntentHandler

**Purpose**: Handles the `AMAZON.HelpIntent`.

**Response**: Provides help information to the user.

```python
class HelpIntentHandler(AbstractRequestHandler):
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
```

### StopIntentHandler

**Purpose**: Handles the `AMAZON.StopIntent`.

**Response**: Says goodbye to the user and ends the session.

```python
class StopIntentHandler(AbstractRequestHandler):
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
```

## Logging

Logging is configured to provide detailed information about the server's operations. Logs include timestamps, log levels, and messages, which are crucial for debugging and monitoring.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

If you want to contribute to this project, please fork the repository and submit a pull request with your changes.

## Contact

For any questions or issues, please open an issue on GitHub.




