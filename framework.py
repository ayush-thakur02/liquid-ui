from flask import Flask, render_template, request, jsonify, send_from_directory
from utils.grid_layout import GridLayout
from utils.components import Text, InputBox, Button, Slider, Checkbox, RadioButton, RadioGroup, Image, FileUpload
from utils.state_manager import get_state_manager
import json
import os


class FlaskUI:
    """Flask wrapper for creating grid-based UIs similar to Gradio with enhanced state preservation"""
    
    def __init__(self, title="Flask UI", columns=5, debug=True, persist_state=True):
        self.app = Flask(__name__)
        self.title = title
        self.layout = GridLayout(columns=columns)
        self.debug = debug
        self.callbacks = {}
        self.state = get_state_manager(app_name=title.lower().replace(" ", "_"), persist=persist_state)
        self._pending_updates = {}
        self.current_page = "Home"
        self.auto_save_form_data = True  # Enable automatic form data preservation
        # Setup routes
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup Flask routes"""        
        @self.app.route('/')
        def index():
            # Get preserved form data for restoration
            form_data = self.state.get_all_form_data() if self.auto_save_form_data else {}
            
            return render_template('index.html',
                                 title=self.title,
                                 grid_content=self.layout.render(self.current_page),
                                 pages=self.layout.get_page_names(),
                                 current_page=self.current_page,
                                 preserved_form_data=json.dumps(form_data))
        
        @self.app.route('/page/<page_name>')
        def switch_page(page_name):
            """Switch to a different page with state preservation"""
            # Preserve current form data before switching
            if self.auto_save_form_data and request.args.get('form_data'):
                try:
                    current_form_data = json.loads(request.args.get('form_data'))
                    self.state.update_form_data(current_form_data)
                except:
                    pass  # Continue even if form data parsing fails
            
            if self.layout.set_current_page(page_name):
                self.current_page = page_name
            
            # Get preserved form data for the new page
            form_data = self.state.get_all_form_data() if self.auto_save_form_data else {}
            
            return render_template('index.html',
                                 title=self.title,
                                 grid_content=self.layout.render(self.current_page),
                                 pages=self.layout.get_page_names(),
                                 current_page=self.current_page,
                                 preserved_form_data=json.dumps(form_data))
        
        @self.app.route('/api/preserve-form', methods=['POST'])
        def preserve_form_data():
            """API endpoint to preserve form data"""
            try:
                form_data = request.get_json() or {}
                if self.auto_save_form_data:
                    self.state.update_form_data(form_data)
                return jsonify({"status": "success"})
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)})
        
        @self.app.route('/images/<filename>')
        def serve_image(filename):
            """Serve images from the images folder"""
            images_dir = os.path.join(os.getcwd(), 'images')
            if os.path.exists(images_dir):
                return send_from_directory(images_dir, filename)
            else:
                # Return a 404 if images directory doesn't exist
                return "Image not found", 404
        
        @self.app.route('/api/button/<button_id>', methods=['POST'])
        def handle_button_click(button_id):
            """Handle button click events with state preservation"""
            print(f"Button clicked: {button_id}")
            print(f"Available callbacks: {list(self.callbacks.keys())}")
            
            if button_id in self.callbacks:
                try:
                    # Clear any pending updates
                    self._pending_updates = {}
                    
                    # Get form data (handle both JSON and form data with files)
                    if request.content_type and 'multipart/form-data' in request.content_type:
                        # Handle file uploads
                        form_data = {}
                        for key, value in request.form.items():
                            form_data[key] = value
                        
                        # Add files to form_data
                        for key, file in request.files.items():
                            form_data[key] = file
                        print(f"Form data with files received: {[k for k in form_data.keys()]}")
                    else:
                        # Handle regular JSON data
                        form_data = request.get_json() or {}
                        print(f"JSON form data received: {form_data}")
                    
                    # Preserve form data before callback execution
                    if self.auto_save_form_data:
                        # Filter out file objects for preservation
                        preservable_data = {k: v for k, v in form_data.items() 
                                          if not hasattr(v, 'filename')}
                        self.state.update_form_data(preservable_data)
                    
                    result = self.callbacks[button_id](form_data)
                      # Get any pending updates from the callback
                    updates = getattr(self, '_pending_updates', {})
                    
                    # Include preserved form data in response for client-side restoration
                    preserved_data = self.state.get_all_form_data() if self.auto_save_form_data else {}
                    
                    print(f"Callback result: {result}")
                    print(f"Pending updates: {updates}")
                    print(f"Preserved form data: {len(preserved_data)} items")
                    
                    return jsonify({
                        "status": "success", 
                        "result": result, 
                        "updates": updates,
                        "preserved_form_data": preserved_data
                    })
                except Exception as e:
                    print(f"Callback error: {e}")
                    return jsonify({"status": "error", "message": str(e)})
            else:
                print(f"Button {button_id} not found in callbacks")
                return jsonify({"status": "error", "message": f"Button {button_id} not found"})
    
    def add_text(self, text="", tag="p", id=None, classes="", style="", area="1x1", page="Home"):
        """Add a text component to the grid"""
        component = Text(text=text, tag=tag, id=id, classes=classes, style=style, area=area, page=page)
        self.layout.add_component(component)
        return component
    
    def add_input(self, placeholder="", value="", input_type="text", id=None, classes="", style="", area="1x1", page="Home"):
        """Add an input box component to the grid"""
        component = InputBox(placeholder=placeholder, value=value, input_type=input_type,
                           id=id, classes=classes, style=style, area=area, page=page)
        self.layout.add_component(component)
        return component
    
    def add_button(self, text="Click Me", callback=None, id=None, classes="", style="", area="1x1", page="Home"):
        """Add a button component to the grid"""
        if not id:
            id = f"btn_{len([c for c in self.layout.components if isinstance(c, Button)])}"
        
        # Setup JavaScript onclick to call API
        onclick = f"handleButtonClick('{id}')"
        component = Button(text=text, onclick=onclick, id=id, classes=classes, style=style, area=area, page=page)
        
        if callback:
            self.callbacks[id] = callback
        
        self.layout.add_component(component)
        return component
    
    def add_slider(self, min_value=0, max_value=100, value=50, step=1, id=None, classes="", style="", area="1x1", page="Home"):
        """Add a slider component to the grid"""
        component = Slider(min_value=min_value, max_value=max_value, value=value, step=step,
                          id=id, classes=classes, style=style, area=area, page=page)
        self.layout.add_component(component)
        return component
    
    def add_checkbox(self, label="", checked=False, value="on", id=None, classes="", style="", area="1x1", page="Home"):
        """Add a checkbox component to the grid"""
        component = Checkbox(label=label, checked=checked, value=value,
                           id=id, classes=classes, style=style, area=area, page=page)
        self.layout.add_component(component)
        return component
    
    def add_radio_button(self, label="", value="", name="radio_group", checked=False, id=None, classes="", style="", area="1x1", page="Home"):
        """Add a radio button component to the grid"""
        component = RadioButton(label=label, value=value, name=name, checked=checked,                              id=id, classes=classes, style=style, area=area, page=page)
        self.layout.add_component(component)
        return component
    
    def add_radio_group(self, name, options, selected_value=None, id=None, classes="", style="", area="1x1", page="Home"):
        """Add a group of radio buttons to the grid"""
        radio_group = RadioGroup(name=name)
        components = []
        
        for i, option in enumerate(options):
            if isinstance(option, dict):
                label = option.get('label', '')
                value = option.get('value', '')
                checked = (selected_value == value) if selected_value else (i == 0)
            else:
                label = str(option)
                value = str(option)
                checked = (selected_value == value) if selected_value else (i == 0)
            
            radio_id = f"{id}_option_{i}" if id else None
            radio = self.add_radio_button(label=label, value=value, name=name, checked=checked,
                                        id=radio_id, classes=classes, style=style, area=area, page=page)
            components.append(radio)
            radio_group.radio_buttons.append(radio)        
        return radio_group

    def add_image(self, src="", alt="Image", width="", height="", id=None, classes="", style="", area="1x1", page="Home"):
        """Add an image component to the grid"""
        component = Image(src=src, alt=alt, width=width, height=height,
                         id=id, classes=classes, style=style, area=area, page=page)
        self.layout.add_component(component)
        return component
    
    def add_file_upload(self, accept="*", multiple=True, placeholder="Drop files here or click to upload", id=None, classes="", style="", area="1x1", page="Home"):
        """Add a file upload component to the grid"""
        component = FileUpload(accept=accept, multiple=multiple, placeholder=placeholder,
                             id=id, classes=classes, style=style, area=area, page=page)
        self.layout.add_component(component)
        return component

    def add_component_at(self, component, row, col):
        """Add a component at a specific grid position"""
        self.layout.add_component_at(component, row, col)
    
    def text(self, text="", tag="p", **kwargs):
        """Shorthand for add_text"""
        return self.add_text(text=text, tag=tag, **kwargs)
    
    def input(self, placeholder="", **kwargs):
        """Shorthand for add_input"""
        return self.add_input(placeholder=placeholder, **kwargs)
    
    def button(self, text="Click Me", callback=None, **kwargs):
        """Shorthand for add_button"""
        return self.add_button(text=text, callback=callback, **kwargs)
    
    def slider(self, min_value=0, max_value=100, value=50, step=1, **kwargs):
        """Shorthand for add_slider"""
        return self.add_slider(min_value=min_value, max_value=max_value, value=value, step=step, **kwargs)
    
    def checkbox(self, label="", checked=False, **kwargs):
        """Shorthand for add_checkbox"""
        return self.add_checkbox(label=label, checked=checked, **kwargs)
    
    def radio_button(self, label="", value="", name="radio_group", **kwargs):
        """Shorthand for add_radio_button"""
        return self.add_radio_button(label=label, value=value, name=name, **kwargs)
    
    def radio_group(self, name, options, selected_value=None, **kwargs):
        """Shorthand for add_radio_group"""
        return self.add_radio_group(name=name, options=options, selected_value=selected_value, **kwargs)
    
    def image(self, src="", alt="Image", **kwargs):
        """Shorthand for add_image"""
        return self.add_image(src=src, alt=alt, **kwargs)
    
    def file_upload(self, accept="*", multiple=True, **kwargs):
        """Shorthand for add_file_upload"""
        return self.add_file_upload(accept=accept, multiple=multiple, **kwargs)

    def get_component(self, component_id):
        """Get a component by its ID"""
        return self.layout.get_component_by_id(component_id)
    
    def clear(self):
        """Clear all components from the grid"""
        self.layout.clear()
        self.callbacks.clear()
    
    # Enhanced state management methods
    def set_state(self, key, value):
        """Set a state value"""
        self.state.set(key, value)
    
    def get_state(self, key, default=None):
        """Get a state value"""
        return self.state.get(key, default)
    
    def update_state(self, updates):
        """Update multiple state values"""
        self.state.update(updates)
    
    def clear_state(self):
        """Clear ALL state data (complete reset)"""
        print(f"🧹 Clearing all state for '{self.title}'...")
        self.state.clear_state()
        # Also clear any pending updates
        self._pending_updates = {}
        print("✅ All state data cleared!")
        return self
    
    def get_all_state(self):
        """Get all state values"""
        return self.state.get_all()

    def update(self, component_id, value):
        """Update a specific component's value with state preservation"""
        # Store updates to be sent to frontend
        if not hasattr(self, '_pending_updates'):
            self._pending_updates = {}
        self._pending_updates[component_id] = value
        
        # Also preserve this update in the state manager
        if self.auto_save_form_data:
            self.state.set_form_data(component_id, value)
        
        return None

    # Enhanced state preservation methods
    def preserve_form_state(self, enable=True):
        """Enable or disable automatic form state preservation"""
        self.auto_save_form_data = enable
        print(f"📝 Form state preservation: {'Enabled' if enable else 'Disabled'}")
        return self
    
    def get_preserved_form_data(self):
        """Get all preserved form data"""
        return self.state.get_all_form_data()
    
    def clear_preserved_form_data(self, component_ids=None):
        """Clear preserved form data"""
        self.state.clear_form_data(component_ids)
        if component_ids:
            print(f"🗑️ Cleared form data for: {component_ids}")
        else:
            print("🗑️ All form data cleared!")
        return self
    
    def restore_component_value(self, component_id, default=None):
        """Restore a component's value from preserved state"""
        return self.state.get_form_data(component_id, default)
    
    def dump_state_info(self):
        """Dump comprehensive state information for debugging"""
        self.state._dump_all_data()
        return self
    
    def get_state_directory(self):
        """Get the path to the state directory"""
        return str(self.state.app_state_dir)
    
    def export_state(self, filename=None):
        """Export all state data to a file"""
        result = self.state.export_state(filename)
        print(result)
        return result
    
    def import_state(self, filename):
        """Import state data from a file"""
        result = self.state.import_state(filename)
        print(result)
        return result

    # Page management methods
    def set_page(self, page_name):
        """Set the current active page"""
        self.current_page = page_name
        return self.layout.set_current_page(page_name)
    
    def get_pages(self):
        """Get all page names"""
        return self.layout.get_page_names()
    
    def clear_page(self, page_name):
        """Clear all components from a specific page"""
        self.layout.clear_page(page_name)

    def run(self, host='127.0.0.1', port=5000):
        """Run the Flask application"""
        print(f"🚀 Starting Flask UI: {self.title}")
        print(f"🌐 Visit: http://{host}:{port}")
        print(f"📁 State directory: {self.get_state_directory()}")
        print(f"💾 State persistence: {'Enabled' if self.state.persist else 'Disabled'}")
        print(f"📝 Form data preservation: {'Enabled' if self.auto_save_form_data else 'Disabled'}")
        self.app.run(host=host, port=port, debug=self.debug)


# Convenience function to create a new UI instance
def create_ui(title="Flask UI", columns=5, debug=True, persist_state=True):
    """Create a new FlaskUI instance with enhanced state management"""
    return FlaskUI(title=title, columns=columns, debug=debug, persist_state=persist_state)
