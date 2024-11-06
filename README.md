# Echo360 VTT Downloader

This script downloads captions from Echo360 lesson URLs in `.vtt` format, cleans up the text, and saves it either as a single line or separate lines based on user preference.

## Prerequisites

Install the required packages using:

```bash
pip install -r requirements.txt
```

## Usage

1. **Update the script with URLs and a cookie.**
   - Replace the placeholder URL in the `urls` list with the actual Echo360 lesson URL(s).
   - Replace the `cookie` variable with your own Echo360 session cookie.

2. **Set Output Format:**
   - Change `single_line` to `True` if you want all captions in a single line.
   - Set `single_line` to `False` to keep each caption on a separate line.

3. **Run the Script:**

```bash
python echo360_downloader.py
```

4. **Output:**
   - The script saves each lesson's cleaned captions as a `.vtt` file with the title and date of the lesson.

### Example

For example, if your lesson title is "Public Finance" and date is "Oct 3," the output file will be named `Public Finance - Thu Oct 03.vtt`.

## Notes
Ensure the `cookie` value remains up-to-date as Echo360 sessions can expire.
