from framework import create_ui

# Create a new UI instance
ui = create_ui(title="Page Demo - Flask UI", columns=3)

# Home page components
ui.text("Welcome to the Home Page!", tag="h2", area="3x1", page="Home")
ui.text("This is the default page of the application.", area="1x1", page="Home", )
ui.input(placeholder="Enter your name", id="name_input", area="2x1", page="Home")
ui.button("Say Hello", callback=lambda data: f"Hello, {data.get('name_input', 'World')}!", id="hello_btn", page="Home")
ui.text("Say Hello to?", id="hello_result", area="2x1", page="Home")

# Settings page components
ui.text("Settings Page", tag="h2", area="3x1", page="Settings")
ui.text("Configure your application settings here.", area="1x1", page="Settings")
ui.checkbox("Enable notifications", id="notifications", page="Settings")
ui.checkbox("Dark mode", id="dark_mode", page="Settings")
ui.text("Volume Level", page="Settings", area="1x1")
ui.slider(min_value=0, max_value=100, value=50, id="volume", area="2x1", page="Settings")
ui.button("Save Settings", callback=lambda data: f"Settings saved! Notifications: {data.get('notifications', False)}, Dark mode: {data.get('dark_mode', False)}, Volume: {data.get('volume', 50)}", id="save_settings_btn", page="Settings")
ui.text("Your Setting will show here!", id="settings_result", page="Settings", area="2x1")

# About page components
ui.text("About This Application", tag="h2", page="About", area="3x1")
ui.text("This is a demonstration of the Flask UI framework with page navigation.", page="About", area="3x1")
ui.text("Features:", tag="h3", page="About", area="1x2")
ui.text("Multiple pages with navigation", page="About", area="1x1")
ui.text("Grid-based layout system", page="About", area="1x1") 
ui.text("Interactive components", page="About", area="1x1")
ui.text("State management", page="About", area="1x1")
ui.text("Image Example:", tag="h3", page="About", area="1x1")
ui.image(src="/images/sample 1.jpg", alt="Sample Image", page="About", area="1x1")
ui.image(src="/images/sample 2.jpg", alt="Sample Image", page="About", area="1x1")


# Dashboard page with various components
ui.text("Dashboard", tag="h2", page="Dashboard", area="3x1")
ui.text("Quick stats and controls", page="Dashboard", area="1x2")
ui.radio_group("priority", ["High", "Medium", "Low"], selected_value="Medium", id="priority_group", page="Dashboard")
ui.file_upload(accept="image/*", id="upload_files", page="Dashboard")
ui.text("Result Text", id="refresh_result", page="Dashboard", area="2x1")
ui.button("Refresh Data", callback=lambda data: "Data refreshed successfully!", id="refresh_btn", page="Dashboard")

# Callback to update results
def update_hello_result(data):
    name = data.get('name_input', 'World')
    result = f"Hello, {name}!"
    ui.update('hello_result', result)
    return result

def update_settings_result(data):
    notifications = data.get('notifications', False)
    dark_mode = data.get('dark_mode', False)
    volume = data.get('volume', 50)
    result = f"Settings saved! Notifications: {notifications}, Dark mode: {dark_mode}, Volume: {volume}"
    ui.update('settings_result', result)
    return result

def update_refresh_result(data):
    result = "Dashboard data refreshed successfully!"
    ui.update('refresh_result', result)
    return result

# Update callbacks
ui.callbacks['hello_btn'] = update_hello_result
ui.callbacks['save_settings_btn'] = update_settings_result
ui.callbacks['refresh_btn'] = update_refresh_result

if __name__ == "__main__":
    print("Available pages:", ui.get_pages())
    ui.run()
