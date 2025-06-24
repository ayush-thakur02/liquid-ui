from .base import BaseComponent


class Checkbox(BaseComponent):
    """
    Checkbox component extending BaseComponent.

    Attributes:
        label (str): Label displayed next to the checkbox.
        checked (bool): Whether the checkbox is initially checked.
        value (str): Value assigned to the checkbox input.
        id (str | None): Unique identifier for the component.
        classes (str): CSS classes applied to the component.
        style (str): Inline CSS styles for the component.
        area (str): Grid area specification for layout positioning.
        page (str): Page identifier where the component belongs.
    """

    def __init__(
        self,
        label: str = "",
        checked: bool = False,
        value: str = "on",
        id: str | None = None,
        classes: str = "",
        style: str = "",
        area: str = "1x1",
        page: str = "Home"
    ) -> None:
        # Add "checkbox-component" to any additional classes
        component_classes = "checkbox-component " + classes
        super().__init__(id, component_classes, style, area, page)

        self.label: str = label
        self.checked: bool = checked
        self.value: str = value

    def render(self) -> str:
        """
        Render the checkbox as an HTML input element (with or without label).

        Returns:
            str: HTML string for the checkbox component.
        """
        checked_attr = 'checked' if self.checked else ''

        if self.label:
            # For labeled checkboxes, split HTML attributes for input and label
            label_attrs: list[str] = []
            input_attrs: list[str] = []

            if self.id:
                input_attrs.append(f'id="{self.id}"')

            # Combine base classes for label
            if self.classes:
                label_attrs.append(f'class="component {self.classes.strip()}"')
            else:
                label_attrs.append('class="component"')

            # Build style string for label, including grid info
            styles: list[str] = []
            if self.style:
                styles.append(self.style)
            if self.grid_position:
                row, col = self.grid_position
                grid_area = f"{row} / {col} / {row + self.grid_rows} / {col + self.grid_cols}"
                styles.append(f"grid-area: {grid_area}")
            if styles:
                label_attrs.append(f'style="{"; ".join(styles)}"')

            label_attr_str = ' '.join(label_attrs)
            input_attr_str = ' '.join(input_attrs)

            return (
                f'<label {label_attr_str}>'
                f'<input type="checkbox" value="{self.value}" {checked_attr} {input_attr_str}>'
                f'{self.label}'
                f'</label>'
            )
        else:
            # Unlabeled checkbox — use base attributes from parent
            attrs = self.get_base_attributes()
            return f'<input type="checkbox" value="{self.value}" {checked_attr} {attrs}>'

    def set_checked(self, checked: bool) -> None:
        """
        Update the checked state of the checkbox.

        Args:
            checked (bool): New checked state.
        """
        self.checked = checked

    def toggle(self) -> None:
        """
        Toggle the current checked state of the checkbox.
        """
        self.checked = not self.checked
