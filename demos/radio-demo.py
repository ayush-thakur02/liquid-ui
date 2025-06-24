from framework import create_ui

# Create a new UI instance with 5 columns
ui = create_ui(title="Color Selection", columns=5)

# Add title
ui.text("Choose Your Favorite Color", tag="h2", area="3x2")

# Define colors list and create radio group
colors = ["Red", "Blue", "Green", "Yellow"]
ui.radio_group("color_group", colors, selected_value="Red", area="1x1")

# Show selection button
def show_color(form_data):
    color = form_data.get('color_group', 'No color selected')
    ui.update("result", f"You selected: {color}")
    return {"status": "success"}

ui.button("Show Selection", callback=show_color, area="3x1")

# Result display
ui.text("You selected: red", id="result", area="2x1")

if __name__ == "__main__":
    ui.run()