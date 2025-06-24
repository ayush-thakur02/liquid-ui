from typing import Dict, List, Set, Tuple, Optional, Any, Union


class GridLayout:
    """
    A professional grid layout manager for organizing components in a CSS grid system.
    
    This class provides a comprehensive solution for managing multi-page layouts with
    automatic component positioning, collision detection, and flexible grid configurations.
    It supports both automatic positioning and manual placement of components within
    a CSS Grid-based layout system.
    
    Attributes:
        columns (int): Number of columns in the grid layout
        components (List[Any]): Global list of all components across all pages
        pages (Dict[str, Dict]): Dictionary storing page-specific component data
        current_page (str): Name of the currently active page
        current_row (int): Current row position for automatic placement (1-indexed)
        current_col (int): Current column position for automatic placement (1-indexed)
        occupied_cells (Set[Tuple[int, int]]): Set of occupied grid cells for collision detection
    """
    
    def __init__(self, columns: int = 5) -> None:
        """
        Initialize the GridLayout with specified number of columns.
        
        Args:
            columns (int, optional): Number of columns in the grid. Defaults to 5.
                                   Must be a positive integer.
        
        Raises:
            ValueError: If columns is not a positive integer.
        """
        if not isinstance(columns, int) or columns <= 0:
            raise ValueError("Columns must be a positive integer")
            
        self.columns: int = columns
        self.components: List[Any] = []
        self.pages: Dict[str, Dict[str, Any]] = {}  # Dictionary to store components by page
        self.current_page: str = "Home"
        self.current_row: int = 1  # CSS Grid is 1-indexed
        self.current_col: int = 1  # CSS Grid is 1-indexed
        self.occupied_cells: Set[Tuple[int, int]] = set()  # Track occupied cells for area spanning    
    def _parse_area(self, area: Optional[str]) -> Tuple[int, int]:
        """
        Parse area string specification into column and row dimensions.
        
        This method converts area specifications like '5x1', '2x3', etc. into
        a tuple of (columns, rows). If the area string is invalid or None,
        returns default dimensions of (1, 1).
        
        Args:
            area (Optional[str]): Area specification string in format 'COLSxROWS'.
                                Examples: '5x1', '2x3', '1x2', None
        
        Returns:
            Tuple[int, int]: A tuple containing (columns, rows) dimensions.
                           Returns (1, 1) for invalid or None input.
        
        Examples:
            >>> layout._parse_area('5x1')
            (5, 1)
            >>> layout._parse_area('2x3')
            (2, 3)
            >>> layout._parse_area(None)
            (1, 1)
            >>> layout._parse_area('invalid')
            (1, 1)
        """
        if not area or 'x' not in area:
            return (1, 1)
        try:
            cols, rows = area.split('x')
            return (int(cols), int(rows))
        except (ValueError, IndexError):
            return (1, 1)    
    def _find_next_position(self, cols_needed: int, rows_needed: int) -> Tuple[int, int]:
        """
        Find the next available position that can accommodate a component with specified dimensions.
        
        This method searches for the next available grid position that can fit a component
        with the given column and row requirements. It performs a systematic search starting
        from the current position and moves row by row until a suitable position is found.
        
        Args:
            cols_needed (int): Number of columns required by the component
            rows_needed (int): Number of rows required by the component
        
        Returns:
            Tuple[int, int]: A tuple containing (row, column) of the next available position
                           that can accommodate the component dimensions
        
        Note:
            - The search is limited to 100 rows from the current position for performance
            - If no position is found in the current row, the search moves to the next row
            - Grid positions are 1-indexed to match CSS Grid specifications
        """
        for row in range(self.current_row, self.current_row + 100):  # Reasonable limit
            for col in range(1, self.columns + 1):
                if self._can_place_at(row, col, cols_needed, rows_needed):
                    return (row, col)
            # If we can't fit in current row, move to next row
            if row == self.current_row:
                self.current_row += 1
        return (self.current_row, 1)    
    def _can_place_at(self, row: int, col: int, cols_needed: int, rows_needed: int) -> bool:
        """
        Check if a component with specified dimensions can be placed at a given position.
        
        This method validates whether a component can be placed at the specified grid
        position without exceeding grid boundaries or overlapping with existing components.
        It performs both boundary checking and collision detection.
        
        Args:
            row (int): Target row position (1-indexed)
            col (int): Target column position (1-indexed)
            cols_needed (int): Number of columns required by the component
            rows_needed (int): Number of rows required by the component
        
        Returns:
            bool: True if the component can be placed at the specified position,
                 False if it would exceed boundaries or overlap with existing components
        
        Note:
            - Grid positions are 1-indexed to match CSS Grid specifications
            - Checks both grid boundary constraints and cell occupation status
        """
        # Check if it fits within grid bounds
        if col + cols_needed - 1 > self.columns:
            return False
          # Check if any of the required cells are occupied
        for r in range(row, row + rows_needed):
            for c in range(col, col + cols_needed):
                if (r, c) in self.occupied_cells:
                    return False        
        return True

    def _mark_cells_occupied(self, row: int, col: int, cols_needed: int, rows_needed: int) -> None:
        """
        Mark specified grid cells as occupied to prevent component overlap.
        
        This method updates the occupied_cells set to track which grid positions
        are currently in use by components. This information is used for collision
        detection when placing new components.
        
        Args:
            row (int): Starting row position (1-indexed)
            col (int): Starting column position (1-indexed)
            cols_needed (int): Number of columns to mark as occupied
            rows_needed (int): Number of rows to mark as occupied
        
        Returns:
            None
          Note:
            - Updates the global occupied_cells set for the entire layout
            - Grid positions are 1-indexed to match CSS Grid specifications
            - All cells within the specified rectangular area are marked as occupied
        """
        for r in range(row, row + rows_needed):
            for c in range(col, col + cols_needed):
                self.occupied_cells.add((r, c))

    def add_component(self, component: Any) -> None:
        """
        Add a component to the grid at the next available position.
        
        This method automatically places a component in the grid layout by finding
        the next available position that can accommodate the component's dimensions.
        It handles page initialization, position calculation, and cell occupation tracking.
        
        Args:
            component (Any): The component to add to the grid. Must have 'page' and 'area'
                           attributes, and support set_grid_position() method.
        
        Returns:
            None
        
        Raises:
            AttributeError: If component lacks required attributes or methods
        
        Note:
            - Creates new page data structure if the component's page doesn't exist
            - Updates both global component list and page-specific component tracking
            - Automatically handles grid position calculation and cell occupation
        """
        # Initialize page if it doesn't exist
        if component.page not in self.pages:
            self.pages[component.page] = {
                'components': [],
                'current_row': 1,
                'current_col': 1,
                'occupied_cells': set()
            }
        
        page_data = self.pages[component.page]
        cols_needed, rows_needed = self._parse_area(component.area)
        row, col = self._find_next_position_for_page(component.page, cols_needed, rows_needed)
        
        component.set_grid_position(row, col, cols_needed, rows_needed)
        page_data['components'].append(component)
        self.components.append(component)  # Keep global list for compatibility
        
        # Mark cells as occupied for this page
        self._mark_cells_occupied_for_page(component.page, row, col, cols_needed, rows_needed)
        
        # Update current position for this page
        page_data['current_col'] = col + cols_needed
        if page_data['current_col'] > self.columns:
            page_data['current_row'] += 1
            page_data['current_col'] = 1    
    def add_component_at(self, component: Any, row: int, col: int) -> None:
        """
        Add a component at a specific grid position.
        
        This method places a component at an explicitly specified grid position
        rather than using automatic positioning. It validates the position and
        ensures no overlap with existing components.
        
        Args:
            component (Any): The component to add to the grid. Must have 'area'
                           attribute and support set_grid_position() method.
            row (int): Target row position (1-indexed)
            col (int): Target column position (1-indexed)
        
        Returns:
            None
        
        Raises:
            ValueError: If column exceeds grid bounds or position is occupied
            AttributeError: If component lacks required attributes or methods
        
        Note:
            - Updates global component tracking and current position markers
            - Grid positions are 1-indexed to match CSS Grid specifications
            - Automatically advances current position if placement is beyond current position
        """
        if col > self.columns:
            raise ValueError(f"Column {col} exceeds maximum columns ({self.columns})")
        
        cols_needed, rows_needed = self._parse_area(component.area)
        
        if not self._can_place_at(row, col, cols_needed, rows_needed):
            raise ValueError(f"Cannot place component at position ({row}, {col}) with area {component.area}")
        
        component.set_grid_position(row, col, cols_needed, rows_needed)
        self.components.append(component)        
        # Mark cells as occupied
        self._mark_cells_occupied(row, col, cols_needed, rows_needed)
        # Update current position if this is beyond current position
        if row > self.current_row or (row == self.current_row and col >= self.current_col):
            self.current_col = col + cols_needed
            if self.current_col > self.columns:
                self.current_row = row + 1
                self.current_col = 1
            else:
                self.current_row = row

    def render(self, page: Optional[str] = None) -> str:
        """
        Render the entire grid as HTML using CSS Grid layout.
        
        This method generates the complete HTML representation of the grid layout
        for a specific page, including all components positioned according to their
        grid coordinates. The output uses CSS Grid for precise component positioning.
        
        Args:
            page (Optional[str], optional): Name of the page to render. 
                                          If None, renders the current active page.
        
        Returns:
            str: Complete HTML string representing the grid layout with all components.
                Returns a message if no components exist on the specified page.
        
        Note:
            - Uses CSS Grid with responsive column sizing (1fr each)
            - Automatically calculates required rows based on component positions
            - Each component renders within its assigned grid area
            - Minimum row height is 60px with auto-expansion capability
        """
        if page is None:
            page = self.current_page
        
        # Get components for the specific page
        page_components = self.get_components_for_page(page)
        
        if not page_components:
            return f'<div class="grid-container">No components on page "{page}"</div>'
        
        # Calculate grid dimensions for this page
        max_row = max((comp.grid_position[0] + comp.grid_rows - 1) for comp in page_components) if page_components else 1
        
        # Generate HTML with CSS Grid
        html = [f'<div class="grid-container" style="grid-template-columns: repeat({self.columns}, 1fr); grid-template-rows: repeat({max_row}, minmax(60px, auto));">']
        
        for component in page_components:
            html.append(component.render())
        
        html.append('</div>')
        return '\n'.join(html)    
    def get_component_by_id(self, component_id: str) -> Optional[Any]:
        """
        Retrieve a component by its unique identifier.
        
        This method searches through all components in the grid layout to find
        a component with the specified ID. It performs a linear search across
        all components regardless of their page assignment.
        
        Args:
            component_id (str): The unique identifier of the component to retrieve
        
        Returns:
            Optional[Any]: The component object if found, None if no component 
                         with the specified ID exists
        
        Note:
            - Searches across all components in all pages
            - Returns the first component found with matching ID
            - Component ID comparison is performed using exact string matching
        """
        for component in self.components:
            if component.id == component_id:
                return component
        return None    
    def clear(self) -> None:
        """
        Clear all components from the grid layout.
        
        This method removes all components from the grid and resets the layout
        to its initial state. It clears both the global component list and
        resets position tracking variables.
        
        Returns:
            None
        
        Note:
            - Removes all components from all pages
            - Resets current position to (1, 1)
            - Clears the occupied cells tracking set
            - Does not affect page structure or column configuration
        """
        self.components = []
        self.current_row = 1
        self.current_col = 1
        self.occupied_cells.clear()        
    def _find_next_position_for_page(self, page: str, cols_needed: int, rows_needed: int) -> Tuple[int, int]:
        """
        Find the next available position for a component on a specific page.
        
        This method searches for the next available grid position on a specific page
        that can accommodate a component with the given dimensions. It maintains
        separate position tracking for each page to prevent cross-page interference.
        
        Args:
            page (str): Name of the page to search for available positions
            cols_needed (int): Number of columns required by the component
            rows_needed (int): Number of rows required by the component
        
        Returns:
            Tuple[int, int]: A tuple containing (row, column) of the next available position
                           on the specified page
        
        Note:
            - Maintains separate position tracking per page
            - Search is limited to 100 rows from current position for performance
            - Automatically advances to next row if current row cannot accommodate component
        """
        page_data = self.pages[page]
        for row in range(page_data['current_row'], page_data['current_row'] + 100):
            for col in range(1, self.columns + 1):
                if self._can_place_at_for_page(page, row, col, cols_needed, rows_needed):
                    return (row, col)
            if row == page_data['current_row']:
                page_data['current_row'] += 1
        return (page_data['current_row'], 1)    
    def _can_place_at_for_page(self, page: str, row: int, col: int, cols_needed: int, rows_needed: int) -> bool:
        """
        Check if a component can be placed at a specific position on a given page.
        
        This method validates whether a component can be placed at the specified
        position on a specific page without exceeding grid boundaries or overlapping
        with existing components on that page.
        
        Args:
            page (str): Name of the page to check for placement
            row (int): Target row position (1-indexed)
            col (int): Target column position (1-indexed)
            cols_needed (int): Number of columns required by the component
            rows_needed (int): Number of rows required by the component
        
        Returns:
            bool: True if the component can be placed at the specified position,
                 False if it would exceed boundaries or overlap with page components
        
        Note:
            - Only checks for conflicts with components on the same page
            - Grid positions are 1-indexed to match CSS Grid specifications
            - Validates both boundary constraints and cell occupation per page
        """
        if col + cols_needed - 1 > self.columns:
            return False
        
        page_data = self.pages[page]
        for r in range(row, row + rows_needed):
            for c in range(col, col + cols_needed):
                if (r, c) in page_data['occupied_cells']:
                    return False
        return True    
    def _mark_cells_occupied_for_page(self, page: str, row: int, col: int, cols_needed: int, rows_needed: int) -> None:
        """
        Mark specified grid cells as occupied for a specific page.
        
        This method updates the page-specific occupied_cells set to track which
        grid positions are currently in use by components on a particular page.
        This enables page-isolated collision detection.
        
        Args:
            page (str): Name of the page where cells should be marked as occupied
            row (int): Starting row position (1-indexed)
            col (int): Starting column position (1-indexed)
            cols_needed (int): Number of columns to mark as occupied
            rows_needed (int): Number of rows to mark as occupied
        
        Returns:
            None
        
        Note:
            - Updates only the specified page's occupied_cells set
            - Grid positions are 1-indexed to match CSS Grid specifications
            - All cells within the specified rectangular area are marked as occupied
        """
        page_data = self.pages[page]
        for r in range(row, row + rows_needed):
            for c in range(col, col + cols_needed):
                page_data['occupied_cells'].add((r, c))    
    def get_components_for_page(self, page: str) -> List[Any]:
        """
        Retrieve all components assigned to a specific page.
        
        This method returns a list of all components that belong to the specified page.
        If the page doesn't exist or has no components, an empty list is returned.
        
        Args:
            page (str): Name of the page to retrieve components from
        
        Returns:
            List[Any]: List of components assigned to the specified page.
                      Returns empty list if page doesn't exist or has no components.
        
        Note:
            - Returns components in the order they were added to the page
            - Does not modify the original component list
            - Safe to call with non-existent page names
        """
        if page in self.pages:
            return self.pages[page]['components']
        return []    
    def get_page_names(self) -> List[str]:
        """
        Retrieve the names of all pages in the grid layout.
        
        This method returns a list of all page names that have been created
        in the grid layout system. Pages are created automatically when
        components are assigned to them.
        
        Returns:
            List[str]: List of all page names currently in the grid layout.
                      Returns empty list if no pages have been created.
        
        Note:
            - Returns page names in arbitrary order (dict key order)
            - Pages are created automatically when components are added
            - Useful for navigation and page management operations
        """
        return list(self.pages.keys())
    def set_current_page(self, page: str) -> bool:
        """
        Set the currently active page for the grid layout.
        
        This method changes the current active page, which affects the default
        page used for rendering and other page-specific operations when no
        explicit page is specified.
        
        Args:
            page (str): Name of the page to set as current active page
        
        Returns:
            bool: True if the page was successfully set as current,
                 False if the specified page doesn't exist
        
        Note:
            - Only existing pages can be set as current
            - Does not create new pages if they don't exist
            - Current page affects default rendering behavior
        """
        if page in self.pages:
            self.current_page = page
            return True
        return False
    def clear_page(self, page: str) -> None:
        """
        Clear all components from a specific page.
        
        This method removes all components from the specified page and resets
        the page's layout state to its initial configuration. Components are
        removed from both the page-specific list and the global component list.
        
        Args:
            page (str): Name of the page to clear
        
        Returns:
            None
        
        Note:
            - Removes components from both page-specific and global component lists
            - Resets page position tracking to (1, 1)
            - Clears page-specific occupied cells tracking
            - Does nothing if the specified page doesn't exist
            - Page structure is preserved (not deleted, just emptied)
        """
        if page in self.pages:
            # Remove components from global list
            page_components = self.pages[page]['components']
            for comp in page_components:
                if comp in self.components:
                    self.components.remove(comp)
            # Reset page data
            self.pages[page] = {
                'components': [],
                'current_row': 1,
                'current_col': 1,
                'occupied_cells': set()
            }
