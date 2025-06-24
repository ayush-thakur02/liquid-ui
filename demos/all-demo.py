from framework import create_ui
import os
import random

# Create a new UI instance with 6 columns for better layout and state preservation enabled
ui = create_ui(title="Complete Framework Demo", columns=6, persist_state=True)

# Enable state preservation for seamless user experience
ui.preserve_form_state(True)

# ===== CALLBACK FUNCTIONS =====

def calculate_sum(form_data):
    """Calculate sum of two numbers"""
    try:
        num1 = float(form_data.get('calc_num1', 0))
        num2 = float(form_data.get('calc_num2', 0))
        result = num1 + num2
        ui.update('calc_result', f"Result: {num1} + {num2} = {result}")
        return None
    except (ValueError, TypeError):
        ui.update('calc_result', "Error: Please enter valid numbers")
        return None

def calculate_multiply(form_data):
    """Calculate product of two numbers"""
    try:
        num1 = float(form_data.get('calc_num1', 0))
        num2 = float(form_data.get('calc_num2', 0))
        result = num1 * num2
        ui.update('calc_result', f"Result: {num1} × {num2} = {result}")
        return None
    except (ValueError, TypeError):
        ui.update('calc_result', "Error: Please enter valid numbers")
        return None

def show_all_values(form_data):
    """Display all current form values"""
    results = []
    
    # Text inputs
    name = form_data.get('name_input', '')
    email = form_data.get('email_input', '')
    age = form_data.get('age_input', '')
    
    if name:
        results.append(f"Name: {name}")
    if email:
        results.append(f"Email: {email}")
    if age:
        results.append(f"Age: {age}")
    
    # Sliders
    volume = form_data.get('volume_slider', 50)
    temp = form_data.get('temp_slider', 20)
    progress = form_data.get('progress_slider', 75)
    opacity = form_data.get('opacity_slider', 0.8)
    
    results.append(f"Volume: {volume}%")
    results.append(f"Temperature: {temp}°C")
    results.append(f"Progress: {progress}%")
    results.append(f"Opacity: {opacity}")
    
    # Checkboxes
    checkboxes = []
    if form_data.get('newsletter_cb'):
        checkboxes.append("Newsletter")
    if form_data.get('notifications_cb'):
        checkboxes.append("Notifications")
    if form_data.get('darkmode_cb'):
        checkboxes.append("Dark Mode")
    if form_data.get('terms_cb'):
        checkboxes.append("Terms Accepted")
    if form_data.get('marketing_cb'):
        checkboxes.append("Marketing Emails")
    if form_data.get('autosave_cb'):
        checkboxes.append("Auto-save")
    
    if checkboxes:
        results.append(f"Enabled: {', '.join(checkboxes)}")
    
    # Radio buttons
    contact_method = form_data.get('contact_method', 'Not selected')
    difficulty = form_data.get('difficulty', 'Not selected')
    
    results.append(f"Contact Method: {contact_method}")
    results.append(f"Difficulty: {difficulty}")
    
    # Format results
    if results:
        result_text = "📋 Current Form Values:\n" + "\n".join(f"• {result}" for result in results)
    else:
        result_text = "No values entered yet"
    
    ui.update('live_results', result_text)
    return None

def handle_file_upload(form_data):
    """Handle file upload and display file info"""
    uploaded_files = []
    
    # Check if files were uploaded
    file_upload = form_data.get('file_upload')
    if file_upload:
        if hasattr(file_upload, 'filename'):
            # Single file
            uploaded_files.append(file_upload.filename)
        elif isinstance(file_upload, list):
            # Multiple files
            for file in file_upload:
                if hasattr(file, 'filename'):
                    uploaded_files.append(file.filename)
    
    if uploaded_files:
        file_info = f"📁 Uploaded {len(uploaded_files)} file(s):\n" + "\n".join(f"• {name}" for name in uploaded_files)
        ui.update('file_info', file_info)
    else:
        ui.update('file_info', "No files uploaded")
    
    return None

def clear_all_values(form_data):
    """Clear all form values and results"""
    # Clear the UI updates
    ui.update('calc_result', "Result: ")
    ui.update('live_results', "All values cleared!")
    ui.update('file_info', "No files uploaded yet")
    
    # Clear preserved form data for better user experience
    ui.clear_preserved_form_data()
    
    return None

def clear_complete_state(form_data):
    """Clear ALL state data - complete reset"""
    # Clear all state data
    ui.clear_state()
    
    # Clear UI displays
    ui.update('calc_result', "Result: ")
    ui.update('live_results', "🧹 Complete state cleared! All data has been reset.")
    ui.update('file_info', "No files uploaded yet")
    
    return None

def show_state_info(form_data):
    """Show information about current preserved state"""
    preserved_data = ui.get_preserved_form_data()
    
    if preserved_data:
        info_items = []
        for key, value in preserved_data.items():
            if isinstance(value, bool):
                info_items.append(f"• {key}: {'✅' if value else '❌'}")
            else:
                display_value = str(value)
                if len(display_value) > 30:
                    display_value = display_value[:30] + "..."
                info_items.append(f"• {key}: {display_value}")
        
        result_text = f"💾 **PRESERVED STATE** ({len(preserved_data)} items):\n\n" + "\n".join(info_items)
        result_text += "\n\n🔄 This data persists across page navigation and UI updates!"
        result_text += f"\n📁 State directory: {ui.get_state_directory()}"
    else:
        result_text = "📭 No preserved state data found."
    
    ui.update('live_results', result_text)
    return None

def dump_state_debug(form_data):
    """Dump detailed state information for debugging"""
    ui.dump_state_info()
    ui.update('live_results', "🔍 State debug information dumped to console! Check the terminal for detailed output.")
    return None

# ===== HOME PAGE =====
ui.text("🎯 Complete Framework Demo", tag="h1", area="6x1", page="Home")

ui.text("Welcome to the Complete Framework Demo! This application showcases all available components and their interactions across different pages.", 
        tag="p", area="6x1", page="Home")

ui.text("🆕 NEW: State Preservation Feature!", tag="h2", area="6x1", page="Home")
ui.text("✨ Your form data is now automatically preserved when you navigate between pages!", tag="p", area="6x1", page="Home")
ui.text("✨ Data survives UI updates, page refreshes, and app restarts!", tag="p", area="6x1", page="Home")
ui.text("✨ Try filling out forms and switching pages - your data will be there when you return!", tag="p", area="6x1", page="Home")

ui.text("📋 Available Pages:", tag="h2", area="6x1", page="Home")
ui.text("• Home - Welcome and overview (you are here)", tag="p", area="1x1", page="Home")
ui.text("• Text & Display - Text components and images", tag="p", area="1x1", page="Home")
ui.text("• Input Forms - Text inputs and form fields", tag="p", area="1x1", page="Home")
ui.text("• Interactive - Sliders, checkboxes, and radio buttons", tag="p", area="1x1", page="Home")
ui.text("• Files & Media - File uploads and media handling", tag="p", area="1x1", page="Home")
ui.text("• Calculator - Interactive calculator functionality", tag="p", area="1x1", page="Home")
ui.text("• Settings - Configuration and utilities", tag="p", area="6x1", page="Home")

ui.text("🚀 Getting Started:", tag="h2", area="6x1", page="Home")
ui.text("Navigate through the pages using the navigation menu to explore different components. Each page demonstrates specific functionality with interactive examples.", 
        tag="p", area="6x1", page="Home")

# ===== TEXT & DISPLAY PAGE =====
ui.text("📝 Text Components", tag="h1", area="6x1", page="Text & Display")

ui.text("This page demonstrates various text formatting and display options.", 
        tag="p", area="6x1", page="Text & Display")

ui.text("Text Formatting Examples:", tag="h2", area="6x1", page="Text & Display")
ui.text("This is a regular paragraph with normal text formatting.", tag="p", area="2x1", page="Text & Display")
ui.text("This is a Heading Level 3", tag="h3", area="2x1", page="Text & Display")
ui.text("This is emphasized text", tag="em", area="2x1", page="Text & Display")

ui.text("Additional Text Examples:", tag="h2", area="6x1", page="Text & Display")
ui.text("Bold text example", tag="strong", area="2x1", page="Text & Display")
ui.text("Code snippet example", tag="code", area="2x1", page="Text & Display")
ui.text("Small text example", tag="small", area="2x1", page="Text & Display")

# ===== IMAGES SECTION =====
ui.text("🖼️ Images", tag="h2", area="6x1", page="Text & Display")

ui.text("Sample Images:", area="6x1", page="Text & Display")
ui.image(src="/images/sample 1.jpg", alt="Sample Image 1", id="sample_image_1", area="3x1", page="Text & Display")
ui.image(src="/images/sample 2.jpg", alt="Sample Image 2", id="sample_image_2", area="3x1", page="Text & Display")

# ===== INPUT FORMS PAGE =====
ui.text("📋 Input Components", tag="h1", area="6x1", page="Input Forms")

ui.text("This page demonstrates various input components and form fields.", 
        tag="p", area="6x1", page="Input Forms")

# Text inputs
ui.text("Personal Information:", tag="h2", area="6x1", page="Input Forms")
ui.text("Name:", area="1x1", page="Input Forms")
ui.input(placeholder="Enter your name", id="name_input", area="2x1", page="Input Forms")
ui.text("Email:", area="1x1", page="Input Forms")
ui.input(placeholder="Enter your email", input_type="email", id="email_input", area="2x1", page="Input Forms")

ui.text("Additional Details:", tag="h2", area="6x1", page="Input Forms")
ui.text("Age:", area="1x1", page="Input Forms")
ui.input(placeholder="Enter your age", input_type="number", id="age_input", area="2x1", page="Input Forms")
ui.text("Password:", area="1x1", page="Input Forms")
ui.input(placeholder="Enter password", input_type="password", id="password_input", area="2x1", page="Input Forms")

# ===== INTERACTIVE PAGE =====
ui.text("🎛️ Interactive Components", tag="h1", area="6x1", page="Interactive")

ui.text("This page showcases interactive components like sliders, checkboxes, and radio buttons.", 
        tag="p", area="6x1", page="Interactive")

# ===== SLIDER SECTION =====
ui.text("🎚️ Sliders", tag="h2", area="6x1", page="Interactive")

ui.text("Volume:", area="1x1", page="Interactive")
ui.slider(min_value=0, max_value=100, value=50, id="volume_slider", area="2x1", page="Interactive")
ui.text("Temperature:", area="1x1", page="Interactive")
ui.slider(min_value=-10, max_value=40, value=20, step=1, id="temp_slider", area="2x1", page="Interactive")

ui.text("Progress:", area="1x1", page="Interactive")
ui.slider(min_value=0, max_value=100, value=75, id="progress_slider", area="2x1", page="Interactive")
ui.text("Opacity:", area="1x1", page="Interactive")
ui.slider(min_value=0, max_value=1, value=0.8, step=0.1, id="opacity_slider", area="2x1", page="Interactive")

# ===== CHECKBOX SECTION =====
ui.text("☑️ Checkboxes", tag="h2", area="6x1", page="Interactive")

ui.text("Preferences:", tag="h3", area="6x1", page="Interactive")
ui.checkbox(label="Subscribe to newsletter", id="newsletter_cb", area="2x1", page="Interactive")
ui.checkbox(label="Enable notifications", id="notifications_cb", checked=True, area="2x1", page="Interactive")
ui.checkbox(label="Dark mode", id="darkmode_cb", area="2x1", page="Interactive")

ui.text("Settings:", tag="h3", area="6x1", page="Interactive")
ui.checkbox(label="Accept terms", id="terms_cb", area="2x1", page="Interactive")
ui.checkbox(label="Marketing emails", id="marketing_cb", area="2x1", page="Interactive")
ui.checkbox(label="Auto-save", id="autosave_cb", checked=True, area="2x1", page="Interactive")

# ===== RADIO BUTTON SECTION =====
ui.text("🔘 Radio Buttons", tag="h2", area="6x1", page="Interactive")

ui.text("Preferred Contact Method:", tag="h3", area="6x1", page="Interactive")
ui.radio_button(label="Email", value="email", name="contact_method", checked=True, id="contact_email", area="2x1", page="Interactive")
ui.radio_button(label="Phone", value="phone", name="contact_method", id="contact_phone", area="2x1", page="Interactive")
ui.radio_button(label="Text", value="text", name="contact_method", id="contact_text", area="2x1", page="Interactive")

ui.text("Difficulty Level:", tag="h3", area="6x1", page="Interactive")
ui.radio_button(label="Easy", value="easy", name="difficulty", checked=True, id="diff_easy", area="2x1", page="Interactive")
ui.radio_button(label="Medium", value="medium", name="difficulty", id="diff_medium", area="2x1", page="Interactive")
ui.radio_button(label="Hard", value="hard", name="difficulty", id="diff_hard", area="2x1", page="Interactive")

# ===== FILES & MEDIA PAGE =====
ui.text("📂 Files & Media", tag="h1", area="6x1", page="Files & Media")

ui.text("This page demonstrates file upload functionality and media handling.", 
        tag="p", area="6x1", page="Files & Media")

# ===== FILE UPLOAD SECTION =====
ui.text("📁 File Upload", tag="h2", area="6x1", page="Files & Media")

ui.file_upload(id="file_upload", accept="*", multiple=True, 
               placeholder="Drop files here or click to upload", area="2x1", page="Files & Media")
ui.text("No files uploaded yet", id="file_info", area="2x1", page="Files & Media")

# File processing button
ui.button("📁 Process Files", callback=handle_file_upload, id="process_files_btn", area="2x1", page="Files & Media")

# ===== CALCULATOR PAGE =====
ui.text("🧮 Calculator", tag="h1", area="6x1", page="Calculator")

ui.text("This page provides calculator functionality with interactive buttons.", 
        tag="p", area="6x1", page="Calculator")

# ===== CALCULATOR SECTION =====
ui.text("Calculator:", tag="h2", area="6x1", page="Calculator")
ui.text("Number 1:", area="1x1", page="Calculator")
ui.input(placeholder="First number", id="calc_num1", input_type="number", area="2x1", page="Calculator")
ui.text("Number 2:", area="1x1", page="Calculator")
ui.input(placeholder="Second number", id="calc_num2", input_type="number", area="2x1", page="Calculator")

ui.text("Result: ", id="calc_result", area="6x1", page="Calculator")

# Calculator buttons
ui.button("➕ Add", callback=calculate_sum, id="add_btn", area="3x1", page="Calculator")
ui.button("✖️ Multiply", callback=calculate_multiply, id="multiply_btn", area="3x1", page="Calculator")

# ===== SETTINGS PAGE =====
ui.text("⚙️ Settings & Utilities", tag="h1", area="6x1", page="Settings")

ui.text("This page provides utility functions and settings for the application.", 
        tag="p", area="6x1", page="Settings")

# ===== RESULT DISPLAY SECTION =====
ui.text("📊 Live Results", tag="h2", area="6x1", page="Settings")

ui.text("Current values will appear here:", id="live_results", area="6x1", page="Settings")

# Action buttons
ui.text("Actions:", tag="h2", area="6x1", page="Settings")
ui.button("📊 Show All Values", callback=show_all_values, id="show_values_btn", area="2x1", page="Settings")
ui.button("💾 Show Preserved State", callback=show_state_info, id="show_state_btn", area="2x1", page="Settings")
ui.button("Debug State Info", callback=dump_state_debug, id="debug_state_btn", area="2x1", page="Settings")

ui.text("Clear Options:", tag="h2", area="6x1", page="Settings")
ui.button("Clear Form Data", callback=clear_all_values, id="clear_btn", area="3x1", page="Settings")
ui.button("🧹 Clear ALL State", callback=clear_complete_state, id="clear_state_btn", area="3x1", page="Settings")
ui.button("🧹 Clear Complete State", callback=clear_complete_state, id="clear_complete_btn", area="2x1", page="Settings")
ui.button("🔍 Dump State Debug Info", callback=dump_state_debug, id="dump_state_btn", area="2x1", page="Settings")

# ===== FOOTER =====
ui.text("✨ Demo completed! Try interacting with the components across all pages.", 
        tag="p", area="6x1", page="Settings")

ui.text("🔄 State Preservation Testing:", tag="h3", area="6x1", page="Settings")
ui.text("1. Fill out forms on different pages", tag="p", area="6x1", page="Settings")
ui.text("2. Switch between pages - your data persists!", tag="p", area="6x1", page="Settings")
ui.text("3. Click buttons and see updates don't clear your forms", tag="p", area="6x1", page="Settings")
ui.text("4. Refresh the page - preserved data remains!", tag="p", area="6x1", page="Settings")

# ===== RUN THE APPLICATION =====
if __name__ == "__main__":
    print("🚀 Starting Complete Framework Demo with Enhanced State Management...")
    print("🌐 Open your browser and navigate to http://127.0.0.1:5000")
    print("💡 Try interacting with all the different components!")
    print("🆕 ENHANCED STATE FEATURES:")
    print("   📁 Dedicated 'state' folder for organized data storage")
    print("   ✨ State Preservation - Your form data persists across page navigation!")
    print("   ✨ Auto-save - Data is automatically saved every 2 seconds")
    print("   ✨ Update Safety - UI updates don't clear your form data")
    print("   ✨ Persistent Storage - Data survives page refresh and app restart")
    print("   🧹 Complete state reset functionality available")
    print("   🔍 Debug state information for troubleshooting")
    ui.run(port=5000)