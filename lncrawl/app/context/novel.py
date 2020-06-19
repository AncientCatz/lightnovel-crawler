# -*- coding: utf-8 -*-

from typing import Any, Dict

from ..utility import UrlUtils


class Novel:
    '''Details of a novel'''

    def __init__(self, url: str) -> None:
        self.url: str = url.strip('/')
        self.name: str = ''
        self.details: str = ''
        self.cover_url: str = ''
        self.extra: Dict[Any, Any] = dict()

    def __hash__(self):
        return hash(self.url)

    def __eq__(self, other) -> bool:
        if isinstance(other, Novel):
            return self.url == other.url
        else:
            return super().__eq__(other)

    def __str__(self) -> str:
        return f"<Novel url='{self.url}' name='{self.name}' cover_url='{self.cover_url}'>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value.strip() if value else 'N/A'

    @property
    def cover_url(self):
        return self._cover_url

    @cover_url.setter
    def cover_url(self, value):
        self._cover_url = UrlUtils.join(self.url, value) if value else ''

    def get_extra(self, key: str):
        return self.extra[key]

    def put_extra(self, key: str, val: Any):
        self.extra[key] = val

    def to_json(self) -> Dict[str, Any]:
        return {
            'toc_url': self.url,
            'name': self.name,
            'cover_url': self.cover_url,
            'details': self.details,
            'extra': self.extra,
        }
