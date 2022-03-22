from dataclasses import dataclass


@dataclass
class User:
    id: str = ''
    username: str = ''
    avatar: str = ''
    discriminator: str = ''
    public_flags: int = 0
    flags: int = 0
    banner: str = ''
    banner_color: str = ''
    accent_color: str = ''
    bio: str = ''
    locale: str = ''
    nsfw_enabled: bool = False
    mfa_enabled: bool = False
    email: str = ''
    verified: bool = False
    phone: str = ''
