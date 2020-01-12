

class Test(Entity):
   pass

class RTest(Entity):
   relationships = {
      "test" : OneToMany(Test, RTest)
   }


r = RTest.find(1)
print(r)

r = RTest()
r.test = Test.findOne(1)
r.save()