# Copyright (C) 2025 Ayrik Nabirahni
# This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or 
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see https://www.gnu.org/licenses.

from config.config import *
from exopy.getdata.getsetting import *
def show_flags():
    for key in user_flags:
        print(f'{key} = {user_flags[key]}')
    print('\n' * 2)

def edit_settings():
    show_flags()
    user_input = get_setting()
    new_setting = get_new_setting(user_flags[user_input])
    user_flags[user_input] = new_setting
    print(f'Flag {user_input} set to {new_setting}')