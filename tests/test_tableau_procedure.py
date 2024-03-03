import unittest
from tableau_procedure import KripkeWorld, KripkeModel, Tableau, check_validity_of
from parse import Parser

class TestKripkeWorld(unittest.TestCase):

    def test_get_name(self):
        world = KripkeWorld("A")
        self.assertEqual(world.get_name(), "A")

    def test_add_value(self):
        world = KripkeWorld("A")
        world.add_value("a")
        self.assertEqual(world.values, ["a"])

    def test_repr(self):
        world = KripkeWorld("A", ["a", "b"])
        self.assertEqual(str(world), "World(A, ['a', 'b'])")

class TestKripkeModel(unittest.TestCase):

    def test_add_relation(self):
        model = KripkeModel()
        model.add_relation("A", "B")
        self.assertEqual(model.relations, {"A": ["B"]})

    def test_add_world(self):
        model = KripkeModel()
        world = KripkeWorld("A")
        model.add_world(world)
        self.assertEqual(model.worlds, [world])

    def test_get_model(self):
        model = KripkeModel()
        world1 = KripkeWorld("A")
        world2 = KripkeWorld("B")
        model.add_world(world1)
        model.add_world(world2)
        model.add_relation("A", "B")
        self.assertEqual(model.get_model(), ([world1, world2], {"A": ["B"]}))
    
class TestTableau(unittest.TestCase):

    def test_update_unfolded(self):
        tableau = Tableau()
        tableau.update_unfolded({"a": True})
        self.assertEqual(tableau.unfolded, {"a": True})

    def test_update_true_col_unfolded(self):
        tableau = Tableau(tr={"a": False})
        tableau.update_true_col_unfolded("a")
        self.assertEqual(tableau.true_column, {"a": False})

    def test_update_false_col_unfolded(self):
        tableau = Tableau(fl={"a": True})
        tableau.update_false_col_unfolded("a")
        self.assertEqual(tableau.false_column, {"a": False})

    def test_update_true_col_folded(self):
        tableau = Tableau()
        tableau.update_true_col_folded("a")
        self.assertEqual(tableau.true_column, {"a": True})

    def test_update_false_col_folded(self):
        tableau = Tableau()
        tableau.update_false_col_folded("a")
        self.assertEqual(tableau.false_column, {"a": True})

    def test_add_accessible(self):
        tableau1 = Tableau()
        tableau2 = Tableau()
        tableau1.add_accessible(tableau2)
        self.assertEqual(tableau1.accessible, [tableau2])

    def test_contradiction_true(self):
        tableau = Tableau(tr={"a": True}, fl={"a": True})
        self.assertTrue(tableau.contradiction())

    def test_contradiction_false(self):
        tableau = Tableau(tr={"a": True}, fl={"b": True})
        self.assertFalse(tableau.contradiction())

class TestCheckValidity(unittest.TestCase):
    def test_valid_formula(formula):
        formula = Parser().parse_text("◊p → ¬□¬p")
        result, model = check_validity_of(formula)
        assert result == True
        assert isinstance(model, KripkeModel)
    
    def test_invalid_formula(formula):
        formula = Parser().parse_text("◊p → □p")
        result, model = check_validity_of(formula)
        assert result == False
        assert isinstance(model, KripkeModel)
    
    def test_rules_combinations(self):
        formula = Parser().parse_text("¬◊(p∧q)→(◻p→ ◻q)")
        result, model = check_validity_of(formula)
        assert result == True
        assert isinstance(model, KripkeModel)

        formula = Parser().parse_text("((p ∧ ¬◊q) ∨ (◻p ∧ q) → (◊p → ◻q)) -> (◇r^~□s)^(□r->◇s)")
        result, model = check_validity_of(formula)
        assert result == False
        assert isinstance(model, KripkeModel)

        formula = Parser().parse_text("(p ∧ ¬◊q) ∨ (◻p ∧ q) → (◊p → ◻q)")
        result, model = check_validity_of(formula)
        assert result == False
        assert isinstance(model, KripkeModel)

        formula = Parser().parse_text("(◇r^~□s)^(□r->◇s)->¬◊(p∧q)→(◻p→ ◻q)")
        result, model = check_validity_of(formula)
        assert result == False
        assert isinstance(model, KripkeModel)

        

    
if __name__ == '__main__':
    unittest.main()