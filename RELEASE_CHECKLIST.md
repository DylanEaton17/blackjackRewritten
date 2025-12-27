# Release Checklist for Blackjack Story Mode v1.0.0

## Pre-Release Testing

### Core Functionality
- [ ] Game starts without errors
- [ ] Browser opens automatically
- [ ] Intro sequence displays correctly
- [ ] Casino gameplay works (deal, hit, stand)
- [ ] 3-round limit enforces correctly
- [ ] Golden Watch grants 4th round
- [ ] Auto-redirect to end_day after rounds
- [ ] Balance syncs across all screens

### Story System
- [ ] End day displays stats and quotes
- [ ] Start day triggers events correctly
- [ ] Day events show authentic dialogue
- [ ] Event choices process correctly
- [ ] Afternoon shows available shops
- [ ] Rank system progresses properly (Poor → Nearly There)

### NPC Encounters
- [ ] Tom appears when balance >= $200
- [ ] Frank appears when balance >= $200
- [ ] Oswald appears when balance >= $200
- [ ] Mechanics stop appearing after Car purchased
- [ ] Meeting mechanics unlocks their shops

### Shops
- [ ] Doctor always available
- [ ] Witch unlocks at Rank 1
- [ ] Tom's shop appears after meeting Tom
- [ ] Frank's shop appears after meeting Frank
- [ ] Oswald's shop appears after meeting Oswald
- [ ] Marvin's shop appears after finding Map
- [ ] Purchase processing works for all shops
- [ ] Balance updates after purchases
- [ ] Items added to inventory correctly

### Items
- [ ] Golden Watch increases rounds to 4
- [ ] Health Indicator shows health on end_day
- [ ] Inventory displays on end_day screen
- [ ] Items show only when player has them
- [ ] Item durability tracked correctly

### UI/UX
- [ ] Minimalist dark theme consistent
- [ ] No round counter visible (hidden)
- [ ] Health hidden without Health Indicator
- [ ] All buttons function correctly
- [ ] Continue buttons advance story
- [ ] Navigation flow is forced (no optional skips)

## Build Process

### Development Build
- [ ] Run `python app.py` successfully
- [ ] All features work in dev mode
- [ ] No console errors

### Production Build
- [ ] Run build script (`build.bat` or `build.sh`)
- [ ] PyInstaller completes without errors
- [ ] Executable created in `dist/` folder
- [ ] Executable file size reasonable (<100MB ideal)

### Executable Testing
- [ ] Executable runs on Windows 10
- [ ] Executable runs on Windows 11
- [ ] Browser opens automatically
- [ ] All game features work in exe
- [ ] Templates/static files bundled correctly
- [ ] No file path errors
- [ ] Server starts on port 5000
- [ ] Can close cleanly with Ctrl+C

## Documentation

- [ ] README.md updated with all features
- [ ] BUILD_INSTRUCTIONS.md complete
- [ ] USER_MANUAL.txt included
- [ ] Version numbers consistent (1.0.0)
- [ ] Credits/attribution included
- [ ] Screenshots captured for release

## Distribution Package

### File Structure
```
BlackjackStoryMode-v1.0.0/
├── BlackjackStoryMode.exe  (or platform-specific executable)
├── USER_MANUAL.txt
├── README.txt (simplified for end users)
└── LICENSE.txt (if applicable)
```

### Package Creation
- [ ] Create distribution folder
- [ ] Copy executable from dist/
- [ ] Include USER_MANUAL.txt
- [ ] Create simplified README.txt for users
- [ ] Include LICENSE if applicable
- [ ] Compress to ZIP file
- [ ] Test extracted ZIP runs correctly

### Platform Builds
- [ ] Windows 64-bit build tested
- [ ] Linux build tested (if applicable)
- [ ] macOS build tested (if applicable)

## Release Assets

### GitHub Release
- [ ] Create new release (v1.0.0)
- [ ] Write release notes
- [ ] Upload Windows ZIP
- [ ] Upload Linux ZIP (if available)
- [ ] Upload macOS ZIP (if available)
- [ ] Mark as latest release

### Release Notes Template
```markdown
# Blackjack Story Mode v1.0.0

First stable release of the web-based Blackjack Story Mode game!

## Features
- Complete story system with 47 unique events
- 3 NPC encounter events (mechanics)
- 7 functional shops with event-based unlocking
- 9 items with durability tracking
- Forced progression gameplay loop
- Minimalist retro aesthetic
- Standalone executable (no installation required)

## Downloads
- Windows 64-bit: `BlackjackStoryMode-v1.0.0-win64.zip`
- Linux: `BlackjackStoryMode-v1.0.0-linux.zip`
- macOS: `BlackjackStoryMode-v1.0.0-macos.zip`

## System Requirements
- Windows 10+, Linux, or macOS
- 100 MB free disk space
- Modern web browser

## Quick Start
1. Extract ZIP file
2. Run BlackjackStoryMode executable
3. Game opens in browser automatically
4. Enjoy!

## Known Issues
- None reported

## Credits
Original Game: DylanEaton17
Web Implementation: GitHub Copilot
```

## Post-Release

### Monitoring
- [ ] Monitor for user issues
- [ ] Check download counts
- [ ] Respond to bug reports

### Future Improvements
- [ ] Collect user feedback
- [ ] Note any bugs for patches
- [ ] Consider feature requests

## Security

- [ ] Executable scanned for viruses
- [ ] No malicious code included
- [ ] Only local connections (127.0.0.1)
- [ ] No data collection/external connections
- [ ] Source code matches executable

## Version Control

- [ ] All changes committed
- [ ] Branch merged to main
- [ ] Tagged as v1.0.0
- [ ] Build artifacts not committed

## Final Checks

- [ ] All checklist items completed
- [ ] Build tested on clean system
- [ ] Documentation reviewed
- [ ] Release package finalized
- [ ] GitHub release published
- [ ] Announcement prepared (if applicable)

---

**Sign-off:** 
- Date: _________________
- Tested by: _________________
- Approved by: _________________
