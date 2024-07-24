import logging

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.helpers.resource_loader import ResourceLoader
from app.models.singleton import SingletonMeta


class JinjaTemplateRenderer(metaclass=SingletonMeta):
    _is_initialized = False

    def __init__(self, template_folder="views", yaml_file=None):
        if not self._is_initialized:
            self.logger = logging.getLogger(__name__)
            self.env = Environment(
                loader=FileSystemLoader(template_folder),
                autoescape=select_autoescape(["html", "xml", "j2"]),
            )
            self.templates = {}
            if yaml_file:
                self.load_templates(yaml_file)
            self._is_initialized = True

    @classmethod
    def initialize(cls, template_folder="views", yaml_file=None):
        """
        Convenience method to explicitly initialize the JinjaTemplateRenderer.
        This method can be expanded to include more initialization parameters if needed.
        """
        cls(template_folder, yaml_file)

    def load_templates(self, yaml_file):
        templates = ResourceLoader.load_templates(yaml_file)
        if templates:
            self.templates = templates
            self.logger.info("Successfully loaded YAML templates: %s", yaml_file)
        else:
            self.logger.error("Failed to load YAML templates: %s", yaml_file)

    def render_template(self, template_name, **context):
        template = self.env.get_template(template_name)
        return template.render(context)

    def render_string_template(self, template_key, **context):
        template_string = self.templates.get(template_key)
        if template_string:
            template = self.env.from_string(template_string)
            return template.render(context)
        else:
            self.logger.error(
                "Template key not found in YAML templates: %s", template_key
            )
            return ""
