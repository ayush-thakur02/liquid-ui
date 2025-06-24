from .base import BaseComponent


class Text(BaseComponent):
    """
    Text display component for rendering static HTML text elements.

    Attributes:
        text (str): The content to display.
        tag (str): The HTML tag used to wrap the text (e.g., 'p', 'h1', 'bold', 'em').
        id (str | None): Unique identifier for the component.
        classes (str): CSS classes applied to the component.
        style (str): Inline CSS styles for the component.
        area (str): Grid area specification for layout positioning.
        page (str): Page identifier where the component belongs.
    """

    def __init__(
        self,
        text: str = "",
        tag: str = "p",
        id: str | None = None,
        classes: str = "",
        style: str = "",
        area: str = "1x1",
        page: str = "Home"
    ) -> None:
        # Append "text-component" to existing class list
        component_classes = "text-component " + classes
        super().__init__(id, component_classes, style, area, page)

        self.text: str = text
        self.tag: str = tag

    def render(self) -> str:
        """
        Render the text component as an HTML element.

        Returns:
            str: HTML string for the text element.
        """
        attrs = self.get_base_attributes()
        return f'<{self.tag} {attrs}>{self.text}</{self.tag}>'

    def update_text(self, new_text: str) -> None:
        """
        Update the text content displayed by the component.

        Args:
            new_text (str): The new text to display.
        """
        self.text = new_text
