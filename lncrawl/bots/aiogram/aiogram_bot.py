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
app = App()
class LNCrawl(StatesGroup):
    get_novel_url = State()
    smelt_2 = State()
    show_crawlers_to_search = State()
    show_novel_selection = State()
    handle_crawler_to_search = State()
    show_source_selection = State()
    handle_select_novel = State()

class AiogramBot:
    def main(self):
        # TODO: must be implemented
        # Start processing using this bot. It should use self methods to take
        # inputs and self.app methods to process them.
        #
        # self.app = App()
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

    @dp.message_handler(state='*', commands='cancel')
    async def cancel_handler(message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state is None:
            return

        logging.info('Cancelling state %r', current_state)
        # Cancel state and inform user about it
        await state.finish()
        # And remove keyboard (just in case)
        await message.reply('Session closed.', reply_markup=types.ReplyKeyboardRemove())

    @dp.message_handler(Command('new'))
    async def new(message: types.Message, state: FSMContext):
        await LNCrawl.get_novel_url.set()

        app.initialize()
        await message.answer('A new session is created.')
        async with state.proxy() as data:
            user_data['app'] = app
        await message.answer(
            'I recognize input of these two categories:\n' +
            '- Profile page url of a lightnovel.\n' +
            '- A query to search your lightnovel.\n' +
            'Enter whatever you want or send /cancel to stop.'
        )

    @dp.message_handler(state=LNCrawl.get_novel_url)
    async def get_novel_url(message: types.Message, state: FSMContext):
        app.user_input = message.text.strip()
        try:
            app.init_search()
        except Exception:
            await message.reply(
                'Sorry! I only recognize these sources:\n' +
                'https://github.com/dipu-bd/lightnovel-crawler#c3-supported-sources'
            )  # '\n'.join(['- %s' % x for x in crawler_list.keys()]))
            await message.reply(
                'Enter something again or send /cancel to stop.')
        # end try

        if app.crawler:
            await message.reply('Got your page link')
            await LNCrawl.smelt_2.set()
        # end if

        if len(app.user_input) < 5:
            await message.reply(
                'Please enter a longer query text (at least 5 letters).')
        # end if

        else:
            await message.reply('Got your query text')
            await LNCrawl.show_crawlers_to_search.set()
        # end else
    # end def

    @dp.message_handler(state=LNCrawl.show_crawlers_to_search)
    async def show_crawlers_to_search(message: types.Message, state: FSMContext):
        keyboard_markup = types.ReplyKeyboardMarkup(row_width=3)
        buttons = []

        def make_button(i, url):
            return '%d - %s' % (i + 1, urlparse(url).hostname)
        # end def
        for i in range(1, len(app.crawler_links) + 1, 2):
            buttons += [[
                make_button(i - 1, app.crawler_links[i - 1]),
                make_button(i, app.crawler_links[i]) if i < len(
                    app.crawler_links) else '',
            ]]
        # end for

        keyboard_markup.add(*(types.KeyboardButton(text) for text in buttons))
        await message.answer(
            'Choose where to search for your novel, \n' +
            'or send /skip to search everywhere.',
            reply_markup=keyboard_markup,
        )
        await LNCrawl.handle_crawler_to_search.set()
    # end def

    @dp.message_handler(state=LNCrawl.handle_crawlers_to_search, commands=['skip'])
    async def handle_crawler_to_search(message: types.Message, state: FSMContext):
        # app = user_data.get('app')

        link = message.text
        if link:
            selected_crawlers = []
            if link.isdigit():
                selected_crawlers += [
                    app.crawler_links[int(link) - 1]
                ]
            else:
                selected_crawlers += [
                    x for i, x in enumerate(app.crawler_links)
                    if '%d - %s' % (i + 1, urlparse(x).hostname) == link
                ]
            # end if
            if len(selected_crawlers) != 0:
                app.crawler_links = selected_crawlers
            # end if
        # end if

        await message.answer(
            'Searching for "%s" in %d sites. Please wait.' % (
                app.user_input, len(app.crawler_links)),
            reply_markup=types.ReplyKeyboardRemove(),
        )
        await message.answer(
            'DO NOT type anything until I reply.\n' +
            'You can only send /cancel to stop this session.'
        )

        app.search_novel()
        await LNCrawl.show_novel_selection.set()
    # end def

    @dp.message_handler(state=LNCrawl.show_novel_selection)
    async def show_novel_selection(message: types.Message, state: FSMContext):
        # app = user_data.get('app')

        if len(app.search_results) == 0:
            await message.answer(
                'No results found by your query.\n'
                'Try again or send /cancel to stop.'
            )
            await LNCrawl.handle_novel_url.set()
        # end if

        if len(app.search_results) == 1:
            data['selected'] = app.search_results[0]
            await LNCrawler.show_source_selection.set()
        # end if

        keyboard_markup = types.ReplyKeyboardMarkup(row_width=3)
        # buttons = [
        #         [
        #             '%d. %s (in %d sources)' % (
        #                 index + 1, res['title'], len(res['novels'])
        #             )
        #         ] for index, res in enumerate(app.search_results)
        #     ]
        await message.answer(
            'Choose any one of the following novels,' +
            ' or send /cancel to stop this session.',
            reply_markup=keyboard.add(*(types.KeyboardButton(text) for text in ([
                [
                    '%d. %s (in %d sources)' % (
                        index + 1, res['title'], len(res['novels'])
                    )
                ] for index, res in enumerate(app.search_results)
            ]))),
        )

        await LNCrawl.handle_select_novel.set()
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
