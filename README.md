# xFlask

## 1. Usages

* Model

```python
class User(Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
```

* DAO

```python
class UserDao(Dao):

    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_user(self, user_id):
        return User.query.get(user_id)

```

* Service

```python
class UserService(Service):

    logger = logging.getLogger(__qualname__)

    @inject
    def __init__(self, user_dao: UserDao):
        self.user_dao = user_dao

    def get_user(self, user_id):
        return self.user_dao.get_user(user_id)
```

* Controller

```python
@app.route('<user_id>')
def get_user(user_id, user_service: UserService):
    user = user_service.get_user(user_id)
    return Response.success(user).to_dict()

```