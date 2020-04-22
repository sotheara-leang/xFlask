xFlask combines the extensions of Flask and it is designed to make getting started quick and easy to build Restful web service, with the ability to scale up to complex applications. It begin as a simple wrapper around Flask and its extensions to provide a simple platform to ease API development.
## 1. Functionalities

* Follow concepts of Model, Data Access Object (DAO), Service and Controller
* Ease to decouple component dependencies by using Flask-Injector
* Provide a simple way to validate Value Object (VO) by using Marshmallow
* Adapt with Flask-Migration to easily maintain the database schema
* Provide simple logging API helping to debug the application flow
* Adapt with Flask-Testing for testing the application components
 

## 2. Usages

* Model

```python
from xflask.sqlalchemy import Column, Integer, String
from xflask.sqlalchemy.model import AuditModel

class User(AuditModel):

    id          = Column(Integer, primary_key=True)
    username    = Column(String(50), unique=True, nullable=False)
    password    = Column(String(50), unique=False, nullable=False)
```

* DAO

```python
from xflask.dao import Dao

from main.model.user import User

class UserDao(Dao):

    def __init__(self):
        super(UserDao, self).__init__(User)

    def get_by_username(self, username):
        return self.query().filter_by(username=username).first()
```

* Service

```python
from injector import inject

from xflask.service import CrudService

from main.dao.user import UserDao

class UserService(CrudService):

    @inject
    def __init__(self, dao: UserDao):
        super(UserService, self).__init__(dao)

    def get_user(self, user_id):
        return self.user_dao.get_user(user_id)
```

* Controller

```python
from injector import inject

from xflask.classy import route, JsonBody
from xflask.controller import Controller
from xflask.web.response import Response

from main.controller.vo.user import UserVo
from main.model.user import User
from main.service.user import UserService

class UserController(Controller):

    route_base = '/api/user/'

    @inject
    def __init__(self, user_service: UserService):
        self.user_service = user_service
    
    @route('<user_id>')
    def get(self, user_id):
        user = self.user_service.get(user_id)
        if user is None:
            return Response.not_found()

        return Response.success(user)
        
    @route('', methods=['PUT'])
    def update(self, user: JsonBody(UserVo)):
        self.user_service.update(User(**user))

        return Response.success()
```

* Value Object (VO)

```python
from xflask.marshmallow import Int, Str
from xflask.marshmallow import validate

from xflask.web.vo import Vo

class UserVo(Vo):

    id          : Int(required=True)
    username    : Str(validate=validate.Length(min=2, max=50), required=True)
    password    : Str(validate=validate.Length(min=2, max=50), required=True)
```