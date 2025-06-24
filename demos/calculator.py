from framework import create_ui

# Create a new UI instance with 5 columns
ui = create_ui(title="UI Components Demo", columns=5)

# Add title
ui.text("UI Components Demo", tag="h2", area="5x1")

# Calculator Section
ui.text("Calculator Section", tag="h3", area="5x1")

# Add input fields for numbers
ui.text("First Number:", area="2x1")
ui.input(placeholder="Enter first number", id="first_number", input_type="number", area="3x1")

ui.text("Second Number:", area="2x1")
ui.input(placeholder="Enter second number", id="second_number", input_type="number", area="3x1")

# Add calculation button
def calculate_sum(form_data):
    try:
        num1 = float(form_data.get('first_number', 0))
        num2 = float(form_data.get('second_number', 0))
        result = num1 + num2
        ui.update('result_display', f"Result: {result}")
        return None  # Don't return anything to component
    except (ValueError, TypeError):
        ui.update('result_display', "Error: Please enter valid numbers")
        return None

ui.button("Calculate Sum", callback=calculate_sum, id="calculate_btn", area="2x2")

# Add result display
ui.text("Enter numbers and click Calculate", id="result_display", area="3x1")

# Add clear button
def clear_calculator(form_data):
    # Use the new update method to clear specific fields
    ui.update('first_number', '')
    ui.update('second_number', '')
    ui.update('result_display', 'Calculator cleared - Enter new numbers')
    return None  # Don't return anything to component

ui.button("Clear", callback=clear_calculator, id="clear_btn", area="3x1")


# Run the application
if __name__ == "__main__":
    ui.run()