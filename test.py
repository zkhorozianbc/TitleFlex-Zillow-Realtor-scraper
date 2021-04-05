class A:

    def __init__(self):
        self.name = "Zach"

    @staticmethod
    def wrapper(self,func):
        def inner(*args,**kwargs):
            self.before()
            func(*args,**kwargs)
            self.after()
        return inner
    
    def before(self):
        print("Before")

    def after(self):
        print("After")

    @A.wrapper
    def f(self):
        print(f"Hello {self.name}")


A().f()