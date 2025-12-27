# Building Blackjack Story Mode Standalone Executable

This document provides instructions for building the standalone Windows executable for the Blackjack Story Mode web application.

## Prerequisites

1. **Python 3.8 or higher** installed
2. **pip** package manager
3. All project dependencies installed

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
pip install pyinstaller
```

### 2. Build the Executable

Run PyInstaller with the provided spec file:

```bash
pyinstaller blackjack_web.spec
```

This will create:
- `build/` directory (temporary build files)
- `dist/` directory containing the standalone executable

### 3. Alternative: One-Directory Build

For a portable folder instead of single executable:

```bash
pyinstaller --onedir --name BlackjackStoryMode --add-data "templates:templates" --add-data "static:static" --add-data "web_story.py:." --add-data "deckOfCards.py:." app.py
```

### 4. Test the Executable

Navigate to the `dist` folder and run:

```bash
cd dist
./BlackjackStoryMode.exe  # Windows
./BlackjackStoryMode      # Linux/Mac
```

The application should:
1. Start a local web server
2. Automatically open your browser to http://127.0.0.1:5000/
3. Display the Blackjack game

## Distribution Package

### Creating a Release Package

1. Copy the executable from `dist/` folder
2. Create a distribution folder with:
   ```
   BlackjackStoryMode/
   ├── BlackjackStoryMode.exe
   ├── README.txt (user instructions)
   └── LICENSE.txt (if applicable)
   ```

3. Compress to ZIP for distribution

### User Instructions (README.txt)

```
BLACKJACK STORY MODE - Standalone Edition

SYSTEM REQUIREMENTS:
- Windows 10 or higher (64-bit)
- 100 MB free disk space
- Modern web browser (Chrome, Firefox, Edge)

INSTALLATION:
1. Extract all files to a folder
2. Double-click BlackjackStoryMode.exe
3. The game will open in your browser automatically

HOW TO PLAY:
- The game uses a forced progression story system
- Play 3 rounds of blackjack per night (4 with Golden Watch)
- Make story choices during day/night events
- Visit shops to purchase items and services
- Survive and reach $1,000,000 to win

FEATURES:
- 47 unique story events
- 7 shops with items and services
- Minimalist retro aesthetic
- Authentic blackjack gameplay
- Item system with durability tracking

TROUBLESHOOTING:
- If browser doesn't open: Navigate to http://127.0.0.1:5000/
- Port conflict: Close other applications using port 5000
- Firewall: Allow the application through Windows Firewall

To exit: Close the browser tab and the console window
```

## Build Options

### Single File vs Directory

**Single File** (`--onefile`):
- Pros: Single executable, easier distribution
- Cons: Slower startup (extracts to temp), larger file

**Directory** (`--onedir`):
- Pros: Faster startup, easier debugging
- Cons: Multiple files to distribute

### Console vs Windowed

**Console Mode** (`console=True`):
- Shows terminal window with server logs
- Recommended for debugging
- User can see server status

**Windowed Mode** (`console=False`):
- No console window
- Cleaner appearance
- Harder to debug issues

### Adding an Icon

1. Create or obtain a `.ico` file
2. Update `blackjack_web.spec`:
   ```python
   icon='path/to/icon.ico'
   ```
3. Rebuild with PyInstaller

## Advanced Configuration

### Optimizing Size

Reduce executable size:

```bash
pyinstaller --onefile --strip --noupx blackjack_web.spec
```

### Including Additional Files

Edit `blackjack_web.spec` to add more data files:

```python
datas=[
    ('templates', 'templates'),
    ('static', 'static'),
    ('custom_data', 'custom_data'),
],
```

### Hidden Imports

If modules aren't detected automatically:

```python
hiddenimports=[
    'flask',
    'your_module_here',
],
```

## Testing Checklist

Before distribution, test:

- [x] Executable runs without errors
- [x] Browser opens automatically
- [x] All game features work
- [x] Story events trigger correctly
- [x] Shop purchases function
- [x] Inventory displays properly
- [x] Auto-redirect works after 3 rounds
- [x] Game saves progress in session
- [x] Can play multiple complete cycles

## Common Issues

### Import Errors

**Problem**: Module not found when running executable
**Solution**: Add module to `hiddenimports` in spec file

### File Not Found Errors

**Problem**: Can't find templates or static files
**Solution**: Verify `datas` list in spec file includes all necessary folders

### Port Already in Use

**Problem**: Flask can't start on port 5000
**Solution**: Change port in `run_standalone.py` and update URLs

### Browser Doesn't Open

**Problem**: webbrowser module fails
**Solution**: User can manually navigate to http://127.0.0.1:5000/

## Platform-Specific Notes

### Windows
- Build on Windows for Windows executables
- Test on multiple Windows versions (10, 11)
- Consider code signing for distribution

### Linux
- May need additional permissions: `chmod +x BlackjackStoryMode`
- Different browsers may be default

### macOS
- Requires macOS build environment
- May need to disable Gatekeeper for unsigned apps
- Use `--windowed` for .app bundle

## Version Information

**Current Version**: 1.0.0
**Build Date**: 2025-12-27
**Python Version**: 3.8+
**PyInstaller Version**: 6.0+

## Support

For issues or questions:
1. Check troubleshooting section
2. Review PyInstaller documentation
3. Verify all dependencies are installed
4. Test in development mode first (`python app.py`)
