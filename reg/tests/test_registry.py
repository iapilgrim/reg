from reg.registry import Registry
from reg.interfaces import IMatcher


def test_registry_sources():
    reg = Registry()

    class Document(object):
        pass

    class SpecialDocument(Document):
        pass

    def linecount(obj):
        pass

    reg.register(linecount, [Document], 'document line count')
    reg.register(linecount, [SpecialDocument], 'special document line count')

    assert (reg.component(linecount, [Document()] ) ==
            'document line count')

    assert (reg.component(linecount, [SpecialDocument()]) ==
            'special document line count')

    class AnotherDocument(Document):
        pass

    assert (reg.component(linecount, [AnotherDocument()]) ==
            'document line count')

    class Other(object):
        pass

    assert reg.component(linecount, [Other()], default=None) is None


def test_registry_target_find_specific():
    reg = Registry()

    class Document(object):
        pass

    class SpecialDocument(Document):
        pass

    def linecount(obj):
        pass

    def special_linecount(obj):
        pass

    reg.register(linecount, [Document], 'line count')
    reg.register(special_linecount, [Document], 'special line count')

    assert reg.component(linecount, [Document()]) == 'line count'
    assert (reg.component(special_linecount, [Document()]) ==
            'special line count')

    assert reg.component(linecount, [SpecialDocument()]) == 'line count'
    assert (reg.component(special_linecount, [SpecialDocument()]) ==
            'special line count')


# def test_registry_target_find_subclass():
#     reg = Registry()

#     class Document(object):
#         pass

#     class Animal(object):
#         pass

#     def 
#     class Elephant(Animal):
#         pass

#     reg.register(Elephant, (Document,), 'elephant')
#     assert reg.component(Animal, (Document(),)) == 'elephant'


def test_registry_no_sources():
    reg = Registry()

    class Animal(object):
        pass

    def something():
        pass

    reg.register(something, (), 'elephant')
    assert reg.component(something, ()) == 'elephant'


def test_matcher():
    reg = Registry()

    class Document(object):
        def __init__(self, id):
            self.id = id

    def linecount(obj):
        pass

    class Matcher(IMatcher):
        def __call__(self, doc):
            if doc.id == 1:
                return 'normal'
            else:
                return 'special'
            
    reg.register(linecount, [Document],
                 Matcher())

    assert reg.component(linecount, [Document(1)]) == 'normal'
    assert reg.component(linecount, [Document(2)]) == 'special'

def test_matcher_inheritance():
    reg = Registry()

    class Document(object):
        def __init__(self, id):
            self.id = id

    class SpecialDocument(Document):
        pass
    
    def linecount(obj):
        pass

    class DocumentMatcher(IMatcher):
        def __call__(self, doc):
            if doc.id == 1:
                return 'normal'
            else:
                return 'special'

    class SpecialDocumentMatcher(IMatcher):
        def __call__(self, doc):
            if doc.id == 2:
                return 'extra normal'
            else:
                return None

    reg.register(linecount, [Document],
                 DocumentMatcher())
    reg.register(linecount, [SpecialDocument],
                 SpecialDocumentMatcher())
    
    assert reg.component(linecount, [Document(1)]) == 'normal'
    assert reg.component(linecount, [Document(2)]) == 'special'
    assert reg.component(linecount, [SpecialDocument(1)]) == 'normal'
    assert reg.component(linecount, [SpecialDocument(2)]) == 'extra normal'
    assert reg.component(linecount, [SpecialDocument(3)]) == 'special'

def test_register_twice_with_sources():
    reg = Registry()

    class Document(object):
        pass

    def linecount(obj):
        pass

    reg.register(linecount, [Document], 'document line count')
    reg.register(linecount, [Document], 'another line count')
    assert reg.component(linecount, [Document()]) == 'another line count'

def test_register_twice_without_sources():
    reg = Registry()

    def linecount(obj):
        pass

    reg.register(linecount, [], 'once')
    reg.register(linecount, [], 'twice')
    assert reg.component(linecount, []) == 'twice'

    
# XXX various default and component lookup error tests