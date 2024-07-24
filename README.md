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

## Logging

Logging is configured to provide detailed information about the server's operations. Logs include timestamps, log levels, and messages, which are crucial for debugging and monitoring.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

If you want to contribute to this project, please fork the repository and submit a pull request with your changes.

## Contact

For any questions or issues, please open an issue on GitHub.

