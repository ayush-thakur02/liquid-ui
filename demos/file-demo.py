from framework import create_ui

# Create a new UI instance with 3 columns for simplicity
ui = create_ui(title="File Upload Demo", columns=3)

# Add title and instructions
ui.text("File Upload Demo", tag="h2", area="3x1")
ui.text("Upload any file to see its details", tag="p", area="3x1")

# Create file upload component
ui.file_upload(id="file_upload", accept="*", multiple=False, 
               placeholder="Drop a file here or click to select", area="3x1")

# Simple callback to handle file upload
def handle_file_upload(form_data):
    uploaded_file = form_data.get('file_upload')
    
    if not uploaded_file or not hasattr(uploaded_file, 'filename'):
        ui.update("file_info", "No file uploaded")
        return {"status": "error", "message": "No file uploaded"}
    
    filename = uploaded_file.filename
    if not filename:
        ui.update("file_info", "No file selected")
        return {"status": "error", "message": "No file selected"}
    
    # Get file size
    uploaded_file.seek(0, 2)  # Seek to end
    file_size = uploaded_file.tell()
    uploaded_file.seek(0)  # Reset to beginning
    
    # Format file size
    if file_size < 1024:
        size_str = f"{file_size} bytes"
    elif file_size < 1024 * 1024:
        size_str = f"{file_size / 1024:.1f} KB"
    else:
        size_str = f"{file_size / (1024 * 1024):.1f} MB"
    
    # Display file information
    file_info = f"✅ File uploaded successfully!\n\nFilename: {filename}\nSize: {size_str}"
    ui.update("file_info", file_info)
    
    return {"status": "success", "message": f"Successfully uploaded {filename}"}

ui.button("Upload File", callback=handle_file_upload, area="3x1")

# Display area for file information
ui.text("No file uploaded yet", id="file_info", area="3x2")

if __name__ == "__main__":
    ui.run()