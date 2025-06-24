from .base import BaseComponent


class Button(BaseComponent):
    """
    Button component extending BaseComponent.

    Attributes:
        text (str): The label displayed on the button.
        onclick (str): JavaScript function to execute on click.
        callback (Callable | None): Python-side callback function (optional).
        id (str | None): Unique identifier for the component.
        classes (str): CSS classes applied to the component.
        style (str): Inline CSS styles for the component.
        area (str): Grid area specification for layout positioning.
        page (str): Page identifier where the component belongs.
    """

    def __init__(
        self,
        text: str = "Click Me",
        onclick: str = "",
        id: str | None= None,
        classes: str = "",
        style: str = "",
        area: str = "1x1",
        page: str = "Home"
    ) -> None:
        # Add "button-component" class to any additional classes provided
        component_classes = "button-component " + classes
        super().__init__(id, component_classes, style, area, page)

        self.text: str = text
        self.onclick: str = onclick
        self.callback: callable | None = None

    def render(self) -> str:
        """
        Render the button component as an HTML <button> element.

        Returns:
            str: HTML string for the button.
        """
        attrs = self.get_base_attributes()

        # Include onclick attribute if a JS function is specified
        onclick_attr = f'onclick="{self.onclick}"' if self.onclick else ''

        return f'<button {attrs} {onclick_attr}>{self.text}</button>'

    def set_callback(self, callback: callable) -> None:
        """
        Set a Python callback function for the button.

        Args:
            callback (callable): Function to call when the button is triggered.
        """
        self.callback = callback

    def set_text(self, new_text: str) -> None:
        """
        Update the text displayed on the button.

        Args:
            new_text (str): New label text for the button.
        """
        self.text = new_text
