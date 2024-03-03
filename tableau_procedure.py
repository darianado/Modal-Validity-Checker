
import copy
from parse import Node


class KripkeWorld:
    """
    Encapsulate the behaviour of Kripke World.

    Attributes
    ----------
    name: str
    values: list

    Methods
    -------
    get_name(self)
        Returns the name of the world.
    add_variable(self, value)
        Adds the true variable to the world.
    __repr__(self)
        Returns the string representation of the world.
    __del__(self)
        Deletes the Kripke World.

    """

    def __init__(self, name: str, values: list = []):
        self.name = name
        self.values = values

    def get_name(self) -> str:
        """
        Returns the name of the world.

        Returns
        -------
        str
            Name of the world.

        """
        return self.name

    def add_variable(self, value) -> None:
        """
        Adds the true variable to the world.

        Parameters
        ----------
        value: object
            True variable in the world.

        Returns
        -------
        None

        """
        self.values.append(value)

    def __repr__(self) -> str:
        """
        Returns the string representation of the world.

        Returns
        -------
        str
            String representation of the world.

        """
        return f"World({self.name}, {self.values})"

    def __del__(self) -> None:
        """
        Deletes the Kripke World.

        Returns
        -------
        None

        """
        self.values = []
        self.name = ""


class KripkeModel:
    """
    Encapsulate the behaviour of Kripke Model.

    Attributes
    ----------
    worlds: list
    relations: dict

    Methods
    -------
    add_relation(self, world1, world2)
        Adds the relation between two worlds.
    add_world(self, world)
        Adds the world to the model.
    get_model(self)
        Returns the generated Kripke model.
    __repr__(self)
        Returns the string representation of the model.
    __del__(self)
        Deletes the Kripke Model.
    new_copy(self, mapping)
        Returns the new copy of the model.

    """

    def __init__(self, worlds: list = None, relations: dict = None):
        if worlds == None: worlds = []
        if relations == None: relations = {}
        self.worlds = worlds  # list of KripkeWorlds
        self.relations = relations  # world name: [wordls]

    def __del__(self) -> None:
        """
        Deletes the Kripke Model.

        Returns
        -------
        None

        """
        self.relations = []
        self.worlds = []

    def add_relation(self, world1: str, world2: str) -> None:
        """
        Adds the relation between two worlds.

        Parameters
        ----------
        world1: str
            Name of the first world.
        world2: str
            Name of the second world.

        Returns
        -------
        None

        """
        if world1 not in self.relations:
            self.relations[world1] = []
        self.relations[world1].append(world2)

    def add_world(self, world) -> None:
        """
        Adds the world to the model.

        Parameters
        ----------
        world: KripkeWorld
            World to be added.

        Returns
        -------
        None

        """
        self.worlds.append(world)

    def get_model(self) -> tuple:
        """
        Returns the generated Kripke model.

        Returns
        -------
        tuple
            Kripke model.

        """
        return self.worlds, self.relations

    def __repr__(self) -> str:
        """
        Returns the string representation of the model.

        Returns
        -------
        str
            String representation of the model.

        """
        return f"Model({self.worlds},\n {self.relations})"

    def new_copy(self, mapping: dict) -> 'KripkeModel':
        """
        Returns the new copy of the model.

        Parameters
        ----------
        mapping: dict
            Mapping of the worlds names.

        Returns
        -------
        KripkeModel
            New copy of the model with the new names.

        """
        new_model = KripkeModel()

        for world in self.worlds:
            if not world.name in mapping:
                mapping[world.name] = world
                new_model.add_world(world)
            else:
                new_model.add_world(mapping[world.name])

        for world_name, related_worlds in self.relations.items():
            for related_world in related_worlds:
                new_model.add_relation(mapping[world_name].name, mapping[related_world].name)

        return new_model



class Tableau:
    """
    Encapsulate the behaviour of Tableau.

    Attributes
    ----------
    true_column: dict
        True column of Tableau.
    false_column: dict
        False column of Tableau.
    unfolded: dict
        Unfolded set of Tableau.
    accessible: list
        Accessible world of Tableau.
    true_in_accessible: list
        True in accessible world of Tableau.
    false_in_accessible: list
        False in accessible world of Tableau.
    world: KripkeWorld
        World of Tableau.

    Methods
    -------
    update_true_col_unfolded(self, tr)
        Updates the true column of Tableau.
    update_false_col_unfolded(self, fl)
        Updates the false column of Tableau.
    update_true_col_folded(self, tr)
        Updates the true column of Tableau.
    update_false_col_folded(self, fl)
        Updates the false column of Tableau.
    add_accessible(self, tbl)
        Adds the accessible world of Tableau.
    contradiction(self)
        Checks the contradiction of Tableau.

    """

    def __init__(self, tr: dict = None, fl: dict = None, unfld: dict = None, accs: list = None, tr_accs: list = None, fl_accs: list = None):
        if tr is None:
            tr = {}
        if fl is None:
            fl = {}
        if unfld is None:
            unfld = {}
        if accs is None:
            accs = []
        if tr_accs is None:
            tr_accs = []
        if fl_accs is None:
            fl_accs = []

        self.true_column = tr
        self.false_column = fl
        self.unfolded = unfld
        self.accessible = accs
        self.true_in_accessible = tr_accs
        self.false_in_accessible = fl_accs
        self.world = KripkeWorld(generate_new_name(), [])

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.false_column = {}
        self.true_column = {}
        self.unfolded = {}
        self.accessible = []
        self.true_in_accessible = []
        self.false_in_accessible = []

    def __repr__(self):
        return f"Tableu {self.world}\n false:{self.false_column}, \ntrue:{self.true_column}"

    def update_true_col_unfolded(self, tr: Node) -> None:
        """
        Updates the true column of Tableau.

        Parameters
        ----------
        tr: Node
            Make Node unfolded in the true column.

        Returns
        -------
        None


        """
        self.true_column[tr] = False

    def update_false_col_unfolded(self, fl: Node) -> None:
        """
        Updates the false column of Tableau.

        Parameters
        ----------
        fl: Node
            Make Node unfolded in the false column.

        Returns
        -------
        None


        """
        self.false_column[fl] = False

    def update_true_col_folded(self, tr: Node) -> None:
        """
        Updates the true column of Tableau.

        Parameters
        ----------
        tr: Node
            Make Node folded in the true column.

        Returns
        -------
        None


        """
        self.true_column[tr] = True

    def update_false_col_folded(self, fl: Node) -> None:
        """
        Updates the false column of Tableau.

        Parameters
        ----------
        fl: Node
            Make Node folded in the false column.

        Returns
        -------
        None


        """
        self.false_column[fl] = True

    def add_accessible(self, tbl) -> None:
        """
        Adds the accessible Tableau.

        Parameters
        ----------
        tbl: Tableau
            Accessible Tableau.

        Returns
        -------
        None


        """
        self.accessible.append(tbl)

    def contradiction(self) -> bool:
        """
        Checks the contradiction of Tableau.

        Returns
        -------
        bool
            Returns True if contradiction found.


        """
        for i, _ in self.true_column.items():
            for j, _ in self.false_column.items():
                if i == j:
                    return True
        return False


    def check_validity(self,kripke_model:KripkeModel):
        """
        Checks the validity of Tableau in the Kripke model.

       Returns
        -------
        tuple
            Validity of Formula and Model.


        """
        
        for etr,folded in self.true_column.items():
            if(not folded):
                self.unfolded[etr]=True
        for efl,folded in self.false_column.items():
            if(not folded):
                self.unfolded[efl]=False

        while len(self.unfolded) > 0:
            current, value = self.unfolded.popitem()
            
            type = current.type
            if type == "NOT": 
                if value == True:
                    self.update_true_col_folded(current)

                    self.update_false_col_unfolded(current.right)
                    self.unfolded[current.right]=False
                if value == False:
                    self.update_false_col_folded(current)

                    self.update_true_col_unfolded(current.right)
                    self.unfolded[current.right]=True
            
            elif type == "AND": 
                if value == True:
                    self.update_true_col_folded(current)

                    self.update_true_col_unfolded(current.left)
                    self.update_true_col_unfolded(current.right)
                    self.unfolded[current.left]=True
                    self.unfolded[current.right]=True
                if value == False:
                    self.update_false_col_folded(current)

                    with Tableau(tr=copy.deepcopy(self.true_column), fl=copy.deepcopy(self.false_column),
                                tr_accs=copy.deepcopy(self.true_in_accessible),
                                fl_accs=copy.deepcopy(self.false_in_accessible)) as tableau1:
                        
                        map_new_worlds={}
                        map_new_worlds[self.world.get_name()]=tableau1.world

                        for a in self.accessible:
                            tbl=Tableau(tr=copy.deepcopy(a.true_column), fl=copy.deepcopy(a.false_column))
                            tableau1.add_accessible(tbl)

                            new_world =KripkeWorld(tbl.world.name,a.world.values)
                            map_new_worlds[a.world.name]=new_world

                        aux_kripke_model= kripke_model.new_copy(map_new_worlds)

                        tableau1.update_false_col_unfolded(current.left)

                        result,model = tableau1.check_validity(aux_kripke_model)
                        if result == True: return (True,model)
                    
                    self.update_false_col_unfolded(current.right)
                    self.unfolded[current.right]=False
            
            elif type == "OR": 
                if value == True:
                    self.update_true_col_folded(current)

                    with Tableau(tr=copy.deepcopy(self.true_column), fl=copy.deepcopy(self.false_column),
                                tr_accs=copy.deepcopy(self.true_in_accessible),
                                fl_accs=copy.deepcopy(self.false_in_accessible)) as tableau1:
                    
                        map_new_worlds={}
                        map_new_worlds[self.world.get_name()]=tableau1.world

                        for a in self.accessible:
                            tbl=Tableau(tr=copy.deepcopy(a.true_column), fl=copy.deepcopy(a.false_column))
                            tableau1.add_accessible(tbl)

                            new_world =KripkeWorld(tbl.world.name,a.world.values)
                            map_new_worlds[a.world.name]=new_world

                        tableau1.update_true_col_unfolded(current.left)
                        
                        aux_kripke_model= kripke_model.new_copy(map_new_worlds)
                        
                        result,model = tableau1.check_validity(aux_kripke_model)
                        if result == True: return (True,model)

                    self.update_true_col_unfolded(current.right)
                    self.unfolded[current.right]=True
                    
                if value == False:
                    self.update_false_col_folded(current)

                    self.update_false_col_unfolded(current.left)
                    self.update_false_col_unfolded(current.right)
                    self.unfolded[current.left]=False
                    self.unfolded[current.right]=False
            
            elif type == "IMPLIES": 
                if value == True:
                    self.update_true_col_folded(current)
                    with Tableau(tr=copy.deepcopy(self.true_column), fl=copy.deepcopy(self.false_column),
                                tr_accs=copy.deepcopy(self.true_in_accessible),
                                fl_accs=copy.deepcopy(self.false_in_accessible)) as tableau1:
                        
                        map_new_worlds={}
                        map_new_worlds[self.world.get_name()]=tableau1.world

                        for a in self.accessible:
                            tbl=Tableau(tr=copy.deepcopy(a.true_column), fl=copy.deepcopy(a.false_column))
                            tableau1.add_accessible(tbl)

                            new_world =KripkeWorld(tbl.world.name,a.world.values)
                            map_new_worlds[a.world.name]=new_world

                        tableau1.update_false_col_unfolded(current.left)
                        aux_kripke_model= kripke_model.new_copy(map_new_worlds)
                        result,model = tableau1.check_validity(aux_kripke_model)
                        if result == True: return (True,model)
                    
                    self.update_true_col_unfolded(current.right)
                    self.unfolded[current.right]=True
                    
                if value == False:
                    self.update_false_col_folded(current)

                    self.update_true_col_unfolded(current.left)
                    self.update_false_col_unfolded(current.right)
                    self.unfolded[current.left]=True
                    self.unfolded[current.right]=False

            elif type == "NECESSARILY": 
                if value == True:
                    self.update_true_col_folded(current)

                    self.true_in_accessible.append(current.right)
                if value == False:
                    self.update_false_col_folded(current)

                    tableau1 = Tableau()
                    tableau1.update_false_col_unfolded(current.right)

                    kripke_model.add_world(tableau1.world)
                    kripke_model.add_relation(self.world.name,tableau1.world.name) 
                    self.accessible.append(tableau1)

            elif type == "POSSIBLY": 
                if value == True:
                    self.update_true_col_folded(current)

                    tableau1 = Tableau()
                    tableau1.update_true_col_unfolded(current.right)
                    
                    kripke_model.add_world(tableau1.world)
                    kripke_model.add_relation(self.world.name,tableau1.world.name)
                    self.accessible.append(tableau1) 
                if value == False:
                    self.update_false_col_folded(current)

                    self.false_in_accessible.append(current.right)
            
            elif type == "VARIABLE": 
                if value == True:
                    self.update_true_col_folded(current)
                
                    self.world.add_variable(current.value)
                if value == False: 
                    self.update_false_col_folded(current)
                    
            if self.contradiction():return (True,kripke_model)
       
        for tabl in self.accessible:
            for i in self.true_in_accessible:
                tabl.update_true_col_unfolded(i)
            for j in self.false_in_accessible:
                tabl.update_false_col_unfolded(j)
        
        for tableau in self.accessible:
            with tableau:
                result,model = tableau.check_validity(kripke_model)
                if result == True:
                    return (True, model)
          
        return (False,kripke_model)
            
            
        
counter = 0
def generate_new_name() -> str:
    """
    Generates the new unique name.

    Returns
    -------
    str
        New Name.

    """
    global counter
    counter += 1
    return "world" + str(counter)


def check_validity_of(formula: Node) -> tuple:
    """
    Checks the validity of formula.

    Parameters
    ----------
    formula: Node
        Formula to check.

    Returns
    -------
    tuple
        Validity of Formula and Model.

    """
    kripke_model= KripkeModel()
    with Tableau() as tableau:
        tableau.update_false_col_unfolded(formula)
        kripke_model.add_world(tableau.world)
        result,model= tableau.check_validity(kripke_model)
        return result,model

