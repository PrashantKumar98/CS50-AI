import collections
import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # raise NotImplementedError
        for variable in self.domains.keys():
            n = variable.length
            temp = self.domains[variable].copy()
            for word in temp:
                if len(word) != n:
                    self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # raise NotImplementedError
        revised = False
        overlap = self.crossword.overlaps[x, y]
        if overlap is None:
            return False
        temp = self.domains[x].copy()
        for word_x in temp:
            flag = True
            for word_y in self.domains[y]:
                if word_x[overlap[0]] == word_y[overlap[1]]:
                    flag = False

            # if constraint is not satisfied then remove from x domain
            if flag:
                revised = True
                self.domains[x].remove(word_x)

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        #raise NotImplementedError
        if arcs is None:
            arcs = list()
            for var in self.crossword.variables:
                for neighbor in self.crossword.neighbors(var):
                    arcs.append((var,neighbor))
        while len(arcs) > 0:
            (x,y) = arcs.pop()
            if self.revise(x,y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x):
                    if z != y:
                        arcs.append((z,x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # raise NotImplementedError
        return self.crossword.variables == set(assignment.keys())

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        #raise NotImplementedError
        # chech if every value of correct length
        for var_x in assignment:
            word_x = assignment[var_x]
            if word_x:
                if var_x.length != len(word_x):
                    return False
                #Check if values are distinct
                for var_y in assignment:
                    word_y = assignment[var_y]
                    if var_x != var_y:
                        if word_x == word_y:
                            return False
                        # check for overlap
                        overlap = self.crossword.overlaps[var_x,var_y]
                        if overlap is not None:
                            if word_x[overlap[0]] != word_y[overlap[1]]:
                                return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        #raise NotImplementedError
        count = 0
        # list to keep track of the number of values ruled out for neighboring variables
        counter_list = [0] * len(self.domains[var])
        for word in self.domains[var]:
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment.keys():
                    if word in self.domains[neighbor]:
                        counter_list[count] = counter_list[count] + 1
            count = count + 1

        # create a dictionary of sorted count values and return sorted domain
        dom_dict = dict(zip(self.domains[var], counter_list))
        # descending order of values
        sorted_dom = sorted(dom_dict.items(), key=lambda kv: kv[1], reverse= True)
        # convert list of tuples to dict
        sorted_dom_dict = collections.OrderedDict(sorted_dom)
        # return list of domains
        return list(sorted_dom_dict.keys())

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # raise NotImplementedError
        min = 9999999
        min_val = ()
        for var in self.crossword.variables:
            if var not in assignment.keys():
                # Choose the variable with the minimum number of remaining values
                if len(self.domains[var]) < min:
                    min_val = var
                    min = len(self.domains[var])

                    # if there is tie then choose variable with most neighbour
                elif len(self.domains[var]) == min:

                    if len(self.crossword.neighbors(min_val)) < len(self.crossword.neighbors(var)):
                        min_val = var
        return min_val

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # raise NotImplementedError

        # base case
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result != None:
                    return result
            assignment.pop(var)
        return None


def main():
    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
