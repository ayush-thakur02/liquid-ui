from .base import BaseComponent


class FileUpload(BaseComponent):
    """
    File upload component with drag-and-drop support.

    Attributes:
        accept (str): Comma-separated list of accepted file MIME types or extensions.
        multiple (bool): Whether multiple file uploads are allowed.
        placeholder (str): Placeholder text shown to the user.
        max_files (int): Maximum number of files allowed (default is 10).
        max_size (int): Maximum size of each file in bytes (default is 10MB).
        id (str | None): Unique identifier for the component.
        classes (str): CSS classes applied to the component.
        style (str): Inline CSS styles for the component.
        area (str): Grid area specification for layout positioning.
        page (str): Page identifier where the component belongs.
    """

    def __init__(
        self,
        accept: str = "*",
        multiple: bool = True,
        placeholder: str = "Drop files here or click to upload",
        id: str | None = None,
        classes: str = "",
        style: str = "",
        area: str = "1x1",
        page: str = "Home"
    ) -> None:
        # Add "file-component" class to any additional classes
        component_classes = "file-component " + classes
        super().__init__(id, component_classes, style, area, page)

        self.accept: str = accept
        self.multiple: bool = multiple
        self.placeholder: str = placeholder
        self.max_files: int = 10  # Default limit on number of files
        self.max_size: int = 10 * 1024 * 1024  # 10 MB default size limit

    def render(self) -> str:
        """
        Render the file upload input element and container to HTML.

        Returns:
            str: HTML string representing the file upload component.
        """
        attrs = self.get_base_attributes()
        multiple_attr = 'multiple' if self.multiple else ''
        upload_id = self.id or 'file_upload'

        return f'''
        <div class="file-upload-container" {attrs}>
            <input type="file" 
                   id="{upload_id}" 
                   accept="{self.accept}" 
                   {multiple_attr}
                   class="file-input-direct"
                   onchange="console.log('File input changed for {upload_id}:', event.target.files); handleFileSelect(event, '{upload_id}')">
            <div id="{upload_id}_files" class="file-list"></div>
        </div>'''

    def set_accept(self, accept_types: str) -> None:
        """
        Set the accepted file types for the upload input.

        Args:
            accept_types (str): Comma-separated list of MIME types or file extensions.
        """
        self.accept = accept_types

    def set_multiple(self, multiple: bool) -> None:
        """
        Enable or disable selection of multiple files.

        Args:
            multiple (bool): True to allow multiple file uploads; False otherwise.
        """
        self.multiple = multiple
