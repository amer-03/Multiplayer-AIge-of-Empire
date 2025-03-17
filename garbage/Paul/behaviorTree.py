class treeNode:

    def __init__(self, status):
        self.status=status
    
    def update(self,x):
        return self.status
    
    def start(self):
        self.update()

class ctrlNode(treeNode):

    def __init__(self, status, childlist):
        self.status=status
        self.childlist=childlist                #a ctrl node has several children, here implemented as a list

        assert (isinstance(childlist[i],treeNode) for i in range(len(childlist)))

class decoNode(treeNode):

    def __init__(self, status, child):
        self.status=status
        self.child=child                        #a deco node has only one child

        assert isinstance(child,treeNode)

class leafNode(treeNode):
    pass                                        #a leaf node has no children

class Sequence(ctrlNode):

    def update(self,x):    #have to add an unused x variable, otherwise it doesnt work because of some reason. i looked it up but i forgot why, sorry.
        for (child) in self.childlist:
            if (child.update(child)!="success"): #if the child process returns anything but success, the sequence stops updating its branches and returns failure
                self.status="failure"
                print(self.status)
                return self.status
        
        self.status="success"  #else, the sequence updates all of its children and returns success 
        return self.status

    
class Fallback(ctrlNode):
    
    def update(self,x):
        for i in range(len(self.childlist)):
            if (self.childlist[i].update(self.childlist[i])=="success"): #if the child process returns a success, the fallback stops updating its branches and returns success
                self.status="success"
                return self.status
        else:
            self.status="failure"   #if the fallback arrives at the end of its childlist without encountering any success, it returns failure
            return self.status

class UntilSuccess(decoNode):
    
    def update(self,x):
        while (self.child.status!="success"):  
            self.child.update(self.child)
        self.status="success"
        return self.status

class UntilFail(decoNode):
    def update(self,x):
        while (self.child.status!="failure"):  
            self.child.update(self.child)
        self.status="success"
        return self.status

class ForceFail(decoNode):
    
    def update(self,x):
        self.child.update(self.child) 
        self.status="failure"
        return self.status

class Invert(decoNode):
    
    def update(self,x):
        if (self.child.update(self.child)=="success"):  
            self.status="failure"
        elif (self.child.update(self.child)=="failure"):  
            self.status="success"
        return self.status       

class Action(leafNode):
    pass

class Condition(leafNode):
    pass

class BehaviorTree(decoNode):
    def update(self):
        self.status=self.child.update(self.child) 
        return self.status


class Test1(Action):   
    def update(self,x):
        print("test leaf 1")
        return self.status 

class Test2(Action):   
    def update(self,x):
        print("test leaf 2")
        return self.status

class Test3(Action):   
    def update(self,x):
        print("test leaf 3")
        return self.status
    

class Test4(Action):   
    def update(self,x):
        print("test leaf 4")
        return self.status

class Test5(Action):   
    def update(self,x):
        print("test leaf 5")
        return self.status

class attack(Action):
	def __init__(self,status,unit):
		self.status=status
		self.unit=unit

	def update(self,x):
		self.unit.attack_entity(entity_id)
		#now what abt status tho