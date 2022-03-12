from typing import Optional
import re
import subprocess
import uuid


def get_windows_uuid() -> Optional[uuid.UUID]:
    try:
        # Ask Windows for the device's permanent UUID. Throws if command missing/fails.
        txt = subprocess.check_output("wmic csproduct get uuid").decode()

        # Attempt to extract the UUID from the command's result.
        match = re.search(r"\bUUID\b[\s\r\n]+([^\s\r\n]+)", txt)
        if match is not None:
            txt = match.group(1)
            if txt is not None:
                # Remove the surrounding whitespace (newlines, space, etc)
                # and useless dashes etc, by only keeping hex (0-9 A-F) chars.
                txt = re.sub(r"[^0-9A-Fa-f]+", "", txt)

                # Ensure we have exactly 32 characters (16 bytes).
                if len(txt) == 32:
                    return uuid.UUID(txt)
    except:
        pass # Silence subprocess exception.

    return None