from framework import create_ui

# Create a new UI instance with 4 columns
ui = create_ui(title="Image Gallery Demo", columns=4)

# Add title
ui.text("Image Gallery", tag="h2", area="2x2")

# Display first image initially
ui.image(src="images/sample 1.jpg", alt="Sample Image 1", width="300", height="200", id="gallery_image", area="2x2")

# Current image indicator
ui.text("Currently showing: Sample 1", id="image_status", area="2x1")

# Toggle button to switch between images
current_image = 1  # Track current image (1 or 2)

def toggle_image(form_data):
    global current_image
    
    if current_image == 1:
        # Switch to image 2
        image_component = ui.get_component("gallery_image")
        if image_component:
            image_component.set_src("images/sample 2.jpg")
        # Send update to frontend
        ui.update("gallery_image", "images/sample 2.jpg")
        ui.update("image_status", "Currently showing: Sample 2")
        ui.update("result", "Switched to Sample Image 2")
        current_image = 2
    else:
        # Switch to image 1
        image_component = ui.get_component("gallery_image")
        if image_component:
            image_component.set_src("images/sample 1.jpg")
        # Send update to frontend
        ui.update("gallery_image", "images/sample 1.jpg")
        ui.update("image_status", "Currently showing: Sample 1")
        ui.update("result", "Switched to Sample Image 1")
        current_image = 1
    
    return {"status": "success"}

ui.button("Change Image", callback=toggle_image, area="2x1")

# Result display
ui.text("Click button to change images", id="result", area="2x1")

if __name__ == "__main__":
    ui.run()