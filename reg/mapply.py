import inspect

def mapply(func, *args, **kw):
    """Apply keyword arguments to function only if it defines them.

    So this works without error as ``b`` is ignored::

      def foo(a):
          pass

      mapply(foo, a=1, b=2)

    Zope has an mapply that does this but a lot more too. py.test has
    an implementation of getting the argument names for a
    function/method that we've borrowed.
    """
    new_kw = { name: kw[name] for name in argnames(func) if name in kw }
    return func(*args, **new_kw)

_argnames_cache = {}

def argnames(func):
    """Get arg names for given function or method or constructor.

    Taken from pytest.core, varnames. Adjusted to get argument names
    for class constructors too.
    """
    try:
        return _argnames_cache[func]
    except KeyError:
        pass
    origfunc = func
    if (not inspect.isfunction(func) and
        not inspect.ismethod(func) and
        not inspect.isclass(func)):
        func = getattr(func, '__call__', func)
    if inspect.isclass(func):
        func = func.__init__
    ismethod = inspect.ismethod(func)
    rawcode = getrawcode(func)
    try:
        result = rawcode.co_varnames[ismethod:rawcode.co_argcount]
    except AttributeError:
        result = ()
    _argnames_cache[origfunc] = result
    return result


def getrawcode(obj, trycall=True):
    """Return code object for given function.

    Taken from py._code.code
    """
    try:
        return obj.__code__
    except AttributeError:
        obj = getattr(obj, 'im_func', obj)
        obj = getattr(obj, 'func_code', obj)
        obj = getattr(obj, 'f_code', obj)
        obj = getattr(obj, '__code__', obj)
        if trycall and not hasattr(obj, 'co_firstlineno'):
            if hasattr(obj, '__call__') and not inspect.isclass(obj):
                x = getrawcode(obj.__call__, trycall=False)
                if hasattr(x, 'co_firstlineno'):
                    return x
        return obj
