from uuid import uuid4


class TransactionFactory:
    def __init__(self, scope, on_call, on_raise, on_return):
        if not isinstance(scope):
            raise TypeError('scope must be an instance of an object')

        self.scope = scope

        for k, v in {'on_call': on_call, 'on_raise': on_raise, 'on_return': on_return}.items():
            if not callable(v):
                raise TypeError('{} not a valid callable for {}'.format(v, k))

        self.on_call = on_call
        self.on_raise = on_raise
        self.on_return = on_return

    def new(self, func, args, kwargs):
        return Transaction(scope=self.scope, on_start=self.on_start,
                           on_raise=self.on_call, on_return=self.on_return,
                           func=func, args=args, kwargs=kwargs)


class Transaction:

    def __init__(self, scope, on_call, on_raise, on_return, func, args, kwargs):
        self.__id = uuid4()
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs
        self.__scope = scope
        self.__on_call = on_call
        self.__on_raise = on_raise
        self.__on_return = on_return
        self.__completed = False
        self.__raise = None
        self.__return = None

    @property
    def id(self):
        return self.__id

    @property
    def func(self):
        return self.__func

    @property
    def args(self):
        return self.__args

    @property
    def kwargs(self):
        return self.__kwargs

    @property
    def scope(self):
        return self.__scope

    @property
    def on_call(self):
        return self.__on_call

    @property
    def on_raise(self):
        return self.__on_raise

    @property
    def on_return(self):
        return self.__on_raise

    @property
    def raised(self):
        return self.__raise

    @property
    def has_raised(self):
        return self.__raise is not None

    @property
    def returned(self):
        return self.__return

    @property
    def has_returned(self):
        return self.__return is not None

    @property
    def completed(self):
        return self.__completed

    @property
    def namespace(self):
        return self.func.__module__

    @property
    def short_name(self):
        return self.func.__qualname__

    @property
    def name(self):
        return self.namespace + '.' + self.short_name

    def __call__(self):
        self.on_call(self.scope, self)

        func = self.func
        args = self.args
        kwargs = self.kwargs

        try:
            self.__return = func(*args, **kwargs)
            self.on_return(self.scope, self)
            self.__completed = True
            return self.__return
        except Exception as exc:
            self.__raise = exc
            self.on_raise(self.scope, self)
            self.__completed = True
            raise

