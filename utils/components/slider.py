from .base import BaseComponent


class Slider(BaseComponent):
    """
    Slider component for selecting a numeric value within a defined range.

    Attributes:
        min_value (int | float): Minimum value of the slider.
        max_value (int | float): Maximum value of the slider.
        value (int | float): Current value of the slider.
        step (int | float): Step interval between values.
    """

    def __init__(
        self,
        min_value: int | float = 0,
        max_value: int | float = 100,
        value: int | float = 50,
        step: int | float = 1,
        id: str | None = None,
        classes: str = "",
        style: str = "",
        area: str = "1x1",
        page: str = "Home"
    ) -> None:
        # Add "slider-component" to custom classes
        component_classes = "slider-component " + classes
        super().__init__(id, component_classes, style, area, page)

        self.min_value: int | float = min_value
        self.max_value: int | float = max_value
        self.value: int | float = value
        self.step: int | float = step

    def render(self) -> str:
        """
        Render the slider component as an HTML input element with range type.

        Returns:
            str: HTML representation of the slider and its current value.
        """
        attrs: list[str] = []

        if self.id:
            attrs.append(f'id="{self.id}"')

        # Use a different container class to avoid layout conflicts
        slider_classes = "slider-container " + self.classes
        attrs.append(f'class="{slider_classes.strip()}"')

        styles: list[str] = []

        if self.style:
            styles.append(self.style)

        if self.grid_position:
            row, col = self.grid_position
            grid_area = f"{row} / {col} / {row + self.grid_rows} / {col + self.grid_cols}"
            styles.append(f"grid-area: {grid_area}")

        if styles:
            attrs.append(f'style="{"; ".join(styles)}"')

        attrs_str = ' '.join(attrs)

        return f'''
        <div {attrs_str}>
            <input type="range" 
                   id="{self.id}"
                   min="{self.min_value}" 
                   max="{self.max_value}" 
                   value="{self.value}" 
                   step="{self.step}">
            <span class="slider-value" id="{self.id}_value">{self.value}</span>
        </div>'''

    def set_value(self, new_value: int | float) -> None:
        """
        Update the slider's current value, clamped to the slider's range.

        Args:
            new_value (int | float): New value to set.
        """
        self.value = max(self.min_value, min(self.max_value, new_value))

    def set_range(self, min_value: int | float, max_value: int | float) -> None:
        """
        Update the slider's minimum and maximum range, and clamp current value if necessary.

        Args:
            min_value (int | float): Minimum value for the slider.
            max_value (int | float): Maximum value for the slider.
        """
        self.min_value = min_value
        self.max_value = max_value
        self.value = max(min_value, min(max_value, self.value))
