import os

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal

class ConsoleWidget(QtWidgets.QWidget):
    input_signal = pyqtSignal(str)
    hidden_input_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self._server_is_active = False

        # Create a QTextEdit widget for the console
        self.console = QtWidgets.QTextEdit()
        self.console.setReadOnly(True)
        self.console.setMinimumHeight(100)

        self.input = QtWidgets.QLineEdit(self)
        self.input.textChanged.connect(self._input_text_changed)
        self.input.returnPressed.connect(self._write_to_console)

        # Create a layout for the widget
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.console)
        layout.addWidget(self.input)
        layout.setSpacing(0)
        self.setLayout(layout)

        # Initialize a list to store previous commands
        self.prev_commands = []
        self.current_command_index = 0

        # List of available commands for autocompletion
        self.available_commands = []
        self._suggestions = []

        # Install an event filter to capture Tab key events
        self.input.installEventFilter(self)

    def write(self, text):
        cursor = self.console.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        self.console.setTextCursor(cursor)
        self.console.insertPlainText(text)
        self.console.verticalScrollBar().setValue(self.console.verticalScrollBar().maximum())

    def set_available_commands(self, text):
        print(text)
        self.available_commands = self.parse_commands(text)
        self._server_is_active = True

    def parse_commands(self, text):
        lines = text.split('\n')
        commands_dict = {}

        for line in lines:
            if ' /' in line:
                parts = line.split(' /')
                command = parts[1].strip()

                main_command, *options = command.split(' ')

                if '->' in options:
                    options = commands_dict[options[1]]
                commands_dict[main_command] = options

        return commands_dict

    def _write_to_console(self):
        if not self._server_is_active:
            return

        text = self.input.text()
        if text:
            # Add the current command to the list
            self.prev_commands.append(text)
            self.current_command_index = len(self.prev_commands)

            # Write a message to the console
            self.input_signal.emit(text)
            self.write(f'{text}\n')
            self.input.clear()

    def _autocomplete_command(self):
        if not self._server_is_active:
            return

        current_text = self.input.text().lower()

        # current_input = current_text.split(' ')
        current_main_command, *current_options = current_text.split(' ')
        if current_options:
            matching_commands = [cmd for cmd in self._suggestions if cmd.lower().startswith(current_options[-1])]
        else:
            matching_commands = [cmd for cmd in self.available_commands.keys() if cmd.lower().startswith(current_main_command)]
        if matching_commands:
            common_prefix = os.path.commonprefix(matching_commands)
            if common_prefix != current_text:
                current_input = self.input.text()
                current_input = current_input.split(' ')
                if isinstance(current_input, list) and len(current_input) > 1:
                    current_input = ' '.join(current_input[:-1])
                    current_input += ' '
                else:
                    current_input = ''
                self.input.setText(current_input + common_prefix)

    def _input_text_changed(self, text):
        if not self._server_is_active:
            return

        current_main_command, *current_options = text.split(' ')

        matching_commands = [cmd for cmd in self.available_commands.keys() if cmd.lower().startswith(current_main_command)]

        if not matching_commands:
            return

        if len(matching_commands) > 1:
            # TODO: Show a list of matching commands
            self._suggestions = matching_commands
            print(f'Multiple matching commands: {matching_commands}')
            return

        matched_command = matching_commands[0]

        if current_main_command != matched_command:
            self._suggestions = [matched_command]
            print(f'Autocompleted command: {matched_command}')
            return

        if not current_options:
            return

        command_arguments = self.available_commands[matched_command]

        isOptional = False
        isVariable = False

        argument_index = len(current_options) - 1
        if argument_index >= len(command_arguments):
            return

        argument_suggestions = command_arguments[argument_index]

        if argument_suggestions.startswith('('):
            argument_suggestions = argument_suggestions[1:-1]
            suggestions = argument_suggestions.split('|')
        else:
            suggestions = [argument_suggestions]

        for suggestionIdx in range(len(suggestions)):
            if suggestions[suggestionIdx].startswith('['):
                suggestions[suggestionIdx] = suggestions[suggestionIdx][1:-1]
                isOptional = True

            if suggestions[suggestionIdx].startswith('<'):
                suggestions[suggestionIdx] = suggestions[suggestionIdx][1:-1]
                isVariable = True

        matched_suggestions = [suggestion for suggestion in suggestions if suggestion.lower().startswith(current_options[-1].lower())]
        self._suggestions = matched_suggestions
        print(matched_suggestions, isOptional, isVariable)

    def clear(self):
        self.console.clear()
        self.input.clear()
        self.prev_commands = []
        self.current_command_index = 0

    def eventFilter(self, obj, event):
        if obj == self.input and event.type() == QtGui.QKeyEvent.KeyPress:
            if event.key() == Qt.Key_Up:
                # Handle the up arrow key to cycle through previous commands
                if self.current_command_index > 0:
                    self.current_command_index -= 1
                    self.input.setText(self.prev_commands[self.current_command_index])
            elif event.key() == Qt.Key_Down:
                # Handle the down arrow key to cycle through next commands
                if self.current_command_index < len(self.prev_commands) - 1:
                    self.current_command_index += 1
                    self.input.setText(self.prev_commands[self.current_command_index])
                elif self.current_command_index == len(self.prev_commands) - 1:
                    self.input.setText('')
                    self.current_command_index += 1
            elif event.key() == Qt.Key_Tab:
                # Handle the Tab key for autocompletion
                self._autocomplete_command()
                return True  # Consume the event

        return super().eventFilter(obj, event)
