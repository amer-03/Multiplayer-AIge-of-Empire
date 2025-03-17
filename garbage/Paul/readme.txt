Part of Paul

ideas for ai development :
behavior tree method seems the most useful
currently figuring it out

3 types of nodes :
composite (sequence, etc)(has one or more children, determines in which order they are processed)

    Sequence processes the 1st child and only processes the next one if the previous one
     returns success, returns success only if every child returns success

    Selector/Fallback processes the 1st child and only processes the next one if the
     previous one returns Failure, stops processing and returns success at the first success it encounters

decorator (inverter, etc)

    UntilSuccess and Until Failure continue processing the child until they return Success or Failure respectively

    ForceSuccess and ForceFail process the child and always return Success or Failure respectively no matter what the child returns

    Invert always returns the opposite status of its child (Success->Failure, Failure->Success, Running->Running)

leaf (actual functions, e.g. move this horseman)


ideas : (NOT FINAL, MUSINGS ON WHICH APPROACH TO TAKE FOR IMPLEMENTATION)

Status class
	Running
	Success
	Failure 


Create a TreeNode class (TreeNode child, Status status,)

    Start()
    Update(){
        Do shit
        Return running, failure or success
    }  

Create ControlNode class (inherits treeNode)
instead of a single child, sth like a list of children

Create decoNode class (inherits treeNode)
single child

Create LeafNode class (inherits treeNode)
no child

Create actionNode class (inherits LeafNode)
(specific nodes inheriting this will be stuff like walk or attack)

Create conditionNode class (inherits LeafNode)
(specific nodes inheriting this will be stuff like checking if the player is being attacked)

Sequence, Fallback (or selector, idk what name you prefer) all inherit control
UntilSuccess, UntilFail, ForceSuccess, ForceFail, Invert all inherit deco

for the actual tree, select(hah) which node to use when making the tree depending on the aggressivity
(case match) 


ideas for bits of the tree :

fallback under_attack(
	condition currently_safe()
	fallback defensive_action(
		sequence defend(
			condition close_to_defensive_building()
			action attack(closest_def_build, enemy_unit))
		sequence send_cavalry(
			condition unit_available(horseman)
			action attack(horseman, enemy_unit))
		sequence send ... (etc, etc) (find a way to send multiple units) (which unit to send first ?)
		.
		.
		.
		sequence train_units(
			fallback can_train(
				condition trainable_buildings_exist()
				sequence build_building(
					condition enough_resources()
					action build(building))) (again, try to generalize this)
			condition enough_resources()
			condition can_add_unit()
			action add_units()))))

leaf nodes to make :

class attack(Action)

class collect(action):
	
class check_unfinished_buildings(condition):

class check_available_resources(condition):

class can_add_unit(condition):


implement dt somehow


useful links
https://www.gamedeveloper.com/programming/behavior-trees-for-ai-how-they-work
https://www.behaviortree.dev/
https://en.wikipedia.org/wiki/Behavior_tree_(artificial_intelligence,_robotics_and_control)
https://lisyarus.github.io/blog/posts/behavior-trees.html