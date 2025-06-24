from framework import create_ui

# Create a new UI instance with 5 columns
ui = create_ui(title="My Options", columns=5)

# Add title
ui.text("Select Options", tag="h2", area="5x1")

ui.text("Option 1:", area="2x1")
ui.checkbox(
    label="Enable Feature A",
    id="feature_a",
    area="3x1"
)

ui.text("Option 2:", area="2x1")
ui.checkbox(
    label="Enable Feature B",
    id="feature_b",
    area="3x1"
)

ui.text("You Selected:", id="result_display", area="5x1")

def update_selection(form_data):
    selected_options = []
    if form_data.get('feature_a'):
        selected_options.append("Feature A")
    if form_data.get('feature_b'):
        selected_options.append("Feature B")
    
    if selected_options:
        ui.update('result_display', f"Selected: {', '.join(selected_options)}")
    else:
        ui.update('result_display', "No features selected")
    
    return None  # Don't return anything to component

ui.button("Update Selection", callback=update_selection, id="update_btn", area="5x1")
ui.text("Click the button to see selected options", area="5x1")

if __name__ == "__main__":
    # Run the application
    ui.run()