from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from mars import create_app
from config.setting.alpha import Config

# 需要导入model，要不然无法执行迁移,生成数据表

app, db = create_app(Config)

# 1.托管app启动    python manage.py runserver
manager = Manager(app)

# 2.数据库迁移
Migrate(app, db)

# 3.自定迁移命令    python manage.py db [init] [migrate] [upgrade]
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

    # import os
    # os.system('export FLASK_APP=manage.py')
    # os.system('export FLASK_ENV=development')
    # os.system('export FLASK_DEBUG=1')
    # os.system('python -m flask run')

