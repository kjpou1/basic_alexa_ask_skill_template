import asyncio
import logging

from gevent.pywsgi import WSGIServer

from app.config.config import Config
from app.models.command_line_args import CommandLineArgs
from app.skill.alexa import app


class Host:
    def __init__(self, args: CommandLineArgs):
        """
        Initialize the Host class with command line arguments and configuration.

        Parameters:
        args (CommandLineArgs): Command line arguments passed to the script.
        """
        self.args = args
        self.config = Config()
        self.logger = logging.getLogger(__name__)

        # Override configuration with command line arguments if provided
        if args.server:
            self.config.set_server_host(args.server)
        if args.port:
            self.config.set_server_port(args.port)
        if args.intent:
            self.config.set_intent(args.intent)

    def run(self):
        """
        Run the asynchronous run_async method.
        """
        return asyncio.run(self.run_async())

    async def run_async(self):
        """
        Asynchronous method to perform the main logic.
        """
        self.logger.info("Starting host process.")
        await self.run_gevent()

    async def run_gevent(self):

        http_server = WSGIServer(
            (self.config.server_host, self.config.server_port),
            app,
            keyfile=self.config.key_file,
            certfile=self.config.cert_file,
        )
        self.logger.info("Running server with gevent on: %s", http_server.address)
        http_server.serve_forever()


# if __name__ == "__main__":
#     # Setup logging configuration
#     logging.basicConfig(
#         level=logging.INFO,
#         format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     )

#     args = parse_args()
#     host = Host(args)
#     host.run()
