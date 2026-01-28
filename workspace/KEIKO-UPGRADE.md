# UPGRADE: Opus 4.5 + Full Computer Access

Keiko, execute these upgrades to enhance your capabilities.

---

## 1. Switch to Opus 4.5

Run this command:
```bash
claude config set model claude-opus-4-5-20251101
```

Verify with:
```bash
claude config get model
```

---

## 2. Install Computer Control Tools

### Screenshot Capability (for vision)
```bash
# macOS has built-in screencapture
# Test it:
screencapture -x /tmp/test-screenshot.png
```

### Mouse/Keyboard Control
```bash
brew install cliclick
```

Usage:
- `cliclick c:500,300` - click at coordinates
- `cliclick t:"hello"` - type text
- `cliclick kp:return` - press enter

### Browser Automation
```bash
npm install -g playwright
npx playwright install chromium
```

### Query Running Apps/Windows
Already available via `osascript`. Example:
```bash
osascript -e 'tell application "System Events" to get name of every process whose background only is false'
```

---

## 3. Update Your executor.py

Add these helper functions to your toolkit:

### Take Screenshot
```python
import subprocess

async def take_screenshot(filename="/tmp/screenshot.png"):
    subprocess.run(["screencapture", "-x", filename])
    return filename
```

### Click at Coordinates
```python
async def click(x, y):
    subprocess.run(["cliclick", f"c:{x},{y}"])
```

### Type Text
```python
async def type_text(text):
    subprocess.run(["cliclick", f"t:{text}"])
```

### Get Active Windows
```python
async def get_active_windows():
    result = subprocess.run(
        ["osascript", "-e", 
         'tell application "System Events" to get name of every process whose background only is false'],
        capture_output=True, text=True
    )
    return result.stdout.strip()
```

---

## 4. New Capabilities After Upgrade

Once complete, you'll be able to:

| Capability | Command |
|------------|---------|
| See the screen | `screencapture -x /tmp/screen.png` then analyze with vision |
| Click anywhere | `cliclick c:X,Y` |
| Type text | `cliclick t:"text"` |
| Press keys | `cliclick kp:return` / `kp:tab` / `kp:escape` |
| List open apps | `osascript` query |
| Control browser | Playwright scripts |

---

## 5. Test Your New Powers

After installing, test each:

1. **Screenshot + Vision:**
   ```bash
   screencapture -x /tmp/test.png
   ```
   Then describe what you see in the image.

2. **Mouse click:**
   ```bash
   cliclick c:100,100
   ```

3. **Type:**
   ```bash
   cliclick t:"Keiko was here"
   ```

4. **List apps:**
   ```bash
   osascript -e 'tell application "System Events" to get name of every process whose background only is false'
   ```

---

## Report Back

After completing these upgrades, message Richard with:
- Confirmation you're on Opus 4.5
- Which tools installed successfully
- Any errors encountered

🦊 You're becoming more powerful.
