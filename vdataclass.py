from typing import Any, List, Optional
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config


# vendor provided URL type alias for clarity
VendorUrl = str


@dataclass_json
@dataclass
class Firmware:
    version: str
    models: List[str]
    filename: str
    url: VendorUrl
    size_bytes: Optional[int] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    md5: Optional[str] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    sha256: Optional[str] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    sha512: Optional[str] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    sha1: Optional[str] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    release_date: Optional[str] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    release_notes: Optional[VendorUrl] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    user_manual: Optional[str] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    # catch all for vendor data that doesn't fit in our schema
    # It's a catch-all for vendor data that doesn't fit in our schema.
    vendor_metadata: Optional[Any] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    # stretch goal: CVEs fixed in this specific firmware release
    fixed_cves: Optional[List[str]] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    vulnerable_to_cves: Optional[List[str]] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    # New fields to scrape if possible
    description: Optional[str] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    device_picture_urls: Optional[List[str]] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    discontinued: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    replacements: Optional[str] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )