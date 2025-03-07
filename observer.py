import inspect
import weakref

class Observable:
    """Broadcasts a notification to a registry of function objects

----------------------------------------------------------------
TODO

* Not thread-safe
  * self.observers needs protection
* Currently only supports 'bound methods'. Do we need support for lambdas etc?
* What happens if both a SuperClass and a SubClass register the same function 
  * e.g. SubClass.init() and SuperClass.init() both register some function
  * Does it receive two notifications?
  * What if the function is overloaded?

----------------------------------------------------------------
Notes

* Bound Methods and weak references
  * See link for special handling of 'bound method' objects
  * https://docs.python.org/3/library/weakref.html#weakref.WeakMethod

* Threading
  * The notification will be broadcast on the thread calling notify
  * If notify occurs on a background, GUI elements will need make sure
    that updates are performed on the main/UI thread

----------------------------------------------------------------
How memory leaks and seg faults are prevented

Consider the object map of Observable and the Observer.
Observable contains a reference to each Observer
If an Observer object is 'deleted', what happens to the reference contained in Obserable's registry list?

* If Observable holds a weak reference, upon 'deleting' the Observer,
  the Observer is dealloc and the reference is now invalid (potential seg fault)
  *** The weakref module lets us check if the object has been dealloc

* If Observable holds a strong reference, upon 'deleting' the Observer,
  the reference will remain valid and Observer will never dealloc.
  The zombie Observer will continue to receive notifications
----------------------------------------------------------------
"""
    def __init__(self):
        self.observers = []

    def register_observer(self, func):
        """Add a function to the notification registry

        func: a bound method, i.e. method of a class with alloc'd instance
        """
        # check if already registered
        if func in self.observers:
            return

        # add to registry
        self.observers.append(weakref.WeakMethod(func))

    def unregister_observer(self, func):
        """Removes a function from the notification registry"""
        self.observers.remove(func)
        
    def notify_observers(self, user_data=None):
        """Notify all observers"""
        will_prune = []
        for ref in self.observers:
            func = ref()
            if func is None:
                # the object has been dealloc
                will_prune.append(ref)

            # notify
            if len(inspect.signature(func).parameters) > 1:
                func(self, user_data)
            elif len(inspect.signature(func).parameters) > 0:
                func(self)
            else:
                func()
                
        # remove dealloc'd references
        for ref in will_prune:
            self.observers.remove(ref)
      
