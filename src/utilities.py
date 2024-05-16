import os
import sys

def open_pdf(output_pdf):
    try:
        if os.name == 'nt':  # Windows
            os.startfile(output_pdf)
        elif os.name == 'posix':  # macOS or Linux
            os.system(f'open "{output_pdf}"' if sys.platform == 'darwin' else f'xdg-open "{output_pdf}"')
    except Exception as e:
        print(f"Failed to open file: {e}")