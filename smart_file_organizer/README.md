# 🗂️ Smart File Organizer

A beginner-to-intermediate Python CLI utility that organizes files into folders such as **Images**, **Documents**, **Audio**, **Video**, **Archives**, **Code**, and **Others**.

## ✨ Features

- Organizes files by extension
- `--dry-run` preview mode
- Prevents overwriting duplicate filenames
- Ignores hidden files
- Works with a chosen folder or the current directory
- Uses only Python's standard library

## 🚀 Usage

Preview changes first:

```bash
python file_organizer.py ~/Downloads --dry-run
```

Apply the organization:

```bash
python file_organizer.py ~/Downloads
```

## 📁 Project Structure

```text
smart_file_organizer/
├── file_organizer.py
└── README.md
```

## 🛡️ Safety Notes

Always run `--dry-run` before organizing an important folder. The script moves files only; it does not delete them. Avoid running it on system directories.

## 📄 License

MIT License.
