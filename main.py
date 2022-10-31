from aiogram.utils import executor

import handlers.registration_handlers
from create_bot import dp
import handlers


async def on_startup(_):
    print('Бот онлайн')

handlers.registration_handlers.register_registration_handlers(dp)
handlers.menu_handlers.register_menu_handlers(dp)
handlers.send_request_handlers.register_requests_handlers(dp)
handlers.send_idea_handlers.register_idea_handlers(dp)
handlers.settings_handlers.register_settings_handlers(dp)
handlers.contact_us_handlers.register_contact_us_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
