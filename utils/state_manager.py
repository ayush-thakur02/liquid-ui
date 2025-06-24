import json
import os
import time
from typing import Any, Dict, Optional
from pathlib import Path


class StateManager:
    """Enhanced state management with dedicated state folder and persistent storage"""
    
    def __init__(self, app_name="flask_ui", persist=True):
        self.app_name = self._sanitize_filename(app_name)
        self.persist = persist
        self.state = {}
        self.form_data = {}  # Store current form values
        self.component_states = {}  # Store component-specific states
        
        # Create state directory structure
        self.state_dir = Path("state")
        self.app_state_dir = self.state_dir / self.app_name
        
        # Initialize state directory
        self._initialize_state_directory()
        
        # Define file paths within the app's state directory
        self.state_file = self.app_state_dir / "app_state.json"
        self.form_data_file = self.app_state_dir / "form_data.json"
        self.component_states_file = self.app_state_dir / "component_states.json"
        self.metadata_file = self.app_state_dir / "metadata.json"
        
        if self.persist:
            self._load_all_state()
            self._verify_state_integrity()
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize filename to be safe for filesystem"""
        # Replace spaces and special characters with underscores
        safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
        sanitized = "".join(c if c in safe_chars else "_" for c in name)
        return sanitized.lower()
    
    def _initialize_state_directory(self):
        """Initialize the state directory structure"""
        try:
            # Create main state directory
            self.state_dir.mkdir(exist_ok=True)
            
            # Create app-specific directory
            self.app_state_dir.mkdir(exist_ok=True)
            
            print(f"📁 State directory initialized: {self.app_state_dir}")
            
        except Exception as e:
            print(f"⚠️ Warning: Could not create state directory: {e}")
            # Fallback to current directory
            self.app_state_dir = Path(".")
    
    def _get_timestamp(self) -> float:
        """Get current timestamp"""
        return time.time()
    
    def _create_metadata(self) -> Dict[str, Any]:
        """Create metadata for the state files"""
        return {
            "app_name": self.app_name,
            "created_at": self._get_timestamp(),
            "last_updated": self._get_timestamp(),
            "version": "1.0",
            "state_items": len(self.state),
            "form_data_items": len(self.form_data),
            "component_states_items": len(self.component_states)
        }
    
    def _update_metadata(self):
        """Update metadata with current information"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    metadata = json.load(f)
            except:
                metadata = self._create_metadata()
        else:
            metadata = self._create_metadata()
        
        # Update current stats
        metadata.update({
            "last_updated": self._get_timestamp(),
            "state_items": len(self.state),
            "form_data_items": len(self.form_data),
            "component_states_items": len(self.component_states)
        })
        
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2, default=str)
        except Exception as e:
            print(f"⚠️ Warning: Could not update metadata: {e}")
    
    def _verify_state_integrity(self):
        """Verify the integrity of loaded state data"""
        try:
            total_items = len(self.state) + len(self.form_data) + len(self.component_states)
            if total_items > 0:
                print(f"✅ State integrity verified: {total_items} total items loaded")
                print(f"   📊 App state: {len(self.state)} items")
                print(f"   📝 Form data: {len(self.form_data)} items") 
                print(f"   🧩 Component states: {len(self.component_states)} items")
            else:
                print("📭 No existing state data found - starting fresh")
        except Exception as e:
            print(f"⚠️ State integrity check failed: {e}")
    
    def _dump_all_data(self):
        """Dump all current data to console for debugging"""
        print("\n" + "="*50)
        print(f"📊 COMPLETE STATE DUMP for '{self.app_name}'")
        print("="*50)
        
        print(f"\n📁 State Directory: {self.app_state_dir}")
        print(f"💾 Persistence: {'Enabled' if self.persist else 'Disabled'}")
        
        print(f"\n🏢 APP STATE ({len(self.state)} items):")
        if self.state:
            for key, value in self.state.items():
                print(f"   • {key}: {str(value)[:100]}{'...' if len(str(value)) > 100 else ''}")
        else:
            print("   (empty)")
        
        print(f"\n📝 FORM DATA ({len(self.form_data)} items):")
        if self.form_data:
            for key, value in self.form_data.items():
                if isinstance(value, dict):
                    display_value = value.get('value', 'N/A')
                    data_type = value.get('type', 'unknown')
                    timestamp = value.get('timestamp', 'N/A')
                    print(f"   • {key}: {display_value} ({data_type}) [{timestamp}]")
                else:
                    print(f"   • {key}: {value}")
        else:
            print("   (empty)")
        
        print(f"\n🧩 COMPONENT STATES ({len(self.component_states)} items):")
        if self.component_states:
            for key, value in self.component_states.items():
                print(f"   • {key}: {str(value)[:100]}{'...' if len(str(value)) > 100 else ''}")
        else:
            print("   (empty)")
        
        # File existence check
        print(f"\n📂 STATE FILES:")
        files_info = [
            ("App State", self.state_file),
            ("Form Data", self.form_data_file),
            ("Component States", self.component_states_file),
            ("Metadata", self.metadata_file)
        ]
        
        for name, file_path in files_info:
            exists = "✅" if file_path.exists() else "❌"
            size = f"({file_path.stat().st_size} bytes)" if file_path.exists() else "(not found)"
            print(f"   {exists} {name}: {file_path} {size}")
        
        print("="*50 + "\n")
    
    def set(self, key: str, value: Any) -> None:
        """Set a state value"""
        self.state[key] = value
        if self.persist:
            self.save_state()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a state value"""
        return self.state.get(key, default)
    
    def update(self, updates: Dict[str, Any]) -> None:
        """Update multiple state values"""
        self.state.update(updates)
        if self.persist:
            self.save_state()
    
    def delete(self, key: str) -> None:
        """Delete a state value"""
        if key in self.state:
            del self.state[key]
            if self.persist:
                self.save_state()
    
    def clear(self) -> None:
        """Clear all state"""
        self.state.clear()
        if self.persist:
            self.save_state()
    
    def get_all(self) -> Dict[str, Any]:
        """Get all state values"""
        return self.state.copy()
    
    # Enhanced form data preservation methods
    def set_form_data(self, component_id: str, value: Any, component_type: str = "input") -> None:
        """Set form data for a specific component"""
        self.form_data[component_id] = {
            'value': value,
            'type': component_type,
            'timestamp': self._get_timestamp()
        }
        if self.persist:
            self.save_form_data()
    
    def get_form_data(self, component_id: str, default: Any = None) -> Any:
        """Get form data for a specific component"""
        if component_id in self.form_data:
            return self.form_data[component_id]['value']
        return default
    
    def get_all_form_data(self) -> Dict[str, Any]:
        """Get all form data as a simplified dict"""
        return {k: v['value'] for k, v in self.form_data.items()}
    
    def update_form_data(self, form_updates: Dict[str, Any]) -> None:
        """Update multiple form data values"""
        timestamp = self._get_timestamp()
        for component_id, value in form_updates.items():
            self.form_data[component_id] = {
                'value': value,
                'type': self._detect_component_type(value),
                'timestamp': timestamp
            }
        if self.persist:
            self.save_form_data()
    
    def clear_form_data(self, component_ids: Optional[list] = None) -> None:
        """Clear form data for specific components or all if none specified"""
        if component_ids:
            for component_id in component_ids:
                if component_id in self.form_data:
                    del self.form_data[component_id]
        else:
            self.form_data.clear()
        
        if self.persist:
            self.save_form_data()
    
    def preserve_component_state(self, component_id: str, state_data: Dict[str, Any]) -> None:
        """Preserve component-specific state data"""
        self.component_states[component_id] = {
            **state_data,
            'timestamp': self._get_timestamp()
        }
        if self.persist:
            self.save_component_states()
    
    def get_component_state(self, component_id: str) -> Dict[str, Any]:
        """Get component-specific state data"""
        return self.component_states.get(component_id, {})
    
    def clear_state(self) -> None:
        """Clear ALL state data (app state, form data, component states)"""
        print(f"🧹 Clearing all state data for '{self.app_name}'...")
        
        # Clear in-memory data
        self.state.clear()
        self.form_data.clear() 
        self.component_states.clear()
        
        # Remove state files
        files_to_remove = [
            self.state_file,
            self.form_data_file,
            self.component_states_file,
            self.metadata_file
        ]
        
        removed_count = 0
        for file_path in files_to_remove:
            try:
                if file_path.exists():
                    file_path.unlink()
                    removed_count += 1
                    print(f"   🗑️ Removed: {file_path.name}")
            except Exception as e:
                print(f"   ⚠️ Could not remove {file_path.name}: {e}")
        
        print(f"✅ State cleared: {removed_count} files removed")
        
        # Try to remove app directory if empty
        try:
            if self.app_state_dir.exists() and not any(self.app_state_dir.iterdir()):
                self.app_state_dir.rmdir()
                print(f"   📁 Removed empty directory: {self.app_state_dir}")
        except:
            pass  # Directory not empty or other issue
    
    def _detect_component_type(self, value: Any) -> str:
        """Detect component type based on value"""
        if isinstance(value, bool):
            return "checkbox"
        elif isinstance(value, (int, float)):
            return "number"
        elif isinstance(value, str) and value in ['on', 'off']:
            return "checkbox"
        else:
            return "input"
    
    def save_state(self) -> None:
        """Save app state to file"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2, default=str)
            self._update_metadata()
        except Exception as e:
            print(f"⚠️ Warning: Could not save app state: {e}")
    
    def load_state(self) -> None:
        """Load app state from file"""
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r') as f:
                    self.state = json.load(f)
        except Exception as e:
            print(f"⚠️ Warning: Could not load app state: {e}")
            self.state = {}
    
    def save_form_data(self) -> None:
        """Save form data to file"""
        try:
            with open(self.form_data_file, 'w') as f:
                json.dump(self.form_data, f, indent=2, default=str)
            self._update_metadata()
        except Exception as e:
            print(f"⚠️ Warning: Could not save form data: {e}")
    
    def load_form_data(self) -> None:
        """Load form data from file"""
        try:
            if self.form_data_file.exists():
                with open(self.form_data_file, 'r') as f:
                    self.form_data = json.load(f)
        except Exception as e:
            print(f"⚠️ Warning: Could not load form data: {e}")
            self.form_data = {}
    
    def save_component_states(self) -> None:
        """Save component states to file"""
        try:
            with open(self.component_states_file, 'w') as f:
                json.dump(self.component_states, f, indent=2, default=str)
            self._update_metadata()
        except Exception as e:
            print(f"⚠️ Warning: Could not save component states: {e}")
    
    def load_component_states(self) -> None:
        """Load component states from file"""
        try:
            if self.component_states_file.exists():
                with open(self.component_states_file, 'r') as f:
                    self.component_states = json.load(f)
        except Exception as e:
            print(f"⚠️ Warning: Could not load component states: {e}")
            self.component_states = {}
    
    def _load_all_state(self):
        """Load all state data from files"""
        self.load_state()
        self.load_form_data()
        self.load_component_states()
    
    def export_state(self, filename: Optional[str] = None) -> str:
        """Export all state to a specific file"""
        if not filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = self.app_state_dir / f"export_{timestamp}.json"
        else:
            filename = Path(filename)
            
        try:
            export_data = {
                'app_name': self.app_name,
                'export_timestamp': self._get_timestamp(),
                'state': self.state,
                'form_data': self.form_data,
                'component_states': self.component_states,
                'metadata': self._create_metadata()
            }
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            return f"✅ State exported to {filename}"
        except Exception as e:
            return f"❌ Export failed: {e}"
    
    def import_state(self, filename: str) -> str:
        """Import state from a file"""
        try:
            filename = Path(filename)
            with open(filename, 'r') as f:
                imported_data = json.load(f)
            
            if 'state' in imported_data:
                self.state.update(imported_data['state'])
            if 'form_data' in imported_data:
                self.form_data.update(imported_data['form_data'])
            if 'component_states' in imported_data:
                self.component_states.update(imported_data['component_states'])
            
            if self.persist:
                self.save_state()
                self.save_form_data()
                self.save_component_states()
            
            return f"✅ State imported from {filename}"
        except Exception as e:
            return f"❌ Import failed: {e}"


# Global state instance
_global_state = None

def get_state_manager(app_name="flask_ui", persist=True) -> StateManager:
    """Get or create the global state manager"""
    global _global_state
    if _global_state is None:
        _global_state = StateManager(app_name, persist)
        # Dump all data on initialization for verification
        _global_state._dump_all_data()
    return _global_state
