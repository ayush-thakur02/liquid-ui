from framework import create_ui
import random
import time

# Create a new UI instance with state preservation enabled
ui = create_ui(title="State Preservation Demo", columns=4, persist_state=True)

# ===== CALLBACK FUNCTIONS =====

def process_user_data(form_data):
    """Process user data and demonstrate state preservation"""
    try:
        # Get form values
        name = form_data.get('user_name', '')
        email = form_data.get('user_email', '')
        age = form_data.get('user_age', '')
        bio = form_data.get('user_bio', '')
        
        # Get preferences
        notifications = form_data.get('notifications_enabled', False)
        newsletter = form_data.get('newsletter_sub', False)
        theme = form_data.get('preferred_theme', 'light')
        
        # Get settings
        volume = form_data.get('volume_level', 50)
        quality = form_data.get('quality_setting', 'medium')
        
        # Format results
        results = []
        if name:
            results.append(f"👤 Name: {name}")
        if email:
            results.append(f"📧 Email: {email}")
        if age:
            results.append(f"🎂 Age: {age}")
        if bio:
            results.append(f"📝 Bio: {bio[:50]}{'...' if len(bio) > 50 else ''}")
        
        results.append(f"🔔 Notifications: {'✅' if notifications else '❌'}")
        results.append(f"📰 Newsletter: {'✅' if newsletter else '❌'}")
        results.append(f"🎨 Theme: {theme.title()}")
        results.append(f"🔊 Volume: {volume}%")
        results.append(f"⚙️ Quality: {quality.title()}")
        
        result_text = "📋 **PROCESSED DATA** (All values preserved!):\n\n" + "\n".join(results)
        result_text += f"\n\n⏰ Processed at: {time.strftime('%H:%M:%S')}"
        
        ui.update('processing_results', result_text)
        
        # Also update a status message
        ui.update('status_message', f"✅ Data processed successfully! Switch pages and come back - your data will be preserved.")
        
        return None
        
    except Exception as e:
        ui.update('processing_results', f"❌ Error processing data: {str(e)}")
        return None

def simulate_work(form_data):
    """Simulate some work and show that state is preserved during updates"""
    steps = [
        "🔄 Starting process...",
        "📊 Analyzing data...",
        "🔍 Validating inputs...",
        "💾 Saving to database...",
        "✅ Process completed!"
    ]
    
    for i, step in enumerate(steps):
        ui.update('work_status', f"Step {i+1}/5: {step}")
        time.sleep(0.5)  # Simulate work
    
    # Final message
    ui.update('work_status', "🎯 All done! Your form data remained intact during this process.")
    
    return None

def reset_form_data(form_data):
    """Reset specific form data"""
    # Clear specific fields
    ui.clear_preserved_form_data(['user_name', 'user_email', 'user_age', 'user_bio'])
    
    # Update display
    ui.update('processing_results', "🗑️ User data cleared! Other settings preserved.")
    ui.update('status_message', "Form data partially reset. Page navigation will now start fresh for cleared fields.")
    
    return None

def clear_all_data(form_data):
    """Clear all preserved data"""
    ui.clear_preserved_form_data()  # Clear all preserved data
    
    ui.update('processing_results', "🧹 All preserved data cleared!")
    ui.update('status_message', "Complete reset done. All form fields will be empty on page navigation.")
    ui.update('work_status', "Ready for new data...")
    
    return None

def show_preserved_data(form_data):
    """Show what data is currently preserved"""
    preserved_data = ui.get_preserved_form_data()
    
    if preserved_data:
        data_items = []
        for key, value in preserved_data.items():
            if isinstance(value, bool):
                data_items.append(f"• {key}: {'✅' if value else '❌'}")
            else:
                data_items.append(f"• {key}: {str(value)[:30]}{'...' if len(str(value)) > 30 else ''}")
        
        result = f"💾 **PRESERVED DATA** ({len(preserved_data)} items):\n\n" + "\n".join(data_items)
    else:
        result = "📭 No data is currently preserved."
    
    ui.update('processing_results', result)
    return None

# ===== HOME PAGE =====
ui.text("🔄 State Preservation Demo", tag="h1", area="4x1", page="Home")
ui.text("This demo showcases the new state preservation feature that prevents data loss during page navigation and UI updates.", 
        tag="p", area="4x1", page="Home")

ui.text("🎯 **Key Features:**", tag="h2", area="4x1", page="Home")
ui.text("• **Auto-save**: Form data is automatically saved every 2 seconds", tag="p", area="4x1", page="Home")
ui.text("• **Page Navigation**: Switch between pages without losing your input", tag="p", area="4x1", page="Home")
ui.text("• **Update Preservation**: Data remains intact when UI components are updated", tag="p", area="4x1", page="Home")
ui.text("• **Persistent State**: Data survives browser refresh and app restart", tag="p", area="4x1", page="Home")

ui.text("🧪 **How to Test:**", tag="h2", area="4x1", page="Home")
ui.text("1. Go to the 'User Input' page and fill out the form", tag="p", area="4x1", page="Home")
ui.text("2. Switch to other pages and come back - your data will still be there!", tag="p", area="4x1", page="Home")
ui.text("3. Click process buttons to see updates don't clear your form", tag="p", area="4x1", page="Home")
ui.text("4. Even refresh the page - your data persists!", tag="p", area="4x1", page="Home")

ui.text("🚀 Navigate to 'User Input' to start testing!", tag="h2", area="4x1", page="Home")

# ===== USER INPUT PAGE =====
ui.text("👤 User Information", tag="h1", area="4x1", page="User Input")
ui.text("Fill out this form, then navigate between pages to see state preservation in action!", 
        tag="p", area="4x1", page="User Input")

# Personal Information Section
ui.text("📝 Personal Details:", tag="h2", area="4x1", page="User Input")

ui.text("Full Name:", area="1x1", page="User Input")
ui.input(placeholder="Enter your full name", id="user_name", area="3x1", page="User Input")

ui.text("Email:", area="1x1", page="User Input")
ui.input(placeholder="your.email@domain.com", input_type="email", id="user_email", area="3x1", page="User Input")

ui.text("Age:", area="1x1", page="User Input")
ui.input(placeholder="Your age", input_type="number", id="user_age", area="3x1", page="User Input")

ui.text("Bio:", area="1x1", page="User Input")
ui.input(placeholder="Tell us about yourself...", id="user_bio", area="3x1", page="User Input")

# ===== PREFERENCES PAGE =====
ui.text("⚙️ Preferences & Settings", tag="h1", area="4x1", page="Preferences")
ui.text("Adjust your preferences below. These settings will be preserved across page navigation!", 
        tag="p", area="4x1", page="Preferences")

# Checkbox preferences
ui.text("🔔 Notifications:", tag="h2", area="4x1", page="Preferences")
ui.checkbox(label="Enable notifications", id="notifications_enabled", area="2x1", page="Preferences")
ui.checkbox(label="Subscribe to newsletter", id="newsletter_sub", area="2x1", page="Preferences")

# Radio button preferences
ui.text("🎨 Theme Preference:", tag="h2", area="4x1", page="Preferences")
ui.radio_button(label="Light Theme", value="light", name="preferred_theme", checked=True, area="2x1", page="Preferences")
ui.radio_button(label="Dark Theme", value="dark", name="preferred_theme", area="2x1", page="Preferences")

# Slider preferences
ui.text("🔊 Audio Settings:", tag="h2", area="4x1", page="Preferences")
ui.text("Volume Level:", area="1x1", page="Preferences")
ui.slider(min_value=0, max_value=100, value=50, id="volume_level", area="3x1", page="Preferences")

# More radio options
ui.text("📺 Quality Setting:", tag="h2", area="4x1", page="Preferences")
ui.radio_button(label="Low", value="low", name="quality_setting", area="1x1", page="Preferences")
ui.radio_button(label="Medium", value="medium", name="quality_setting", checked=True, area="1x1", page="Preferences")
ui.radio_button(label="High", value="high", name="quality_setting", area="1x1", page="Preferences")
ui.radio_button(label="Ultra", value="ultra", name="quality_setting", area="1x1", page="Preferences")

# ===== PROCESSING PAGE =====
ui.text("🔄 Data Processing", tag="h1", area="4x1", page="Processing")
ui.text("Use the buttons below to process your data. Notice how your form data stays intact during processing!", 
        tag="p", area="4x1", page="Processing")

# Status displays
ui.text("📋 Processing Results:", tag="h2", area="4x1", page="Processing")
ui.text("No data processed yet. Click 'Process Data' to see your preserved form values!", 
        id="processing_results", area="4x1", page="Processing")

ui.text("📊 Work Status:", tag="h2", area="4x1", page="Processing")
ui.text("Ready to process...", id="work_status", area="4x1", page="Processing")

ui.text("💬 Status Message:", tag="h2", area="4x1", page="Processing")
ui.text("Fill out the forms on other pages, then come back here to process!", 
        id="status_message", area="4x1", page="Processing")

# Action buttons
ui.text("🎛️ Actions:", tag="h2", area="4x1", page="Processing")
ui.button("📊 Process Data", callback=process_user_data, area="2x1", page="Processing")
ui.button("⚙️ Simulate Work", callback=simulate_work, area="2x1", page="Processing")
ui.button("🔍 Show Preserved Data", callback=show_preserved_data, area="2x1", page="Processing")
ui.button("🗑️ Reset User Data", callback=reset_form_data, area="2x1", page="Processing")

# ===== UTILITIES PAGE =====
ui.text("🛠️ Utilities & Controls", tag="h1", area="4x1", page="Utilities")
ui.text("Advanced controls for managing the state preservation system.", 
        tag="p", area="4x1", page="Utilities")

ui.text("🎮 State Management:", tag="h2", area="4x1", page="Utilities")
ui.button("🧹 Clear All Data", callback=clear_all_data, area="4x1", page="Utilities")

ui.text("📋 Instructions:", tag="h2", area="4x1", page="Utilities")
ui.text("1. **Test Navigation**: Fill forms on other pages, switch pages, come back", tag="p", area="4x1", page="Utilities")
ui.text("2. **Test Updates**: Click processing buttons - your form data survives!", tag="p", area="4x1", page="Utilities")
ui.text("3. **Test Persistence**: Refresh browser or restart app - data remains!", tag="p", area="4x1", page="Utilities")
ui.text("4. **Auto-save**: Watch console logs to see automatic saving every 2 seconds", tag="p", area="4x1", page="Utilities")

ui.text("🔧 Technical Details:", tag="h2", area="4x1", page="Utilities")
ui.text("• Form data is saved both locally (localStorage) and on server", tag="p", area="4x1", page="Utilities")
ui.text("• Data is automatically restored when pages load", tag="p", area="4x1", page="Utilities")
ui.text("• Updates preserve existing form state instead of clearing it", tag="p", area="4x1", page="Utilities")
ui.text("• Navigation includes form data in URL parameters for seamless transition", tag="p", area="4x1", page="Utilities")

# ===== RUN THE APPLICATION =====
if __name__ == "__main__":
    print("🚀 Starting State Preservation Demo...")
    print("🌐 Open your browser and navigate to http://127.0.0.1:5000")
    print("💡 Features to test:")
    print("   • Fill out forms and navigate between pages")
    print("   • Click processing buttons and see data preservation")
    print("   • Refresh the page and see persistent state")
    print("   • Check browser console for auto-save logs")
    ui.run(port=5000)
