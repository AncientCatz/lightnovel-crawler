# -*- coding: utf-8 -*-
import logging
import os
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from ...core.app import App
from ...sources import crawler_list
from ...utils.uploader import upload
from ...utils.loading_bar import progress

logger = logging.getLogger(__name__)

available_formats = [
    'epub',
    'text',
    'web',
    'mobi',
    'pdf',
]

# TODO: It is recommended to implemented all methods. But you can skip those
#       Which return values by default.
# Initialize bot and dispatcher
API_TOKEN = os.getenv('TELEGRAM_TOKEN', '')
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

class LNCrawl(StatesGroup):
    smelt = State()

class AiogramBot:
    def main(self):
        # TODO: must be implemented
        # Start processing using this bot. It should use self methods to take
        # inputs and self.app methods to process them.
        #
        self.app = App()
        # self.app.initialize()
        #
        print("Aiogram is online!")
        executor.start_polling(dp, skip_updates=True)
        # Checkout console.py for a sample implementation
    # end def

    @dp.message_handler(Command('start'))
    async def start(message: types.Message):
        await message.answer(
            'Hi!\n'
            'I\'m Lightnovel Crawler! I can help you generate lightnovels in EPUB format, etc.'
            'Send /new to start a new session.'
        )
    # end def

    @dp.message_handler(Command('help'))
    async def start(message: types.Message):
        await message.answer(
            'Send /new to start a new session.'
        )
    # end def

    @dp.message_handler(Command('new'))
    async def new(message: types.Message):
        await LNCrawl.smelt.set()

        app.initialize()
        user_data['app'] = app
        await message.answer('A new session is created.')

        await message.answer(
            'I recognize input of these two categories:\n'
            '- Profile page url of a lightnovel.\n'
            '- A query to search your lightnovel.\n'
            'Enter whatever you want or send /cancel to stop.'
        )

    def get_novel_url(self):
        # Returns a novel page url or a query
        pass
    # end def

    def get_crawlers_to_search(self):
        # Returns user choice to search the choosen sites for a novel
        pass
    # end def

    def choose_a_novel(self):
        # The search_results is an array of (novel_title, novel_url).
        # This method should return a single novel_url only
        #
        # By default, returns the first search_results. Implemented it to
        # handle multiple search_results
        pass
    # end def

    def get_login_info(self):
        # By default, returns None to skip login
        pass
    # end if

    def get_output_path(self):
        # You should return a valid absolute path. The parameter suggested_path
        # is valid but not gurranteed to exists.
        #
        # NOTE: If you do not want to use any pre-downloaded files, remove all
        #       contents inside of your selected output directory.
        #
        # By default, returns a valid existing path from suggested_path
        pass
    # end def

    def get_output_formats(self):
        # The keys should be from from `self.output_formats`. Each value
        # corresponding a key defines whether create output in that format.
        #
        # By default, it returns all True to all of the output formats.
        pass
    # end def

    def should_pack_by_volume(self):
        # By default, returns False to generate a single file
        pass
    # end def

    def get_range_selection(self):
        # Should return a key from `self.selections` array
        pass
    # end def

    def get_range_using_urls(self):
        # Should return a list of chapters to download
        pass
    # end def

    def get_range_using_index(self):
        # Should return a list of chapters to download
        pass
    # end def

    def get_range_from_volumes(self):
        # Should return a list of chapters to download
        pass
    # end def

    def get_range_from_chapters(self):
        # Should return a list of chapters to download
        pass
    # end def
# end class
