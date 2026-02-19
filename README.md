# QuickURL - URL Template Generator

A simple, elegant GUI application for generating test URLs with variable substitution. Perfect for testing Cloudflare tunnels, API endpoints, or any scenario where you need to quickly generate multiple URLs from templates.

## Features

- **Source URL Management**: Enter your base URL once
- **Dynamic Templates**: Add unlimited URL templates with custom function names
- **Variable Substitution**: Automatic replacement of placeholders
- **One-Click Copy**: Copy all generated URLs to clipboard instantly
- **Clean Interface**: Simple, intuitive GUI built with tkinter

## Installation

1. **Prerequisites**: Python 3.6 or higher

2. **Install Dependencies**:
```bash
cd QuickURL
pip install -r requirements.txt
```

## Usage

### Running the App

```bash
python url_generator.py
```

Or on macOS/Linux:
```bash
./url_generator.py
```

### Using the App

1. **Enter Source URL**: 
   - Type your actual URL in the "Source URL" field
   - Example: `https://my-tunnel.trycloudflare.com`

2. **Configure Templates**:
   - Default templates are pre-loaded for Cloudflare tunnel testing
   - Click **"+ Add Template"** to add more templates
   - Each template has:
     - **Function**: A descriptive name (e.g., "Health Check")
     - **URL Template**: The URL pattern with `[your-tunnel-url]` placeholder
   - Click **"−"** button to remove unwanted templates

3. **Generate URLs**:
   - Click **"🔗 Generate URLs"** button
   - View all generated URLs in the results panel

4. **Copy Results**:
   - Click **"📋 Copy All"** to copy all URLs to clipboard
   - Paste into your browser, documentation, or testing tools

### Example

**Source URL:**
```
https://toxic-promises-whatever-observations.trycloudflare.com
```

**Templates:**
- Function: `Health Check`
- Template: `[your-tunnel-url]/health`

- Function: `Run Preview`
- Template: `[your-tunnel-url]/preview?code=import%20SwiftUI...`

**Generated Output:**
```
[Health Check]
https://toxic-promises-whatever-observations.trycloudflare.com/health

[Run Preview]
https://toxic-promises-whatever-observations.trycloudflare.com/preview?code=import%20SwiftUI...
```

## Creating an Executable (Optional)

To create a standalone executable that doesn't require Python:

### macOS/Linux
```bash
pip install pyinstaller
pyinstaller --onefile --windowed url_generator.py
```

The executable will be in the `dist/` folder.

### Windows
```bash
pip install pyinstaller
pyinstaller --onefile --windowed url_generator.py
```

## Use Cases

- **Cloudflare Tunnel Testing**: Quickly test tunnel URLs
- **API Endpoint Testing**: Generate multiple API test URLs
- **Documentation**: Create URL examples for docs
- **Development**: Test different URL patterns rapidly

## Keyboard Shortcuts

- **Cmd+C / Ctrl+C**: Copy selected text
- **Cmd+V / Ctrl+V**: Paste text
- **Cmd+Q / Ctrl+Q**: Quit application

## Troubleshooting

**Issue**: "pyperclip" not working on Linux
- **Solution**: Install xclip or xsel: `sudo apt-get install xclip`

**Issue**: GUI not appearing
- **Solution**: Ensure tkinter is installed (comes with Python by default)

## License

Free to use for any purpose.

## Author

Created for SwiftCodePlatform development workflow.
