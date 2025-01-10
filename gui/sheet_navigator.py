from tksheet import Sheet
import tkinter as tk
from tkinter import messagebox

class SheetNavigator(Sheet):
    def __init__(self, parent, headers=None, rows=20, columns=2, default_value=""):
        """Initialize the Sheet Navigator with tksheet."""
        super().__init__(parent)

        self.headers_list = headers if headers else [f"Column {i+1}" for i in range(columns)]
        default_data = [[default_value for _ in range(len(self.headers_list))] for _ in range(rows)]

        self.headers(self.headers_list)
        self.set_sheet_data(default_data)

        self.history_stack = []  # Undo history stack

        self.enable_bindings((
            "single_select",
            "row_select",     # Enable row selection
            "column_select",  # Enable column selection            
            "edit_cell",
            "copy",
            "cut",
            "paste",
            "all_select",
            "insert_row",
            "delete_row",
            "insert_column",
            "delete_column",
            "column_resize",
            "row_resize",
            "arrowkeys",
            "shift_select",
            "ctrl_select",
        ))
        self.bind("<Delete>", lambda event: self.handle_delete(event))
        self.bind("<Return>", lambda event: self.handle_enter(event))
        self.bind("<Control-a>", self.handle_select_all)
        self.bind("<Control-v>", self.handle_paste)
        self.bind("<Control-z>", self.handle_undo)
        self.bind("<Shift-Button-1>", self.handle_shift_mouse_select)
    # Clear sheet data
    def clear_sheet(self):
        """Clear all data in the sheet."""
        self.save_to_history()  # Save the current state for undo
        empty_data = [["" for _ in self.headers_list] for _ in range(len(self.get_sheet_data()))]
        self.set_sheet_data(empty_data)        
    # ctrl + z 용
    def save_to_history(self):
        """Save the current state to history for undo functionality."""
        self.history_stack.append(self.get_sheet_data())

    def handle_undo(self, event=None):
        """Undo the last operation."""
        if self.history_stack:
            last_state = self.history_stack.pop()
            self.set_sheet_data(last_state)
        else:
            messagebox.showinfo("Undo", "No actions to undo.")
    # delete 키
    def handle_delete(self, event=None):
        self.save_to_history()
        selected_cells = self.get_selected_cells()
        
        # Ensure selected_cells has valid data
        if not selected_cells:
            selected_cells = [self.get_currently_selected()]

        current_data = self.get_sheet_data()
        for cell in selected_cells:
            if len(cell) == 2:  # Check if the cell has row and column
                row, col = cell
                if 0 <= row < len(current_data) and 0 <= col < len(current_data[row]):
                    current_data[row][col] = ""

        self.set_sheet_data(current_data)
    # 자동 행 추가
    def handle_enter(self, event=None):
        current_cell = self.get_currently_selected()
        if not current_cell:
            return

        row, col = current_cell[:2]
        if row == len(self.get_sheet_data()) - 1:
            self.add_row()
        self.select_cell(row + 1, col)
    # ctri + a
    def handle_select_all(self, event=None):
        self.select_all(True)

    def add_row(self, default_value=""):
        self.save_to_history()
        current_data = self.get_sheet_data()
        new_row = [default_value for _ in range(len(self.headers_list))]
        current_data.append(new_row)
        self.set_sheet_data(current_data)

    def add_column(self, header_name=None, default_value=""):
        self.save_to_history()
        header_name = header_name or f"Column {len(self.headers_list) + 1}"
        self.headers_list.append(header_name)
        self.headers(self.headers_list)

        current_data = self.get_sheet_data()
        for row in current_data:
            row.append(default_value)
        self.set_sheet_data(current_data)

    def get_data(self):
        return self.get_sheet_data()

    def set_data(self, data):
        self.save_to_history()
        self.set_sheet_data(data)
        
    # ctrl + c, ctrl + x, ctrl + v
    def handle_paste(self, event=None):
        """Handle pasting clipboard data into the sheet."""
        self.save_to_history()
        clipboard_data = self.clipboard_get().strip()
        rows = [row.split('\t') for row in clipboard_data.split('\n') if row]

        currently_selected = self.get_currently_selected()
        if not currently_selected:
            messagebox.showerror("Error", "No cell selected to paste data.")
            return

        start_row, start_col = currently_selected[:2]
        current_data = self.get_sheet_data()

        for i, row_data in enumerate(rows):
            target_row = start_row + i

            # Ensure enough rows exist
            while target_row >= len(current_data):
                current_data.append(["" for _ in range(len(self.headers_list))])

            for j, value in enumerate(row_data):
                target_col = start_col + j

                # Ensure enough columns exist
                if target_col >= len(self.headers_list):
                    self.headers_list.append(f"Column {len(self.headers_list) + 1}")
                    for row in current_data:
                        row.append("")
                    self.headers(self.headers_list)

                # Update the cell value
                current_data[target_row][target_col] = value

        # Apply updated data to the sheet
        self.set_sheet_data(current_data)

    # shift + 마우스
    def handle_shift_mouse_select(self, event=None):
        """Handle Shift + Mouse for range selection."""
        try:
            if event is None or not hasattr(event, "x") or not hasattr(event, "y"):
                raise ValueError("Invalid event or missing x, y coordinates.")

            # Debug: Log event details
            print(f"Event type: {type(event)}")
            print(f"Event x: {event.x}, Event y: {event.y}")

            # Get the currently selected cell as the starting point
            current_selection = self.get_currently_selected()
            if not current_selection:
                print("No cell is currently selected.")
                return

            # Starting cell (anchor)
            start_row, start_col = current_selection[:2]

            # Calculate the target row and column based on mouse event coordinates
            end_row = self._calculate_row_from_y(event.y)
            end_col = self._calculate_column_from_x(event.x)

            # Debugging information
            print(f"Calculated end_row: {end_row}, end_col: {end_col}")

            # Ensure indices are within the valid range
            end_row = max(0, min(end_row, len(self.get_sheet_data()) - 1))
            end_col = max(0, min(end_col, len(self.headers_list) - 1))

            # Clear previous selection
            self.deselect("all")  # Deselect all previous selections

            # Select the range between the starting cell and the target cell
            self.create_selection_box(start_row, start_col, end_row, end_col)

            # Redraw to reflect changes
            self.redraw()
        except Exception as e:
            print(f"Error during shift selection: {e}")
            messagebox.showerror("Error", f"Shift-Mouse Selection Error: {e}")

    def _calculate_row_from_y(self, y):
        """Calculate the row index based on Y coordinate."""
        try:
            row_positions = self.MT.row_positions  # Access row positions from tksheet
            for index, position in enumerate(row_positions):
                if y < position:
                    return max(0, index - 1)
            return len(row_positions) - 1
        except AttributeError:
            raise ValueError("Unable to calculate row index: 'row_positions' not available.")

    def _calculate_column_from_x(self, x):
        """Calculate the column index based on X coordinate."""
        try:
            column_positions = self.MT.col_positions  # Access column positions from tksheet
            for index, position in enumerate(column_positions):
                if x < position:
                    return max(0, index - 1)
            return len(column_positions) - 1
        except AttributeError:
            raise ValueError("Unable to calculate column index: 'col_positions' not available.")
           


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sheet Navigator with Headers")
    sheet = SheetNavigator(root, headers=["Name", "Email", "Group"], rows=10)
    sheet.pack(expand=True, fill=tk.BOTH)

    def add_row():
        sheet.add_row()

    def add_column():
        sheet.add_column(header_name="New Column")
    def clear_data():
        sheet.clear_sheet()        

    tk.Button(root, text="Add Row", command=add_row).pack()
    tk.Button(root, text="Add Column", command=add_column).pack()

    root.mainloop()
