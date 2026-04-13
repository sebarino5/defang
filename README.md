# Defanger

Defanger is a simple web app with a dark theme that wraps punctuation characters in square brackets, useful for defanging IoCs (Indicators of Compromise).

## Features

- Simple text input
- Automatic detection and wrapping of punctuation:
  - Period (.) → [.]
  - Comma (,) → [,]
  - Question mark (?) → [?]
  - Exclamation mark (!) → [!]
  - Semicolon (;) → [;]
  - Colon (:) → [:]
- Copy processed text to clipboard
- Responsive design for all devices
- Keyboard shortcut: Ctrl + Enter to process
- Dark theme for better readability

## Technologies

- HTML5
- Tailwind CSS
- Vanilla JavaScript
- Inter font

## Usage

1. Open `index.html` in a modern browser
2. Enter your text in the input field
3. Click "Process Text" or press Ctrl + Enter
4. The processed text appears in the output field
5. Click "Copy to Clipboard" to copy the result

## Example

Input:
```
Hello World. Testing this app! Does it work, as expected? I think so; yes.
```

Output:
```
Hello World[.] Testing this app[!] Does it work[,] as expected[?] I think so[;] yes[.]
```

## License

This project is licensed under the MIT License.
