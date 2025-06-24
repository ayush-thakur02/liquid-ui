from .base import BaseComponent


class InputBox(BaseComponent):
    """
    Input box component for text-based user input.

    Attributes:
        placeholder (str): Text to display when the input is empty.
        value (str): Current value of the input field.
        input_type (str): HTML input type (e.g., "text", "password", "email").
        id (str | None): Unique identifier for the component.
        classes (str): CSS classes applied to the component.
        style (str): Inline CSS styles for the component.
        area (str): Grid area specification for layout positioning.
        page (str): Page identifier where the component belongs.
    """

    def __init__(
        self,
        placeholder: str = "",
        value: str = "",
        input_type: str = "text",
        id: str | None = None,
        classes: str = "",
        style: str = "",
        area: str = "1x1",
        page: str = "Home"
    ) -> None:
        # Add "input-component" to any custom classes
        component_classes = "input-component " + classes
        super().__init__(id, component_classes, style, area, page)

        self.placeholder: str = placeholder
        self.value: str = value
        self.input_type: str = input_type

    def render(self) -> str:
        """
        Render the input box component as an HTML input element.

        Returns:
            str: HTML string for the input element.
        """
        attrs = self.get_base_attributes()
        return f'''
        <input type="{self.input_type}" 
               placeholder="{self.placeholder}" 
               value="{self.value}" 
               {attrs}>'''

    def set_value(self, new_value: str) -> None:
        """
        Update the value of the input box.

        Args:
            new_value (str): The new value to set in the input.
        """
        self.value = new_value
