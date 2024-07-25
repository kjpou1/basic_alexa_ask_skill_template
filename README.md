# BASIC_ALEXA_ASK_SKILL_TEMPLATE

This project is a basic template for creating an Alexa skill server using Bottle, ASK SDK, and supporting Gevent for running the server. It also includes environment configuration using dotenv and follows best practices for logging and configuration management.

## Table of Contents
- [BASIC\_ALEXA\_ASK\_SKILL\_TEMPLATE](#basic_alexa_ask_skill_template)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Environment Variables](#environment-variables)
    - [SERVER\_HOST](#server_host)
    - [SERVER\_PORT](#server_port)
    - [INTENT](#intent)
    - [DEBUG](#debug)
    - [SSL\_CERTIFICATE](#ssl_certificate)
    - [SSL\_PRIVATE\_KEY](#ssl_private_key)
  - [Generating a Self-Signed SSL Certificate](#generating-a-self-signed-ssl-certificate)
    - [Script: self-signed-certificate.sh](#script-self-signed-certificatesh)
    - [Instructions](#instructions)
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
  - [Alexa Skill Interaction Model](#alexa-skill-interaction-model)
    - [Interaction Model Definition](#interaction-model-definition)
    - [Explanation of the Interaction Model](#explanation-of-the-interaction-model)
  - [Logging](#logging)
  - [License](#license)
  - [Contributing](#contributing)
  - [Contact](#contact)

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

## Environment Variables

The following environment variables are used to configure the application. These should be defined in the `.env` file at the root of the project.

### SERVER_HOST

- **Description**: The host address on which the server will run.
- **Default Value**: `0.0.0.0`
- **Example**: `SERVER_HOST=0.0.0.0`

### SERVER_PORT

- **Description**: The port number on which the server will run.
- **Default Value**: `8080`
- **Example**: `SERVER_PORT=8080`

### INTENT

- **Description**: The custom intent to be handled by the skill.
- **Default Value**: `HelloWorldIntent`
- **Example**: `INTENT=HelloWorldIntent`

### DEBUG

- **Description**: Enables or disables debug mode.
- **Default Value**: `true`
- **Example**: `DEBUG=true`

### SSL_CERTIFICATE

- **Description**: The path to the SSL certificate file.
- **Default Value**: `/etc/ssl/private/insecure.pem`
- **Example**: `SSL_CERTIFICATE="/etc/ssl/private/insecure.pem"`

### SSL_PRIVATE_KEY

- **Description**: The path to the SSL private key file.
- **Default Value**: `/etc/ssl/insecure.key`
- **Example**: `SSL_PRIVATE_KEY="/etc/ssl/insecure.key"`

## Generating a Self-Signed SSL Certificate

For testing purposes, you can generate a self-signed SSL certificate using the provided `self-signed-certificate.sh` script. This is not recommended for production use.

### Script: self-signed-certificate.sh

```bash
#!/bin/bash

# Create necessary directories
sudo mkdir -p /etc/ssl/private

# Create a self signed SSL certificate.
sudo openssl req -new -newkey rsa:4096 -x509 -days 3650 -nodes \
             -subj /C=US/ST=NY/L=NY/O=NA/CN=localhost \
             -keyout /etc/ssl/insecure.key -out /etc/ssl/private/insecure.pem

# Create a DHParam file. Use 4096 bits instead of 2048 bits in production.
sudo openssl dhparam -out /etc/ssl/dhparam.pem 2048
```

### Instructions

1. Make the script executable:

```bash
chmod +x self-signed-certificate.sh
```

2. Run the script to generate the SSL certificate and private key:

```bash
./self-signed-certificate.sh
```

This will create the following files:
- `/etc/ssl/insecure.key`: The private key file.
- `/etc/ssl/private/insecure.pem`: The SSL certificate file.
- `/etc/ssl/dhparam.pem`: The DH parameter file.

> [!NOTE]  
>  Ensure the `/etc/ssl/private` directory exists before running the script. This script creates self-signed certificates for testing purposes only and is not recommended for production environments.


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

## Alexa Skill Interaction Model

The Alexa skill is defined by an interaction model, which specifies the intents, slots, and sample utterances that the skill recognizes.

### Interaction Model Definition

Here is the JSON definition of the interaction model for this skill:

```json
{
    "interactionModel": {
        "languageModel": {
            "invocationName": "hello world",
            "intents": [
                {
                    "name": "AMAZON.CancelIntent",
                    "samples": []
                },
                {
                    "name": "AMAZON.HelpIntent",
                    "samples": []
                },
                {
                    "name": "AMAZON.StopIntent",
                    "samples": []
                },
                {
                    "name": "HelloWorldIntent",
                    "slots": [
                        {
                            "name": "firstname",
                            "type": "AMAZON.FirstName",
                            "samples": [
                                "{firstname}"
                            ]
                        }
                    ],
                    "samples": [
                        "say hello to {firstname}",
                        "{firstname}",
                        "say hi to {firstname}",
                        "how are you",
                        "say hi",
                        "hi",
                        "say hello world",
                        "say hello"
                    ]
                },
                {
                    "name": "AMAZON.NavigateHomeIntent",
                    "samples": []
                },
                {
                    "name": "AMAZON.FallbackIntent",
                    "samples": []
                }
            ],
            "types": []
        },
        "dialog": {
            "intents": [
                {
                    "name": "HelloWorldIntent",
                    "confirmationRequired": false,
                    "prompts": {},
                    "slots": [
                        {
                            "name": "firstname",
                            "type": "AMAZON.FirstName",
                            "confirmationRequired": false,
                            "elicitationRequired": true,
                            "prompts": {
                                "elicitation": "Elicit.Slot.1653396877702.19112989472"
                            }
                        }
                    ]
                }
            ],
            "delegationStrategy": "ALWAYS"
        },
        "prompts": [
            {
                "id": "Elicit.Slot.1653396877702.19112989472",
               

 "variations": [
                    {
                        "type": "PlainText",
                        "value": "Who should I say hello to?"
                    },
                    {
                        "type": "PlainText",
                        "value": "Tell me who to say hello to"
                    },
                    {
                        "type": "PlainText",
                        "value": "What is your name"
                    }
                ]
            }
        ]
    }
}
```

### Explanation of the Interaction Model

- **Invocation Name**: The name users say to start the skill (e.g., "Alexa, open hello world").
- **Intents**: The actions that the skill can perform, each represented by an intent. This includes built-in intents like `AMAZON.HelpIntent` and custom intents like `HelloWorldIntent`.
- **Slots**: Parameters that the intents can accept. In this case, `HelloWorldIntent` has a `firstname` slot of type `AMAZON.FirstName`.
- **Samples**: Example phrases users can say to invoke each intent. These help Alexa recognize different ways users might phrase their requests.
- **Dialog**: Defines the dialog management for the intents, including slot elicitation prompts to gather necessary information from the user.
- **Prompts**: Predefined responses Alexa can use to prompt the user for more information.


## Logging

Logging is configured to provide detailed information about the server's operations. Logs include timestamps, log levels, and messages, which are crucial for debugging and monitoring.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

If you want to contribute to this project, please fork the repository and submit a pull request with your changes.

## Contact

For any questions or issues, please open an issue on GitHub.




