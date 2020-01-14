

```python

User.create({
   'username': 'test',
   'password': 'test'
})

user.locations = Location.find()


user.save()
```