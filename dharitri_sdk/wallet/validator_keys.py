from dharitri_sdk.wallet.constants import (VALIDATOR_PUBKEY_LENGTH,
                                             VALIDATOR_SECRETKEY_LENGTH)
from dharitri_sdk.wallet.errors import ErrBadSecretKeyLength
from dharitri_sdk.wallet.interfaces import ISignature
from dharitri_sdk.wallet.libraries.bls_facade import BLSFacade


class ValidatorSecretKey:
    def __init__(self, buffer: bytes) -> None:
        if len(buffer) != VALIDATOR_SECRETKEY_LENGTH:
            raise ErrBadSecretKeyLength()

        self.buffer = buffer

    @classmethod
    def generate(cls) -> 'ValidatorSecretKey':
        secret_key_bytes = BLSFacade().generate_private_key()
        return ValidatorSecretKey(secret_key_bytes)

    @classmethod
    def from_string(cls, buffer_hex: str) -> 'ValidatorSecretKey':
        buffer = bytes.fromhex(buffer_hex)
        return ValidatorSecretKey(buffer)

    def generate_public_key(self) -> 'ValidatorPublicKey':
        public_key_bytes = BLSFacade().generate_public_key(self.buffer)
        return ValidatorPublicKey(public_key_bytes)

    def sign(self, data: bytes) -> ISignature:
        signature = BLSFacade().compute_message_signature(data, self.buffer)
        return signature

    def hex(self) -> str:
        return self.buffer.hex()

    def __str__(self) -> str:
        return ValidatorSecretKey.__name__

    def __repr__(self) -> str:
        return ValidatorSecretKey.__name__


class ValidatorPublicKey:
    def __init__(self, buffer: bytes) -> None:
        if len(buffer) != VALIDATOR_PUBKEY_LENGTH:
            raise ErrBadSecretKeyLength()

        self.buffer = buffer

    @classmethod
    def from_string(cls, buffer_hex: str) -> 'ValidatorPublicKey':
        buffer = bytes.fromhex(buffer_hex)
        return ValidatorPublicKey(buffer)

    def verify(self, data: bytes, signature: ISignature) -> bool:
        ok = BLSFacade().verify_message_signature(self.buffer, data, signature)
        return ok

    def hex(self) -> str:
        return self.buffer.hex()

    def __str__(self) -> str:
        return self.hex()

    def __repr__(self) -> str:
        return self.hex()
