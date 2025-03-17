from behaviorTree import BehaviorTree, Sequence, Fallback, ForceFail, Test1, Test2, Test3, Test4, Test5,Invert


t1=Test1("success")
t2=Test2("success")
t3=Test3("failure")
t4=Test4("success")
t5=Test5("success")



I=Invert("waiting",t2)

F1=Fallback("waiting",[I,t3,t4])

S1=Sequence("waiting",[t1,F1,t5])

testTree=BehaviorTree("waiting",S1)


testTree.start()


#testing the structure of the tree
#the resulting prints should theoretically be testing leaf repeated 4 times
#this is NOT the final tree

#attempt at a pseudo version of what a behavior tree might look like in the final version: 
#initialize all the nodes that dont depend on aggressivity (e.g the leaf nodes, the start nodes, the deco nodes)
#through a if-then or case match initialize different versions of the ctrl nodes (a more agressive tree might try attacking before fleeing in the corresponding fallback node, while a more passive one might put the fleeing node first)

# a snippet of the tree dealing with being attacked might look like this for exemple :

# profile="aggressive"
#
# attack=Action()
# flee=Action()
# checkifenemy=Condition()
# initialize all other nodes accordingly ...
# ...
# if(profile=="aggressive"):
#     underAttack=Fallback("waiting",[checkifenemy,attack,flee])
#     initialize the other ctrl nodes ...
# elif(profile=="passive"):
#     underAttack=Fallback("waiting",[checkifenemy,flee,attack])
#     initialize the other ctrl nodes ...
