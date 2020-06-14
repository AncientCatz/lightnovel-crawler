# -*- coding: utf-8 -*-

from typing import List

from .author import Author
from .language import Language


class Novel:
    '''Details of a novel'''

    def __init__(
            self,
            url: str,
            name: str = None,
            details: str = None,
            cover_url: str = None) -> None:
        super().__init__()
        self.url: str = url
        self.name: str = name
        self.details: str = details
        self.cover_url: str = cover_url
        self.authors: List[Author] = []
        self.language: Language = Language.UNKNOWN

    def __str__(self) -> str:
        return f"<Novel url:'{self.url}'>"

    def __eq__(self, other) -> bool:
        if isinstance(other, Novel):
            return self.url == other.url
        else:
            return super().__eq__(other)
