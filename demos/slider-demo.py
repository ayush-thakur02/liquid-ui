from framework import create_ui

# Create a new UI instance with 5 columns
ui = create_ui(title="Temperature Control", columns=5)

# Add title
ui.text("Set Your Preferred Temperature", tag="h2", area="5x1")

# Create temperature slider (0°C to 40°C, default 22°C)
ui.slider(min_value=0, max_value=40, value=22, step=1, id="temp_slider", area="3x1")

# Display current temperature
ui.text("Current Temperature: 22°C", id="temp_display", area="2x1")

# Update temperature button
def update_temperature(form_data):
    temp = form_data.get('temp_slider', 22)
    ui.update("temp_display", f"Current Temperature: {temp}°C")
    ui.update("result", f"Temperature set to: {temp}°C")
    return {"status": "success"}

ui.button("Update Temperature", callback=update_temperature, area="3x1")

# Result display
ui.text("Temperature set to: 22°C", id="result", area="2x1")

if __name__ == "__main__":
    ui.run()