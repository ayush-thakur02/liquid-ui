from .base import BaseComponent


class Image(BaseComponent):
    """
    Image display component extending BaseComponent.

    Attributes:
        src (str): Image source URL or path.
        alt (str): Alternate text for the image.
        width (str): Width of the image (e.g., "100px", "50%").
        height (str): Height of the image (e.g., "200px", "auto").
        id (str | None): Unique identifier for the component.
        classes (str): CSS classes applied to the component.
        style (str): Inline CSS styles for the component.
        area (str): Grid area specification for layout positioning.
        page (str): Page identifier where the component belongs.
    """

    def __init__(
        self,
        src: str = "",
        alt: str = "Image",
        width: str = "",
        height: str = "",
        id: str | None = None,
        classes: str = "",
        style: str = "",
        area: str = "1x1",
        page: str = "Home"
    ) -> None:
        # Add "image-component" class to any custom classes
        component_classes = "image-component " + classes
        super().__init__(id, component_classes, style, area, page)

        self.src: str = src
        self.alt: str = alt
        self.width: str = width
        self.height: str = height

    def render(self) -> str:
        """
        Render the image component to HTML with fallback for errors.

        Returns:
            str: HTML string for the image container and image element.
        """
        attrs = self.get_base_attributes()

        # Include optional width and height attributes only if provided
        width_attr = f'width="{self.width}"' if self.width else ''
        height_attr = f'height="{self.height}"' if self.height else ''

        return f'''
        <div class="image-container" {attrs}>
            <img src="{self.src}" 
                 alt="{self.alt}" 
                 {width_attr} 
                 {height_attr}
                 onerror="this.style.display='none'; this.nextElementSibling.style.display='block';"
                 onload="this.style.display='block'; this.nextElementSibling.style.display='none';">
            <div class="image-fallback" style="display: none; border: 2px dashed #ccc; padding: 20px; text-align: center; color: #666;">
                Image Here: {self.alt}
            </div>
        </div>'''

    def set_src(self, new_src: str) -> None:
        """
        Update the image source URL.

        Args:
            new_src (str): New source URL or file path.
        """
        self.src = new_src

    def set_size(self, width: str, height: str) -> None:
        """
        Update the image's width and height.

        Args:
            width (str): New width value (e.g., "100px", "auto").
            height (str): New height value (e.g., "100px", "auto").
        """
        self.width = width
        self.height = height
