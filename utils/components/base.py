class BaseComponent:
    """
    Base class for all UI components.

    Attributes:
        id (str | None): Unique identifier for the component.
        classes (str): CSS class names applied to the component.
        style (str): Inline styles applied to the component.
        area (str): Describes the grid area size (e.g., '1x1').
        page (str): The page this component belongs to.
        grid_position (tuple[int, int] | None): Tuple representing (row, column) grid position.
        grid_cols (int): Number of columns the component spans in the grid.
        grid_rows (int): Number of rows the component spans in the grid.
    """

    def __init__(
        self,
        id: str | None = None,
        classes: str = "",
        style: str = "",
        area: str = "1x1",
        page: str = "Home"
    ) -> None:
        self.id = id
        self.classes = classes
        self.style = style
        self.area = area
        self.page = page
        self.grid_position: tuple[int, int] | None = None
        self.grid_cols: int = 1
        self.grid_rows: int = 1

    def set_grid_position(
        self,
        row: int,
        col: int,
        cols: int = 1,
        rows: int = 1
    ) -> None:
        """
        Set the grid position and span dimensions for this component.

        Args:
            row (int): Starting row of the component in the grid.
            col (int): Starting column of the component in the grid.
            cols (int): Number of columns the component spans.
            rows (int): Number of rows the component spans.
        """
        self.grid_position = (row, col)
        self.grid_cols = cols
        self.grid_rows = rows

    def render(self) -> str:
        """
        Render the component to HTML.

        Returns:
            str: HTML representation of the component.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclasses must implement render method")

    def get_base_attributes(self) -> str:
        """
        Construct and return a string of common HTML attributes.

        Includes ID, class names, and inline styles including grid positioning.

        Returns:
            str: HTML attribute string suitable for insertion in a tag.
        """
        attrs: list[str] = []

        # Add ID attribute if provided
        if self.id:
            attrs.append(f'id="{self.id}"')

        # Combine default and custom CSS classes
        all_classes = "component " + self.classes
        attrs.append(f'class="{all_classes.strip()}"')

        # Collect inline styles
        styles: list[str] = []

        if self.style:
            styles.append(self.style)

        # Add grid positioning style if grid position is set
        if self.grid_position:
            row, col = self.grid_position
            grid_area = f"{row} / {col} / {row + self.grid_rows} / {col + self.grid_cols}"
            styles.append(f"grid-area: {grid_area}")

        if styles:
            attrs.append(f'style="{"; ".join(styles)}"')

        return ' '.join(attrs)
