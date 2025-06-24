from .base import BaseComponent


class RadioButton(BaseComponent):
    """
    Radio button component extending BaseComponent.

    Attributes:
        label (str): Display text next to the radio button.
        value (str): Value assigned to the radio button.
        name (str): Name attribute to group radio buttons.
        checked (bool): Whether this radio button is selected.
        id (str | None): Unique identifier for the component.
        classes (str): CSS classes applied to the component.
        style (str): Inline CSS styles for the component.
        area (str): Grid area specification for layout positioning.
        page (str): Page identifier where the component belongs.
    """

    def __init__(
        self,
        label: str = "",
        value: str = "",
        name: str = "radio_group",
        checked: bool = False,
        id: str | None = None,
        classes: str = "",
        style: str = "",
        area: str = "1x1",
        page: str = "Home"
    ) -> None:
        # Add "radio-component" to any custom classes
        component_classes = "radio-component " + classes
        super().__init__(id, component_classes, style, area, page)

        self.label: str = label
        self.value: str = value
        self.name: str = name
        self.checked: bool = checked

    def render(self) -> str:
        """
        Render the radio button as an HTML input element.

        Returns:
            str: HTML string representing the radio button.
        """
        attrs = self.get_base_attributes()
        checked_attr = 'checked' if self.checked else ''

        if self.label:
            return f'''
            <label {attrs}>
                <input type="radio" name="{self.name}" value="{self.value}" {checked_attr}>
                <span>{self.label}</span>
            </label>'''
        else:
            return f'<input type="radio" name="{self.name}" value="{self.value}" {checked_attr} {attrs}>'

    def set_checked(self, checked: bool) -> None:
        """
        Set whether this radio button is selected.

        Args:
            checked (bool): True to mark as selected, False otherwise.
        """
        self.checked = checked


class RadioGroup:
    """
    Helper class to manage a group of RadioButton components.

    Attributes:
        name (str): Common name shared by all radio buttons in the group.
        options (list[tuple[str, str]]): List of (label, value) pairs.
        radio_buttons (list[RadioButton]): Created radio button instances.
    """

    def __init__(self, name: str, options: list[tuple[str, str]] | None = None) -> None:
        self.name: str = name
        self.options: list[tuple[str, str]] = options or []
        self.radio_buttons: list[RadioButton] = []

    def add_option(self, label: str, value: str, checked: bool = False) -> RadioButton:
        """
        Add a new radio button to the group.

        Args:
            label (str): Text label for the radio button.
            value (str): Value associated with the button.
            checked (bool): Whether this button is selected.

        Returns:
            RadioButton: The created radio button instance.
        """
        radio = RadioButton(label=label, value=value, name=self.name, checked=checked)
        self.radio_buttons.append(radio)
        return radio

    def set_selected(self, value: str) -> None:
        """
        Set which radio button is selected based on its value.

        Args:
            value (str): Value to select.
        """
        for radio in self.radio_buttons:
            radio.set_checked(radio.value == value)

    def get_selected(self) -> str | None:
        """
        Get the value of the currently selected radio button.

        Returns:
            str | None: The selected value, or None if none are selected.
        """
        for radio in self.radio_buttons:
            if radio.checked:
                return radio.value
        return None
