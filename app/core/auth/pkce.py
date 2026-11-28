import hashlib
import base64
import re


def verify_pkce(
    verifier: str,
    challenge: str,
) -> bool:

    # RFC 7636 verifier validation
    if not 43 <= len(verifier) <= 128:
        return False

    if not re.fullmatch(
        r"[A-Za-z0-9\-._~]+",
        verifier,
    ):
        return False

    digest = hashlib.sha256(
        verifier.encode("ascii")
    ).digest()

    calculated_challenge = (
        base64.urlsafe_b64encode(digest)
        .rstrip(b"=")
        .decode("ascii")
    )

    return calculated_challenge == challenge